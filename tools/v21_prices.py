#!/usr/bin/env python3
"""v21 – À lancer EN DERNIER (après v19 et les v20) : prix 4,99 € pour Chibi Legends et WYRMSTORM
(PayPal.me maxlolfr2) + pastille « Démo gratuite » sur les cartes payantes de l'accueil.
Idempotent. `--check` : n'écrit rien, affiche le nombre de fichiers à modifier."""
import re, sys, glob
PRICE = "4,99 €"
PP = "https://www.paypal.me/maxlolfr2/4.99EUR"
FREE = {"fr":"Démo gratuite","en":"Free demo","es":"Demo gratis","pt":"Demo grátis","th":"เดโมฟรี","zh":"免费试玩","ja":"無料デモ","ko":"무료 데모","ru":"Бесплатное демо","id":"Demo gratis"}
PAID = ("torch","gt","chibi-legends-rpg","wyrmstorm")
def patch(s):
    for key in ("chibi-legends-rpg","wyrmstorm"):
        s = re.sub(r'("%s":\s*\{ price: )"[^"]*"(, itch: "[^"]*", paypal: )"[^"]*"( \})' % key,
                   lambda m: '%s"%s"%s"%s"%s' % (m.group(1), PRICE, m.group(2), PP, m.group(3)), s)
    m = re.search(r'<html[^>]*\blang="([a-zA-Z-]+)"', s)
    lang = (m.group(1).split('-')[0] if m else 'fr')
    txt = FREE.get(lang, FREE["en"])
    s = re.sub(r'<span class="sfree">[^<]*</span>', '', s)
    s = re.sub(r'(<span class="sprice" data-price="(?:%s)"></span>)' % '|'.join(PAID),
               lambda m: m.group(1) + '<span class="sfree">%s</span>' % txt, s)
    return s
if __name__ == "__main__":
    n = 0
    for f in glob.glob('**/*.html', recursive=True):
        if f.startswith(('art/','node_modules/')): continue
        s = open(f, encoding='utf-8').read(); t = patch(s)
        if t != s:
            n += 1
            if '--check' not in sys.argv: open(f, 'w', encoding='utf-8').write(t)
    print(("à modifier : %d fichiers" if '--check' in sys.argv else "modifié : %d fichiers") % n)
