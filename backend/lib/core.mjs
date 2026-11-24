// Maxlol Games — noyau de paiement commun (tous les jeux). Aucune clé secrète dans ce fichier : tout vient de l'environnement.
import crypto from 'node:crypto';

// ---------- Catalogue : SEULE source de vérité des prix (le client n'envoie jamais un prix) ----------
export const CATALOG = {
  'torch-full': { game: 'torch', name: 'La Dernière Torche — jeu complet', value: '7.99', currency: 'EUR', enabled: true },
  // Pass Confort : annoncé dans le jeu ("paiement bientôt"), désactivé tant que le créateur n'a pas validé.
  'torch-comfort': { game: 'torch', name: 'La Dernière Torche — Pass Confort', value: '1.99', currency: 'USD', enabled: false },
};

export const b64u = b => Buffer.from(b).toString('base64url');
export const sha = s => crypto.createHash('sha256').update(String(s)).digest('hex');
const hmac = (secret, s) => crypto.createHmac('sha256', secret).update(s).digest();

export function cfg(env) {
  const live = env.PAYPAL_ENV === 'live';
  return {
    api: live ? 'https://api-m.paypal.com' : 'https://api-m.sandbox.paypal.com',
    live, id: env.PAYPAL_CLIENT_ID, secret: env.PAYPAL_CLIENT_SECRET, webhookId: env.PAYPAL_WEBHOOK_ID,
    merchantId: env.PAYPAL_MERCHANT_ID || '', licSecret: env.LICENSE_SECRET, signKey: env.SIGNING_PRIVATE_KEY_PEM,
    origins: (env.ALLOWED_ORIGINS || 'https://maxlolgames.com').split(',').map(s => s.trim()),
    site: env.SITE_URL || 'https://maxlolgames.com', apiBase: env.API_BASE || '',
    sbUrl: (env.SUPABASE_URL || '').replace(/\/$/, ''), sbSecret: env.SUPABASE_JWT_SECRET || '', sbService: env.SUPABASE_SERVICE_KEY || '',
  };
}

// ---------- Stockage : adaptateur (Netlify Blobs en production, mémoire en test) ----------
export function memoryStore() {
  const m = new Map();
  return {
    async get(k) { return m.has(k) ? structuredClone(m.get(k)) : null; },
    async set(k, v) { m.set(k, structuredClone(v)); },
    async setIfNew(k, v) { if (m.has(k)) return false; m.set(k, structuredClone(v)); return true; },
    async del(k) { m.delete(k); },
    _dump: () => m,
  };
}
export function blobsStore(getStore) {
  const s = getStore({ name: 'maxlol-pay', consistency: 'strong' });
  return {
    async get(k) { return (await s.get(k, { type: 'json' })) ?? null; },
    async set(k, v) { await s.setJSON(k, v); },
    async setIfNew(k, v) { const r = await s.setJSON(k, v, { onlyIfNew: true }); return r.modified !== false; },
    async del(k) { await s.delete(k); },
  };
}

// ---------- PayPal REST (côté serveur uniquement) ----------
export function paypal(c, f = fetch) {
  let tok = null, exp = 0;
  async function token() {
    if (tok && Date.now() < exp) return tok;
    const r = await f(c.api + '/v1/oauth2/token', { method: 'POST', headers: { Authorization: 'Basic ' + Buffer.from(c.id + ':' + c.secret).toString('base64'), 'Content-Type': 'application/x-www-form-urlencoded' }, body: 'grant_type=client_credentials' });
    if (!r.ok) throw new Error('paypal_auth_' + r.status);
    const j = await r.json(); tok = j.access_token; exp = Date.now() + (j.expires_in - 60) * 1000; return tok;
  }
  async function call(path, method, body, extra = {}) {
    const r = await f(c.api + path, { method, headers: { Authorization: 'Bearer ' + await token(), 'Content-Type': 'application/json', ...extra }, body: body === undefined ? undefined : (typeof body === 'string' ? body : JSON.stringify(body)) });
    const j = await r.json().catch(() => ({})); return { status: r.status, ok: r.ok, body: j };
  }
  return { createOrder: b => call('/v2/checkout/orders', 'POST', b, { 'PayPal-Request-Id': crypto.randomUUID() }), captureOrder: (id, rid) => call('/v2/checkout/orders/' + encodeURIComponent(id) + '/capture', 'POST', '{}', { 'PayPal-Request-Id': rid }),
    getOrder: id => call('/v2/checkout/orders/' + encodeURIComponent(id), 'GET'), verifyWebhook: s => call('/v1/notifications/verify-webhook-signature', 'POST', s) };
}

// ---------- Licences : clé dérivée (jamais stockée en clair) + jeton d'accès signé ES256 ----------
export function licenseKey(c, licenseId) {
  const raw = hmac(c.licSecret, 'key:' + licenseId).subarray(0, 10);
  const A = 'ABCDEFGHJKLMNPQRSTUVWXYZ23456789'; let bits = '', out = '';
  for (const b of raw) bits += b.toString(2).padStart(8, '0');
  for (let i = 0; i < 16; i++) out += A[parseInt(bits.slice(i * 5, i * 5 + 5), 2)];
  return 'MXL-' + out.match(/.{4}/g).join('-');
}
export function signToken(c, payload) {
  const h = b64u(JSON.stringify({ alg: 'ES256', typ: 'MXL' })), p = b64u(JSON.stringify(payload));
  const sig = crypto.sign('sha256', Buffer.from(h + '.' + p), { key: c.signKey, dsaEncoding: 'ieee-p1363' });
  return h + '.' + p + '.' + b64u(sig);
}
export function verifyToken(pubPem, t) {
  try {
    const [h, p, s] = t.split('.');
    if (!crypto.verify('sha256', Buffer.from(h + '.' + p), { key: pubPem, dsaEncoding: 'ieee-p1363' }, Buffer.from(s, 'base64url'))) return null;
    const pl = JSON.parse(Buffer.from(p, 'base64url').toString()); return pl.exp * 1000 > Date.now() ? pl : null;
  } catch { return null; }
}
export const publicKeyPem = c => crypto.createPublicKey(c.signKey).export({ type: 'spki', format: 'pem' });
const TOKEN_DAYS = 14;
const mkToken = (c, lic) => signToken(c, { sub: lic.id, prd: lic.productId, game: CATALOG[lic.productId]?.game, iat: Math.floor(Date.now() / 1000), exp: Math.floor(Date.now() / 1000) + TOKEN_DAYS * 86400 });

// ---------- Validation d'une capture (prix, devise, produit, destinataire, statut) ----------
export function checkCapture(c, order, pp) {
  const pu = pp?.purchase_units?.[0], cap = pu?.payments?.captures?.[0], prod = CATALOG[order.productId];
  if (!prod) return 'produit_inconnu';
  if (!cap) return 'capture_absente';
  if (pu.reference_id !== order.productId || pu.custom_id !== order.productId) return 'produit_different';
  if (cap.amount?.value !== prod.value || cap.amount?.currency_code !== prod.currency) return 'montant_ou_devise_different';
  if (c.merchantId && pu.payee?.merchant_id !== c.merchantId) return 'destinataire_different';
  return null;
}

// ---------- Livraison idempotente ----------
async function grant(c, st, order, capId, payerEmail) {
  const id = 'L' + crypto.randomBytes(9).toString('base64url');
  if (!(await st.setIfNew('capture:' + capId, id))) return { already: true, licenseId: await st.get('capture:' + capId) };   // transaction déjà utilisée : on renvoie la licence existante
  await st.set('license:' + id, { id, productId: order.productId, status: 'active', orderId: order.orderId, captureId: capId, accountId: null, createdAt: Date.now() });
  await st.set('lkey:' + sha(licenseKey(c, id)), id);
  if (payerEmail) await st.set('rec:' + sha(capId + ':' + payerEmail.trim().toLowerCase()), id);
  const o = await st.get('order:' + order.orderId); await st.set('order:' + order.orderId, { ...o, status: 'COMPLETED', captureId: capId, licenseId: id });
  return { licenseId: id };
}
const reply = (c, st, lid) => st.get('license:' + lid).then(l => ({ licenseKey: licenseKey(c, lid), token: mkToken(c, l), product: l.productId }));

// ---------- Étapes métier ----------
export async function createOrder(c, st, ppc, { productId, returnPath }) {
  const prod = CATALOG[productId];
  if (!prod || !prod.enabled) return { status: 400, body: { error: 'produit_indisponible' } };
  const base = c.site, back = typeof returnPath === 'string' && /^\/[a-z0-9\/_-]*$/i.test(returnPath) ? returnPath : '/';
  const r = await ppc.createOrder({ intent: 'CAPTURE', purchase_units: [{ reference_id: productId, custom_id: productId, description: prod.name, amount: { currency_code: prod.currency, value: prod.value }, ...(c.merchantId ? { payee: { merchant_id: c.merchantId } } : {}) }],
    payment_source: { paypal: { experience_context: { return_url: base + '/pay/return/', cancel_url: base + '/pay/cancel/?back=' + encodeURIComponent(back), user_action: 'PAY_NOW', shipping_preference: 'NO_SHIPPING', brand_name: 'Maxlol Games' } } } });
  if (!r.ok || !r.body.id) return { status: 502, body: { error: 'paypal_indisponible' } };
  const approve = (r.body.links || []).find(l => ['payer-action', 'approve'].includes(l.rel))?.href;
  await st.set('order:' + r.body.id, { orderId: r.body.id, productId, status: 'CREATED', createdAt: Date.now() });
  return { status: 200, body: { orderId: r.body.id, approveUrl: approve } };
}

export async function captureOrder(c, st, ppc, { orderId }) {
  const order = typeof orderId === 'string' ? await st.get('order:' + orderId) : null;
  if (!order) return { status: 404, body: { error: 'commande_inconnue' } };
  if (order.status === 'COMPLETED') return { status: 200, body: { status: 'COMPLETED', ...(await reply(c, st, order.licenseId)) } };   // rejeu : même licence, pas de 2e
  if (order.status === 'REFUNDED') return { status: 200, body: { status: 'REFUNDED' } };
    const lock = 'lock:' + orderId + ':' + Math.floor(Date.now() / 60000);
  if (!(await st.setIfNew(lock, 1))) return { status: 409, body: { error: 'capture_en_cours' } };   // verrou atomique : un seul appel capture à la fois
  const r = await ppc.captureOrder(orderId, 'cap-' + orderId);   // PayPal-Request-Id fixe : PayPal ne capture jamais deux fois
  if (!r.ok) { const cancelled = r.body?.details?.some(d => /ORDER_NOT_APPROVED|PAYER_ACTION_REQUIRED/.test(d.issue)); await st.set('order:' + orderId, { ...order, status: cancelled ? 'CREATED' : 'FAILED' }); await st.del(lock); return { status: cancelled ? 402 : 502, body: { status: cancelled ? 'NOT_APPROVED' : 'FAILED' } }; }
  const cap = r.body.purchase_units?.[0]?.payments?.captures?.[0];
  if (r.body.status !== 'COMPLETED' || !cap) { await st.set('order:' + orderId, { ...order, status: 'FAILED' }); await st.del(lock); return { status: 402, body: { status: 'FAILED' } }; }
  const bad = checkCapture(c, order, r.body);
  if (bad) { await st.set('order:' + orderId, { ...order, status: 'REJECTED', reason: bad }); console.error('capture rejetée', orderId, bad); return { status: 422, body: { status: 'REJECTED' } }; }
  if (cap.status === 'PENDING') { await st.set('order:' + orderId, { ...order, status: 'PENDING', captureId: cap.id, payerHash: sha(r.body.payer?.email_address || '') }); return { status: 202, body: { status: 'PENDING' } }; }
  if (cap.status !== 'COMPLETED') { await st.set('order:' + orderId, { ...order, status: 'DENIED' }); return { status: 402, body: { status: 'DENIED' } }; }
  const g = await grant(c, st, order, cap.id, r.body.payer?.email_address);
  return { status: 200, body: { status: 'COMPLETED', ...(await reply(c, st, g.licenseId)) } };
}

export async function webhook(c, st, ppc, headers, raw) {
  const h = k => headers.get ? headers.get(k) : headers[k];
  const ver = await ppc.verifyWebhook(`{"auth_algo":${JSON.stringify(h('paypal-auth-algo'))},"cert_url":${JSON.stringify(h('paypal-cert-url'))},"transmission_id":${JSON.stringify(h('paypal-transmission-id'))},"transmission_sig":${JSON.stringify(h('paypal-transmission-sig'))},"transmission_time":${JSON.stringify(h('paypal-transmission-time'))},"webhook_id":${JSON.stringify(c.webhookId)},"webhook_event":${raw}}`);
  if (!ver.ok || ver.body.verification_status !== 'SUCCESS') return { status: 400, body: { error: 'signature_invalide' } };
  const ev = JSON.parse(raw);
  if (!(await st.setIfNew('evt:' + ev.id, 1))) return { status: 200, body: { dup: true } };   // événement déjà traité
  const res = ev.resource || {}, orderId = res.supplementary_data?.related_ids?.order_id || res.id;
  const order = orderId ? await st.get('order:' + orderId) : null;
  if (!order) return { status: 200, body: { ignored: 'commande_inconnue' } };
  switch (ev.event_type) {
    case 'PAYMENT.CAPTURE.COMPLETED': {
      if (order.status === 'REFUNDED') break;
      const prod = CATALOG[order.productId];
      if (res.amount?.value !== prod?.value || res.amount?.currency_code !== prod?.currency || (c.merchantId && res.payee?.merchant_id && res.payee.merchant_id !== c.merchantId)) { await st.set('order:' + orderId, { ...order, status: 'REJECTED', reason: 'webhook_montant' }); break; }
      await grant(c, st, order, res.id, null); break; }
    case 'PAYMENT.CAPTURE.PENDING': if (order.status !== 'COMPLETED') await st.set('order:' + orderId, { ...order, status: 'PENDING' }); break;
    case 'PAYMENT.CAPTURE.DENIED': case 'PAYMENT.CAPTURE.DECLINED': if (order.status !== 'COMPLETED') await st.set('order:' + orderId, { ...order, status: 'DENIED' }); break;
    case 'PAYMENT.CAPTURE.REFUNDED': case 'PAYMENT.CAPTURE.REVERSED': {
      const prod = CATALOG[order.productId], full = Number(res.amount?.value) >= Number(prod?.value) || ev.event_type.endsWith('REVERSED');
      if (full && order.licenseId) { const l = await st.get('license:' + order.licenseId); await st.set('license:' + l.id, { ...l, status: 'revoked', revokedAt: Date.now() }); await st.set('order:' + orderId, { ...order, status: 'REFUNDED' }); } break; }
  }
  return { status: 200, body: { ok: true } };
}

// ---------- Jeton / restauration ----------
async function limited(st, ip, bucket, max) {
  const k = 'rl:' + bucket + ':' + sha(ip) + ':' + Math.floor(Date.now() / 3600000), n = ((await st.get(k)) || 0) + 1; await st.set(k, n); return n > max;
}
export async function activate(c, st, { licenseKey: key }, ip) {
  if (await limited(st, ip, 'act', 30)) return { status: 429, body: { error: 'trop_de_tentatives' } };
  const lid = typeof key === 'string' ? await st.get('lkey:' + sha(key.trim().toUpperCase())) : null, l = lid && await st.get('license:' + lid);
  if (!l || l.status !== 'active') return { status: 404, body: { error: 'licence_invalide' } };
  return { status: 200, body: await reply(c, st, l.id) };
}
export async function refresh(c, st, { token }) {   // appelé par le jeu en ligne : un remboursement coupe l'accès à l'expiration du jeton
  const pl = verifyToken(publicKeyPem(c), String(token || '')) || (() => { try { return JSON.parse(Buffer.from(String(token).split('.')[1], 'base64url')); } catch { return null; } })();
  const l = pl && await st.get('license:' + pl.sub);
  if (!l) return { status: 404, body: { error: 'licence_invalide' } };
  if (l.status !== 'active') return { status: 403, body: { error: 'licence_revoquee' } };
  return { status: 200, body: await reply(c, st, l.id) };
}
export async function restore(c, st, { transactionId, email }, ip) {   // changement de téléphone / cache vidé : ID de transaction PayPal + e-mail PayPal
  if (await limited(st, ip, 'rst', 10)) return { status: 429, body: { error: 'trop_de_tentatives' } };
  const lid = await st.get('rec:' + sha(String(transactionId || '').trim() + ':' + String(email || '').trim().toLowerCase())), l = lid && await st.get('license:' + lid);
  if (!l || l.status !== 'active') return { status: 404, body: { error: 'achat_introuvable' } };
  return { status: 200, body: await reply(c, st, l.id) };
}
// Futur compte joueur universel : rattache une licence à un compte (sans la déplacer vers un autre).
export async function bindAccount(c, st, { token, accountId }) {
  const pl = verifyToken(publicKeyPem(c), String(token || '')), l = pl && await st.get('license:' + pl.sub);
  if (!l || l.status !== 'active') return { status: 404, body: { error: 'licence_invalide' } };
  if (l.accountId && l.accountId !== accountId) return { status: 409, body: { error: 'deja_rattachee' } };
  await st.set('license:' + l.id, { ...l, accountId }); return { status: 200, body: { ok: true } };
}

// ---------- Compte joueur (Supabase Auth) : le serveur de paiement ne fait confiance qu'à un JWT Supabase vérifié ----------
let jwksCache = { at: 0, keys: [] };
export async function supabaseUser(c, authHeader, f = fetch) {
  const t = /^Bearer (.+)$/.exec(authHeader || '')?.[1]; if (!t || !c.sbUrl) return null;
  try {
    const [h, p, sg] = t.split('.'), head = JSON.parse(Buffer.from(h, 'base64url')), pl = JSON.parse(Buffer.from(p, 'base64url')), data = Buffer.from(h + '.' + p);
    if (pl.exp * 1000 < Date.now() || pl.aud !== 'authenticated' || pl.iss !== c.sbUrl + '/auth/v1' || !pl.sub || pl.role !== 'authenticated') return null;
    let ok = false;
    if (head.alg === 'HS256') { if (!c.sbSecret) return null; const mac = crypto.createHmac('sha256', c.sbSecret).update(data).digest(), got = Buffer.from(sg, 'base64url'); ok = mac.length === got.length && crypto.timingSafeEqual(mac, got); }
    else if (head.alg === 'ES256' || head.alg === 'RS256') {
      if (Date.now() - jwksCache.at > 600000) { const r = await f(c.sbUrl + '/auth/v1/.well-known/jwks.json'); jwksCache = { at: Date.now(), keys: (await r.json()).keys || [] }; }
      const jwk = jwksCache.keys.find(k => k.kid === head.kid); if (!jwk) return null;
      const key = crypto.createPublicKey({ key: jwk, format: 'jwk' });
      ok = head.alg === 'ES256' ? crypto.verify('sha256', data, { key, dsaEncoding: 'ieee-p1363' }, Buffer.from(sg, 'base64url')) : crypto.verify('sha256', data, key, Buffer.from(sg, 'base64url'));
    } else return null;                                    // "alg: none" et tout autre algorithme refusés
    return ok ? { id: pl.sub, email: pl.email } : null;
  } catch { return null; }
}
export const resetJwks = () => { jwksCache = { at: 0, keys: [] }; };
const accList = async (st, id) => (await st.get('acc:' + id)) || [];

// Rattache une licence (clé MXL-… ou jeton) au compte connecté. Une licence = un seul compte.
export async function linkLicense(c, st, user, { licenseKey: key, token }) {
  if (!user) return { status: 401, body: { error: 'non_connecte' } };
  let lid = null;
  if (key) lid = await st.get('lkey:' + sha(String(key).trim().toUpperCase())); else { const pl = verifyToken(publicKeyPem(c), String(token || '')); lid = pl?.sub; }
  const l = lid && await st.get('license:' + lid);
  if (!l || l.status !== 'active') return { status: 404, body: { error: 'licence_invalide' } };
  if (l.accountId && l.accountId !== user.id) return { status: 409, body: { error: 'deja_rattachee' } };
  if (l.accountId !== user.id) { await st.set('license:' + l.id, { ...l, accountId: user.id }); const a = await accList(st, user.id); if (!a.includes(l.id)) await st.set('acc:' + user.id, [...a, l.id]); }
  return { status: 200, body: { ok: true, product: l.productId } };
}
// Bibliothèque + historique d'achats + jeton d'accès frais pour chaque licence active (= restauration sur un nouvel appareil par simple connexion).
export async function library(c, st, user) {
  if (!user) return { status: 401, body: { error: 'non_connecte' } };
  const items = [];
  for (const id of await accList(st, user.id)) {
    const l = await st.get('license:' + id); if (!l) continue; const o = await st.get('order:' + l.orderId), p = CATALOG[l.productId];
    items.push({ product: l.productId, game: p?.game, name: p?.name, status: l.status, purchasedAt: l.createdAt, order: { id: l.orderId, amount: p?.value, currency: p?.currency, status: o?.status }, token: l.status === 'active' ? mkToken(c, l) : null });
  }
  return { status: 200, body: { items } };
}
// Effacement : le compte est détaché des licences ; l'achat reste valide via sa clé (obligation de conserver la trace comptable du paiement).
export async function unlinkAll(c, st, user) {
  if (!user) return { status: 401, body: { error: 'non_connecte' } };
  for (const id of await accList(st, user.id)) { const l = await st.get('license:' + id); if (l) await st.set('license:' + id, { ...l, accountId: null }); }
  await st.set('acc:' + user.id, []); return { status: 200, body: { ok: true } };
}

// Suppression définitive du compte d'authentification (clé service uniquement côté serveur). Les licences sont détachées, pas supprimées.
export async function deleteAccount(c, st, user, f = fetch) {
  if (!user) return { status: 401, body: { error: 'non_connecte' } };
  if (!c.sbService) return { status: 500, body: { error: 'configuration_incomplete' } };
  await unlinkAll(c, st, user);
  const r = await f(c.sbUrl + '/auth/v1/admin/users/' + encodeURIComponent(user.id), { method: 'DELETE', headers: { apikey: c.sbService, Authorization: 'Bearer ' + c.sbService } });
  return r.ok ? { status: 200, body: { ok: true } } : { status: 502, body: { error: 'suppression_impossible' } };
}
