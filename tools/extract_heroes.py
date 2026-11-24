"""Extrait les poses et visages des héros de La Dernière Torche depuis les archives du jeu (repo privé Latorche) vers assets/heroes/.
Usage : python3 -I tools/extract_heroes.py /chemin/vers/Latorche/www"""
import io, json, os, struct, sys
from PIL import Image
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + '/'
W = sys.argv[1].rstrip('/') + '/'
OUT = R + 'assets/heroes/'
os.makedirs(OUT, exist_ok=True)
HEROES = ['aldric', 'selena', 'orin', 'lyra', 'nyx', 'brann', 'ysmere', 'necro']
POSES = {'i0': 'idle_0', 'i1': 'idle_1', 'i2': 'idle_2', 'i3': 'idle_3', 'atk': 'attack_1', 'skill': 'skill_1', 'hit': 'hit_0', 'ko': 'ko_1'}

def unpack(name):
    b = open(W + 'packs/%s.mp3' % name, 'rb').read()
    hl = struct.unpack('<I', b[:4])[0]; hd = json.loads(b[4:4 + hl]); base = 4 + hl
    return {k: b[base + a[0]:base + a[0] + a[1]] for k, a in hd.items()}

def save(data, path, w):
    im = Image.open(io.BytesIO(data)).convert('RGBA')
    im = im.resize((w, round(im.height * w / im.width)), Image.LANCZOS)
    im.save(path, 'WEBP', quality=72, alpha_quality=75, method=6)

cface = unpack('cface'); total = 0; skins = {}
for h in HEROES:
    base = unpack('h_' + h); cos = unpack('c_' + h)
    skins[h] = ['']
    for key, nm in POSES.items():
        save(base['%s_%s' % (h, nm)], OUT + '%s_%s.webp' % (h, key), 440)
    save(open(W + 'img/face_%s.webp' % h, 'rb').read(), OUT + 'face_%s.webp' % h, 112)
    names = sorted({k.split('_idle_0')[0] for k in cos if k.endswith('_idle_0')})
    for sk in names:
        skins[h].append(sk[len(h) + 1:])
        for key, nm in POSES.items():
            save(cos['%s_%s' % (sk, nm)], OUT + '%s_%s.webp' % (sk, key), 440)
        save(cface['face_' + sk], OUT + 'face_%s.webp' % sk, 112)
json.dump(skins, open(OUT + 'skins.json', 'w'), indent=1)
total = sum(os.path.getsize(OUT + f) for f in os.listdir(OUT))
print(len(os.listdir(OUT)), 'fichiers,', total // 1024, 'Ko'); print(skins)
