"""Étape 17 : intro studio v2 (10 accueils). Écran « touche pour entrer » (les navigateurs bloquent le son avant un toucher), puis ~7 s :
montée sonore + mosaïque qui accélère, impact + titre lettre par lettre, onde de choc, secousse, confettis, braises.
Sons : assets/audio/intro-riser|boom|sparkle.mp3 (ElevenLabs, eleven_text_to_sound_v3). Style : assets/css/intro2.css. Idempotent."""
import os, re
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + '/'
LAB = {'en': 'Tap to enter', 'fr': 'Touche pour entrer', 'es': 'Toca para entrar', 'pt': 'Toque para entrar', 'th': 'แตะเพื่อเข้าสู่เว็บไซต์', 'zh': '点击进入', 'ja': 'タップして入る', 'ko': '탭하여 입장', 'ru': 'Нажми, чтобы войти', 'id': 'Ketuk untuk masuk'}
ICON = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M11 5 6 9H3v6h3l5 4V5z"/><path d="M15.5 8.5a5 5 0 0 1 0 7M18.5 5.5a9 9 0 0 1 0 13"/></svg>'
JS = r'''/* --- Intro studio v2 : « touche pour entrer » (débloque le son), montée, impact, titre, confettis (tools/v17_intro.py) --- */
(() => {
  const el = document.getElementById("intro");
  el.querySelectorAll(".in-col").forEach(c => { c.innerHTML += c.innerHTML; });   // boucle sans fin : on double les 4 images ici plutôt que dans le HTML
  let seen = false, muted = false; try { seen = sessionStorage.getItem("mg.intro") === "1"; muted = localStorage.getItem("mg.music") === "0"; } catch(e){}
  const timers = [], at = (ms, fn) => timers.push(setTimeout(fn, ms));
  function finish(){
    if (el.classList.contains("gone")) return;
    timers.forEach(clearTimeout);
    el.classList.add("open"); document.body.classList.remove("intro");
    try { sessionStorage.setItem("mg.intro","1"); } catch(e){}
    heroImpacts();
    setTimeout(() => el.classList.add("gone"), 1050);
  }
  if (seen || RM){ el.classList.add("gone"); document.body.classList.remove("intro"); heroImpacts(); return; }
  /* sons : Web Audio (calé sur l'horloge audio, fonctionne sur iPhone après le toucher) */
  const SRC = { riser: "/assets/audio/intro-riser.mp3", boom: "/assets/audio/intro-boom.mp3", sparkle: "/assets/audio/intro-sparkle.mp3" }, buf = {};
  let ac = null;
  if (!muted) try {
    ac = new (window.AudioContext || window.webkitAudioContext)();
    for (const k in SRC) fetch(SRC[k]).then(r => r.arrayBuffer()).then(b => ac.decodeAudioData(b, d => { buf[k] = d; }, () => {})).catch(() => {});
  } catch(e){ ac = null; }
  function snd(k, when, vol){
    if (!ac || !buf[k]) return;
    try { const s = ac.createBufferSource(), g = ac.createGain(); s.buffer = buf[k]; g.gain.value = vol; s.connect(g); g.connect(ac.destination); s.start(ac.currentTime + when); } catch(e){}
  }
  /* particules : confettis à l'impact + braises qui montent */
  const cv = document.getElementById("introFx"), ctx = cv.getContext("2d");
  const COL = ["#FFB547","#FF5E9C","#3DD6C6","#EEE8FF","#FFE08A"];
  let W, H, ps = [], embers = false;
  const r0 = fitCanvas(cv); W = r0.width; H = r0.height;
  function pop(n){
    for (let i = 0; i < n; i++){ const a = Math.random()*Math.PI*2, sp = Math.random()*11+2;
      ps.push({x:W/2, y:H/2, vx:Math.cos(a)*sp*1.35, vy:Math.sin(a)*sp - 3, l:1, d:Math.random()*.011+.007, r:Math.random()*3.4+1.5, c:COL[i%5], k:i%3, a:Math.random()*6, g:.13}); }
  }
  function loop(){
    if (el.classList.contains("gone")) return;
    ctx.setTransform(DPR,0,0,DPR,0,0); ctx.clearRect(0,0,W,H);
    if (embers && Math.random() < .55) ps.push({x:Math.random()*W, y:H+8, vx:(Math.random()-.5)*.8, vy:-(Math.random()*2.2+.8), l:1, d:.006+Math.random()*.006, r:Math.random()*2.2+.8, c:"#FFB04A", k:3, a:0, g:-.002});
    ps = ps.filter(p => (p.l -= p.d) > 0);
    for (const p of ps){ p.vy += p.g; p.vx *= .985; p.x += p.vx; p.y += p.vy; p.a += .15;
      ctx.globalAlpha = Math.min(1, p.l*1.6); ctx.fillStyle = p.c;
      if (p.k === 0){ ctx.save(); ctx.translate(p.x,p.y); ctx.rotate(p.a); ctx.fillRect(-p.r,-p.r*.6,p.r*2,p.r*1.2); ctx.restore(); }
      else if (p.k === 3){ ctx.globalCompositeOperation = "lighter"; ctx.beginPath(); ctx.arc(p.x,p.y,p.r*2.2,0,7); ctx.globalAlpha *= .25; ctx.fill(); ctx.globalAlpha = Math.min(1, p.l*1.6); ctx.beginPath(); ctx.arc(p.x,p.y,p.r,0,7); ctx.fill(); ctx.globalCompositeOperation = "source-over"; }
      else { ctx.beginPath(); ctx.arc(p.x,p.y,p.r,0,7); ctx.fill(); } }
    ctx.globalAlpha = 1;
    requestAnimationFrame(loop);
  }
  requestAnimationFrame(loop);
  let started = false;
  function start(){
    if (started) return; started = true; el.classList.add("started");
    if (ac){ try { ac.resume(); } catch(e){} snd("riser", 0, .85); snd("boom", 3.0, 1); snd("sparkle", 3.25, .75); }
    at(250, () => el.classList.add("lit", "warp"));
    at(3000, () => { el.classList.add("title", "shake"); pop(190); embers = true; });
    at(3600, () => el.classList.remove("shake"));
    at(3750, () => pop(70));
    at(7000, finish);
  }
  el.querySelector(".in-gate").addEventListener("click", e => { e.stopPropagation(); start(); });
  el.addEventListener("click", () => { if (started) finish(); else start(); });
  if (muted) at(300, start);      // visiteur qui a coupé le son : pas d'écran d'attente, intro silencieuse
})();

'''
PAGES = ['index.html'] + [l + '/index.html' for l in ('fr', 'es', 'pt', 'th', 'zh', 'ja', 'ko', 'ru', 'id')]
n = 0
for path in PAGES:
    p = R + path; s = open(p, encoding='utf8').read(); o = s
    lang = path.split('/')[0] if '/' in path else 'en'
    # HTML : bouton, rayons, anneaux, flash, titre lettre par lettre
    s = re.sub(r'\s*<button class="in-gate".*?</button>|\s*<div class="in-rays"></div>|\s*<div class="in-ring"></div>|\s*<div class="in-ring2"></div>|\s*<div class="in-flash"></div>', '', s, flags=re.S)
    s = s.replace('<canvas id="introFx"></canvas>', '<div class="in-rays"></div><div class="in-ring"></div><div class="in-ring2"></div>\n  <canvas id="introFx"></canvas>\n  <div class="in-flash"></div>', 1)
    s = re.sub(r'(<p class="in-skip">)', '<button class="in-gate" type="button">%s<span>%s</span></button>\n  \\1' % (ICON, LAB[lang]), s, count=1)
    t = re.search(r'<p class="in-t2">(.*?)</p>', s, re.S).group(1)
    if '<span' not in t:
        letters = ''.join('<span style="--i:%d">%s</span>' % (i, '&nbsp;' if c == ' ' else c) for i, c in enumerate(t))
        s = s.replace('<p class="in-t2">%s</p>' % t, '<p class="in-t2">%s</p>' % letters, 1)
    # JS
    i = s.index('/* --- Intro studio'); j = s.index('/* --- Inclinaison 3D')
    s = s[:i] + JS + s[j:]
    # CSS
    if 'intro2.css' not in s:
        s = re.sub(r'(<link rel="stylesheet" href="[^"]*home2\.css">)', r'\1\n<link rel="stylesheet" href="%sassets/css/intro2.css">' % ('../' if '/' in path else '/'), s, count=1)
    if s != o: open(p, 'w', encoding='utf8').write(s); n += 1
print('accueils traités :', n)
