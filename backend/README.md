# maxlol-pay — paiements communs Maxlol Games
Variables d'environnement (Netlify > Site settings > Environment variables), **jamais dans le dépôt** :
`PAYPAL_ENV` (sandbox|live), `PAYPAL_CLIENT_ID`, `PAYPAL_CLIENT_SECRET`, `PAYPAL_WEBHOOK_ID`, `PAYPAL_MERCHANT_ID`, `LICENSE_SECRET` (32+ octets aléatoires), `SIGNING_PRIVATE_KEY_PEM` (EC P-256, PKCS8), `ALLOWED_ORIGINS`, `SITE_URL`.
Nouveau jeu : ajouter une entrée dans `CATALOG` (lib/core.mjs), puis `MaxlolPay.owns('<id>')` dans le jeu. Tests : `npm test`.
