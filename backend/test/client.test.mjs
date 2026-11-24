import test from 'node:test'; import assert from 'node:assert/strict'; import crypto from 'node:crypto'; import vm from 'node:vm'; import fs from 'node:fs';
import * as K from '../lib/core.mjs';
const { privateKey } = crypto.generateKeyPairSync('ec', { namedCurve: 'prime256v1' }), PEM = privateKey.export({ type: 'pkcs8', format: 'pem' }), c = { signKey: PEM }, pub = K.publicKeyPem(c);
const load = (ls = {}) => { const w = { MAXLOL_PAY_PUBKEY: pub, crypto: crypto.webcrypto, TextEncoder, TextDecoder, atob, btoa, localStorage: { getItem: k => ls[k] ?? null, setItem: (k, v) => ls[k] = v, removeItem: k => delete ls[k] } }; vm.runInNewContext(fs.readFileSync(new URL('../../assets/maxlol-pay.js', import.meta.url), 'utf8'), { ...w, window: w, globalThis: w, console }); return { MP: w.MaxlolPay, ls }; };
const now = () => Math.floor(Date.now() / 1000);
test('C1 navigateur : jeton serveur valide → owns()=true pour son produit seulement', async () => {
  const t = K.signToken(c, { sub: 'L1', prd: 'torch-full', exp: now() + 999 }), { MP } = load({ 'mxl-license-v1': JSON.stringify({ token: t }) });
  assert.equal(await MP.owns('torch-full'), true); assert.equal(await MP.owns('torch-comfort'), false);
});
test('C2 navigateur : localStorage falsifié (faux jeton, charge modifiée, expiré, autre clé) → refusé', async () => {
  const good = K.signToken(c, { sub: 'L1', prd: 'torch-full', exp: now() + 999 }), [h, p, s] = good.split('.');
  const forged = h + '.' + K.b64u(JSON.stringify({ sub: 'L1', prd: 'torch-full', exp: now() + 9e8 })) + '.' + s;
  const other = crypto.generateKeyPairSync('ec', { namedCurve: 'prime256v1' }).privateKey.export({ type: 'pkcs8', format: 'pem' });
  for (const token of [forged, 'a.b.c', 'x', K.signToken({ signKey: other }, { sub: 'L1', prd: 'torch-full', exp: now() + 99 }), K.signToken(c, { sub: 'L1', prd: 'torch-full', exp: now() - 1 })]) {
    const { MP } = load({ 'mxl-license-v1': JSON.stringify({ token }) }); assert.equal(await MP.owns('torch-full'), false);
  }
  const { MP } = load({ 'mxl-license-v1': '{"product":"torch-full","owned":true}' }); assert.equal(await MP.owns('torch-full'), false);   // simple drapeau "acheté" sans signature
  assert.equal(await load().MP.owns('torch-full'), false);
});
