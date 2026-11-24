import test from 'node:test'; import assert from 'node:assert/strict'; import crypto from 'node:crypto';
import * as K from '../lib/core.mjs'; import { mockPayPal } from './paypal-mock.mjs';
const SB = 'https://abc.supabase.co', ec = crypto.generateKeyPairSync('ec', { namedCurve: 'P-256' }), sbJwk = { ...ec.publicKey.export({ format: 'jwk' }), kid: 'k1', alg: 'ES256' };
const mine = crypto.generateKeyPairSync('ec', { namedCurve: 'prime256v1' }).privateKey.export({ type: 'pkcs8', format: 'pem' });
const env = { PAYPAL_CLIENT_ID: 'i', PAYPAL_CLIENT_SECRET: 's', LICENSE_SECRET: 'L', SIGNING_PRIVATE_KEY_PEM: mine, PAYPAL_MERCHANT_ID: 'MERCHANT1', SUPABASE_URL: SB, SUPABASE_JWT_SECRET: 'sb-secret-xyz' };
const fakeFetch = async () => ({ json: async () => ({ keys: [sbJwk] }) });
const jwt = (pl, { alg = 'ES256', key = ec.privateKey, kid = 'k1' } = {}) => { const h = K.b64u(JSON.stringify({ alg, typ: 'JWT', kid })), p = K.b64u(JSON.stringify({ aud: 'authenticated', role: 'authenticated', iss: SB + '/auth/v1', exp: Math.floor(Date.now() / 1000) + 600, ...pl })), d = Buffer.from(h + '.' + p);
  const sig = alg === 'HS256' ? crypto.createHmac('sha256', key).update(d).digest() : alg === 'none' ? Buffer.alloc(0) : crypto.sign('sha256', d, { key, dsaEncoding: 'ieee-p1363' }); return h + '.' + p + '.' + K.b64u(sig); };
const U = (sub, extra) => K.supabaseUser(K.cfg(env), 'Bearer ' + jwt({ sub, email: sub + '@ex.com', ...extra }), fakeFetch);
const world = async () => { K.resetJwks(); const c = K.cfg(env), st = K.memoryStore(), pp = mockPayPal(), ppc = K.paypal(c, pp.fetch), r = await K.createOrder(c, st, ppc, { productId: 'torch-full' }); pp.approve(r.body.orderId); const cap = await K.captureOrder(c, st, ppc, { orderId: r.body.orderId }); return { c, st, cap: cap.body, orderId: r.body.orderId }; };

test('A1 JWT Supabase valide accepté ; expiré, mauvaise audience/émetteur, mauvaise clé, alg none, HS256 forgé refusés', async () => {
  K.resetJwks(); assert.equal((await U('u1')).id, 'u1');
  assert.equal(await U('u1', { exp: 1 }), null); assert.equal(await U('u1', { aud: 'anon' }), null); assert.equal(await U('u1', { iss: 'https://evil/auth/v1' }), null); assert.equal(await U('u1', { role: 'anon' }), null);
  const other = crypto.generateKeyPairSync('ec', { namedCurve: 'P-256' }).privateKey;
  assert.equal(await K.supabaseUser(K.cfg(env), 'Bearer ' + jwt({ sub: 'u1' }, { key: other }), fakeFetch), null);
  assert.equal(await K.supabaseUser(K.cfg(env), 'Bearer ' + jwt({ sub: 'u1' }, { alg: 'none' }), fakeFetch), null);
  assert.equal(await K.supabaseUser(K.cfg(env), 'Bearer ' + jwt({ sub: 'u1' }, { alg: 'HS256', key: 'mauvais-secret' }), fakeFetch), null);
  assert.equal((await K.supabaseUser(K.cfg(env), 'Bearer ' + jwt({ sub: 'u2' }, { alg: 'HS256', key: 'sb-secret-xyz' }), fakeFetch)).id, 'u2');
  assert.equal(await K.supabaseUser(K.cfg(env), '', fakeFetch), null); assert.equal(await K.supabaseUser(K.cfg(env), 'Bearer n.i.mp', fakeFetch), null);
});
test('A2 liaison d\'une licence au compte (par clé), idempotente ; une licence = un seul compte', async () => {
  const w = await world(), u1 = await U('u1'), u2 = await U('u2');
  assert.equal((await K.linkLicense(w.c, w.st, u1, { licenseKey: w.cap.licenseKey })).status, 200);
  assert.equal((await K.linkLicense(w.c, w.st, u1, { licenseKey: w.cap.licenseKey })).status, 200);
  assert.equal((await K.linkLicense(w.c, w.st, u2, { licenseKey: w.cap.licenseKey })).status, 409);
  assert.equal((await K.linkLicense(w.c, w.st, null, { licenseKey: w.cap.licenseKey })).status, 401);
  assert.equal((await K.linkLicense(w.c, w.st, u1, { licenseKey: 'MXL-AAAA-AAAA-AAAA-AAAA' })).status, 404);
  assert.equal((await K.library(w.c, w.st, u1)).body.items.length, 1);
});
test('A3 bibliothèque : achats, historique, jeton valide ; un autre compte ne voit rien', async () => {
  const w = await world(), u1 = await U('u1'), u2 = await U('u2'); await K.linkLicense(w.c, w.st, u1, { token: w.cap.token });
  const it = (await K.library(w.c, w.st, u1)).body.items[0]; assert.equal(it.product, 'torch-full'); assert.equal(it.order.amount, '7.99'); assert.equal(it.order.status, 'COMPLETED');
  assert.equal(K.verifyToken(K.publicKeyPem(w.c), it.token).prd, 'torch-full');
  assert.equal((await K.library(w.c, w.st, u2)).body.items.length, 0); assert.equal((await K.library(w.c, w.st, null)).status, 401);
});
test('A4 restauration par connexion : nouveau téléphone, aucune clé nécessaire', async () => {
  const w = await world(), u1 = await U('u1'); await K.linkLicense(w.c, w.st, u1, { licenseKey: w.cap.licenseKey });
  const again = await U('u1'), it = (await K.library(w.c, w.st, again)).body.items[0]; assert.ok(K.verifyToken(K.publicKeyPem(w.c), it.token));
});
test('A5 remboursement : l\'achat apparaît révoqué, plus de jeton', async () => {
  const w = await world(), u1 = await U('u1'); await K.linkLicense(w.c, w.st, u1, { licenseKey: w.cap.licenseKey });
  const l = await w.st.get('license:' + (await w.st.get('capture:CAP' + w.orderId))); await w.st.set('license:' + l.id, { ...l, status: 'revoked' });
  const it = (await K.library(w.c, w.st, u1)).body.items[0]; assert.equal(it.status, 'revoked'); assert.equal(it.token, null);
});
test('A6 suppression du compte : détaché, l\'achat reste valide via sa clé', async () => {
  const w = await world(), u1 = await U('u1'); await K.linkLicense(w.c, w.st, u1, { licenseKey: w.cap.licenseKey });
  assert.equal((await K.unlinkAll(w.c, w.st, u1)).status, 200); assert.equal((await K.library(w.c, w.st, u1)).body.items.length, 0);
  assert.equal((await K.activate(w.c, w.st, { licenseKey: w.cap.licenseKey }, '9.9.9.9')).status, 200);
  assert.equal((await K.linkLicense(w.c, w.st, await U('u3'), { licenseKey: w.cap.licenseKey })).status, 200);   // peut être rattachée à un nouveau compte
});
