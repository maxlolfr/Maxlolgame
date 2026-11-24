"""Étape 11 : pages jeu avec image d'ambiance floutée derrière l'en-tête + galerie plus grande (assets/css/gp2.css). Idempotent.
Usage : python3 tools/v11_gamepages.py (après v7_css, v8_legal, v9_gallery)."""
import os, re
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + '/'
SLUGS = ['la-derniere-torche', 'wyrmstorm', 'gravity-turn', 'infinite-dungeon']
n = 0
for slug in SLUGS:
    for rel in ('%s/index.html' % slug, 'fr/%s/index.html' % slug):
        p = R + rel
        if not os.path.exists(p):
            continue
        s = open(p, encoding='utf8').read()
        o = s
        s = re.sub(r'<section class="gp-hero[^"]*"', '<section class="gp-hero gp2 gp-%s"' % slug, s, count=1)
        if 'gp2.css' not in s:
            s = re.sub(r'(<link rel="stylesheet" href="/assets/css/game\.[a-f0-9]+\.css">)', r'\1\n<link rel="stylesheet" href="/assets/css/gp2.css">', s, count=1)
        if s != o:
            open(p, 'w', encoding='utf8').write(s); n += 1
print('pages jeu traitées :', n)
