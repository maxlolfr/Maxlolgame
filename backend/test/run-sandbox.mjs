// Essai RÉEL en PayPal Sandbox (aucun vrai argent). Variables : PAYPAL_CLIENT_ID, PAYPAL_CLIENT_SECRET (app Sandbox), LICENSE_SECRET, SIGNING_PRIVATE_KEY_PEM.
//   node test/run-sandbox.mjs create            -> crée une commande Sandbox, affiche le lien à ouvrir avec un compte ACHETEUR Sandbox
//   node test/run-sandbox.mjs capture ORDER_ID  -> capture et vérifie la livraison
import * as K from '../lib/core.mjs';
const env = { ...process.env, PAYPAL_ENV: 'sandbox' }; const c = K.cfg(env), st = K.memoryStore(), ppc = K.paypal(c);
const [cmd, id] = process.argv.slice(2);
if (cmd === 'create') { const r = await K.createOrder(c, st, ppc, { productId: 'torch-full' }); console.log(r.status, r.body.orderId, r.body.approveUrl); }
else if (cmd === 'capture') { await st.set('order:' + id, { orderId: id, productId: 'torch-full', status: 'CREATED' }); const r = await K.captureOrder(c, st, ppc, { orderId: id }); console.log(r.status, r.body.status, r.body.licenseKey ? 'licence émise' : 'aucune licence'); }
