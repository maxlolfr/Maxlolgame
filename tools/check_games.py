"""Valide les fiches tools/games/*.json. Usage : python3 tools/check_games.py
Un jeu avec "published": false n'est jamais généré (ni catalogue, ni page, ni sitemap, ni flux)."""
import json, glob, os, re, sys
T = os.path.dirname(os.path.abspath(__file__)) + '/'
R = T[:-6]
err = 0
for f in sorted(glob.glob(T + 'games/*.json')):
    n = os.path.basename(f); g = json.load(open(f, encoding='utf8'))
    pub = g.get('published', True) is not False
    tag = 'PUBLIÉ    ' if pub and not n.startswith('_') else 'non publié'
    miss = [k for k in ('slug', 'name', 'accent', 'cover', 'images', 'genre', 'pitch', 'feats', 'platforms', 'languages') if not g.get(k)]
    notes = []
    if pub and not n.startswith('_'):
        if miss: notes.append('CHAMPS MANQUANTS: ' + ','.join(miss)); err += 1
        if not (g.get('play') or g.get('itch')): notes.append('aucun lien Jouer/itch'); err += 1
        for k in [g.get('cover')] + list(g.get('images', [])) + [g.get('banner'), g.get('logo')]:
            if k and not os.path.exists(R + k): notes.append('image absente: ' + k); err += 1
        ni = len(g.get('images', []))
        if ni < 8: notes.append(f'galerie {ni} images (cible 8-12, aucune zone vide affichée)')
        if g.get('trailer') == '': notes.append('pas de bande-annonce (bloc masqué)')
    print(f'{tag} {n:24} {" | ".join(notes) or "ok"}')
print('erreurs bloquantes :', err); sys.exit(1 if err else 0)
