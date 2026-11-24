/* Maxlol Games — client de paiement commun (tous les jeux). Aucune clé secrète ici : uniquement la clé PUBLIQUE de vérification.
   Les prix ne sont jamais envoyés : on envoie seulement un identifiant produit (le serveur connaît les prix). */
(function (root) {
  'use strict';
  var API = root.MAXLOL_PAY_API || 'https://maxlol-pay.netlify.app/api';
  var PUB = root.MAXLOL_PAY_PUBKEY || '';            // PEM SPKI de la clé publique (affichée par GET /api/public-key), figée dans le site
  var LS = 'mxl-license-v1';
  function store(k, v) { try { if (v === undefined) return localStorage.getItem(k); if (v === null) localStorage.removeItem(k); else localStorage.setItem(k, v); } catch (e) { return null; } }
  function post(path, body) {
    return fetch(API + path, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(body || {}) })
      .then(function (r) { return r.json().catch(function () { return {}; }).then(function (j) { return { status: r.status, body: j }; }); });
  }
  function fromB64u(s) { s = s.replace(/-/g, '+').replace(/_/g, '/'); while (s.length % 4) s += '='; var b = atob(s), u = new Uint8Array(b.length); for (var i = 0; i < b.length; i++) u[i] = b.charCodeAt(i); return u; }
  var keyP = null;
  function pubKey() {
    if (!keyP) { var der = fromB64u(PUB.replace(/-----[A-Z ]+-----/g, '').replace(/\s+/g, '').replace(/\+/g, '-').replace(/\//g, '_').replace(/=+$/, '')); keyP = crypto.subtle.importKey('spki', der, { name: 'ECDSA', namedCurve: 'P-256' }, false, ['verify']); }
    return keyP;
  }
  // Vérifie la signature ES256 + l'expiration du jeton. Retourne la charge utile ou null.
  function verify(token) {
    try {
      var p = String(token || '').split('.'); if (p.length !== 3 || !PUB) return Promise.resolve(null);
      return pubKey().then(function (k) { return crypto.subtle.verify({ name: 'ECDSA', hash: 'SHA-256' }, k, fromB64u(p[2]), new TextEncoder().encode(p[0] + '.' + p[1])); })
        .then(function (ok) { if (!ok) return null; var pl = JSON.parse(new TextDecoder().decode(fromB64u(p[1]))); return pl.exp * 1000 > Date.now() ? pl : null; })
        .catch(function () { return null; });
    } catch (e) { return Promise.resolve(null); }
  }
  function save(r) { if (r && r.token) store(LS, JSON.stringify({ token: r.token, key: r.licenseKey, product: r.product })); return r; }
  var MP = {
    verify: verify,
    // Lance l'achat : le serveur crée la commande au bon prix, on redirige vers PayPal.
    buy: function (productId, backPath) {
      return post('/orders/create', { productId: productId, returnPath: backPath || location.pathname }).then(function (r) {
        if (r.body && r.body.approveUrl) { location.href = r.body.approveUrl; return true; } throw new Error(r.body && r.body.error || 'paiement_indisponible');
      });
    },
    // Page de retour PayPal : capture côté serveur puis mémorise la licence.
    complete: function (orderId) { return post('/orders/capture', { orderId: orderId }).then(function (r) { if (r.body.status === 'COMPLETED') save(r.body); return r; }); },
    activate: function (licenseKey) { return post('/license/activate', { licenseKey: licenseKey }).then(function (r) { if (r.status === 200) save(r.body); return r; }); },
    restore: function (transactionId, email) { return post('/license/restore', { transactionId: transactionId, email: email }).then(function (r) { if (r.status === 200) save(r.body); return r; }); },
    // Le jeu appelle ceci au démarrage : vrai seulement si le jeton stocké est signé par Maxlol Games, non expiré et pour ce jeu/produit.
    // Rien n'est cru depuis localStorage sans vérification de signature.
    owns: function (productId) {
      var d; try { d = JSON.parse(store(LS) || 'null'); } catch (e) { d = null; }
      if (!d) return Promise.resolve(false);
      return verify(d.token).then(function (pl) { return !!pl && pl.prd === productId; });
    },
    // En ligne : renouvelle le jeton (un remboursement coupe l'accès à la prochaine actualisation, au plus tard à l'expiration du jeton).
    refresh: function () {
      var d; try { d = JSON.parse(store(LS) || 'null'); } catch (e) { d = null; } if (!d) return Promise.resolve(null);
      return post('/license/refresh', { token: d.token }).then(function (r) { if (r.status === 200) { save(r.body); return true; } if (r.status === 403 || r.status === 404) { store(LS, null); return false; } return null; }).catch(function () { return null; });
    },
    savedKey: function () { try { return (JSON.parse(store(LS) || 'null') || {}).key || ''; } catch (e) { return ''; } }
  };
  root.MaxlolPay = MP;
})(typeof window !== 'undefined' ? window : globalThis);
