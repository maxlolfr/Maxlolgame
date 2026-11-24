"""Étape 9 : ajoute la bannière et le visuel plateau en tête de la galerie Gravity Turn (FR + EN). Idempotent."""
import os
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + '/'
ALT = {'fr/gravity-turn/index.html': ('Gravity Turn – logo et plateau de cubes', 'Gravity Turn – le plateau pivote'),
       'gravity-turn/index.html': ('Gravity Turn – logo and block board', 'Gravity Turn – the board turns')}
for rel, (a1, a2) in ALT.items():
    p = R + rel; s = open(p, encoding='utf8').read()
    if 'gt-banner.webp' in s: continue
    mk = lambda f, alt, w, h: '<button type="button" data-full="/assets/%s"><img src="/assets/%s" alt="%s" loading="lazy" decoding="async" width="%d" height="%d"></button>' % (f, f, alt, w, h)
    new = mk('gt-banner.webp', a1, 1200, 628) + mk('gt-key.webp', a2, 1280, 720)
    key = '<div class="gal" aria-label='
    i = s.index(key); j = s.index('>', i) + 1
    open(p, 'w', encoding='utf8').write(s[:j] + new + s[j:]); print('galerie GT :', rel)
