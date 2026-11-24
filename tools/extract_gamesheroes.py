"""Extrait les images des héros d'Infinite Dungeon et des pilotes/dragons de WYRMSTORM pour les fiches des pages jeu.
Usage : python3 -I tools/extract_gamesheroes.py /chemin/Stepquest/prototype/infinite-dungeon-v08 /chemin/Wyrmstrom
Sorties : assets/hid/<hero>_<pose>.webp, assets/hws/<element>_<forme>.webp (alpha conservé, WEBP q72)."""
import os, sys
from PIL import Image
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + '/'
ID, WS = sys.argv[1] + '/img/', sys.argv[2] + '/assets/'
def save(src, dst, w):
    im = Image.open(src).convert('RGBA'); h = round(im.height * w / im.width)
    im.resize((w, h), Image.LANCZOS).save(dst, 'WEBP', quality=72, alpha_quality=75, method=6)
os.makedirs(R + 'assets/hid', exist_ok=True); os.makedirs(R + 'assets/hws', exist_ok=True)
n = 0
for h in ['aldric', 'selena', 'orin', 'lyra', 'nyx']:
    b = ID + 'heroes/%s/%s_' % (h, h); o = R + 'assets/hid/%s_' % h
    for k, f in [('i0', 'idle_0'), ('i1', 'idle_1'), ('i2', 'idle_2'), ('i3', 'idle_3'), ('atk', 'attack_1'), ('skill', 'skill_1'), ('hit', 'hit_0'), ('ko', 'ko_1'), ('win', 'victory_0')]:
        save(b + f + '.webp', o + k + '.webp', 440); n += 1
    c = ID + 'heroes/%s/costumes/' % h; ck = os.listdir(c)[0]; cb = c + ck + '/%s_' % h
    for k, f in [('ci0', 'idle_0'), ('catk', 'attack_0'), ('cskill', 'skill_0'), ('chit', 'hit_0')]:
        save(cb + f + '.webp', o + k + '.webp', 440); n += 1
    save(ID + 'ult_%s.webp' % h, o + 'ult.webp', 400); n += 1
for e in ['water', 'fire', 'ice', 'nature', 'storm', 'shadow', 'light']:
    o = R + 'assets/hws/%s_' % e
    for k, f in [('p1', 'pilots/%s.webp' % e), ('p2', 'pilots/%s_2.webp' % e), ('p3', 'pilots/%s_3.webp' % e), ('pb', 'pilots/%s_back.webp' % e),
                 ('d0', 'dragons/%s.webp' % e if e != 'water' else 'monsters/aurelion.webp'), ('d1', 'dragons/%s_evo1.webp' % e), ('d2', 'dragons/%s_evo2.webp' % e), ('sk', 'skins/%s.webp' % e)]:
        save(WS + f, o + k + '.webp', 400); n += 1
print(n, 'images')
