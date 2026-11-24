// Simulateur PayPal (même contrat que l'API REST v2 / webhooks). Sert aux tests hors ligne ; les vrais essais Sandbox utilisent le mode "sandbox" de run-sandbox.mjs.
import crypto from 'node:crypto';
export function mockPayPal({ webhookId = 'WH-TEST', merchantId = 'MERCHANT1', payerEmail = 'Acheteur@Example.com' } = {}) {
  const orders = new Map(), calls = { capture: 0, create: 0, token: 0 }; let n = 0;
  const sigOf = raw => 'sig:' + crypto.createHash('sha256').update(raw).digest('hex');
  const R = (status, body) => ({ ok: status < 300, status, json: async () => body });
  async function f(url, init = {}) {
    const p = new URL(url).pathname, body = init.body, m = init.method || 'GET';
    if (p === '/v1/oauth2/token') { calls.token++; return R(200, { access_token: 'tok-' + calls.token, expires_in: 3000 }); }
    if (p === '/v2/checkout/orders' && m === 'POST') {
      calls.create++; const b = JSON.parse(body), id = 'ORD' + (++n);
      orders.set(id, { id, unit: b.purchase_units[0], state: 'CREATED', mode: 'ok', captured: null });
      return R(201, { id, status: 'PAYER_ACTION_REQUIRED', links: [{ rel: 'payer-action', href: 'https://sandbox.paypal.com/checkoutnow?token=' + id }] });
    }
    let mm = p.match(/^\/v2\/checkout\/orders\/([^/]+)\/capture$/);
    if (mm) {
      calls.capture++; const o = orders.get(mm[1]);
      if (!o) return R(404, { name: 'RESOURCE_NOT_FOUND' });
      if (o.captured) return R(200, o.captured);                               // PayPal-Request-Id identique : même réponse, pas de 2e débit
      if (o.state !== 'APPROVED') return R(422, { name: 'UNPROCESSABLE_ENTITY', details: [{ issue: 'ORDER_NOT_APPROVED' }] });
      const u = o.unit, mode = o.mode;
      if (mode === 'declined') return R(422, { name: 'UNPROCESSABLE_ENTITY', details: [{ issue: 'INSTRUMENT_DECLINED' }] });
      const amount = { currency_code: mode === 'tamper_currency' ? 'USD' : u.amount.currency_code, value: mode === 'tamper_amount' ? '0.01' : u.amount.value };
      const cap = { id: 'CAP' + o.id, status: mode === 'pending' ? 'PENDING' : 'COMPLETED', amount };
      o.captured = { id: o.id, status: 'COMPLETED', payer: { email_address: payerEmail }, purchase_units: [{ reference_id: mode === 'tamper_ref' ? 'torch-comfort' : u.reference_id, custom_id: u.custom_id, payee: { merchant_id: mode === 'tamper_payee' ? 'ATTACKER' : merchantId }, payments: { captures: [cap] } }] };
      return R(201, o.captured);
    }
    if (p === '/v1/notifications/verify-webhook-signature') {
      const b = JSON.parse(body), raw = body.slice(body.indexOf('"webhook_event":') + 16, -1);
      return R(200, { verification_status: b.transmission_sig === sigOf(raw) && b.webhook_id === webhookId ? 'SUCCESS' : 'FAILURE' });
    }
    return R(404, {});
  }
  const approve = (id, mode = 'ok') => { const o = orders.get(id); o.state = 'APPROVED'; o.mode = mode; };
  const event = (type, orderId, o = {}) => { const e = { id: 'WH-EVT-' + (++n), event_type: type, resource: { id: 'CAP' + orderId, amount: o.amount || { value: '7.99', currency_code: 'EUR' }, payee: { merchant_id: merchantId }, supplementary_data: { related_ids: { order_id: orderId } } } }, raw = JSON.stringify(e);
    return { raw, headers: new Map(Object.entries({ 'paypal-auth-algo': 'SHA256withRSA', 'paypal-cert-url': 'https://api.paypal.com/cert', 'paypal-transmission-id': 'tid', 'paypal-transmission-time': new Date().toISOString(), 'paypal-transmission-sig': o.badSig ? 'forged' : sigOf(raw) })) }; };
  return { fetch: f, orders, calls, approve, event, merchantId, payerEmail };
}
