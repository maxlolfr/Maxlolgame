#!/usr/bin/env python3
"""v22 – À lancer EN DERNIER (après v21) : retire les mentions de taxes / TVA et remplit la livraison
(code de déblocage envoyé par e-mail à l'adresse PayPal, sous 48 h). Idempotent. `--check` n'écrit rien."""
import re, sys, glob
M = r'<mark class="todo">(?:À compléter|To complete) : ?%s</mark>'
M2 = r'<mark class="todo">(?:À compléter : |To complete: )%s</mark>'
DELIV = {"fr": "un code de déblocage est envoyé par e-mail à l’adresse de ton compte PayPal, au plus tard sous 48 h après le paiement",
         "en": "an unlock code is sent by e-mail to your PayPal account address, within 48 hours of payment at the latest"}
def patch(s):
    # taxes dans l'encart « Avant de payer »
    s = re.sub(r' Taxes ?: ' + M2 % 'TAXES_PRIX', '', s)
    # TVA dans les mentions légales
    s = re.sub(r' — ' + M2 % 'TVA_SI_APPLICABLE', '', s)
    # livraison
    m = re.search(r'<html[^>]*\blang="([a-z]{2})', s); en = bool(m) and m.group(1) != 'fr'
    s = re.sub(M2 % 'MODE_ET_DELAI_LIVRAISON', DELIV['en' if en else 'fr'], s)
    return s
if __name__ == "__main__":
    n = 0
    for f in glob.glob('**/*.html', recursive=True):
        if f.startswith(('art/', 'node_modules/')): continue
        s = open(f, encoding='utf-8').read(); t = patch(s)
        if t != s:
            n += 1
            if '--check' not in sys.argv: open(f, 'w', encoding='utf-8').write(t)
    print(("à modifier : %d fichiers" if '--check' in sys.argv else "modifié : %d fichiers") % n)
