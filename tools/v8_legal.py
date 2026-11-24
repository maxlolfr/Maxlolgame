"""Étape 8 (après build_i18n.py et v7_css.py) : pages juridiques FR + EN, liens de pied de page, encadré d'achat PayPal. Idempotent.
Sources : tools/legal/src/*.html (ChatGPT, FR) + tools/legal/en.py (EN) + tools/legal/facts.json (faits confirmés).
Pages : noindex, avertissement brouillon conservé, hors sitemap. Usage : python3 tools/v8_legal.py"""
import re, glob, os, json, html, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + '/'
L = ROOT + 'tools/legal/'
sys.path.insert(0, L)
from en import EN

KEYS = ['assistance', 'cgv', 'remboursements', 'confidentialite', 'mentions-legales', 'cookies', 'cgu']
SLUG = {'assistance': ('assistance', 'support'), 'cgv': ('conditions-de-vente', 'terms-of-sale'),
        'remboursements': ('remboursements', 'refunds'), 'confidentialite': ('confidentialite', 'privacy'),
        'mentions-legales': ('mentions-legales', 'legal-notice'), 'cookies': ('cookies', 'cookies'),
        'cgu': ('conditions-utilisation', 'terms-of-use')}
def url(k, lang): return ('/fr/%s/' % SLUG[k][0]) if lang == 'fr' else ('/%s/' % SLUG[k][1])
FOOT = {'fr': ['Assistance', 'Conditions de vente', 'Remboursements', 'Confidentialité', 'Mentions légales', 'Cookies', "Conditions d’utilisation"],
        'en': ['Support', 'Terms of sale', 'Refunds', 'Privacy', 'Legal notice', 'Cookies', 'Terms of use']}
BAN = {'fr': 'Brouillon de préproduction — informations à vérifier avant publication.', 'en': 'Pre-production draft — information to be verified before publication.'}
TODO = {'fr': 'À compléter : %s', 'en': 'To complete: %s'}
FACTS = json.load(open(L + 'facts.json', encoding='utf8'))

# ---------- contenu ----------
def fr_pages():
    out = {}
    for k in KEYS:
        s = open(L + 'src/%s.html' % k, encoding='utf8').read()
        main = re.search(r'<main>(.*?)</main>', s, re.S).group(1)
        title = html.unescape(re.search(r'<h1>(.*?)</h1>', main).group(1))
        secs = [(html.unescape(a), html.unescape(b)) for a, b in re.findall(r'<section><h2>(.*?)</h2><p>(.*?)</p></section>', main, re.S)]
        out[k] = (title, secs)
    # consignes de rédaction ChatGPT retirées du texte public (équivalents EN dans en.py)
    t, secs = out['confidentialite']
    out['confidentialite'] = (t, [
        (secs[0][0], secs[0][1]),
        ('Données et finalités', 'Inventaire des données : [[INVENTAIRE_DONNEES]]. Traitements, finalités, base légale, caractère obligatoire et conséquences de l’absence de données : [[TABLE_TRAITEMENTS]]. Les sauvegardes locales sont distinctes des données transmises à un serveur.'),
        ('Destinataires et paiements', 'Prestataires réellement utilisés et rôles : [[PRESTATAIRES]]. PayPal dispose de sa propre politique de confidentialité pour ses traitements.'),
        secs[3], secs[4], secs[5]])
    return out
FR = fr_pages()

def fill(text, lang):
    text = html.escape(text, quote=False)
    for _ in range(3):                                   # les faits peuvent contenir d'autres marqueurs
        def rep(m):
            v = FACTS.get(m.group(1))
            if v is None: return m.group(0)
            return html.escape(v[lang] if isinstance(v, dict) else v, quote=False)
        text = re.sub(r'\[\[([A-Z_]+)\]\]', rep, text)
    return re.sub(r'\[\[([A-Z_]+)\]\]', lambda m: '<mark class="todo">%s</mark>' % (TODO[lang] % m.group(1)), text)

# ---------- gabarit pris sur les pages existantes (identité graphique identique) ----------
def template(lang):
    p = ROOT + ('fr/actualites/index.html' if lang == 'fr' else 'news/index.html')
    s = open(p, encoding='utf8').read()
    css = re.search(r'<link rel="stylesheet" href="(/assets/css/news\.[0-9a-f]+\.css)">', s).group(1)
    header = re.search(r'<header class="top">.*?</header>', s, re.S).group(0)
    footer = re.search(r'<footer>.*?</footer>', s, re.S).group(0)
    tail = s[s.index('</footer>') + 9:]
    csp = re.search(r'<meta http-equiv="Content-Security-Policy"[^>]*>', s).group(0)
    return css, header, footer, tail, csp

def page(k, lang):
    css, header, footer, tail, csp = template(lang)
    title, secs = FR[k] if lang == 'fr' else EN[k]
    me, other = url(k, lang), url(k, 'en' if lang == 'fr' else 'fr')
    hdr = header
    hdr = re.sub(r'<a href="[^"]*" hreflang="fr"', '<a href="%s" hreflang="fr"' % url(k, 'fr'), hdr)
    hdr = re.sub(r'<a href="[^"]*" hreflang="en"', '<a href="%s" hreflang="en"' % url(k, 'en'), hdr)
    home = '/fr/' if lang == 'fr' else '/'
    body = ''.join('<section><h2>%s</h2><p>%s</p></section>' % (html.escape(a), fill(b, lang)) for a, b in secs)
    return ('<!DOCTYPE html>\n<html lang="%s">\n<head>\n<meta charset="utf-8">\n%s\n<meta name="referrer" content="strict-origin-when-cross-origin">\n'
            '<meta name="viewport" content="width=device-width, initial-scale=1">\n<link rel="manifest" href="/manifest.webmanifest">\n'
            '<link rel="apple-touch-icon" href="/assets/icon-180.png">\n<link rel="preload" href="/assets/fonts/lilita-one.woff" as="font" type="font/woff" crossorigin>\n'
            '<link rel="preload" href="/assets/fonts/nunito.woff" as="font" type="font/woff" crossorigin>\n<link rel="icon" href="/favicon.ico" sizes="48x48">\n'
            '<title>%s | Maxlol Games</title>\n<meta name="robots" content="noindex, nofollow">\n<link rel="stylesheet" href="%s">\n</head>\n<body class="gp">\n%s\n'
            '<main class="nw legal"><div class="wrap"><p class="crumb"><a href="%s">%s</a> › %s</p><h1>%s</h1><p class="draft">%s</p>%s</div></main>\n%s\n%s'
            ) % (lang, csp, html.escape(title), css, hdr, home, 'Accueil' if lang == 'fr' else 'Home', html.escape(title), html.escape(title), BAN[lang], body, footer, tail)

for k in KEYS:
    for lang in ('fr', 'en'):
        d = ROOT + url(k, lang).strip('/') + '/'
        os.makedirs(d, exist_ok=True)
        open(d + 'index.html', 'w', encoding='utf8').write(page(k, lang))

# ---------- liens de pied de page + CSS légal + encadré d'achat sur toutes les pages publiques ----------
SKIP = ('tools/', 'backend', 'account', 'pay/', 'chibi', 'legal/', 'press/', 'node_modules')
BUY = {
 'fr': ('Avant de payer avec PayPal', 'Prix total : <b data-bb-price></b>, en euros (EUR). Taxes : %s',
        'Contenu : le jeu complet (20 mondes ; la démo gratuite donne accès aux mondes 1 à 5).',
        'Compatibilité : navigateur web récent, sur ordinateur, téléphone ou tablette.', 'Livraison : %s',
        "J’ai lu et j’accepte les <a href=\"/fr/conditions-de-vente/\">conditions de vente</a>.",
        'En cliquant sur « Payer avec PayPal », vous avez une obligation de paiement.', 'Payer %s avec PayPal'),
 'en': ('Before paying with PayPal', 'Total price: <b data-bb-price></b>, in euros (EUR). Taxes: %s',
        'Content: the full game (20 worlds; the free demo covers worlds 1 to 5).',
        'Compatibility: recent web browser, on computer, phone or tablet.', 'Delivery: %s',
        'I have read and accept the <a href="/terms-of-sale/">terms of sale</a>.',
        'By clicking “Pay with PayPal”, you are under an obligation to pay.', 'Pay %s with PayPal')}
GATE = ("<script>(function(){var c=document.getElementById('cgv-ok'),b=document.querySelector('[data-paypal]');if(!c||!b)return;var x=document.querySelector('[data-buybox]');if(b.hidden){if(x)x.hidden=true;return;}"
        "var h=b.getAttribute('href');function s(){if(c.checked&&h){b.setAttribute('href',h);b.removeAttribute('aria-disabled');}"
        "else{b.removeAttribute('href');b.setAttribute('aria-disabled','true');}}c.checked=false;c.addEventListener('change',s);s();"
        "var p=document.querySelector('[data-bb-price]'),q=b.querySelector('.price');if(p&&q)p.textContent=q.textContent;})();</script>")
done_pages = 0
for p in sorted(glob.glob(ROOT + '**/index.html', recursive=True)):
    rel = os.path.relpath(p, ROOT)
    if any(x in rel for x in SKIP):
        continue
    s = open(p, encoding='utf8').read()
    m = re.search(r'<html lang="([^"]+)"', s)
    if not m or '<footer>' not in s:
        continue
    lang = 'fr' if m.group(1) == 'fr' else 'en'
    o = s
    if 'legal.css' not in s:
        s = s.replace('</head>', '<link rel="stylesheet" href="/assets/css/legal.css"></head>', 1)
    # nettoie toute exécution précédente (script de validation et encadré d'achat)
    s = re.sub(r"<script>\(function\(\)\{var c=document\.getElementById\('cgv-ok'\).*?</script>", '', s, flags=re.S)
    s = re.sub(r'<div class="buybox" data-buybox>.*?</div>', '', s, flags=re.S)
    if 'legal-nav' not in s:
        links = ''.join('<a href="%s">%s</a>' % (url(k, lang), FOOT[lang][i]) for i, k in enumerate(KEYS))
        nav = '<div class="wrap legal-nav" role="navigation" aria-label="%s">%s</div>' % ('Informations légales et assistance' if lang == 'fr' else 'Legal information and support', links)
        s = s.replace('</footer>', nav + '</footer>', 1)
    has_cta = '<div class="gp-cta" id="cta">' in s and 'class="btn paypal"' in s
    if has_cta and 'data-buybox' not in s:
        b = BUY[lang]
        box = ('<div class="buybox" data-buybox><p class="bb-t">%s</p><ul><li>%s</li><li>%s</li><li>%s</li><li>%s</li></ul>'
               '<label><input type="checkbox" id="cgv-ok"><span>%s</span></label><p class="bb-n">%s</p></div>') % (
               b[0], b[1] % fill('[[TAXES_PRIX]]', lang), b[2], b[3], b[4] % fill('[[MODE_ET_DELAI_LIVRAISON]]', lang), b[5], b[6])
        s = re.sub(r'(<div class="gp-cta" id="cta">.*?</div>)', lambda mm: mm.group(1) + box, s, count=1, flags=re.S)
        s = re.sub(r'>PayPal <span class="price"></span></a>', '>' + (b[7] % '<span class="price"></span>') + '</a>', s, count=1)
    if has_cta:
        s = s.replace('</body>', GATE + '</body>', 1)
    if s != o:
        open(p, 'w', encoding='utf8').write(s); done_pages += 1
print('pages juridiques : 14 générées ; pages modifiées (pied de page/achat) :', done_pages)
