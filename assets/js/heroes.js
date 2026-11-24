/* Fiche héros de La Dernière Torche : tenues (costumes), animation de repos et planche de poses. Chargée sur les accueils. */
(function () {
  var HERO = ['aldric', 'selena', 'orin', 'lyra', 'nyx', 'brann', 'ysmere', 'necro'];
  var SK = {aldric: ['', 'noel', 'obs', 'or'], selena: ['', 'etoile', 'noel', 'or'], orin: ['', 'flame', 'noel', 'or'], lyra: ['', 'autumn', 'hood', 'noel', 'or'],
    nyx: ['', 'glace', 'or', 'rouge', 'violet'], brann: ['', 'forge', 'noel', 'or', 'royal'], ysmere: ['', 'glace', 'or', 'storm'], necro: ['', 'bone', 'glace', 'or', 'rouge']};
  var UI = {
    en: ['Outfits', 'Pose sheet', 'Idle', 'Attack', 'Skill', 'Hit', 'Down', 'Ultimate', 'Close', 'Default outfit'],
    fr: ['Tenues', 'Planche de poses', 'Repos', 'Attaque', 'Compétence', 'Touché', 'K.O.', 'Ultime', 'Fermer', 'Tenue de base'],
    es: ['Trajes', 'Hoja de poses', 'Reposo', 'Ataque', 'Habilidad', 'Golpeado', 'K.O.', 'Definitiva', 'Cerrar', 'Traje base'],
    pt: ['Trajes', 'Folha de poses', 'Parado', 'Ataque', 'Habilidade', 'Atingido', 'K.O.', 'Suprema', 'Fechar', 'Traje padrão'],
    th: ['ชุด', 'แผ่นท่าทาง', 'ยืนนิ่ง', 'โจมตี', 'สกิล', 'ถูกโจมตี', 'แพ้', 'อัลติเมต', 'ปิด', 'ชุดพื้นฐาน'],
    zh: ['服装', '姿势表', '待机', '攻击', '技能', '受击', '倒下', '必杀技', '关闭', '默认服装'],
    ja: ['コスチューム', 'ポーズ集', '待機', '攻撃', 'スキル', '被弾', '戦闘不能', '必殺技', '閉じる', '基本の衣装'],
    ko: ['의상', '포즈 시트', '대기', '공격', '스킬', '피격', '쓰러짐', '궁극기', '닫기', '기본 의상'],
    ru: ['Наряды', 'Лист поз', 'Покой', 'Атака', 'Умение', 'Удар', 'Поражение', 'Ультимейт', 'Закрыть', 'Базовый наряд'],
    id: ['Kostum', 'Lembar pose', 'Siaga', 'Serang', 'Skill', 'Terkena', 'Kalah', 'Ultimate', 'Tutup', 'Kostum dasar']};
  var NAMES = {
    fr: {aldric_noel: 'Aldric de Noël', aldric_or: 'Aldric Doré', aldric_obs: 'Aldric d’obsidienne', selena_etoile: 'Séléna étoilée', selena_noel: 'Séléna de Noël', selena_or: 'Séléna Dorée',
      orin_flame: 'Orin, mage des flammes', orin_noel: 'Orin de Noël', orin_or: 'Orin Doré', lyra_autumn: 'Lyra d’automne', lyra_hood: 'Lyra, capuche d’automne', lyra_noel: 'Lyra de Noël', lyra_or: 'Lyra Dorée',
      nyx_glace: 'Nyx Givre', nyx_or: 'Nyx Dorée', nyx_rouge: 'Nyx, capuche écarlate', nyx_violet: 'Nyx Violette', brann_forge: 'Brann, forge glacée', brann_noel: 'Brann de Noël', brann_or: 'Brann Doré',
      brann_royal: 'Brann, couronne royale', ysmere_glace: 'Ysmère Léopard des neiges', ysmere_or: 'Ysmère Dorée', ysmere_storm: 'Ysmère tempête', necro_bone: 'Malric, couronne d’os',
      necro_glace: 'Malric Glace', necro_or: 'Malric Doré', necro_rouge: 'Malric, nécromant écarlate'},
    en: {aldric_noel: 'Christmas Aldric', aldric_or: 'Golden Aldric', aldric_obs: 'Obsidian Aldric', selena_etoile: 'Starry Selena', selena_noel: 'Christmas Selena', selena_or: 'Golden Selena',
      orin_flame: 'Orin, Flame Mage', orin_noel: 'Christmas Orin', orin_or: 'Golden Orin', lyra_autumn: 'Autumn Lyra', lyra_hood: 'Lyra, Autumn Hood', lyra_noel: 'Christmas Lyra', lyra_or: 'Golden Lyra',
      nyx_glace: 'Frost Nyx', nyx_or: 'Golden Nyx', nyx_rouge: 'Nyx, Scarlet Hood', nyx_violet: 'Violet Nyx', brann_forge: 'Brann, Frozen Forge', brann_noel: 'Christmas Brann', brann_or: 'Golden Brann',
      brann_royal: 'Brann, Royal Crown', ysmere_glace: 'Ysmère, Snow Leopard', ysmere_or: 'Golden Ysmère', ysmere_storm: 'Storm Ysmère', necro_bone: 'Malric, Bone Crown',
      necro_glace: 'Frost Malric', necro_or: 'Golden Malric', necro_rouge: 'Malric, Scarlet Necromancer'}};
  var lang = (document.documentElement.lang || 'en').slice(0, 2), ui = UI[lang] || UI.en, nm = lang === 'fr' ? NAMES.fr : NAMES.en;
  var RM = window.matchMedia && matchMedia('(prefers-reduced-motion: reduce)').matches;
  var P = '/assets/heroes/', box, img, tm, cur = {h: '', s: ''}, opener = null;
  function el(t, c, h) { var e = document.createElement(t); if (c) e.className = c; if (h != null) e.textContent = h; return e; }
  function src(h, s, k) { return P + (s ? h + '_' + s : h) + '_' + k + '.webp'; }
  function build() {
    box = el('div', 'hm'); box.setAttribute('role', 'dialog'); box.setAttribute('aria-modal', 'true'); box.hidden = true;
    var card = el('div', 'hm-box');
    var x = el('button', 'hm-x', '×'); x.type = 'button'; x.setAttribute('aria-label', ui[8]); x.onclick = close;
    var role = el('p', 'hm-role'), name = el('h3', 'hm-name'); name.id = 'hmName'; box.setAttribute('aria-labelledby', 'hmName');
    var stage = el('div', 'hm-stage'); img = el('img'); img.alt = ''; img.width = 440; img.height = 275; stage.appendChild(img);
    var sk = el('p', 'hm-skin');
    var h1 = el('p', 'hm-h', ui[0]), chips = el('div', 'hm-chips');
    var h2 = el('p', 'hm-h', ui[1]), sheet = el('div', 'hm-sheet');
    card.append(x, role, name, stage, sk, h1, chips, h2, sheet); box.appendChild(card); document.body.appendChild(box);
    box._r = {role: role, name: name, sk: sk, chips: chips, sheet: sheet, x: x};
    box.addEventListener('click', function (e) { if (e.target === box) close(); });
    document.addEventListener('keydown', function (e) {
      if (box.hidden) return;
      if (e.key === 'Escape') { close(); return; }
      if (e.key === 'Tab') { var f = box.querySelectorAll('button'); if (!f.length) return; var a = f[0], z = f[f.length - 1];
        if (e.shiftKey && document.activeElement === a) { e.preventDefault(); z.focus(); } else if (!e.shiftKey && document.activeElement === z) { e.preventDefault(); a.focus(); } }
    });
  }
  function anim(h, s) {
    clearInterval(tm); var fr = [0, 1, 2, 3].map(function (i) { return src(h, s, 'i' + i); });
    fr.forEach(function (u) { var im = new Image(); im.src = u; });
    img.src = fr[0]; if (RM) return; var n = 0; tm = setInterval(function () { n = (n + 1) % 4; img.src = fr[n]; }, 260);
  }
  function pick(h, s) {
    cur = {h: h, s: s}; var r = box._r, key = h + (s ? '_' + s : '');
    r.sk.textContent = s ? nm[key] : ui[9]; anim(h, s);
    Array.prototype.forEach.call(r.chips.children, function (b) { var on = b.getAttribute('data-s') === s; b.setAttribute('aria-pressed', on ? 'true' : 'false'); b.className = 'hm-chip' + (on ? ' on' : ''); });
    r.sheet.textContent = '';
    [['atk', ui[3]], ['skill', ui[4]], ['hit', ui[5]], ['ko', ui[6]]].forEach(function (p) {
      var f = el('figure', 'hm-pose'), i = el('img'); i.src = src(h, s, p[0]); i.alt = ''; i.loading = 'lazy'; i.width = 440; i.height = 275;
      f.append(i, el('figcaption', '', p[1])); r.sheet.appendChild(f); });
    if (s) return;
    var f = el('figure', 'hm-pose hm-ult'), i = el('img'); i.src = '/assets/t-ult-' + h + '.webp'; i.alt = ''; i.loading = 'lazy'; f.append(i, el('figcaption', '', ui[7])); r.sheet.appendChild(f);
  }
  function open(idx, label, role, btn) {
    if (!box) build(); var h = HERO[idx], r = box._r; opener = btn;
    r.role.textContent = role; r.name.textContent = label; r.chips.textContent = '';
    SK[h].forEach(function (s) { var b = el('button', 'hm-chip'); b.type = 'button'; b.setAttribute('data-s', s);
      var i = el('img'); i.src = P + 'face_' + (s ? h + '_' + s : h) + '.webp'; i.alt = ''; i.width = 56; i.height = 56; b.appendChild(i);
      b.setAttribute('aria-label', s ? nm[h + '_' + s] : ui[9]); b.onclick = function () { pick(h, s); }; r.chips.appendChild(b); });
    pick(h, ''); box.hidden = false; document.documentElement.classList.add('hm-open'); r.x.focus();
  }
  function close() { if (!box || box.hidden) return; box.hidden = true; clearInterval(tm); document.documentElement.classList.remove('hm-open'); if (opener) opener.focus(); }
  document.addEventListener('click', function (e) {
    var b = e.target.closest && e.target.closest('.t-heroes .hc'); if (!b) return;
    var idx = +b.getAttribute('data-i'); open(idx, b.querySelector('b').textContent, b.querySelector('.hc-t span').textContent, b);
  });
})();
