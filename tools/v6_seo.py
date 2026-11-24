# ================= V6 : SEO technique (accueils, actualités, flux RSS, sitemap, robots) =================
# Exécuté APRÈS v5_build : v6_build() corrige les accueils déjà écrits et crée les pages d'actualités.
import json as _j6, datetime as _dt6, email.utils as _eu6, os as _os6
_LOC6={'fr':'fr_FR','en':'en_US','es':'es_ES','pt':'pt_BR','th':'th_TH','zh':'zh_CN','ja':'ja_JP','ko':'ko_KR','ru':'ru_RU','id':'id_ID'}
_HL6={'fr':'fr','en':'en','es':'es','pt':'pt-BR','th':'th','zh':'zh-Hans','ja':'ja','ko':'ko','ru':'ru','id':'id'}
_PATH6={'fr':'fr/','en':'','es':'es/','pt':'pt/','th':'th/','zh':'zh/','ja':'ja/','ko':'ko/','ru':'ru/','id':'id/'}
def _cfg6(): return _j6.load(open(ROOT+'tools/seo_config.json'))
def _news6(): return _j6.load(open(ROOT+'tools/news.json'))['items']
NEWS_URL={'fr':'/fr/actualites/','en':'/news/'}
def v6_head(lang,rss=True):
    """Balises communes : vérification Search Console / Bing (si fournies) + flux RSS."""
    c=_cfg6(); o=''
    if c.get('google_site_verification'): o+='<meta name="google-site-verification" content="%s">\n'%_x(c['google_site_verification'])
    if c.get('bing_site_verification'): o+='<meta name="msvalidate.01" content="%s">\n'%_x(c['bing_site_verification'])
    if rss and lang in NEWS_URL: o+='<link rel="alternate" type="application/rss+xml" title="Maxlol Games – %s" href="%s">\n'%('Actualités' if lang=='fr' else 'News',('/fr/feed.xml' if lang=='fr' else '/feed.xml'))
    return o
V6_TITLE={
 'fr':("Maxlol Games – Jeux indépendants : RPG, roguelite, puzzle, shoot'em up","Jeux indépendants à jouer dans le navigateur : RPG de donjon, roguelite, puzzle et shoot'em up à dragons. Essai gratuit, sans compte."),
 'en':("Maxlol Games – Indie Games: RPG, Roguelite, Puzzle & Shoot'em Up","Indie games you can play in your browser: a dungeon RPG, a roguelite, a puzzle game and a dragon shoot'em up. Free to try, no account needed."),
 'es':("Maxlol Games – Juegos indie: RPG, roguelite, puzles y shoot'em up","Juegos indie para jugar en el navegador: un RPG de mazmorras, un roguelite, un puzle y un shoot'em up de dragones. Prueba gratis, sin cuenta."),
 'pt':("Maxlol Games – Jogos indie: RPG, roguelite, quebra-cabeça e shoot'em up","Jogos indie para jogar no navegador: um RPG de masmorra, um roguelite, um quebra-cabeça e um shoot'em up de dragões. Teste grátis, sem conta."),
 'th':("Maxlol Games – เกมอินดี้: RPG โรกูไลต์ พัซเซิล ชูตเอมอัป","เกมอินดี้ที่เล่นได้บนเบราว์เซอร์: RPG ดันเจี้ยน โรกูไลต์ พัซเซิล และเกมยิงมังกร ลองเล่นฟรี ไม่ต้องสมัครบัญชี"),
 'zh':("Maxlol Games – 独立游戏：RPG、Roguelite、益智、飞行射击","可在浏览器中游玩的独立游戏：地牢 RPG、Roguelite、益智游戏和龙之射击游戏。免费试玩，无需账号。"),
 'ja':("Maxlol Games – インディーゲーム：RPG・ローグライト・パズル・シューティング","ブラウザで遊べるインディーゲーム：ダンジョンRPG、ローグライト、パズル、ドラゴンシューティング。無料で試せて、アカウント不要。"),
 'ko':("Maxlol Games – 인디 게임: RPG, 로그라이트, 퍼즐, 슈팅","브라우저에서 바로 즐기는 인디 게임: 던전 RPG, 로그라이트, 퍼즐, 드래곤 슈팅. 무료 체험, 계정 불필요."),
 'ru':("Maxlol Games – Инди-игры: RPG, рогалик, головоломка, шутер","Инди-игры в браузере: RPG-подземелье, рогалик, головоломка и шутер с драконами. Бесплатная проба, без аккаунта."),
 'id':("Maxlol Games – Game indie: RPG, roguelite, puzzle, shoot'em up","Game indie yang bisa dimainkan di browser: RPG dungeon, roguelite, puzzle, dan shoot'em up naga. Coba gratis, tanpa akun.")}
V6_ALT={'la-derniere-torche':'La Dernière Torche','wyrmstorm':'WYRMSTORM','gravity-turn':'Gravity Turn','infinite-dungeon':'Infinite Dungeon'}
def _hreflang_block(urls):
    return ''.join('<link rel="alternate" hreflang="%s" href="%s">\n'%(h,u) for h,u in urls)

def v6_patch_home(lang,s):
    k=s.index('<style>'); head,rest=s[:k],s[k:]
    # titres / descriptions ciblés (fr/en) : mots-clés naturels, pas de bourrage
    if lang in V6_TITLE:  # titre + description courts, dans chaque langue
        t,d=V6_TITLE[lang]
        head=re.sub(r'<title>.*?</title>','<title>%s</title>'%_x(t),head,count=1)
        head=re.sub(r'(<meta name="description" content=")[^"]*(")',lambda m:m.group(1)+_x(d)+m.group(2),head,count=1)
        head=re.sub(r'(<meta property="og:description" content=")[^"]*(")',lambda m:m.group(1)+_x(d)+m.group(2),head,count=1)
        head=re.sub(r'(<meta name="twitter:description" content=")[^"]*(")',lambda m:m.group(1)+_x(d)+m.group(2),head,count=1)
        head=re.sub(r'(<meta property="og:title" content=")[^"]*(")',lambda m:m.group(1)+_x(t)+m.group(2),head,count=1)
        head=re.sub(r'(<meta name="twitter:title" content=")[^"]*(")',lambda m:m.group(1)+_x(t)+m.group(2),head,count=1)
    # image de partage : dimensions complètes + texte alternatif
    alt={'fr':'Maxlol Games : les jeux du studio indépendant','en':'Maxlol Games: the indie studio\'s games'}.get(lang,'Maxlol Games')
    head=re.sub(r'(<meta property="og:image:width" content="1200">)(?!\s*<meta property="og:image:height")',r'\1\n<meta property="og:image:height" content="630">\n<meta property="og:image:type" content="image/jpeg">\n<meta property="og:image:alt" content="%s">'%_x(alt),head,count=1)
    head=head.replace('<meta name="twitter:image" content="https://maxlolgames.com/assets/og.jpg">','<meta name="twitter:image" content="https://maxlolgames.com/assets/og.jpg">\n<meta name="twitter:image:alt" content="%s">'%_x(alt),1)
    alts=''.join('<meta property="og:locale:alternate" content="%s">\n'%_LOC6[c] for c in _O if c!=lang)
    head=head.replace('</head>',alts+v6_head(lang)+'</head>',1) if 'og:locale:alternate' not in head else head.replace('</head>',v6_head(lang)+'</head>',1)
    # données structurées : liste des jeux (pages dédiées en fr/en) à la place du VideoGame unique
    def fixld(m):
        d=_j6.loads(m.group(1)); g=[x for x in d['@graph'] if x.get('@type')!='VideoGame']; items=[]
        for i,(slug,name) in enumerate(V6_ALT.items(),1):
            u='https://maxlolgames.com%s%s/'%(('/fr/' if lang=='fr' else '/'),slug) if lang in('fr','en') else 'https://maxlolgames.com/%s#%s'%(_PATH6[lang],slug)
            gm={"@type":"VideoGame","name":name,"url":u,"image":"https://maxlolgames.com/assets/og/%s.jpg"%slug,"applicationCategory":"Game","gamePlatform":"Web browser","author":{"@id":"https://maxlolgames.com/#studio"}}
            if lang in V5_G.get(slug,{}) : gm["genre"]=V5_G[slug][lang]['genre']; gm["description"]=V5_SEO[slug][lang][1].replace('{p}',v5_fmt_price(lang,s))
            items.append({"@type":"ListItem","position":i,"item":gm})
        g.append({"@type":"ItemList","name":"Maxlol Games","itemListElement":items})
        d['@graph']=g; return '<script type="application/ld+json">'+_j6.dumps(d,ensure_ascii=False).replace('</','<\\/')+'</script>'
    rest=re.sub(r'<script type="application/ld\+json">(.*?)</script>',fixld,rest,count=1,flags=re.S)
    head=re.sub(r'<script type="application/ld\+json">(.*?)</script>',fixld,head,count=1,flags=re.S)
    # textes alternatifs des visuels des cartes du hero (liens sans texte)
    for slug,name in V6_ALT.items():
        rest=re.sub(r'(<a class="card c\d" href="#%s"[^>]*><img [^>]*?)alt=""'%slug,lambda m:m.group(1)+'alt="%s"'%_x(name),rest,count=1)
    rest=re.sub(r'(<a class="card c\d" href="#gravity-turn"[^>]*><span class="gtc"><img src="[^"]*gt-jelly[^>]*?)alt=""',lambda m:m.group(1)+'alt="Gravity Turn"',rest,count=1)
    # intro décorative : masquée aux lecteurs d'écran
    rest=rest.replace('<div id="intro"','<div id="intro" aria-hidden="true"',1) if 'id="intro" aria-hidden' not in rest else rest
    # actualités : lien vers la page dédiée (fr/en) + lien "toutes les actualités"
    if lang in NEWS_URL:
        for n in _news6():
            old='<a href="#%s"><span class="ntag">'%n['game'];
        rest=re.sub(r'(<li><time datetime="(\d{4}-\d\d-\d\d)">[^<]*</time>)<a href="#([a-z-]+)"><span class="ntag">([^<]*)</span>([^<]*)</a>',
            lambda m:'%s<a href="%s%s"><span class="ntag">%s</span>%s</a>'%(m.group(1),NEWS_URL[lang],'#'+_news_id(m.group(2),m.group(3),m.group(5),lang),m.group(4),m.group(5)),rest)
        more={'fr':'Toutes les actualités','en':'All news'}[lang]
        rest=rest.replace('</ol></div></section>','</ol><p class="nmore"><a href="%s">%s →</a></p></div></section>'%(NEWS_URL[lang],more),1)
    return head+rest
def _news_id(date,anchor,title,lang):
    for n in _news6():
        if n['date']==date and (n['game']==anchor) and _x(n['title'][lang])==title: return n['id']
    for n in _news6():
        if n['date']==date and n['game']==anchor: return n['id']
    return ''

NEWS_T={'fr':dict(h='Actualités et mises à jour',lead="Les nouveautés des jeux Maxlol Games : mises à jour, nouvelles versions et nouveaux jeux.",desc="Actualités de Maxlol Games : mises à jour et nouveautés de La Dernière Torche, WYRMSTORM, Gravity Turn et Infinite Dungeon.",ti="Actualités et mises à jour | Maxlol Games",rss="S'abonner au flux RSS",game='Voir le jeu',home='Accueil'),
        'en':dict(h='News and updates',lead="What's new in Maxlol Games titles: updates, new versions and new games.",desc="Maxlol Games news: updates and new features for La Dernière Torche, WYRMSTORM, Gravity Turn and Infinite Dungeon.",ti="News and updates | Maxlol Games",rss="Subscribe via RSS",game='See the game',home='Home')}
NEWS_CSS='''
.nw{padding:28px 0 60px}.nw h1{font:400 clamp(2rem,6vw,3rem)/1.05 var(--display);margin:6px 0}.nw .lead{color:var(--lavande);margin:0 0 22px}
.nw article{background:var(--prune);border-radius:18px;padding:18px;margin:0 0 14px;box-shadow:inset 0 0 0 1px rgba(255,255,255,.07)}
.nw article h2{font:400 1.35rem/1.15 var(--display);margin:6px 0}.nw article p{margin:0;color:var(--brume)}.nw time{font-weight:800;color:var(--bonbon);font-size:.85rem}
.nw .tag{display:inline-block;margin-left:8px;padding:2px 10px;border-radius:999px;background:rgba(255,255,255,.09);font-weight:800;font-size:.8rem;text-decoration:none;color:inherit}
.nw .rss{display:inline-block;margin-top:8px}.nmore{margin:12px 0 0}.nmore a{font-weight:800}
'''
def v6_news_page(lang,home):
    T=NEWS_T[lang]; pre='/fr/' if lang=='fr' else '/'; url='https://maxlolgames.com'+NEWS_URL[lang]; feed='https://maxlolgames.com'+('/fr/feed.xml' if lang=='fr' else '/feed.xml')
    links,csp,css,header,footer,script=v5_chrome(lang,home,NEWS_URL['fr'],NEWS_URL['en'],pre,'')
    items=sorted(_news6(),key=lambda n:n['date'],reverse=True)
    arts=''
    for n in items:
        gl=('<a class="tag" href="%s%s/">%s</a>'%(pre,n['game'],_x(n['tag']))) if n['game'] in V5_SLUGS else '<span class="tag">%s</span>'%_x(n['tag'])
        arts+='<article id="%s"><time datetime="%s">%s</time>%s<h2>%s</h2><p>%s</p></article>\n'%(n['id'],n['date'],n['date'],gl,_x(n['title'][lang]),_x(n['body'][lang]))
    ld={"@context":"https://schema.org","@graph":[{"@type":"Blog","@id":url+"#blog","name":T['h']+' – Maxlol Games',"url":url,"inLanguage":lang,"publisher":{"@id":"https://maxlolgames.com/#studio"},
        "blogPost":[{"@type":"BlogPosting","headline":n['title'][lang],"datePublished":n['date'],"dateModified":n['date'],"url":url+'#'+n['id'],"description":n['body'][lang],"author":{"@id":"https://maxlolgames.com/#studio"},"publisher":{"@id":"https://maxlolgames.com/#studio"},"image":"https://maxlolgames.com/assets/og.jpg","inLanguage":lang} for n in items]},
        {"@type":"BreadcrumbList","itemListElement":[{"@type":"ListItem","position":1,"name":T['home'],"item":'https://maxlolgames.com'+pre},{"@type":"ListItem","position":2,"name":T['h'],"item":url}]}]}
    ldj=_j6.dumps(ld,ensure_ascii=False).replace('</','<\\/')
    alts='<link rel="alternate" hreflang="fr" href="https://maxlolgames.com/fr/actualites/">\n<link rel="alternate" hreflang="en" href="https://maxlolgames.com/news/">\n<link rel="alternate" hreflang="x-default" href="https://maxlolgames.com/news/">\n'
    return ('<!DOCTYPE html>\n<html lang="%s">\n<head>\n<meta charset="utf-8">\n%s\n<meta name="viewport" content="width=device-width, initial-scale=1">\n%s<title>%s</title>\n<meta name="description" content="%s">\n<meta name="robots" content="index, follow, max-image-preview:large">\n<link rel="canonical" href="%s">\n%s'
        '<meta property="og:type" content="website">\n<meta property="og:site_name" content="Maxlol Games">\n<meta property="og:locale" content="%s">\n<meta property="og:title" content="%s">\n<meta property="og:description" content="%s">\n<meta property="og:url" content="%s">\n<meta property="og:image" content="https://maxlolgames.com/assets/og.jpg">\n<meta property="og:image:type" content="image/jpeg">\n<meta property="og:image:width" content="1200">\n<meta property="og:image:height" content="630">\n<meta property="og:image:alt" content="Maxlol Games">\n'
        '<meta name="twitter:card" content="summary_large_image">\n<meta name="twitter:title" content="%s">\n<meta name="twitter:description" content="%s">\n<meta name="twitter:image" content="https://maxlolgames.com/assets/og.jpg">\n<link rel="alternate" type="application/rss+xml" title="Maxlol Games" href="%s">\n%s<script type="application/ld+json">%s</script>\n<style>%s%s%s</style>\n</head>\n'
        '<body class="gp">\n%s\n<main class="nw"><div class="wrap"><p class="crumb"><a href="%s">%s</a> › %s</p><h1>%s</h1><p class="lead">%s</p>\n%s<a class="rss btn ghost" href="%s">%s</a></div></main>\n%s\n<script>\n%s\ndocument.addEventListener("click",e=>{document.querySelectorAll(".mmenu[open],.langmenu[open]").forEach(d=>{if(!d.contains(e.target)||e.target.closest(".mm a"))d.open=false});});\n</script>\n</body>\n</html>\n')%(
        lang,csp,links,_x(T['ti']),_x(T['desc']),url,alts,_LOC6[lang],_x(T['ti']),_x(T['desc']),url,_x(T['ti']),_x(T['desc']),feed,v6_head(lang,False),ldj,css,V5_CSS,NEWS_CSS,header,pre,_x(T['home']),_x(T['h']),_x(T['h']),_x(T['lead']),arts,feed,_x(T['rss']),footer,script)

def v6_feed(lang):
    pre='/fr/' if lang=='fr' else '/'; items=sorted(_news6(),key=lambda n:n['date'],reverse=True); base='https://maxlolgames.com'
    rfc=lambda d:_eu6.format_datetime(_dt6.datetime.strptime(d,'%Y-%m-%d').replace(hour=9,tzinfo=_dt6.timezone.utc))
    it=''.join('<item><title>%s</title><link>%s</link><guid isPermaLink="true">%s</guid><pubDate>%s</pubDate><description>%s</description></item>\n'%(_x(n['title'][lang]),base+NEWS_URL[lang]+'#'+n['id'],base+NEWS_URL[lang]+'#'+n['id'],rfc(n['date']),_x(n['body'][lang])) for n in items)
    return ('<?xml version="1.0" encoding="UTF-8"?>\n<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom"><channel><title>Maxlol Games – %s</title><link>%s</link><description>%s</description><language>%s</language><lastBuildDate>%s</lastBuildDate>\n<atom:link href="%s" rel="self" type="application/rss+xml"/>\n%s</channel></rss>\n')%(NEWS_T[lang]['h'],base+NEWS_URL[lang],_x(NEWS_T[lang]['desc']),lang,rfc(items[0]['date']),base+pre+'feed.xml',it)

def v6_sitemap():
    base='https://maxlolgames.com'; news=_news6(); last=max(n['date'] for n in news)
    def u(loc,lm,pr,alts): return '  <url><loc>%s</loc><lastmod>%s</lastmod><priority>%s</priority>\n%s  </url>\n'%(loc,lm,pr,''.join('    <xhtml:link rel="alternate" hreflang="%s" href="%s"/>\n'%a for a in alts))
    out='<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">\n'
    home=[(_HL6[c],base+'/'+_PATH6[c]) for c in _O]+[('x-default',base+'/')]
    for c in _O: out+=u(base+'/'+_PATH6[c],last,'1.0' if c=='en' else '0.9',home)
    for slug in V5_SLUGS:
        lm=max([n['date'] for n in news if n['game']==slug]+['2026-11-24']); al=[('fr',base+'/fr/%s/'%slug),('en',base+'/%s/'%slug),('x-default',base+'/%s/'%slug)]
        for pth in ('/','/fr/'): out+=u(base+pth+slug+'/',lm,'0.8',al)
    al=[('fr',base+NEWS_URL['fr']),('en',base+NEWS_URL['en']),('x-default',base+NEWS_URL['en'])]
    for c in ('en','fr'): out+=u(base+NEWS_URL[c],last,'0.6',al)
    out+=u(base+'/press/',last,'0.4',[])
    return out+'</urlset>\n'
ROBOTS='''User-agent: *
Allow: /
Disallow: /backend/
Disallow: /account/
Disallow: /pay/
Disallow: /tools/
Disallow: /chibi-test/

Sitemap: https://maxlolgames.com/sitemap.xml
'''
def v6_build():
    for c in _O:
        f=ROOT+_PATH6[c]+'index.html'; s=open(f).read()
        if 'og:image:height' in s and 'twitter:image:alt' in s and 'ItemList' in s: continue          # déjà corrigé (idempotent)
        open(f,'w').write(v6_patch_home(c,s))
    for lang in ('fr','en'):
        home=open(ROOT+_PATH6[lang]+'index.html').read(); d=ROOT+NEWS_URL[lang].strip('/')+'/'; _os6.makedirs(d,exist_ok=True)
        open(d+'index.html','w').write(v6_news_page(lang,home)); open(ROOT+_PATH6[lang]+'feed.xml','w').write(v6_feed(lang))
    open(ROOT+'sitemap.xml','w').write(v6_sitemap()); open(ROOT+'robots.txt','w').write(ROBOTS)
    print('seo: accueils + actualités + flux + sitemap + robots')
