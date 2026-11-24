#!/usr/bin/env python3 -I
"""v20 — Gravity Turn : démo gratuite (24 niveaux) + jeu complet en achat unique (PayPal), prix : voir GT_PRICE.
À lancer APRÈS v19. Idempotent. Ne modifie que : les accueils (10 langues, boutique JS) et les fiches FR/EN de Gravity Turn.
Le jeu lui-même (dépôt maxlolfr/Gravityturn) gère la démo et le déblocage par code.
Usage : python3 -I tools/v20_gt_paid.py [--check]
"""
import re, sys, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
GT_AMOUNT = "2.99"                     # montant PayPal.me
PAYPAL = "https://www.paypal.me/maxlolfr2/%sEUR" % GT_AMOUNT
FREE_LEVELS, ALL_LEVELS = 24, 84
SKIP = ("chibi-legends/", "chibi-test/", "backend/", "art/", "tools/", ".git/")

HOMES = [p for p in ["index.html"] + ["%s/index.html" % l for l in "fr es pt th zh ja ko ru id".split()]]

# ---------- accueils : prix + PayPal dans la boutique JS ----------
def gt_price_from_torch(s):
    m = re.search(r'"torch": \{ price: "([^"]*)"', s)
    if not m: return None
    p = m.group(1)
    return p.replace("7,99", "2,99").replace("7.99", "2.99")

def patch_home(s):
    price = gt_price_from_torch(s)
    if not price: return s
    new = '"gt":    { price: "%s", itch: "", paypal: "%s" },' % (price, PAYPAL)
    return re.sub(r'"gt":\s*\{ price: "[^"]*",\s*itch: ""(?:, paypal: "[^"]*")? \},', new, s, count=1)

# ---------- fiches FR / EN ----------
T = {
 "fr": dict(
  page="fr/gravity-turn/index.html",
  old_title="Gravity Turn – Puzzle de blocs gratuit | Maxlol Games",
  title="Gravity Turn – Puzzle de blocs, démo gratuite | Maxlol Games",
  old_desc="Puzzle de blocs gratuit : le plateau 8×8 tourne toutes les trois pièces et les blocs retombent. 84 niveaux, cascades, défi du jour. Sans achat.",
  desc="Puzzle de blocs : le plateau 8×8 tourne toutes les trois pièces et les blocs retombent. Démo gratuite de 24 niveaux, jeu complet de 84 niveaux à 2,99 €.",
  offer_name_old="Gratuit", offer_name="Jeu complet",
  chips_old='<div class="chips"><span class="chip">Gratuit</span><span class="chip">Aucun achat</span></div>',
  chips='<div class="chips"><span class="chip">Démo gratuite : 24 niveaux</span><span class="chip">Jeu complet : 2,99 €, achat unique</span></div>',
  play_old="Jouer gratuitement", play="Essayer gratuitement",
  pay='Payer <span class="price"></span> avec PayPal', cgv="/fr/conditions-de-vente/",
  model_old='<div class="model"><h2>Gratuit, sans achat</h2><ul><li>Tu joues gratuitement, directement dans ton navigateur.</li><li>Aucun achat n&#x27;est proposé dans le jeu pour l&#x27;instant.</li></ul></div>',
  model=('<div class="model"><h2>Démo gratuite, jeu complet en achat unique</h2><ul>'
         '<li>Tu peux essayer les 24 premiers niveaux (2 mondes) gratuitement, sans compte, directement dans ton navigateur.</li>'
         '<li>Si tu accroches, le jeu complet (84 niveaux, 7 mondes) s&#x27;achète une seule fois (2,99 €) : pas d&#x27;abonnement.</li>'
         '<li>Tu paies avec PayPal. Ton code de déblocage t&#x27;est ensuite envoyé par e-mail, à l&#x27;adresse de ton compte PayPal : l&#x27;accès n&#x27;est donc pas instantané.</li></ul>'
         '<div class="cmp"><div class="h">Contenu</div><div class="h">Démo gratuite</div><div class="h hf">Jeu complet</div>'
         '<div class="h">Niveaux</div><div>24 niveaux (mondes 1 et 2)</div><div>Les 84 niveaux et 7 mondes</div>'
         '<div class="h">Prix</div><div>Gratuit</div><div>2,99 €, achat unique</div></div></div>'),
  bb=('<div class="buybox" data-buybox><p class="bb-t">Avant de payer avec PayPal</p><ul>'
      '<li>Prix total : <b data-bb-price></b>, en euros (EUR). Taxes : <mark class="todo">À compléter : TAXES_PRIX</mark></li>'
      '<li>Contenu : le jeu complet (84 niveaux, 7 mondes ; la démo gratuite donne accès aux 24 premiers niveaux).</li>'
      '<li>Compatibilité : navigateur web récent, sur ordinateur, téléphone ou tablette.</li>'
      '<li>Livraison : un code de déblocage est envoyé par e-mail à l’adresse de ton compte PayPal, au plus tard sous 48 h après le paiement.</li></ul>'
      '<label><input type="checkbox" id="cgv-ok"><span>J’ai lu et j’accepte les <a href="/fr/conditions-de-vente/">conditions de vente</a>.</span></label>'
      '<p class="bb-n">En cliquant sur « Payer avec PayPal », vous avez une obligation de paiement.</p></div>'),
 ),
 "en": dict(
  page="gravity-turn/index.html",
  old_title="Gravity Turn – Free Rotating Block Puzzle | Maxlol Games",
  title="Gravity Turn – Rotating Block Puzzle, Free Demo | Maxlol Games",
  old_desc="Free block puzzle: the 8×8 board turns every three pieces and blocks fall. 84 levels, cascades, daily challenge. No purchases.",
  desc="Block puzzle: the 8×8 board turns every three pieces and blocks fall. Free 24-level demo, full 84-level game for €2.99.",
  offer_name_old="Free", offer_name="Full game",
  chips_old='<div class="chips"><span class="chip">Free</span><span class="chip">No purchases</span></div>',
  chips='<div class="chips"><span class="chip">Free demo: 24 levels</span><span class="chip">Full game: €2.99, one-time purchase</span></div>',
  play_old="Play for free", play="Try for free",
  pay='Pay <span class="price"></span> with PayPal', cgv="/terms-of-sale/",
  model_old=None,
  model=('<div class="model"><h2>Free demo, full game as a one-time purchase</h2><ul>'
         '<li>Try the first 24 levels (2 worlds) for free, with no account, right in your browser.</li>'
         '<li>If you like it, the full game (84 levels, 7 worlds) is a single purchase (€2.99): no subscription.</li>'
         '<li>You pay with PayPal. Your unlock code is then sent by e-mail, to your PayPal account address: access is not instant.</li></ul>'
         '<div class="cmp"><div class="h">Content</div><div class="h">Free demo</div><div class="h hf">Full game</div>'
         '<div class="h">Levels</div><div>24 levels (worlds 1 and 2)</div><div>All 84 levels and 7 worlds</div>'
         '<div class="h">Price</div><div>Free</div><div>€2.99, one-time purchase</div></div></div>'),
  bb=('<div class="buybox" data-buybox><p class="bb-t">Before paying with PayPal</p><ul>'
      '<li>Total price: <b data-bb-price></b>, in euros (EUR). Taxes: <mark class="todo">To complete: TAXES_PRIX</mark></li>'
      '<li>Content: the full game (84 levels, 7 worlds; the free demo covers the first 24 levels).</li>'
      '<li>Compatibility: recent web browser, on computer, phone or tablet.</li>'
      '<li>Delivery: an unlock code is sent by e-mail to your PayPal account address, within 48 hours of payment at the latest.</li></ul>'
      '<label><input type="checkbox" id="cgv-ok"><span>I have read and accept the <a href="/terms-of-sale/">terms of sale</a>.</span></label>'
      '<p class="bb-n">By clicking “Pay with PayPal”, you are under an obligation to pay.</p></div>'),
 ),
}
CGV_JS = ("(function(){var c=document.getElementById('cgv-ok'),b=document.querySelector('[data-paypal]');if(!c||!b)return;"
          "var x=document.querySelector('[data-buybox]');if(b.hidden){if(x)x.hidden=true;return;}var h=b.getAttribute('href');"
          "function s(){if(c.checked&&h){b.setAttribute('href',h);b.removeAttribute('aria-disabled');}else{b.removeAttribute('href');b.setAttribute('aria-disabled','true');}}"
          "c.checked=false;c.addEventListener('change',s);s();var p=document.querySelector('[data-bb-price]'),q=b.querySelector('.price');if(p&&q)p.textContent=q.textContent;})();")

def patch_gt_page(s, t, price):
    # 1. titres et descriptions
    s = s.replace(t["old_title"], t["title"]).replace(t["old_desc"], t["desc"])
    # 2. offre structurée
    s = re.sub(r'"offers": \{"@type": "Offer", "name": "%s", "price": "0"' % re.escape(t["offer_name_old"]),
               '"offers": {"@type": "Offer", "name": "%s", "price": "%s"' % (t["offer_name"], GT_AMOUNT), s)
    # 3. pastilles
    s = s.replace(t["chips_old"], t["chips"])
    # 4. boutons : Jouer -> Essayer ; ajout du bouton PayPal + encadré d'achat (une seule fois)
    if 'data-paypal="gt"' not in s:
        cta = re.search(r'(<div class="gp-cta" id="cta">.*?)(</div>)', s, flags=re.S)
        if cta:
            block = cta.group(1).replace(t["play_old"], t["play"], 1) + \
                    '<a class="btn paypal" data-paypal="gt" href="#" target="_blank" rel="noopener">%s</a>' % t["pay"] + "</div>" + t["bb"]
            s = s[:cta.start()] + block + s[cta.end():]
    # 4b. barre fixe mobile
    s = re.sub(r'(<div class="sbar" id="sbar">.*?)%s(</a></div>)' % re.escape(t["play_old"]), lambda m: m.group(1) + t["play"] + m.group(2), s, count=1, flags=re.S)
    # 5. panneau « modèle » (gratuit / achat unique)
    s = re.sub(r'<div class="model">.*?</div></div></section>', lambda m: t["model"] + "</div></section>", s, count=1, flags=re.S) \
        if 'class="cmp"' not in s.split('<div class="model">')[-1][:1500] else s
    # 6. boutique JS de la page : prix + PayPal
    s = re.sub(r'"gt":\s*\{ price: "[^"]*",\s*itch: ""(?:, paypal: "[^"]*")? \},',
               '"gt":    { price: "%s", itch: "", paypal: "%s" },' % (price, PAYPAL), s, count=1)
    # 7. activation du bouton PayPal par la case « conditions de vente »
    if "cgv-ok'" not in s:
        s = s.replace("</body>", "<script>" + CGV_JS + "</script>\n</body>", 1)
    return s

def main():
    check = "--check" in sys.argv
    changed = 0
    for rel in HOMES:
        p = ROOT / rel
        if not p.exists(): continue
        s = p.read_text(encoding="utf-8"); n = patch_home(s)
        if n != s:
            changed += 1
            if not check: p.write_text(n, encoding="utf-8")
    for lang, t in T.items():
        p = ROOT / t["page"]
        s = p.read_text(encoding="utf-8")
        price = "2,99 €" if lang == "fr" else "€2.99"
        n = patch_gt_page(s, t, price)
        if n != s:
            changed += 1
            if not check: p.write_text(n, encoding="utf-8")
    print(("à modifier : " if check else "modifié : ") + str(changed) + " fichiers")

if __name__ == "__main__":
    main()
