"""Étape 7 (après build_i18n.py) : CSS partagé + cibles tactiles >= 44 px. Idempotent.
- Sort le gros <style> dupliqué dans chaque page vers /assets/css/<type>.<empreinte>.css (cache long, un seul fichier par type).
- Ajoute les correctifs tactiles (marqueur /*touch*/) pour téléphones.
Usage : python3 tools/v7_css.py"""
import re, glob, os, hashlib

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + '/'
SKIP = ('tools/', 'chibi', 'backend', 'account', 'pay/', 'node_modules', 'legal/')
MIN_INLINE = 20000          # seuls les gros blocs sont extraits

TOUCH = """
/*touch*/
@media (max-width:900px),(pointer:coarse){
.brand{display:inline-flex;align-items:center;min-height:44px}
.langmenu summary{display:inline-flex;align-items:center;justify-content:center;box-sizing:border-box;min-height:44px;min-width:44px}
.mmenu summary{width:44px;height:44px}
.nav .snd,.snd{width:44px;height:44px}
.crumb a,.presslink,.sname a,.tag,.nmore a{display:inline-flex;align-items:center;min-height:44px}
.nl a{display:block;padding-block:10px}
}
"""
TOUCH_PRESS = """/*touch*/@media (max-width:900px),(pointer:coarse){main a{display:inline-block;padding-block:10px}.back{padding-block:12px}}"""

os.makedirs(ROOT + 'assets/css', exist_ok=True)
done = {}
pages = glob.glob(ROOT + '**/index.html', recursive=True) + [ROOT + '404.html']
for p in sorted(pages):
    rel = os.path.relpath(p, ROOT)
    if any(x in rel for x in SKIP):
        continue
    s = open(p, encoding='utf8').read()
    m = re.search(r'<style[^>]*>(.*?)</style>', s, re.S)
    if not m:
        continue
    css = m.group(1)
    if rel.startswith('press/'):
        if '/*touch*/' not in css:
            s = s.replace(css, css + TOUCH_PRESS, 1)
            open(p, 'w', encoding='utf8').write(s)
            print('press: correctif tactile')
        continue
    if len(css) < MIN_INLINE:
        continue
    # chemins relatifs -> absolus pour que le fichier partagé marche depuis toutes les pages
    norm = re.sub(r'url\((["\']?)(?:\.\./)?assets/', r'url(\1/assets/', css)
    if '/*touch*/' not in norm:
        norm += TOUCH
    parts = rel.split('/')
    kind = 'home' if (rel == 'index.html' or (len(parts) == 2 and len(parts[0]) == 2)) else ('news' if 'news' in rel or 'actualites' in rel else 'game')
    h = hashlib.md5(norm.encode('utf8')).hexdigest()[:8]
    name = f'{kind}.{h}.css'
    open(ROOT + 'assets/css/' + name, 'w', encoding='utf8').write(norm)
    done[name] = done.get(name, 0) + 1
    link = f'<link rel="stylesheet" href="/assets/css/{name}">'
    s = s[:m.start()] + link + s[m.end():]
    open(p, 'w', encoding='utf8').write(s)

# supprimer les anciennes versions non utilisées
used = set(done)
for f in glob.glob(ROOT + 'assets/css/*.css'):
    n = os.path.basename(f)
    if n not in used and done:
        # ne supprime que si plus aucune page ne le référence
        if not any(n in open(q, encoding='utf8', errors='ignore').read() for q in pages if os.path.exists(q)):
            os.remove(f)
print('CSS partagés :', done)
