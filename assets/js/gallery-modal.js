/* Fiche cliquable des pages jeu (héros d'Infinite Dungeon, dragons et pilotes de WYRMSTORM).
   Données : <script type="application/json" id="hm-data"> dans la page (ajouté par tools/v15_gameheroes.py). */
(function () {
  var node = document.getElementById('hm-data'); if (!node) return;
  var D; try { D = JSON.parse(node.textContent); } catch (e) { return; }
  var RM = window.matchMedia && matchMedia('(prefers-reduced-motion: reduce)').matches;
  var box, img, tm, opener = null, cur = null;
  function el(t, c, h) { var e = document.createElement(t); if (c) e.className = c; if (h != null) e.textContent = h; return e; }
  function build() {
    box = el('div', 'hm' + (D.sq ? ' sq' : '')); box.setAttribute('role', 'dialog'); box.setAttribute('aria-modal', 'true'); box.setAttribute('aria-labelledby', 'hmName'); box.hidden = true;
    var card = el('div', 'hm-box'), x = el('button', 'hm-x', '×'); x.type = 'button'; x.setAttribute('aria-label', D.ui.close); x.onclick = close;
    var role = el('p', 'hm-role'), name = el('h3', 'hm-name'); name.id = 'hmName';
    var stage = el('div', 'hm-stage'); img = el('img'); img.alt = ''; stage.appendChild(img);
    var sk = el('p', 'hm-skin'), h1 = el('p', 'hm-h', D.ui.outfits), chips = el('div', 'hm-chips'), h2 = el('p', 'hm-h', D.ui.sheet), sheet = el('div', 'hm-sheet');
    card.append(x, role, name, stage, sk, h1, chips, h2, sheet); box.appendChild(card); document.body.appendChild(box);
    box._r = {role: role, name: name, sk: sk, chips: chips, sheet: sheet, x: x, h1: h1};
    box.addEventListener('click', function (e) { if (e.target === box) close(); });
    document.addEventListener('keydown', function (e) {
      if (box.hidden) return; if (e.key === 'Escape') { close(); return; }
      if (e.key === 'Tab') { var f = box.querySelectorAll('button'), a = f[0], z = f[f.length - 1];
        if (e.shiftKey && document.activeElement === a) { e.preventDefault(); z.focus(); } else if (!e.shiftKey && document.activeElement === z) { e.preventDefault(); a.focus(); } }
    });
  }
  function anim(fr) {
    clearInterval(tm); fr.forEach(function (u) { var i = new Image(); i.src = u; }); img.src = fr[0];
    if (RM || fr.length < 2) return; var n = 0; tm = setInterval(function () { n = (n + 1) % fr.length; img.src = fr[n]; }, 260);
  }
  function pick(h, vi) {
    var v = h.variants[vi], r = box._r; r.sk.textContent = v.label; anim(v.frames);
    Array.prototype.forEach.call(r.chips.children, function (b, i) { b.className = 'hm-chip' + (i === vi ? ' on' : ''); b.setAttribute('aria-pressed', i === vi ? 'true' : 'false'); });
    r.sheet.textContent = '';
    (v.poses || []).concat(v.extra || []).forEach(function (p, i) {
      var f = el('figure', 'hm-pose' + (i >= (v.poses || []).length ? ' hm-ult' : '')), im = el('img'); im.src = p[1]; im.alt = ''; im.loading = 'lazy'; f.append(im, el('figcaption', '', p[0])); r.sheet.appendChild(f);
    });
  }
  function open(i, btn) {
    if (!box) build(); var h = D.heroes[i], r = box._r; opener = btn; r.role.textContent = h.role; r.name.textContent = h.name; r.chips.textContent = '';
    r.h1.hidden = h.variants.length < 2; r.chips.hidden = h.variants.length < 2;
    h.variants.forEach(function (v, k) { var b = el('button', 'hm-chip'); b.type = 'button'; b.setAttribute('aria-label', v.label);
      var im = el('img'); im.src = v.thumb; im.alt = ''; im.width = 56; im.height = 56; if (D.sq) im.style.objectFit = 'contain'; else im.style.objectPosition = '50% 18%'; b.appendChild(im); b.onclick = function () { pick(h, k); }; r.chips.appendChild(b); });
    pick(h, 0); box.hidden = false; document.documentElement.classList.add('hm-open'); r.x.focus();
  }
  function close() { if (!box || box.hidden) return; box.hidden = true; clearInterval(tm); document.documentElement.classList.remove('hm-open'); if (opener) opener.focus(); }
  document.addEventListener('click', function (e) { var b = e.target.closest && e.target.closest('.gh .hc'); if (b) open(+b.getAttribute('data-i'), b); });
})();
