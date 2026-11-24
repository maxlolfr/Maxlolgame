import test from 'node:test';
import assert from 'node:assert/strict';
import crypto from 'node:crypto';
import * as K from '../lib/core.mjs';
import { mockPayPal } from './paypal-mock.mjs';

const SECRETS = { id: 'CLIENTID_SECRETVALUE', secret: 'PAYPAL_SECRET_ZZZ_9f3', lic: 'LICENSE_SECRET_QQQ_71a' };
const { privateKey } = crypto.generateKeyPairSync('ec', { namedCurve: 'prime256v1' });
const PEM = privateKey.export({ type: 'pkcs8', format: 'pem' });
const env = { PAYPAL_ENV: 'sandbox', PAYPAL_CLIENT_ID: SECRETS.id, PAYPAL_CLIENT_SECRET: SECRETS.secret, PAYPAL_WEBHOOK_ID: 'WH-TEST', PAYPAL_MERCHANT_ID: 'MERCHANT1', LICENSE_SECRET: SECRETS.lic, SIGNING_PRIVATE_KEY_PEM: PEM };
const logs = []; for (const k of ['log', 'error', 'warn']) { const o = console[k]; console[k] = (...a) => { logs.push(a.join(' ')); }; }
const world = () => { const c = K.cfg(env), st = K.memoryStore(), pp = mockPayPal(), ppc = K.paypal(c, pp.fetch); return { c, st, pp, ppc }; };
const buy = async (w, mode = 'ok', productId = 'torch-full') => { const r = await K.createOrder(w.c, w.st, w.ppc, { productId }); if (mode !== 'unapproved') w.pp.approve(r.body.orderId, mode); return r.body.orderId; };
const licCount = w => [...w.st._dump().keys()].filter(k => k.startsWith('license:')).length;
const pub = () => K.publicKeyPem(K.cfg(env));

test('S1 création : prix/devise viennent du catalogue serveur, jamais du client', async () => {
  const w = world(), r = await K.createOrder(w.c, w.st, w.ppc, { productId: 'torch-full', price: '0.01', amount: '0.01', currency: 'JPY' });
  assert.equal(r.status, 200);
  const u = w.pp.orders.get(r.body.orderId).unit;
  assert.deepEqual(u.amount, { currency_code: 'EUR', value: '7.99' }); assert.equal(u.payee.merchant_id, 'MERCHANT1');
  assert.match(r.body.approveUrl, /paypal\.com/);
});
test('S2 produit inconnu ou désactivé refusé (Pass Confort non lancé)', async () => {
  const w = world();
  assert.equal((await K.createOrder(w.c, w.st, w.ppc, { productId: 'gratuit' })).status, 400);
  assert.equal((await K.createOrder(w.c, w.st, w.ppc, { productId: 'torch-comfort' })).status, 400);
  assert.equal(w.pp.calls.create, 0);
});
test('S3 paiement réussi : statut COMPLETED → une licence + jeton valide', async () => {
  const w = world(), id = await buy(w), r = await K.captureOrder(w.c, w.st, w.ppc, { orderId: id });
  assert.equal(r.status, 200); assert.equal(r.body.status, 'COMPLETED'); assert.match(r.body.licenseKey, /^MXL(-[A-Z2-9]{4}){4}$/);
  const pl = K.verifyToken(pub(), r.body.token); assert.equal(pl.prd, 'torch-full'); assert.equal(licCount(w), 1);
});
test('S4 rejeu de la même capture (double clic, rechargement) : même licence, pas de 2e livraison', async () => {
  const w = world(), id = await buy(w), a = await K.captureOrder(w.c, w.st, w.ppc, { orderId: id }), b = await K.captureOrder(w.c, w.st, w.ppc, { orderId: id });
  assert.equal(a.body.licenseKey, b.body.licenseKey); assert.equal(licCount(w), 1); assert.equal(w.pp.calls.capture, 1);
});
test('S5 captures simultanées : une seule licence', async () => {
  const w = world(), id = await buy(w), rs = await Promise.all([1, 2, 3, 4].map(() => K.captureOrder(w.c, w.st, w.ppc, { orderId: id })));
  assert.equal(licCount(w), 1); assert.ok(rs.some(r => r.status === 200));
});
test('S6 paiement annulé / non approuvé : aucune licence', async () => {
  const w = world(), id = await buy(w, 'unapproved'), r = await K.captureOrder(w.c, w.st, w.ppc, { orderId: id });
  assert.equal(r.status, 402); assert.equal(r.body.status, 'NOT_APPROVED'); assert.equal(licCount(w), 0);
  w.pp.approve(id); assert.equal((await K.captureOrder(w.c, w.st, w.ppc, { orderId: id })).status, 200);   // il peut réessayer ensuite
});
test('S7 paiement refusé : aucune licence', async () => {
  const w = world(), id = await buy(w, 'declined'), r = await K.captureOrder(w.c, w.st, w.ppc, { orderId: id });
  assert.equal(r.body.status, 'FAILED'); assert.equal(licCount(w), 0);
});
test('S8 paiement en attente (PENDING) : pas de livraison, puis webhook COMPLETED → livraison', async () => {
  const w = world(), id = await buy(w, 'pending'), r = await K.captureOrder(w.c, w.st, w.ppc, { orderId: id });
  assert.equal(r.status, 202); assert.equal(r.body.status, 'PENDING'); assert.equal(licCount(w), 0);
  const e = w.pp.event('PAYMENT.CAPTURE.COMPLETED', id); assert.equal((await K.webhook(w.c, w.st, w.ppc, e.headers, e.raw)).status, 200);
  assert.equal(licCount(w), 1); assert.equal((await K.captureOrder(w.c, w.st, w.ppc, { orderId: id })).body.status, 'COMPLETED');
});
for (const [mode, why] of [['tamper_amount', 'montant'], ['tamper_currency', 'devise'], ['tamper_ref', 'produit'], ['tamper_payee', 'destinataire']])
  test(`S9 ${why} incohérent côté PayPal : rejeté, aucune licence`, async () => {
    const w = world(), id = await buy(w, mode), r = await K.captureOrder(w.c, w.st, w.ppc, { orderId: id });
    assert.equal(r.status, 422); assert.equal(licCount(w), 0); assert.equal(w.st._dump().get('order:' + id).status, 'REJECTED');
  });
test('S10 commande inconnue ou identifiant forgé : refusée', async () => {
  const w = world();
  for (const orderId of ['ORD999', '', null, { $ne: 1 }]) assert.equal((await K.captureOrder(w.c, w.st, w.ppc, { orderId })).status, 404);
  assert.equal(w.pp.calls.capture, 0);
});
test('S11 une même transaction ne peut pas servir deux commandes', async () => {
  const w = world(), id = await buy(w); await K.captureOrder(w.c, w.st, w.ppc, { orderId: id });
  const o2 = { orderId: 'ORDX', productId: 'torch-full', status: 'CREATED' }; await w.st.set('order:ORDX', o2);
  const e = w.pp.event('PAYMENT.CAPTURE.COMPLETED', 'ORDX'); e.raw = e.raw.replace('CAPORDX', 'CAP' + id);
  const hdr = new Map(e.headers); hdr.set('paypal-transmission-sig', 'sig:' + crypto.createHash('sha256').update(e.raw).digest('hex'));
  await K.webhook(w.c, w.st, w.ppc, hdr, e.raw); assert.equal(licCount(w), 1);
});
test('S12 webhook : signature forgée refusée, valide acceptée, doublon ignoré', async () => {
  const w = world(), id = await buy(w);
  const bad = w.pp.event('PAYMENT.CAPTURE.COMPLETED', id, { badSig: true }); assert.equal((await K.webhook(w.c, w.st, w.ppc, bad.headers, bad.raw)).status, 400); assert.equal(licCount(w), 0);
  const ok = w.pp.event('PAYMENT.CAPTURE.COMPLETED', id); assert.equal((await K.webhook(w.c, w.st, w.ppc, ok.headers, ok.raw)).status, 200);
  assert.equal(licCount(w), 1); assert.equal((await K.webhook(w.c, w.st, w.ppc, ok.headers, ok.raw)).body.dup, true); assert.equal(licCount(w), 1);
  const tampered = ok.raw.replace('7.99', '0.01'); assert.equal((await K.webhook(w.c, w.st, w.ppc, ok.headers, tampered)).status, 400);
});
test('S13 webhook COMPLETED avec mauvais montant : pas de licence', async () => {
  const w = world(), id = await buy(w), e = w.pp.event('PAYMENT.CAPTURE.COMPLETED', id, { amount: { value: '0.01', currency_code: 'EUR' } });
  await K.webhook(w.c, w.st, w.ppc, e.headers, e.raw); assert.equal(licCount(w), 0);
});
test('S14 remboursement : licence révoquée, refresh/activation refusés ; remboursement partiel : conservée', async () => {
  const w = world(), id = await buy(w), r = await K.captureOrder(w.c, w.st, w.ppc, { orderId: id });
  const part = w.pp.event('PAYMENT.CAPTURE.REFUNDED', id, { amount: { value: '2.00', currency_code: 'EUR' } }); await K.webhook(w.c, w.st, w.ppc, part.headers, part.raw);
  assert.equal((await K.refresh(w.c, w.st, { token: r.body.token })).status, 200);
  const full = w.pp.event('PAYMENT.CAPTURE.REFUNDED', id); await K.webhook(w.c, w.st, w.ppc, full.headers, full.raw);
  assert.equal((await K.refresh(w.c, w.st, { token: r.body.token })).status, 403);
  assert.equal((await K.activate(w.c, w.st, { licenseKey: r.body.licenseKey }, '1.1.1.1')).status, 404);
  assert.equal((await K.captureOrder(w.c, w.st, w.ppc, { orderId: id })).body.status, 'REFUNDED');
});
test('S15 litige / rétrofacturation (REVERSED) : licence révoquée', async () => {
  const w = world(), id = await buy(w), r = await K.captureOrder(w.c, w.st, w.ppc, { orderId: id });
  const e = w.pp.event('PAYMENT.CAPTURE.REVERSED', id); await K.webhook(w.c, w.st, w.ppc, e.headers, e.raw);
  assert.equal((await K.refresh(w.c, w.st, { token: r.body.token })).status, 403);
});
test('S16 restauration (nouveau téléphone) : clé de licence, ou ID transaction + e-mail PayPal', async () => {
  const w = world(), id = await buy(w), r = await K.captureOrder(w.c, w.st, w.ppc, { orderId: id });
  const a = await K.activate(w.c, w.st, { licenseKey: r.body.licenseKey.toLowerCase() }, '2.2.2.2'); assert.equal(a.status, 200); assert.equal(K.verifyToken(pub(), a.body.token).prd, 'torch-full');
  const b = await K.restore(w.c, w.st, { transactionId: 'CAP' + id, email: ' acheteur@example.COM ' }, '2.2.2.2'); assert.equal(b.body.licenseKey, r.body.licenseKey);
  assert.equal((await K.restore(w.c, w.st, { transactionId: 'CAP' + id, email: 'autre@example.com' }, '2.2.2.2')).status, 404);
  assert.equal((await K.activate(w.c, w.st, { licenseKey: 'MXL-AAAA-BBBB-CCCC-DDDD' }, '2.2.2.2')).status, 404);
});
test('S17 restauration après webhook seul (navigateur fermé avant retour) : possible via ID transaction + e-mail ? non → clé via PayPal reçu', async () => {
  const w = world(), id = await buy(w), e = w.pp.event('PAYMENT.CAPTURE.COMPLETED', id); await K.webhook(w.c, w.st, w.ppc, e.headers, e.raw);
  assert.equal(licCount(w), 1);                       // livrée côté serveur
  const r = await K.captureOrder(w.c, w.st, w.ppc, { orderId: id }); assert.equal(r.body.status, 'COMPLETED');   // la page retour récupère la clé quand l'acheteur revient
});
test('S18 anti force brute : activation/restauration limitées par IP', async () => {
  const w = world(); let last;
  for (let i = 0; i < 12; i++) last = await K.restore(w.c, w.st, { transactionId: 'X' + i, email: 'a@b.c' }, '3.3.3.3'); assert.equal(last.status, 429);
  for (let i = 0; i < 32; i++) last = await K.activate(w.c, w.st, { licenseKey: 'MXL-0000-0000-0000-' + i }, '4.4.4.4'); assert.equal(last.status, 429);
});
test('S19 manipulation du localStorage : jeton modifié, expiré ou signé par un autre ne passe pas', async () => {
  const w = world(), id = await buy(w), r = await K.captureOrder(w.c, w.st, w.ppc, { orderId: id }), [h, p, s] = r.body.token.split('.');
  const pl = JSON.parse(Buffer.from(p, 'base64url')); pl.prd = 'torch-comfort'; pl.exp += 99999999;
  assert.equal(K.verifyToken(pub(), h + '.' + K.b64u(JSON.stringify(pl)) + '.' + s), null);
  const other = crypto.generateKeyPairSync('ec', { namedCurve: 'prime256v1' }).privateKey.export({ type: 'pkcs8', format: 'pem' });
  assert.equal(K.verifyToken(pub(), K.signToken({ signKey: other }, { sub: 'L1', prd: 'torch-full', exp: Math.floor(Date.now() / 1000) + 999 })), null);
  assert.equal(K.verifyToken(pub(), K.signToken({ signKey: PEM }, { sub: 'L1', prd: 'torch-full', exp: Math.floor(Date.now() / 1000) - 5 })), null);
  assert.equal(K.verifyToken(pub(), 'n.importe.quoi'), null); assert.equal(K.verifyToken(pub(), ''), null);
  assert.equal((await K.refresh(w.c, w.st, { token: h + '.' + K.b64u(JSON.stringify({ sub: 'LFAKE' })) + '.' + s })).status, 404);
});
test('S20 rattachement à un compte joueur : une licence, un compte', async () => {
  const w = world(), id = await buy(w), r = await K.captureOrder(w.c, w.st, w.ppc, { orderId: id });
  assert.equal((await K.bindAccount(w.c, w.st, { token: r.body.token, accountId: 'acc1' })).status, 200);
  assert.equal((await K.bindAccount(w.c, w.st, { token: r.body.token, accountId: 'acc1' })).status, 200);
  assert.equal((await K.bindAccount(w.c, w.st, { token: r.body.token, accountId: 'acc2' })).status, 409);
});
test('S21 aucun secret dans les réponses ni dans les journaux', async () => {
  const w = world(), id = await buy(w), outs = [];
  outs.push(JSON.stringify(await K.captureOrder(w.c, w.st, w.ppc, { orderId: id })), JSON.stringify(await K.createOrder(w.c, w.st, w.ppc, { productId: 'nope' })), JSON.stringify(await K.captureOrder(w.c, w.st, w.ppc, { orderId: 'zzz' })), K.publicKeyPem(w.c));
  const blob = outs.join('|') + logs.join('|');
  for (const s of [SECRETS.id, SECRETS.secret, SECRETS.lic, 'PRIVATE KEY', 'Basic ']) assert.ok(!blob.includes(s), 'fuite: ' + s);
  const stored = JSON.stringify([...w.st._dump()]); assert.ok(!stored.includes('MXL-'), 'clé de licence stockée en clair');
});
