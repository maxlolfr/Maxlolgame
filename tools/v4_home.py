# ================= V4 : accueil boutique (hero 4 jeux, catalogue, nouveautés, menu mobile) =================
# Appliqué à la page FINALE de chaque langue (après traduction). Utilise LAB, LANGS (v3_extra / build_i18n).
_O=('fr','en','es','pt','th','zh','ja','ko','ru','id')
def _d(*v): return dict(zip(_O,v))
V4_NEWS_L=_d('Nouveautés','News','Novedades','Novidades','ข่าวสาร','最新动态','お知らせ','새 소식','Новости','Berita')
V4_MENU_L=_d('Menu','Menu','Menú','Menu','เมนู','菜单','メニュー','메뉴','Меню','Menu')
V4_SEE_L=_d('Voir le jeu','See the game','Ver el juego','Ver o jogo','ดูเกม','查看游戏','ゲームを見る','게임 보기','Подробнее','Lihat game')
V4_DESC_ADD=_d(" Nouveau : WYRMSTORM, un shoot'em up à dragons gratuit."," New: WYRMSTORM, a free dragon shoot'em up."," Novedad: WYRMSTORM, un shoot'em up de dragones gratis."," Novo: WYRMSTORM, um shoot'em up de dragões grátis."," ใหม่: WYRMSTORM เกมยิงมังกรเล่นฟรี"," 新作：WYRMSTORM，免费的龙主题射击游戏。"," 新作：WYRMSTORM、無料のドラゴン・シューティング。"," 신작: WYRMSTORM, 무료 드래곤 슈팅 게임."," Новинка: WYRMSTORM — бесплатный шутер с драконами."," Baru: WYRMSTORM, shoot'em up naga gratis.")
V4_ABOUT_H=_d('Qui fait ces jeux ?','Who makes these games?','¿Quién hace estos juegos?','Quem faz estes jogos?','ใครคือผู้สร้างเกมเหล่านี้?','谁在制作这些游戏？','このゲームを作っているのは？','이 게임은 누가 만들까요?','Кто делает эти игры?','Siapa yang membuat game ini?')
V4_ABOUT_LI=_d(
 "🐉 <b>WYRMSTORM</b> : pilote ton héros, lâche tes dragons et traverse le ciel, boss après boss.",
 "🐉 <b>WYRMSTORM</b>: pilot your hero, unleash your dragons and cross the sky, boss after boss.",
 "🐉 <b>WYRMSTORM</b>: pilota a tu héroe, suelta a tus dragones y cruza el cielo, jefe tras jefe.",
 "🐉 <b>WYRMSTORM</b>: pilote seu herói, solte seus dragões e cruze o céu, chefe após chefe.",
 "🐉 <b>WYRMSTORM</b>: บังคับฮีโร่ ปล่อยมังกร แล้วบินข้ามท้องฟ้า สู้บอสทีละตัว",
 "🐉 <b>WYRMSTORM</b>：驾驶你的英雄，放出巨龙，穿越天空，一个接一个击败首领。",
 "🐉 <b>WYRMSTORM</b>：英雄を操り、ドラゴンを解き放って空を駆け抜け、ボスを次々に倒そう。",
 "🐉 <b>WYRMSTORM</b>: 영웅을 조종하고 드래곤을 풀어 하늘을 가로지르며 보스를 차례로 쓰러뜨리세요.",
 "🐉 <b>WYRMSTORM</b>: управляй героем, выпускай драконов и пересекай небо, босс за боссом.",
 "🐉 <b>WYRMSTORM</b>: pandu pahlawanmu, lepaskan naga-nagamu dan jelajahi langit, bos demi bos.")
# (date, jeu, ancre, titres) : uniquement des mises à jour réelles (historique du dépôt)
V4_NEWS=[
 ('2026-11-24','WYRMSTORM','wyrmstorm',_d("WYRMSTORM arrive : un shoot'em up à dragons, gratuit","WYRMSTORM is here: a free dragon shoot'em up","Llega WYRMSTORM: un shoot'em up de dragones gratis","Chegou WYRMSTORM: um shoot'em up de dragões grátis","WYRMSTORM มาแล้ว: เกมยิงมังกรเล่นฟรี","WYRMSTORM 上线：免费的龙主题射击游戏","WYRMSTORM 登場：無料のドラゴン・シューティング","WYRMSTORM 공개: 무료 드래곤 슈팅 게임","Вышел WYRMSTORM — бесплатный шутер с драконами","WYRMSTORM hadir: shoot'em up naga gratis")),
 ('2026-11-24','La Dernière Torche','la-derniere-torche',_d("Achat possible via PayPal","You can now buy it with PayPal","Ya puedes comprarla con PayPal","Agora dá para comprar com PayPal","ซื้อผ่าน PayPal ได้แล้ว","现在可通过 PayPal 购买","PayPal で購入できるようになりました","이제 PayPal로 구매할 수 있어요","Теперь можно купить через PayPal","Kini bisa dibeli lewat PayPal")),
 ('2026-11-24','Maxlol Games','hero',_d("Nouvelle intro du studio","New studio intro","Nueva intro del estudio","Nova abertura do estúdio","อินโทรใหม่ของสตูดิโอ","全新的工作室开场动画","スタジオの新しいイントロ","새로운 스튜디오 인트로","Новая заставка студии","Intro studio yang baru")),
 ('2026-11-23','La Dernière Torche','la-derniere-torche',_d("8 héros, 28 costumes et des voix","8 heroes, 28 costumes and voices","8 héroes, 28 trajes y voces","8 heróis, 28 trajes e vozes","ฮีโร่ 8 คน ชุด 28 แบบ และเสียงพากย์","8 位英雄、28 套服装和语音","8人の英雄、28種のコスチューム、ボイス","영웅 8명, 코스튬 28종, 음성","8 героев, 28 костюмов и озвучка","8 pahlawan, 28 kostum, dan suara")),
 ('2026-11-18','Gravity Turn','gravity-turn',_d("Passage en version 1.4","Now at version 1.4","Pasa a la versión 1.4","Chega à versão 1.4","อัปเดตเป็นเวอร์ชัน 1.4","更新至 1.4 版","バージョン1.4に","1.4 버전 업데이트","Обновление до версии 1.4","Naik ke versi 1.4")),
]
V4_CSS='''
/* ===== V4 : accueil boutique ===== */
.card{width:44%}
.card.c1{left:0;top:8%;--base:rotate(-12deg)}
.card.c2{left:19%;top:0;--base:rotate(-3deg) translateY(-3%);z-index:3}
.card.c4{left:38%;top:5%;--base:rotate(6deg);animation-delay:1.7s;z-index:4}
.card.c3{left:56%;top:12%;--base:rotate(14deg);animation-delay:1.85s;z-index:2}
.card.c4.dealt{animation-delay:-1s}
@media (max-width:860px){.card.c2{left:19%}.card.c4{left:38%}.card.c3{left:56%}}
.store{display:grid;grid-template-columns:repeat(2,1fr);gap:18px;margin-top:28px}
@media (max-width:900px){.store{grid-template-columns:1fr}}
.scard{position:relative;display:flex;background:var(--prune);border-radius:22px;overflow:hidden;box-shadow:0 14px 30px rgba(5,2,20,.45),inset 0 0 0 1px rgba(255,255,255,.08);transition:transform .2s cubic-bezier(.3,1.4,.5,1)}
.scard:hover{transform:translateY(-4px)}
.scard.feat{box-shadow:0 14px 34px rgba(5,2,20,.5),inset 0 0 0 2px var(--a,#FFB547)}
.simg{position:relative;flex:0 0 38%;aspect-ratio:3/4;overflow:hidden;background:#120C2B;display:block}
.simg>img{width:100%;height:100%;object-fit:cover;object-position:50% 10%}
.simg .gtc{position:absolute;inset:0}
.sprice{position:absolute;left:10px;top:10px;padding:4px 11px;border-radius:999px;background:rgba(18,12,43,.88);color:var(--bonbon);font-weight:800;font-size:.82rem}
.sstar{position:absolute;right:8px;top:8px;width:26px;height:26px;border-radius:50%;display:grid;place-items:center;background:var(--a,#FFB547);color:#1B0B33;font-size:.85rem;font-weight:900}
.sbody{padding:16px 16px 16px 18px;display:flex;flex-direction:column;gap:6px;min-width:0;flex:1}
.sgenre{font-size:.76rem;font-weight:800;letter-spacing:.05em;text-transform:uppercase;color:var(--a,#B9AEDD)}
.sname{font:400 clamp(1.25rem,3vw,1.6rem)/1.1 var(--display);margin:0}
.sname a{text-decoration:none;color:var(--lavande)}
.sdesc{font-size:.92rem;line-height:1.45;color:var(--brume);margin:0;flex:1}
.sact{display:flex;flex-wrap:wrap;gap:8px;margin-top:8px}
.sact .btn{padding:9px 14px;font-size:.88rem}
@media (max-width:420px){.simg{flex-basis:36%}.sbody{padding:12px 12px 12px 14px}.sdesc{font-size:.86rem}}
.news{padding:0 0 44px}
.news h2{font-size:clamp(1.8rem,4vw,2.4rem)}
.nl{list-style:none;margin:18px 0 0;padding:0;display:grid;gap:10px}
.nl li{display:flex;gap:14px;align-items:baseline;background:var(--prune);border-radius:16px;padding:12px 16px;box-shadow:inset 0 0 0 1px rgba(255,255,255,.07)}
.nl time{flex:0 0 auto;min-width:7.5em;font-weight:800;font-size:.82rem;color:var(--brume)}
.nl a{text-decoration:none;color:var(--lavande);font-weight:700;line-height:1.35}
.ntag{display:inline-block;font-size:.72rem;font-weight:800;padding:2px 8px;border-radius:999px;background:rgba(255,181,71,.18);color:var(--bonbon);margin-right:8px}
@media (max-width:520px){.nl li{flex-direction:column;gap:4px}}
.mmenu{display:none;position:relative}
.mmenu summary{list-style:none;cursor:pointer;display:grid;place-items:center;width:40px;height:40px;border-radius:50%;border:1.5px solid rgba(185,174,221,.45);color:var(--brume)}
.mmenu summary::-webkit-details-marker{display:none}
.mmenu[open] summary{color:var(--lavande);background:rgba(255,255,255,.08)}
.mmenu svg{width:20px;height:20px}
.mmenu .mm{position:absolute;right:0;top:calc(100% + 8px);background:var(--prune);border:1px solid rgba(255,255,255,.14);border-radius:18px;padding:6px;display:grid;min-width:190px;z-index:60;box-shadow:0 14px 40px rgba(0,0,0,.45)}
.mmenu .mm a{padding:12px 14px;border-radius:12px;color:var(--lavande);font-size:1rem}
@media (max-width:600px){.mmenu{display:block}.nav .itch{display:none}.nav>.snd{margin-left:0}}
'''
V4_JS='''<script>
document.querySelectorAll(".nl time").forEach(t=>{try{t.textContent=new Date(t.dateTime+"T12:00:00").toLocaleDateString(document.documentElement.lang||undefined,{day:"numeric",month:"short",year:"numeric"})}catch(e){}});
document.addEventListener("click",e=>{document.querySelectorAll(".mmenu[open]").forEach(d=>{if(!d.contains(e.target)||e.target.closest(".mm a"))d.open=false});});
document.querySelectorAll(".mmenu,.langmenu").forEach(d=>d.addEventListener("toggle",()=>{if(d.open)document.querySelectorAll(".mmenu[open],.langmenu[open]").forEach(o=>{if(o!==d)o.open=false})}));
</script>
'''
def _v4_short(t):
    t=re.sub(r'<[^>]+>','',t).strip(); out=''
    for x in re.split(r'(?<=[.!?。！？])\s*',t):
        if not x: continue
        if out and len(out+' '+x)>140: break
        out=(out+' '+x).strip()
        if len(out)>=70: break
    return out if len(out)<=170 else out[:167].rstrip()+'…'
def _v4_info(s,sid):
    m=re.search(r'<section class="game[^"]*" id="%s".*?</section>'%sid,s,re.S)
    sec=m.group(0) if m else ''
    g=re.search(r'<p class="genre[^"]*">\s*([^<]*?)\s*<span class="tagp"',sec)
    p=re.search(r'<p class="pitch[^"]*">(.*?)</p>',sec,re.S)
    return (g.group(1) if g else ''), _v4_short(p.group(1) if p else '')
def home_patch(s,cur,P):
    L=LAB[cur]; i=_O.index(cur)
    # --- SEO : WYRMSTORM dans le titre, le h1 et les descriptions
    k=s.index('<style>'); head,rest=s[:k],s[k:]
    add=lambda m: m.group(1)+m.group(2)+m.group(3)+'WYRMSTORM' if 'WYRMSTORM' not in m.group(0) else m.group(0)
    head=re.sub(r'(Gravity Turn)([,、，] ?)(Infinite Dungeon)(?![,、，] ?WYRMSTORM)',lambda m:m.group(1)+m.group(2)+m.group(3)+m.group(2)+'WYRMSTORM',head)
    if 'WYRMSTORM' not in re.search(r'<title>(.*?)</title>',head).group(1): head=re.sub(r'</title>',' · WYRMSTORM</title>',head,count=1)
    head=re.sub(r'(<meta (?:name="description"|property="og:description") content=")([^"]*)(")',lambda m:m.group(1)+m.group(2)+V4_DESC_ADD[cur]+m.group(3),head)
    rest=re.sub(r'(<h1 id="titre" class="sr">[^<]*?)(Gravity Turn)([,、，] ?)(Infinite Dungeon)(</h1>)',lambda m:m.group(1)+m.group(2)+m.group(3)+m.group(4)+m.group(3)+'WYRMSTORM'+m.group(5),rest)
    rest=rest.replace('</style>',V4_CSS+'</style>',1)
    s=head+rest
    # --- hero : 4e carte (WYRMSTORM) et bouton principal vers tous les jeux
    s=re.sub(r'(<a class="card c3".*?</a>)',lambda m:m.group(1)+'\n      <a class="card c4" href="#wyrmstorm" tabindex="-1"><img src="%sassets/ws-cover.webp" alt="" width="640" height="960"><span class="shine"></span></a>'%P,s,count=1,flags=re.S)
    s=re.sub(r'<a class="btn main" href="#la-derniere-torche">[^<]*</a>\s*<a class="btn ghost" href="#jeux">([^<]*)</a>',lambda m:'<a class="btn main" href="#jeux">%s</a>'%m.group(1),s,count=1)
    # --- à propos : titre traduit + WYRMSTORM
    s=re.sub(r'<h2 id="ap-t">[^<]*</h2>','<h2 id="ap-t">%s</h2>'%V4_ABOUT_H[cur],s,count=1)
    s=re.sub(r'(<ul class="ap-games">.*?)(</ul>)',lambda m:m.group(1)+'  <li>%s</li>\n        '%V4_ABOUT_LI[cur]+m.group(2),s,count=1,flags=re.S)
    # --- menu : "Nouveau" devient "Nouveautés", menu mobile compact
    g=re.search(r'<a class="opt" href="#jeux">([^<]*)</a>',s); a=re.search(r'<a class="opt" href="#apropos">([^<]*)</a>',s)
    s=re.sub(r'<a class="opt" href="#la-derniere-torche">[^<]*</a>','<a class="opt" href="#nouveautes">%s</a>'%V4_NEWS_L[cur],s,count=1)
    burger='<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" aria-hidden="true"><path d="M4 7h16M4 12h16M4 17h16"/></svg>'
    mm='<details class="mmenu"><summary aria-label="%s">%s</summary><div class="mm"><a href="#jeux">%s</a><a href="#nouveautes">%s</a><a href="#apropos">%s</a><a href="/press/">%s</a><a data-link="itch" href="#suivre" target="_blank" rel="noopener">itch.io</a></div></details>\n'%(V4_MENU_L[cur],burger,g.group(1) if g else 'Games',V4_NEWS_L[cur],a.group(1) if a else 'About',_e(L[6]))
    s=s.replace('<details class="langmenu">',mm+'<details class="langmenu">',1)
    # --- catalogue : 4 jeux (genre, courte description, prix ou gratuit, actions)
    cards=[('la-derniere-torche','torch','La Dernière Torche','assets/t-cover2.webp',True),('wyrmstorm','wyrmstorm','WYRMSTORM','assets/ws-cover.webp',True),('gravity-turn','gt','Gravity Turn',None,False),('infinite-dungeon','id','Infinite Dungeon','assets/id-title.webp',False)]
    out=[]
    gpf=lambda sid:('/fr/' if cur=='fr' else '/')+sid+'/'
    for sid,key,name,img,feat in cards:
        genre,desc=_v4_info(s,sid)
        if img: vis='<img src="%s%s" alt="%s" width="640" height="960" loading="lazy" decoding="async">'%(P,img,_e(name))
        else: vis='<span class="gtc"><img src="%sassets/gt-jelly.webp" alt="" width="256" height="256" loading="lazy"><img class="gtl" src="%sassets/gt-logo.webp" alt="" width="720" height="241" loading="lazy"></span>'%(P,P)
        acc={'torch':'#FF9F2E','wyrmstorm':'#B26BFF','gt':'#4FA8FF','id':'#FFB547'}[key]
        out.append('<article class="scard%s" style="--a:%s"><a class="simg" href="GP%s" aria-label="%s">%s<span class="sprice" data-price="%s"></span>%s</a><div class="sbody"><p class="sgenre">%s</p><h3 class="sname"><a href="GP%s">%s</a></h3><p class="sdesc">%s</p><div class="sact"><a class="btn main" data-link="%s-play" href="#" target="_blank" rel="noopener">%s</a><a class="btn buy" data-buy="%s" href="#" target="_blank" rel="noopener">%s <span class="price"></span></a><a class="btn paypal" data-paypal="%s" href="#" target="_blank" rel="noopener">PayPal <span class="price"></span></a><a class="btn ghost" href="GP%s">%s</a></div></div></article>'%(' feat' if feat else '',acc,sid,_e(name),vis,key,'<span class="sstar" aria-hidden="true">★</span>' if feat else '',genre,sid,name,desc,key,_e(L[0].format(n=name)),key,_e(L[1]),key,sid,_e(V4_SEE_L[cur])))
    out=[re.sub(r'href="GP([a-z-]+)"',lambda m:'href="%s"'%gpf(m.group(1)),x) for x in out]
    s,n=re.subn(r'<div class="covers">.*?<!--/COVERS-->\s*</div>',lambda m:'<div class="store">'+''.join(out)+'</div>',s,count=1,flags=re.S); assert n==1,'covers'
    # --- nouveautés (vraies mises à jour)
    items=''.join('<li><time datetime="%s">%s</time><a href="#%s"><span class="ntag">%s</span>%s</a></li>'%(d,d,anc,_e(tag),_e(t[cur])) for d,tag,anc,t in V4_NEWS)
    news='<section class="news" id="nouveautes" aria-labelledby="news-t"><div class="wrap"><h2 id="news-t">%s</h2><ol class="nl">%s</ol></div></section>\n'%(V4_NEWS_L[cur],items)
    s,n=re.subn(r'(<section class="shelf" id="jeux".*?</section>\n)',lambda m:m.group(1)+'\n  '+news,s,count=1,flags=re.S); assert n==1,'shelf'
    s=s.replace('</body>',V4_JS+'</body>',1)
    return s
