/* Maxlol Games — compte joueur universel (client). Sans dépendance : parle directement à Supabase Auth + PostgREST.
   Règles d'or : jouer sans compte reste possible ; AUCUNE sauvegarde n'est écrasée sans confirmation ; la clé "anon" est publique, la sécurité vient du RLS côté base.
   Usage : const A = MaxlolAccount.create({ url, anonKey, payApi, mock? }); A.signInEmail(email) ; A.sync(adapter, askUser) ... */
(function (root) {
  'use strict';
  var LSK = 'mxl-session-v1', LSD = 'mxl-device-v1', LSS = 'mxl-sync-v1:';
  var ls = {
    get: function (k) { try { return localStorage.getItem(k); } catch (e) { return null; } },
    set: function (k, v) { try { localStorage.setItem(k, v); } catch (e) {} },
    del: function (k) { try { localStorage.removeItem(k); } catch (e) {} }
  };
  function hash(s) { var h = 5381, i = s.length; while (i) h = (h * 33) ^ s.charCodeAt(--i); return (h >>> 0).toString(36) + ':' + s.length; }   // empreinte rapide (détection de changement, pas de sécurité)
  function deviceId() { var d = ls.get(LSD); if (!d) { d = 'd' + Math.random().toString(36).slice(2, 10); ls.set(LSD, d); } return d; }

  /* ---- Plan de synchronisation (fonction pure, testée) ----
     local : { exists, raw }  | cloud : { exists, version, raw } | base : { version, hash } (dernier état synchronisé sur CET appareil) ou null
     Retour : 'noop' | 'upload' | 'download' | 'ask' | 'adopt' (identiques : on mémorise juste l'état)
     'download' n'est proposé automatiquement que si le local n'a PAS changé depuis la dernière synchro (rien à perdre) ; sinon 'ask'. */
  function planSync(local, cloud, base) {
    if (!local.exists && !cloud.exists) return 'noop';
    if (local.exists && !cloud.exists) return 'upload';
    if (!local.exists && cloud.exists) return 'download';
    var lh = hash(local.raw);
    if (!base) return hash(cloud.raw) === lh ? 'adopt' : 'ask';           // premier rattachement de cet appareil : jamais de choix automatique
    var localChanged = lh !== base.hash, cloudChanged = cloud.version !== base.version;
    if (!localChanged && !cloudChanged) return 'noop';
    if (localChanged && !cloudChanged) return 'upload';
    if (!localChanged && cloudChanged) return 'download';
    return hash(cloud.raw) === lh ? 'adopt' : 'ask';                      // modifié des deux côtés
  }

  function create(cfg) {
    var base = cfg.url.replace(/\/$/, ''), anon = cfg.anonKey, S = null, mock = cfg.mock || null;
    try { S = JSON.parse(ls.get(LSK) || 'null'); } catch (e) { S = null; }

    function http(path, opt, auth) {
      if (mock) return mock(path, opt, auth && S);
      var h = { apikey: anon, 'Content-Type': 'application/json' }; if (auth && S) h.Authorization = 'Bearer ' + S.access_token; else h.Authorization = 'Bearer ' + anon;
      return fetch(base + path, { method: opt.method || 'POST', headers: h, body: opt.body === undefined ? undefined : JSON.stringify(opt.body) })
        .then(function (r) { return r.text().then(function (t) { var j; try { j = t ? JSON.parse(t) : {}; } catch (e) { j = {}; } return { status: r.status, body: j }; }); });
    }
    function setSession(j) { S = { access_token: j.access_token, refresh_token: j.refresh_token, expires_at: Math.floor(Date.now() / 1000) + (j.expires_in || 3600), user: j.user ? { id: j.user.id, email: j.user.email } : (S && S.user) }; ls.set(LSK, JSON.stringify(S)); return S; }
    function ensure() {                                                   // renouvelle le jeton si besoin
      if (!S) return Promise.reject(new Error('non_connecte'));
      if (S.expires_at - 60 > Date.now() / 1000) return Promise.resolve(S);
      return http('/auth/v1/token?grant_type=refresh_token', { body: { refresh_token: S.refresh_token } }).then(function (r) { if (r.status !== 200) { S = null; ls.del(LSK); throw new Error('session_expiree'); } return setSession(r.body); });
    }
    function rpc(fn, args) { return ensure().then(function () { return http('/rest/v1/rpc/' + fn, { body: args || {} }, true); }).then(function (r) { if (r.status >= 300) throw new Error((r.body && r.body.message) || 'erreur_' + r.status); return r.body; }); }
    function sel(table, q) { return ensure().then(function () { return http('/rest/v1/' + table + '?' + q, { method: 'GET' }, true); }).then(function (r) { if (r.status >= 300) throw new Error('erreur_' + r.status); return r.body; }); }
    function pay(path) { return ensure().then(function () { return fetch((cfg.payApi || '') + path, { method: 'POST', headers: { 'Content-Type': 'application/json', Authorization: 'Bearer ' + S.access_token }, body: '{}' }).then(function (r) { return r.json().then(function (j) { return { status: r.status, body: j }; }); }); }); }
    function syncKey(a) { return LSS + a.game + ':' + (a.slot || 'main'); }
    function getBase(a) { try { return JSON.parse(ls.get(syncKey(a)) || 'null'); } catch (e) { return null; } }
    function setBase(a, version, raw) { ls.set(syncKey(a), JSON.stringify({ version: version, hash: hash(raw) })); }
    function backup(a, raw, why) { try { ls.set('mxl-backup:' + a.game + ':' + (a.slot || 'main') + ':' + why + ':' + Date.now(), raw); } catch (e) {} }   // copie locale avant tout remplacement

    var A = {
      get user() { return S && S.user || null; },
      isSignedIn: function () { return !!S; },
      // Connexion : e-mail → lien magique ET code à 6 chiffres (le code marche aussi quand le lien s'ouvre dans un autre navigateur).
      signInEmail: function (email) { return http('/auth/v1/otp' + (cfg.redirectTo ? '?redirect_to=' + encodeURIComponent(cfg.redirectTo) : ''), { body: { email: email, create_user: true } }).then(function (r) { if (r.status >= 300) throw new Error((r.body && (r.body.msg || r.body.error_description)) || 'envoi_impossible'); return true; }); },
      verifyCode: function (email, code) { return http('/auth/v1/verify', { body: { type: 'email', email: email, token: String(code).trim() } }).then(function (r) { if (r.status !== 200) throw new Error('code_invalide'); return setSession(r.body).user; }); },
      // Retour du lien magique : les jetons arrivent dans le fragment d'URL (#access_token=…) ; on les range puis on nettoie l'adresse.
      handleRedirect: function () {
        var h = (root.location && root.location.hash || '').replace(/^#/, ''); if (!/access_token=/.test(h)) return null;
        var p = new URLSearchParams(h); setSession({ access_token: p.get('access_token'), refresh_token: p.get('refresh_token'), expires_in: +p.get('expires_in') || 3600, user: null });
        try { history.replaceState(null, '', location.pathname + location.search); } catch (e) {}
        return http('/auth/v1/user', { method: 'GET' }, true).then(function (r) { if (r.status === 200) setSession({ access_token: S.access_token, refresh_token: S.refresh_token, expires_in: 3600, user: r.body }); return S.user; });
      },
      signOut: function () { var t = S; S = null; ls.del(LSK); return t && !mock ? fetch(base + '/auth/v1/logout', { method: 'POST', headers: { apikey: anon, Authorization: 'Bearer ' + t.access_token } }).catch(function () {}) : Promise.resolve(); },

      // Synchronisation d'une sauvegarde de jeu. adapter = { game, slot?, read():string|null, write(string) }.
      // ask(info) doit répondre 'local' | 'cloud' | 'both' | 'cancel' : appelé dès qu'une perte de données est possible.
      sync: function (a, ask) {
        var local = a.read(), L = { exists: local != null && local !== '', raw: local || '' };
        return sel('saves', 'select=version,data,updated_at,device_id&game=eq.' + a.game + '&slot=eq.' + (a.slot || 'main')).then(function (rows) {
          var c = rows[0], C = c ? { exists: true, version: c.version, raw: typeof c.data === 'string' ? c.data : JSON.stringify(c.data), at: c.updated_at, device: c.device_id } : { exists: false, version: 0, raw: '' };
          var plan = planSync(L, C, getBase(a));
          var up = function (baseV) { var data; try { data = JSON.parse(L.raw); } catch (e) { data = { raw: L.raw }; } return rpc('put_save', { p_game: a.game, p_slot: a.slot || 'main', p_base_version: baseV, p_data: data, p_device: deviceId() }).then(function (r) { if (r.status === 'ok') { setBase(a, r.version, L.raw); return { action: 'uploaded', version: r.version }; } if (r.status === 'too_large') return { action: 'too_large' }; return { action: 'conflict', cloud: r }; }); };
          var down = function () { backup(a, L.raw, 'avant-cloud'); a.write(C.raw); setBase(a, C.version, C.raw); return { action: 'downloaded', version: C.version }; };
          if (plan === 'noop') return { action: 'noop' };
          if (plan === 'adopt') { setBase(a, C.version, C.raw); return { action: 'adopted' }; }
          if (plan === 'upload') return up(C.version);
          if (plan === 'download') return down();
          return Promise.resolve(ask({ game: a.game, local: L, cloud: C })).then(function (choice) {     // plan === 'ask'
            if (choice === 'local') return up(C.version);                       // l'utilisateur a choisi : le cloud est archivé par put_save (historique)
            if (choice === 'cloud') return down();
            if (choice === 'both') { backup(a, L.raw, 'copie-locale'); return down(); }
            return { action: 'cancelled' };
          });
        });
      },
      // Migration d'une ancienne sauvegarde localStorage vers le cloud (opt-in explicite).
      migrate: function (a, ask) { return A.sync(a, ask); },
      history: function (a) { return sel('save_history', 'select=id,version,replaced_at,device_id&game=eq.' + a.game + '&slot=eq.' + (a.slot || 'main') + '&order=replaced_at.desc'); },
      restoreVersion: function (a, id) { return rpc('restore_save', { p_game: a.game, p_slot: a.slot || 'main', p_history_id: id }); },
      library: function () { return pay('/api/account/library'); },
      linkLicense: function (key) { return ensure().then(function () { return fetch((cfg.payApi || '') + '/api/account/link', { method: 'POST', headers: { 'Content-Type': 'application/json', Authorization: 'Bearer ' + S.access_token }, body: JSON.stringify({ licenseKey: key }) }).then(function (r) { return r.json().then(function (j) { return { status: r.status, body: j }; }); }); }); },
      exportData: function () { return rpc('export_my_data'); },
      deleteGameData: function () { return rpc('delete_my_game_data').then(function () { return pay('/api/account/unlink-all'); }); },
      // Suppression complète du compte : données de jeu + détachement des achats + compte d'authentification (via le serveur, clé admin jamais côté client).
      deleteAccount: function () { return rpc('delete_my_game_data').then(function () { return pay('/api/account/delete'); }).then(function (r) { if (r.status === 200) { S = null; ls.del(LSK); } return r; }); },
      planSync: planSync
    };
    return A;
  }
  root.MaxlolAccount = { create: create, planSync: planSync, hash: hash };
})(typeof window !== 'undefined' ? window : globalThis);
