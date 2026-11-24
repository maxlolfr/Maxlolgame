// Point d'entrée unique /api/* (Netlify Functions v2). Secrets : variables d'environnement Netlify uniquement.
import { getStore } from '@netlify/blobs';
import { cfg, blobsStore, paypal, createOrder, captureOrder, webhook, activate, supabaseUser, linkLicense, library, unlinkAll, deleteAccount, refresh, restore, bindAccount, publicKeyPem } from '../../lib/core.mjs';

export const config = { path: '/api/*' };
const J = (c, req, status, body) => {
  const o = req.headers.get('origin'), ok = o && c.origins.includes(o);
  return new Response(JSON.stringify(body), { status, headers: { 'Content-Type': 'application/json', 'Cache-Control': 'no-store', 'X-Content-Type-Options': 'nosniff', ...(ok ? { 'Access-Control-Allow-Origin': o, 'Vary': 'Origin' } : {}) } });
};

export default async (req, context) => {
  const c = cfg(process.env), url = new URL(req.url), route = url.pathname.replace(/^\/api/, '');
  if (!c.id || !c.secret || !c.licSecret || !c.signKey) return J(c, req, 500, { error: 'configuration_incomplete' });
  const o = req.headers.get('origin');
  if (req.method === 'OPTIONS') return new Response(null, { status: 204, headers: o && c.origins.includes(o) ? { 'Access-Control-Allow-Origin': o, 'Access-Control-Allow-Methods': 'POST, GET', 'Access-Control-Allow-Headers': 'Content-Type, Authorization', 'Vary': 'Origin' } : {} });
  const ppc = paypal(c), ip = context?.ip || req.headers.get('x-nf-client-connection-ip') || 'x';
  try {
    if (route === '/public-key' && req.method === 'GET') return J(c, req, 200, { pem: publicKeyPem(c) });
    if (req.method !== 'POST') return J(c, req, 405, { error: 'methode' });
    if (route === '/paypal-webhook') { const st = blobsStore(getStore), r = await webhook(c, st, ppc, req.headers, await req.text()); return J(c, req, r.status, r.body); }
    if (!o || !c.origins.includes(o)) return J(c, req, 403, { error: 'origine_refusee' });           // appels navigateur : uniquement depuis maxlolgames.com
    const st = blobsStore(getStore), b = await req.json().catch(() => ({})), h = { '/orders/create': () => createOrder(c, st, ppc, b), '/orders/capture': () => captureOrder(c, st, ppc, b), '/license/activate': () => activate(c, st, b, ip), '/license/refresh': () => refresh(c, st, b), '/license/restore': () => restore(c, st, b, ip), '/license/bind': () => bindAccount(c, st, b),
      '/account/link': async () => linkLicense(c, st, await supabaseUser(c, req.headers.get('authorization')), b), '/account/library': async () => library(c, st, await supabaseUser(c, req.headers.get('authorization'))), '/account/delete': async () => deleteAccount(c, st, await supabaseUser(c, req.headers.get('authorization'))), '/account/unlink-all': async () => unlinkAll(c, st, await supabaseUser(c, req.headers.get('authorization'))) }[route];
    if (!h) return J(c, req, 404, { error: 'inconnu' });
    const r = await h(); return J(c, req, r.status, r.body);
  } catch (e) { console.error('erreur', route, e.message); return J(c, req, 500, { error: 'erreur_serveur' }); }   // jamais de secret ni de stack dans la réponse
};
