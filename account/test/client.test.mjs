// Test d'intégration : le VRAI client (assets/maxlol-account.js) contre le VRAI schéma SQL (Postgres WASM), deux "appareils" distincts.
import test from 'node:test'; import assert from 'node:assert/strict'; import fs from 'node:fs'; import vm from 'node:vm'; import { PGlite } from '@electric-sql/pglite';
const U = '33333333-3333-3333-3333-333333333333', db = new PGlite();
await db.exec(`create role anon nologin; create role authenticated nologin; create schema auth;
  create function auth.uid() returns uuid language sql stable as $$ select nullif(current_setting('request.jwt.claim.sub', true),'')::uuid $$;
  grant usage on schema auth, public to anon, authenticated; grant execute on function auth.uid() to anon, authenticated;`);
await db.exec(fs.readFileSync(new URL('../schema.sql', import.meta.url), 'utf8')); await db.exec('grant select on public.saves, public.save_history to authenticated');
async function asUser(sql, params) { await db.exec('begin'); try { await db.exec(`set local role authenticated; select set_config('request.jwt.claim.sub','${U}',true)`); const r = await db.query(sql, params); await db.exec('commit'); return r.rows; } catch (e) { await db.exec('rollback'); throw e; } }
// faux Supabase : route les appels REST du client vers Postgres
async function mock(path, opt) {
  if (path.startsWith('/auth/v1/token')) return { status: 200, body: { access_token: 'a', refresh_token: 'r', expires_in: 3600, user: { id: U, email: 'a@b.c' } } };
  let m = path.match(/^\/rest\/v1\/rpc\/(\w+)$/);
  if (m) { const b = opt.body || {}; const q = { put_save: ['select public.put_save($1,$2,$3,$4::jsonb,$5) r', [b.p_game, b.p_slot, b.p_base_version, JSON.stringify(b.p_data), b.p_device]], restore_save: ['select public.restore_save($1,$2,$3) r', [b.p_game, b.p_slot, b.p_history_id]], export_my_data: ['select public.export_my_data() r', []] }[m[1]]; return { status: 200, body: (await asUser(...q))[0].r }; }
  m = path.match(/^\/rest\/v1\/(saves|save_history)\?(.*)$/);
  if (m) { const p = new URLSearchParams(m[2]); const rows = await asUser(`select * from public.${m[1]} where game=$1 and slot=$2 ${m[1] === 'save_history' ? 'order by replaced_at desc, id desc' : ''}`, [p.get('game').replace('eq.', ''), p.get('slot').replace('eq.', '')]); return { status: 200, body: rows }; }
  return { status: 404, body: {} };
}
function device() {
  const store = {}, w = { localStorage: { getItem: k => store[k] ?? null, setItem: (k, v) => store[k] = v, removeItem: k => delete store[k] }, URLSearchParams, location: { hash: '', pathname: '/' }, console };
  vm.runInNewContext(fs.readFileSync(new URL('../../assets/maxlol-account.js', import.meta.url), 'utf8'), { ...w, window: w, globalThis: w });
  const A = w.MaxlolAccount.create({ url: 'https://x.supabase.co', anonKey: 'anon', mock }); store['mxl-session-v1'] = JSON.stringify({ access_token: 'a', refresh_token: 'r', expires_at: 9e9, user: { id: U } });
  const A2 = w.MaxlolAccount.create({ url: 'https://x.supabase.co', anonKey: 'anon', mock });
  let save = null; const adapter = { game: 'torch', read: () => save, write: v => { save = v; } };
  return { A: A2, adapter, store, set: v => save = v, get: () => save };
}
const never = () => { throw new Error('ask ne doit pas être appelé'); };
const PT = (...a) => { const T = device().A.planSync; return T(...a); };

test('P1 table de décision de planSync', () => {
  assert.equal(PT({ exists: false }, { exists: false }, null), 'noop');
  assert.equal(PT({ exists: true, raw: 'a' }, { exists: false }, null), 'upload');
  assert.equal(PT({ exists: false }, { exists: true, raw: 'a', version: 1 }, null), 'download');
  assert.equal(PT({ exists: true, raw: 'a' }, { exists: true, raw: 'a', version: 1 }, null), 'adopt');
  assert.equal(PT({ exists: true, raw: 'a' }, { exists: true, raw: 'b', version: 1 }, null), 'ask');            // 1er rattachement différent : jamais automatique
});
test('S1 migration : sauvegarde localStorage locale → cloud (aucun écrasement)', async () => {
  const d1 = device(); d1.set('{"gold":10}'); const r = await d1.A.migrate(d1.adapter, never); assert.equal(r.action, 'uploaded'); assert.equal(r.version, 1);
});
test('S2 deuxième téléphone sans sauvegarde : téléchargement automatique', async () => {
  const d2 = device(); const r = await d2.A.sync(d2.adapter, never); assert.equal(r.action, 'downloaded'); assert.equal(d2.get(), '{"gold":10}');
});
test('S3 modifications sur un appareil seulement : synchro silencieuse dans les deux sens', async () => {
  const d1 = device(); d1.set('{"gold":10}'); await d1.A.sync(d1.adapter, () => 'local');          // d1 rattache (même contenu que le cloud → adopt)
  d1.set('{"gold":50}'); assert.equal((await d1.A.sync(d1.adapter, never)).action, 'uploaded');
  const d2 = device(); await d2.A.sync(d2.adapter, never); assert.equal(d2.get(), '{"gold":50}');
  assert.equal((await d2.A.sync(d2.adapter, never)).action, 'noop');
});
test('S4 conflit (les deux ont changé) : on demande ; "annuler" ne touche à rien', async () => {
  const a = device(), b = device(); a.set('{"gold":50}'); await a.A.sync(a.adapter, () => 'cloud'); await b.A.sync(b.adapter, () => 'cloud');
  a.set('{"gold":60}'); await a.A.sync(a.adapter, never);                                          // a pousse v+1
  b.set('{"gold":70}');                                                                            // b a aussi changé, sans le savoir
  let asked = null; const r = await b.A.sync(b.adapter, i => { asked = i; return 'cancel'; });
  assert.equal(r.action, 'cancelled'); assert.ok(asked); assert.equal(b.get(), '{"gold":70}');
  assert.equal((await asUser(`select data->>'gold' g from public.saves where game='torch'`))[0].g, '60');
});
test('S5 conflit → "garder le local" : cloud remplacé MAIS ancienne version archivée', async () => {
  const b = device(); b.set('{"gold":70}'); const r = await b.A.sync(b.adapter, () => 'local');
  assert.equal(r.action, 'uploaded'); assert.equal((await asUser(`select data->>'gold' g from public.saves where game='torch'`))[0].g, '70');
  assert.ok((await asUser(`select 1 from public.save_history where data->>'gold'='60'`)).length >= 1);
});
test('S6 conflit → "garder les deux" : copie locale sauvegardée avant d\'appliquer le cloud', async () => {
  const a = device(); a.set('{"gold":1}'); await a.A.sync(a.adapter, () => 'cloud'); a.set('{"gold":2}');
  const b = device(); b.set('{"gold":3}'); await b.A.sync(b.adapter, () => 'local');                // cloud = 3, version avancée
  const r = await a.A.sync(a.adapter, () => 'both'); assert.equal(r.action, 'downloaded'); assert.equal(a.get(), '{"gold":3}');
  assert.ok(Object.keys(a.store).some(k => k.startsWith('mxl-backup:torch:main:copie-locale')) && Object.entries(a.store).some(([k, v]) => k.startsWith('mxl-backup') && v === '{"gold":2}'));
});
test('S7 course : un appareil à version obsolète reçoit un conflit du serveur, rien n\'est écrasé', async () => {
  const a = device(); a.set('{"gold":9}'); await a.A.sync(a.adapter, () => 'local');
  const v = (await asUser(`select version v from public.saves where game='torch'`))[0].v;
  const r = (await asUser('select public.put_save($1,$2,$3,$4::jsonb,$5) r', ['torch', 'main', v - 1, '{"gold":-1}', 'zz']))[0].r; assert.equal(r.status, 'conflict');
  assert.notEqual((await asUser(`select data->>'gold' g from public.saves where game='torch'`))[0].g, '-1');
});
test('S8 restauration d\'une ancienne version via le client', async () => {
  const a = device(), h = await a.A.history(a.adapter); assert.ok(h.length > 0); const r = await a.A.restoreVersion(a.adapter, h[h.length - 1].id); assert.equal(r.status, 'ok');
});
test('S9 export RGPD via le client', async () => { const a = device(), e = await a.A.exportData(); assert.equal(e.user_id, U); assert.ok(e.saves.length >= 1); });
