"""Étape 16 : Infinite Dungeon momentanément indisponible (lien de jeu hors service) : remplace les boutons « Jouer » par une mention grisée.
Pour le remettre en ligne : passer UNAVAILABLE à False, relancer la chaîne de génération, et mettre le bon lien dans LINKS « id-play ». Idempotent."""
import os, re, glob
UNAVAILABLE = True
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + '/'
LAB = {'en': 'Temporarily unavailable', 'fr': 'Momentanément indisponible', 'es': 'Temporalmente no disponible', 'pt': 'Temporariamente indisponível', 'th': 'ไม่พร้อมใช้งานชั่วคราว',
       'zh': '暂时无法游玩', 'ja': '一時的に利用できません', 'ko': '일시적으로 이용할 수 없음', 'ru': 'Временно недоступно', 'id': 'Sementara tidak tersedia'}
NOTE = {'en': 'The playable link is temporarily unavailable while the game is being reworked. The game page stays online for reference.',
        'fr': 'Le lien pour jouer est momentanément indisponible : le jeu est en cours de refonte. Cette page reste en ligne à titre d’information.'}
CSS = '\n/* Infinite Dungeon indisponible (tools/v16_id_unavailable.py) */\n.btn.unavail{opacity:.6;cursor:not-allowed;filter:grayscale(.6);box-shadow:inset 0 0 0 1.5px rgba(255,255,255,.3);background:rgba(18,12,43,.7)!important;color:#E9E3FF!important;pointer-events:none}\n.unavail-note{margin:10px 0 0;padding:10px 14px;border-radius:12px;background:rgba(255,181,71,.1);box-shadow:inset 0 0 0 1px rgba(255,181,71,.35);color:#FFE3B0;font-weight:700;font-size:.95rem}\n'
if not UNAVAILABLE: raise SystemExit('UNAVAILABLE = False : relancer la chaîne de génération pour restaurer les liens.')
for c in ['assets/css/home2.css', 'assets/css/gp2.css']:
    s = open(R + c, encoding='utf8').read()
    if 'v16_id_unavailable' not in s: open(R + c, 'w', encoding='utf8').write(s + CSS)
n = 0
for p in glob.glob(R + '**/index.html', recursive=True):
    if '/tools/' in p: continue
    s = open(p, encoding='utf8').read(); o = s
    rel = p[len(R):]; lang = rel.split('/')[0] if rel.split('/')[0] in LAB else 'en'
    if re.fullmatch(r'(?:fr/)?infinite-dungeon/index\.html', rel):
        s = re.sub(r'<meta name="robots" content="[^"]*">', '<meta name="robots" content="noindex, follow">', s, count=1)
    first = [True]
    def rep(m):
        cls = re.search(r'class="([^"]*)"', m.group(0)); cls = (cls.group(1) if cls else 'btn') + ' unavail'
        out = '<span class="%s" role="note" aria-disabled="true">%s</span>' % (cls, LAB[lang])
        if first[0] and re.match(r'(fr/)?infinite-dungeon/', rel) and lang in NOTE:
            out += '<p class="unavail-note">%s</p>' % NOTE[lang]
        first[0] = False
        return out
    s = re.sub(r'<a [^>]*data-link="id-play"[^>]*>.*?</a>', rep, s, flags=re.S)
    if s != o: open(p, 'w', encoding='utf8').write(s); n += 1
print('pages modifiées :', n)
