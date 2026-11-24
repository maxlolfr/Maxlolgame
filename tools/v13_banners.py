"""Étape 13 : bannières 16:9 (assets/b/<slug>.webp, voir art/<jeu>/banniere-16x9.png) dans le carrousel de l'accueil. Idempotent.
Le hero et les fonds des pages jeu sont réglés dans assets/css/home2.css / gp2.css. Usage : python3 tools/v13_banners.py"""
import os, re
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + '/'
PAGES = ['index.html'] + [l + '/index.html' for l in ('fr', 'es', 'pt', 'th', 'zh', 'ja', 'ko', 'ru', 'id')]
n = 0
for path in PAGES:
    p = R + path; s = open(p, encoding='utf8').read(); o = s
    m = re.search(r'<div class="fc-track".*?</div>\s*<button class="fc-nav fc-next"', s, re.S)
    if not m: print('carrousel introuvable', path); continue
    blk = m.group(0)
    def fix(a):
        a = a.group(0); h = re.search(r'class="simg" href="[^"]*?/([a-z-]+)/"', a)
        if not h: return a
        return re.sub(r'<img src="[^"]*" ([^>]*?)width="\d+" height="\d+"', lambda _m: '<img src="/assets/b/%s.webp" %swidth="1600" height="900"' % (h.group(1), _m.group(1)), a, count=1)
    nb = re.sub(r'<article class="fslide".*?</article>', fix, blk, flags=re.S)
    s = s.replace(blk, nb, 1)
    if s != o: open(p, 'w', encoding='utf8').write(s); n += 1
print('accueils traités :', n)
