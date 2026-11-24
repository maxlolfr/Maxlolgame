# ================= V3 : jeux supplémentaires, sécurité, compteur, presse =================
import glob, os, html as _html
TOOLS=ROOT+'tools/'
def _cfg():
    try: return json.load(open(TOOLS+'config.json'))
    except Exception: return {}
def _games():
    out=[]
    for f in sorted(glob.glob(TOOLS+'games/*.json')):
        if os.path.basename(f).startswith('_'): continue
        g=json.load(open(f))
        if g.get('published',True) is False: continue   # jeu non publié : invisible partout
        out.append(g)
    return out
LAB={
'fr':('Jouer à {n}','Acheter','Voir sur itch.io','Plateformes','Version','Langues','Presse'),
'en':('Play {n}','Buy','See on itch.io','Platforms','Version','Languages','Press kit'),
'es':('Jugar a {n}','Comprar','Ver en itch.io','Plataformas','Versión','Idiomas','Prensa'),
'pt':('Jogar {n}','Comprar','Ver no itch.io','Plataformas','Versão','Idiomas','Imprensa'),
'th':('เล่น {n}','ซื้อ','ดูบน itch.io','แพลตฟอร์ม','เวอร์ชัน','ภาษา','ข้อมูลสื่อ'),
'zh':('游玩 {n}','购买','在 itch.io 上查看','平台','版本','语言','媒体资料'),
'ja':('{n} を遊ぶ','購入','itch.io で見る','対応機種','バージョン','言語','プレスキット'),
'ko':('{n} 플레이','구매','itch.io에서 보기','플랫폼','버전','언어','프레스 킷'),
'ru':('Играть в {n}','Купить','Смотреть на itch.io','Платформы','Версия','Языки','Пресса'),
'id':('Mainkan {n}','Beli','Lihat di itch.io','Platform','Versi','Bahasa','Media'),
}
def _g(d,lang,default=''):
    if not isinstance(d,dict): return d if d is not None else default
    return d.get(lang) or d.get('en') or d.get('fr') or default
def _e(t): return _html.escape(str(t),quote=True)
def _rgb(h):
    h=h.lstrip('#'); return ','.join(str(int(h[i:i+2],16)) for i in (0,2,4))
BUYSVG='<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M6 7h12l-1 13H7z"/><path d="M9 7a3 3 0 0 1 6 0"/></svg>'
PLAYSVG='<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M8 5.5v13a1 1 0 0 0 1.5.86l10.5-6.5a1 1 0 0 0 0-1.72L9.5 4.64A1 1 0 0 0 8 5.5z"/></svg>'
def game_section(g,lang,i):
    L=LAB[lang]; sl=g['slug']; n=_e(g['name']); a=g.get('accent','#3DD6C6'); ink=g.get('accent_ink','#10122A')
    feats=''.join('<li>%s</li>'%_e(x) for x in _g(g.get('feats'),lang,[]))
    facts=[]
    if g.get('platforms'): facts.append((L[3],_g(g['platforms'],lang)))
    if g.get('version'): facts.append((L[4],g['version']))
    if g.get('languages'): facts.append((L[5],_g(g['languages'],lang)))
    dl=''.join('<div><dt>%s</dt><dd>%s</dd></div>'%(_e(k),_e(v)) for k,v in facts)
    strip=''.join('<button data-full="%s"><img src="%s" alt="%s" loading="lazy" width="88" height="132"></button>'%(_e(x),_e(x),n) for x in g.get('images',[]))
    strip=('<div class="strip" aria-label="%s">%s</div>'%(n,strip)) if strip else ''
    cover=g.get('cover','')
    vis=('<div class="poster"><img src="%s" alt="%s" width="640" height="960" loading="lazy"></div>'%(_e(cover),n)) if cover else ''
    flip=' flip' if i%2==0 else ''
    return ('  <section class="game%s" id="%s" aria-labelledby="%s-t" style="--a:%s;--a-ink:%s">\n'
    '    <div class="flash" aria-hidden="true"></div>\n'
    '    <canvas class="fxc" data-fx="embers" data-col="%s|255,255,255" aria-hidden="true"></canvas>\n'
    '    <div class="wrap grid">\n      <div class="visual reveal from-art">%s</div>\n      <div>\n'
    '        <p class="genre reveal">%s <span class="tagp" data-price="%s"></span></p>\n'
    '        <h2 id="%s-t" class="reveal slam">%s</h2>\n        <p class="pitch reveal">%s</p>\n'
    '        <ul class="feats reveal">%s</ul>\n        <dl class="facts">%s</dl>\n        %s\n'
    '        <div class="cta">\n          <a class="btn main" data-link="%s-play" href="#" target="_blank" rel="noopener">%s%s</a>\n'
    '          <a class="btn buy" data-buy="%s" href="#" target="_blank" rel="noopener">%s%s <span class="price"></span></a>\n'
    '          <a class="btn paypal" data-paypal="%s" href="#" target="_blank" rel="noopener">PayPal <span class="price"></span></a>\n'
    '          <a class="btn ghost" data-link="%s-itch" href="#" target="_blank" rel="noopener">%s</a>\n'
    '        </div>\n      </div>\n    </div>\n  </section>\n')%(flip,_e(sl),_e(sl),a,ink,_rgb(a),vis,_e(_g(g.get('genre'),lang)),_e(sl),_e(sl),n,_e(_g(g.get('pitch'),lang)),feats,dl,strip,_e(sl),PLAYSVG,_e(L[0].format(n=g['name'])),_e(sl),BUYSVG,_e(L[1]),_e(sl),_e(sl),_e(L[2]))
def cover_card(g,lang):
    cover=g.get('cover',''); n=_e(g['name'])
    img=('<img src="%s" alt="" width="640" height="960" loading="lazy">'%_e(cover)) if cover else ''
    return '<a class="cover reveal" href="#%s"><div class="art">%s<span class="shine"></span></div><b>%s</b><span>%s</span></a>'%(_e(g["slug"]),img,n,_e(_g(g.get("genre"),lang)))
def apply_games(s,lang,cur):
    G=_games(); pre=(lambda t:t) if cur=='fr' or not [l for l in LANGS if l[0]==cur][0][1] else (lambda t:re.sub(r'(["\'`(])assets/',r'\1../assets/',t))
    s=re.sub(r'<!--GAMES-->.*?<!--/GAMES-->',lambda m:'<!--GAMES-->\n'+pre(''.join(game_section(g,lang,i) for i,g in enumerate(G)))+'<!--/GAMES-->',s,flags=re.S)
    s=re.sub(r'<!--COVERS-->.*?<!--/COVERS-->',lambda m:'<!--COVERS-->'+pre(''.join(cover_card(g,lang) for g in G))+'<!--/COVERS-->',s,flags=re.S)
    shop=''.join(',\n  "%s": { price: %s, itch: %s, paypal: %s }'%(g["slug"],json.dumps(g.get("price",""),ensure_ascii=False),json.dumps(g.get("itch","")),json.dumps(g.get("paypal",""))) for g in G)
    s=re.sub(r'/\*GS\*/.*?/\*GE\*/',lambda m:'/*GS*/'+shop+'/*GE*/',s,flags=re.S)
    links=''.join('"%s-play": %s, "%s-itch": %s,\n  '%(g["slug"],json.dumps(g.get("play","")),g["slug"],json.dumps(g.get("itch",""))) for g in G)
    s=re.sub(r'/\*LS\*/.*?/\*LE\*/',lambda m:'/*LS*/'+links+'/*LE*/',s,flags=re.S)
    m=re.search(r'<script type="application/ld\+json">(.*?)</script>',s,re.S); ld=json.loads(m.group(1))
    ld['@graph']=[n for n in ld['@graph'] if not n.get('@extra')]
    L_=[l for l in LANGS if l[0]==cur][0]
    for g in G:
        ld['@graph'].append({"@extra":1,"@type":"VideoGame","name":g['name'],"description":_g(g.get('pitch'),lang),"url":'https://maxlolgames.com/'+L_[1]+'#'+g['slug'],"genre":_g(g.get('genre'),lang),"inLanguage":L_[2],"image":'https://maxlolgames.com/'+g.get('cover',''),"applicationCategory":"Game","author":{"@id":"https://maxlolgames.com/#studio"},"publisher":{"@id":"https://maxlolgames.com/#studio"}})
    return s[:m.start(1)]+json.dumps(ld,ensure_ascii=False)+s[m.end(1):]
def apply_sec(s):
    tok=(_cfg().get('analytics_token') or '').strip()
    scr="'self' 'unsafe-inline'"+(' https://static.cloudflareinsights.com' if tok else '')
    con="'self'"+(' https://cloudflareinsights.com' if tok else '')
    csp='<meta http-equiv="Content-Security-Policy" content="default-src \'self\'; script-src %s; style-src \'self\' \'unsafe-inline\'; img-src \'self\' data: blob:; font-src \'self\'; media-src \'self\' blob:; connect-src %s; object-src \'none\'; base-uri \'self\'; form-action \'none\'">\n<meta name="referrer" content="strict-origin-when-cross-origin">\n'%(scr,con)
    s=re.sub(r'<meta http-equiv="Content-Security-Policy"[^>]*>\n?<meta name="referrer"[^>]*>\n?','',s)
    s=re.sub(r'<script defer src="https://static\.cloudflareinsights\.com[^<]*</script>\n?','',s)
    s=re.sub(r'<link rel="manifest"[^>]*>\n?|<link rel="apple-touch-icon"[^>]*>\n?','',s)
    csp+='<link rel="manifest" href="/manifest.webmanifest">\n<link rel="apple-touch-icon" href="/assets/icon-180.png">\n'
    s=s.replace('<meta charset="utf-8">\n','<meta charset="utf-8">\n'+csp,1)
    if tok: s=s.replace('</head>','<script defer src="https://static.cloudflareinsights.com/beacon.min.js" data-cf-beacon=\'{"token": "'+tok+'"}\'></script>\n</head>',1)
    return s
def apply_press(s,lang,cur):
    href='/press/'
    return re.sub(r'<a class="presslink"[^>]*>[^<]*</a>|<!--PL-->',lambda m:'<a class="presslink" href="%s">%s</a>'%(href,_e(LAB[lang][6])),s,count=1)
