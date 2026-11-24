// Teste schema.sql sur un vrai Postgres (WASM) avec le même mécanisme d'identité que Supabase (auth.uid() lit le claim JWT).
import test from 'node:test'; import assert from 'node:assert/strict'; import fs from 'node:fs'; import { PGlite } from '@electric-sql/pglite';
const A = '11111111-1111-1111-1111-111111111111', B = '22222222-2222-2222-2222-222222222222';
const db = new PGlite();
await db.exec(`create role anon nologin; create role authenticated nologin; create schema auth;
  create function auth.uid() returns uuid language sql stable as $$ select nullif(current_setting('request.jwt.claim.sub', true),'')::uuid $$;
  grant usage on schema auth, public to anon, authenticated; grant execute on function auth.uid() to anon, authenticated;`);
await db.exec(fs.readFileSync(new URL('../schema.sql', import.meta.url), 'utf8'));
await db.exec(`grant select on public.profiles, public.saves, public.save_history to authenticated; grant update on public.profiles to authenticated;`);
// exécute une requête "en tant que" un utilisateur (rôle + claim), comme PostgREST
async function as(uid, sql, params = []) {
  await db.exec('begin'); try {
    await db.exec(`set local role ${uid ? 'authenticated' : 'anon'}; select set_config('request.jwt.claim.sub', '${uid || ''}', true)`);
    const r = await db.query(sql, params); await db.exec('commit'); return r.rows;
  } catch (e) { await db.exec('rollback'); throw e; }
}
const put = (u, g, base, data, slot = 'main') => as(u, 'select public.put_save($1,$2,$3,$4::jsonb,$5) r', [g, slot, base, JSON.stringify(data), 'tel-' + (u || 'x')[0]]).then(r => r[0].r);

test('Q1 première sauvegarde puis mise à jour avec bonne version', async () => {
  assert.deepEqual(await put(A, 'torch', 0, { gold: 10 }), { status: 'ok', version: 1 });
  assert.deepEqual(await put(A, 'torch', 1, { gold: 20 }), { status: 'ok', version: 2 });
});
test('Q2 conflit : base obsolète → rien n\'est écrit, le cloud est intact', async () => {
  const r = await put(A, 'torch', 1, { gold: 999 }); assert.equal(r.status, 'conflict'); assert.equal(r.cloud_version, 2);
  assert.equal((await as(A, `select data->>'gold' g from public.saves where game='torch'`))[0].g, '20');
  assert.equal((await put(A, 'torch', 0, { gold: 1 })).status, 'conflict');     // "je n'ai rien" alors qu'il existe une sauvegarde cloud
});
test('Q3 isolation RLS : B ne voit rien de A', async () => {
  assert.equal((await as(B, 'select * from public.saves')).length, 0); assert.equal((await as(B, 'select * from public.save_history')).length, 0);
  assert.equal((await as(B, 'select * from public.profiles')).length, 0);
  assert.deepEqual(await put(B, 'torch', 0, { gold: 5 }), { status: 'ok', version: 1 });          // B a sa propre ligne
  assert.equal((await as(A, `select data->>'gold' g from public.saves`))[0].g, '20');             // celle de A n'a pas bougé
});
test('Q4 écritures directes interdites (INSERT/UPDATE/DELETE sur saves)', async () => {
  for (const q of [`insert into public.saves(user_id,game,data,size_bytes) values ('${A}','x','{}',2)`, `update public.saves set data='{"gold":99999}'`, `delete from public.saves`])
    await assert.rejects(as(A, q), /permission denied/);
});
test('Q5 anonyme : aucune lecture, aucune fonction', async () => {
  await assert.rejects(as(null, 'select * from public.saves'), /permission denied/);
  await assert.rejects(as(null, `select public.put_save('torch','main',0,'{}'::jsonb)`), /permission denied/);
  await assert.rejects(as(null, 'select public.export_my_data()'), /permission denied/);
});
test('Q6 historique limité à 5 ; restauration non destructive', async () => {
  let v = 2; for (let i = 0; i < 8; i++) { const r = await put(A, 'torch', v, { gold: 100 + i }); v = r.version; }
  const h = await as(A, `select id, version, data->>'gold' g from public.save_history where game='torch' order by replaced_at desc, id desc`); assert.equal(h.length, 5);
  const old = h[h.length - 1], r = (await as(A, 'select public.restore_save($1,$2,$3) r', ['torch', 'main', old.id]))[0].r; assert.equal(r.status, 'ok');
  assert.equal((await as(A, `select data->>'gold' g from public.saves where game='torch'`))[0].g, old.g);
  assert.ok((await as(A, `select 1 from public.save_history where game='torch' and data->>'gold'='107'`)).length >= 1);   // la version qu'on vient de quitter est conservée
});
test('Q7 B ne peut pas restaurer l\'historique de A', async () => {
  const id = (await as(A, `select id from public.save_history limit 1`))[0].id;
  assert.equal((await as(B, 'select public.restore_save($1,$2,$3) r', ['torch', 'main', id]))[0].r.status, 'not_found');
});
test('Q8 taille max 256 Ko et noms de jeu/slot validés', async () => {
  assert.equal((await put(A, 'big', 0, { x: 'a'.repeat(300000) })).status, 'too_large');
  await assert.rejects(put(A, "x'; drop table public.saves;--", 0, {}), /check constraint|violates/);
  await assert.rejects(put(A, 'torch', 0, {}, 'SLOT MAJ'), /check constraint|violates/);
});
test('Q9 export RGPD : uniquement ses données', async () => {
  const e = (await as(A, 'select public.export_my_data() r'))[0].r; assert.equal(e.user_id, A);
  assert.ok(e.saves.length >= 1 && e.saves.every(s => s.user_id === A)); assert.ok(e.save_history.every(s => s.user_id === A));
});
test('Q10 suppression : efface ses données et pas celles des autres', async () => {
  await as(A, 'select public.delete_my_game_data()');
  assert.equal((await as(A, 'select * from public.saves')).length, 0); assert.equal((await as(A, 'select * from public.save_history')).length, 0);
  assert.equal((await as(B, 'select * from public.saves')).length, 1);
});
test('Q11 non authentifié (jeton sans sub) : put_save refuse', async () => {
  await db.exec('begin'); await db.exec(`set local role authenticated; select set_config('request.jwt.claim.sub','',true)`);
  await assert.rejects(db.query(`select public.put_save('torch','main',0,'{}'::jsonb)`), /not_authenticated/); await db.exec('rollback');
});
