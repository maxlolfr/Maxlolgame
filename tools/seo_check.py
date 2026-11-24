#!/usr/bin/env python3
"""Contrôle SEO automatique de tout le site (à relancer après chaque modification). Usage : python3 tools/seo_check.py [racine]
Vérifie : titres/descriptions uniques et de bonne longueur, canonical, hreflang réciproques, Open Graph + images 1200x630, JSON-LD valide,
alt des images, un seul h1, liens internes, sitemap (URLs existantes, indexables, canoniques), robots, flux RSS."""
import re,sys,os,json,glob,html,collections
from xml.etree import ElementTree as ET
from PIL import Image
R=(sys.argv[1] if len(sys.argv)>1 else os.path.dirname(os.path.dirname(os.path.abspath(__file__))))+'/'
B='https://maxlolgames.com'; err=[]; warn=[]; info=collections.OrderedDict()
def e(m): err.append(m)
def w(m): warn.append(m)
def path_of(url):
    p=url.replace(B,''); p=p.split('#')[0].split('?')[0]
    return R+p.lstrip('/')+('index.html' if p.endswith('/') or p=='' else '')
sm=ET.parse(R+'sitemap.xml').getroot(); ns={'s':'http://www.sitemaps.org/schemas/sitemap/0.9','x':'http://www.w3.org/1999/xhtml'}
urls=[u.find('s:loc',ns).text for u in sm.findall('s:url',ns)]; info['URL dans le sitemap']=len(urls)
if len(set(urls))!=len(urls): e('sitemap : doublons')
titles={}; descs={}; pages={}
for u in urls:
    f=path_of(u)
    if not os.path.exists(f): e('sitemap : fichier absent '+u); continue
    t=open(f).read(); pages[u]=t; h=t[:t.index('</head>')]
    if re.search(r'<meta name="robots"[^>]*noindex',h): e('indexable attendu mais noindex : '+u)
    m=re.search(r'<link rel="canonical" href="([^"]+)"',h)
    if not m: e('canonical manquant '+u)
    elif m.group(1)!=u: e('canonical ≠ URL du sitemap : %s -> %s'%(u,m.group(1)))
    ti=html.unescape(re.search(r'<title>(.*?)</title>',h).group(1)); de=html.unescape((re.search(r'<meta name="description" content="([^"]*)"',h) or [0,''])[1])
    if not de: e('description manquante '+u)
    titles.setdefault(ti,[]).append(u); descs.setdefault(de,[]).append(u)
    if len(ti)>72: w('titre long (%d) %s'%(len(ti),u))
    if len(ti)<20: w('titre court %s'%u)
    cjk=sum(1 for ch in de if ord(ch)>0x2E80); n=len(de)+cjk
    if de and not 70<=n<=175: w('description %d car. %s'%(len(de),u))
    if len(re.findall(r'<h1[ >]',t))!=1: e('h1 : %d sur %s'%(len(re.findall(r'<h1[ >]',t)),u))
    for p in ('og:title','og:description','og:url','og:image','og:image:width','og:image:height','og:image:alt','og:locale'):
        if 'property="%s"'%p not in h: e('%s manquant %s'%(p,u))
    for p in ('twitter:card','twitter:title','twitter:image'):
        if 'name="%s"'%p not in h: e('%s manquant %s'%(p,u))
    ou=re.search(r'property="og:url" content="([^"]+)"',h)
    if ou and ou.group(1)!=u: e('og:url ≠ canonical '+u)
    oi=re.search(r'property="og:image" content="([^"]+)"',h)
    if oi:
        fp=R+oi.group(1).replace(B+'/','')
        if not os.path.exists(fp): e('image de partage absente '+oi.group(1))
        else:
            sz=Image.open(fp).size
            if sz!=(1200,630): e('image de partage %s = %s (attendu 1200x630)'%(oi.group(1),sz))
            if os.path.getsize(fp)>300*1024: w('image de partage lourde %s'%oi.group(1))
    # JSON-LD
    for x in re.findall(r'<script type="application/ld\+json">(.*?)</script>',t,re.S):
        try: d=json.loads(x)
        except Exception as ex: e('JSON-LD invalide %s : %s'%(u,ex)); continue
        types=[n.get('@type') for n in d.get('@graph',[d])]
        info.setdefault('types JSON-LD',set()).update(map(str,types))
    # alt
    imgs=re.findall(r'<img[^>]*>',t)
    noalt=[i for i in imgs if 'alt=' not in i]
    if noalt: e('%d image(s) sans attribut alt sur %s'%(len(noalt),u))
    # liens internes
    for hr in set(re.findall(r'(?:href|src)="(/[^"#?]*)',t)):
        p=hr.lstrip('/')
        if p and not (os.path.exists(R+p) or os.path.exists(R+p.rstrip('/')+'/index.html')): e('lien interne cassé %s -> %s'%(u,hr))
    # liens canoniques vers hreflang : réciprocité
    hl=dict(re.findall(r'<link rel="alternate" hreflang="([^"]+)" href="([^"]+)"',h))
    for xl in sm.findall('s:url',ns):
        pass
    if hl:
        if m and m.group(1) not in hl.values(): e('hreflang sans auto-référence '+u)
        if 'x-default' not in hl: w('x-default absent '+u)
        for lg,hu in hl.items():
            tf=path_of(hu)
            if not os.path.exists(tf): e('hreflang vers page absente %s -> %s'%(u,hu)); continue
            back=re.findall(r'<link rel="alternate" hreflang="([^"]+)" href="([^"]+)"',open(tf).read()[:open(tf).read().index('</head>')])
            if u not in [b[1] for b in back]: e('hreflang non réciproque %s <-> %s'%(u,hu))
    # hreflang du sitemap cohérents avec la page
    ent=[x for x in sm.findall('s:url',ns) if x.find('s:loc',ns).text==u][0]
    smh=set(a.get('href') for a in ent.findall('x:link',ns))
    if hl and smh and smh!=set(hl.values()): e('hreflang sitemap ≠ page : '+u)
for ti,us in titles.items():
    if len(us)>1: e('titre dupliqué "%s" : %s'%(ti[:50],us))
for de,us in descs.items():
    if len(us)>1: e('description dupliquée : %s'%us)
# robots
rb=open(R+'robots.txt').read()
if 'Sitemap: %s/sitemap.xml'%B not in rb: e('robots : sitemap non déclaré')
for d in re.findall(r'Disallow: (\S+)',rb):
    for u in urls:
        if u.replace(B,'').startswith(d): e('robots bloque une URL du sitemap : '+u)
# flux RSS
for f in ('feed.xml','fr/feed.xml'):
    try: r=ET.parse(R+f).getroot(); info['articles '+f]=len(r.findall('./channel/item'))
    except Exception as ex: e('RSS invalide %s : %s'%(f,ex))
# pages publiques absentes du sitemap
for f in glob.glob(R+'**/index.html',recursive=True):
    rel=f[len(R):]
    if rel.split('/')[0] in('tools','backend','account','pay','chibi-test','chibi-legends','legal','node_modules','en'): continue
    u=B+'/'+rel[:-10]
    if u not in urls and u!=B+'/': w('page publique hors sitemap : '+u)
print('===== Contrôle SEO =====')
for k,v in info.items(): print(' ',k,':',sorted(v) if isinstance(v,set) else v)
print('  erreurs :',len(err),'| avertissements :',len(warn))
for x in err: print('  ✗',x)
for x in warn[:25]: print('  !',x)
sys.exit(1 if err else 0)
