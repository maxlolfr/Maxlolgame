#!/usr/bin/env python3
"""v23 : met les vraies URL dans le HTML pour les boutons « Jouer » (liens statiques, utiles aux moteurs
de recherche qui n'exécutent pas toujours le script). Idempotent. À lancer en dernier."""
import re, glob
URLS = {
 "torch-play": "https://la-derniere-torche.netlify.app",
 "gt-play": "https://gravity-turn.netlify.app",
 "wyrmstorm-play": "https://wyrmstorm.netlify.app",
 "chibi-legends-rpg-play": "https://maxlolgames.com/chibi-legends/",
 "github": "https://github.com/maxlolfr",
 "mail": "mailto:Maxlolgames@proton.me",
}
pat = re.compile(r'(<a\b[^>]*?\bdata-link="(%s)"[^>]*?\bhref=")(#[^"]*|)(")' % "|".join(URLS))
n = 0
for f in glob.glob("**/index.html", recursive=True):
    s = open(f, encoding="utf-8").read()
    t = pat.sub(lambda m: m.group(1) + URLS[m.group(2)] + m.group(4), s)
    if t != s:
        open(f, "w", encoding="utf-8").write(t); n += 1
print("pages modifiées :", n)
