import re, json
exec(open('/home/claude/build_en.py').read().split('# fix placeholder')[0].split("SRC=")[0])  # imports only
src=open('/home/claude/build_en.py').read()
exec(src[src.index('R=['):src.index('# fix placeholder')])
R=[r for r in R if r[0]!="Des jeux faits main, pensés d'abord pour le téléphone.</p>"]
exec(open('/home/claude/i18n_es_pt.py').read().replace('print(len(ES),len(PT))',''))
exec(open('/home/claude/i18n_th_zh.py').read())
exec(open('/home/claude/i18n_ja_ko_ru_id.py').read())
EN=[b.replace('("The Last Torch", a','(&quot;The Last Torch&quot;, a').replace('"The Last Torch"','&quot;The Last Torch&quot;') for a,b in R]
FRK=[a for a,b in R]
assert len(EN)==len(ES)==len(PT)==len(FRK)
ROOT='/home/claude/maxlolgame/'
LANGS=[('fr','',  'fr','Français','FR'),('en','en/','en','English','EN'),('es','es/','es','Español','ES'),('pt','pt/','pt-BR','Português','PT'),('th','th/','th','ไทย','TH'),('zh','zh/','zh-Hans','中文','中文'),('ja','ja/','ja','日本語','日本語'),('ko','ko/','ko','한국어','한국어'),('ru','ru/','ru','Русский','RU'),('id','id/','id','Bahasa Indonesia','ID')]
TR={'en':EN,'es':ES,'pt':PT,'th':TH,'zh':ZH,'ja':JA,'ko':KO,'ru':RU,'id':ID}
LD_DESC={
 'en':["Turn-based dungeon crawler for mobile: your torch fades with every room, 20 bosses to beat.","Mobile puzzle: place the blocks, the board rotates, cascades chain.","Auto-battle fantasy roguelite: 100 floors, 10 bosses, teams of 3 heroes."],
 'es':["Mazmorras por turnos para móvil: tu antorcha se apaga en cada sala, 20 jefes por vencer.","Puzle móvil: coloca los bloques, el tablero gira y las cascadas se encadenan.","Roguelite de fantasía con combate automático: 100 pisos, 10 jefes, equipos de 3 héroes."],
 'th':["ดันเจี้ยนแบบผลัดตาบนมือถือ: คบเพลิงอ่อนแรงลงทุกห้อง มีบอส 20 ตัวให้โค่น","เกมปริศนามือถือ: วางบล็อก กระดานหมุน แล้วคอมโบก็ต่อเนื่อง","โรกูไลต์แฟนตาซีต่อสู้อัตโนมัติ: 100 ชั้น บอส 10 ตัว ทีมฮีโร่ 3 คน"],
 'zh':["手机回合制地牢：火炬每进一个房间就变弱，等你击败 20 个首领。","手机益智：放置方块，棋盘旋转，连锁不断。","自动战斗的奇幻 Roguelite：100 层、10 个首领、三人英雄小队。"],
 'ja':["スマホ向けのターン制ダンジョン：松明は部屋ごとに弱まり、20体のボスが待ち受ける。","スマホ向けパズル：ブロックを置くと盤面が回転し、連鎖が続く。","自動戦闘のファンタジー・ローグライト：100階層、10体のボス、3人編成。"],
 'ko':["모바일 턴제 던전: 방마다 횃불이 약해지고, 20명의 보스가 기다린다.","모바일 퍼즐: 블록을 놓으면 판이 돌고 연쇄가 이어진다.","자동 전투 판타지 로그라이트: 100개 층, 보스 10명, 영웅 3명 팀."],
 'ru':["Пошаговое подземелье для телефона: факел слабеет в каждой комнате, впереди 20 боссов.","Мобильная головоломка: ставьте блоки, поле вращается, каскады идут цепочкой.","Фэнтезийный рогалик с автобоем: 100 этажей, 10 боссов, команды из 3 героев."],
 'id':["Dungeon bergiliran untuk ponsel: obormu melemah di setiap ruangan, 20 bos menanti.","Teka-teki ponsel: letakkan blok, papan berputar, kaskade berantai.","Roguelite fantasi dengan pertarungan otomatis: 100 lantai, 10 bos, tim 3 pahlawan."],
 'pt':["Masmorra por turnos para celular: sua tocha enfraquece a cada sala, 20 chefes para vencer.","Quebra-cabeça mobile: coloque os blocos, o tabuleiro gira e as cascatas se encadeiam.","Roguelite de fantasia com combate automático: 100 andares, 10 chefes, equipes de 3 heróis."]}
exec(open('/home/claude/v3_extra.py').read())
fr=open(ROOT+'index.html').read()

CSS='''.langmenu{position:relative}
.langmenu summary{list-style:none;cursor:pointer;font-weight:800;font-size:.82rem;border:1.5px solid rgba(185,174,221,.45);padding:7px 11px;border-radius:999px;color:var(--brume)}
.langmenu summary::-webkit-details-marker{display:none}
.langmenu[open] summary{color:var(--lavande);background:rgba(255,255,255,.08)}
.langmenu .lm{position:absolute;right:0;top:calc(100% + 8px);background:var(--prune);border:1px solid rgba(255,255,255,.14);border-radius:18px;padding:6px;display:grid;min-width:150px;z-index:60;box-shadow:0 14px 40px rgba(0,0,0,.45)}
.langmenu .lm a{padding:11px 14px;border-radius:12px;color:var(--lavande)}
.langmenu .lm a[aria-current]{background:rgba(255,181,71,.16);color:var(--bonbon)}
'''
JS='''document.addEventListener("click", e => { const d = document.querySelector(".langmenu"); if (d && d.open && !d.contains(e.target)) d.open = false; });
'''
# --- normalise the French source (menu, css, js) once
fr=re.sub(r'\s*<a class="lang"[^>]*>[A-Z]{2}</a>','\n<!--LM-->',fr) if '<!--LM-->' not in fr and 'langmenu"' not in fr.split('<style>')[0] else fr
if '.langmenu{' not in fr:
    fr=re.sub(r'\.nav \.lang\{[^}]*\}\n','',fr); fr=fr.replace('.nav .itch{color:#2A1300',CSS+'.nav .itch{color:#2A1300',1)
if 'd.open = false' not in fr:
    fr=fr.replace('</script>\n</body>',JS+'</script>\n</body>',1) if '</script>\n</body>' in fr else fr
assert 'd.open = false' in fr, 'js'
def menu(cur):
    pref={'fr':'../'} 
    items=[]
    for code,path,hl,name,short in LANGS:
        href=(path if cur=='fr' else '../'+path) if True else ''
        if cur!='fr' and code=='fr': href='../'
        cura=' aria-current="true"' if code==cur else ''
        items.append(f'<a href="{href}" hreflang="{hl}" lang="{hl}"{cura}>{name}</a>')
    short=[l for l in LANGS if l[0]==cur][0][4]
    return f'<details class="langmenu"><summary aria-label="Language / Langue / Idioma">{short}</summary><div class="lm">{"".join(items)}</div></details>'
def alternates():
    out=[f'<link rel="alternate" hreflang="{hl}" href="https://maxlolgames.com/{path}">' for _,path,hl,_,_ in LANGS]
    out.append('<link rel="alternate" hreflang="x-default" href="https://maxlolgames.com/">')
    return '\n'.join(out)
def finish(s,cur):
    path=[l for l in LANGS if l[0]==cur][0][1]; hl=[l for l in LANGS if l[0]==cur][0][2]
    s=re.sub(r'(<link rel="alternate" hreflang="[^"]*" href="[^"]*">\n?)+',alternates()+'\n',s,count=1)
    s=re.sub(r'<details class="langmenu">.*?</details>|<!--LM-->',lambda m:menu(cur),s,count=1,flags=re.S)
    url='https://maxlolgames.com/'+path
    s=re.sub(r'(<meta property="og:url" content=")[^"]*(")',r'\g<1>'+url+r'\2',s)
    s=re.sub(r'(<link rel="canonical" href=")[^"]*(")',r'\g<1>'+url+r'\2',s)
    m=re.search(r'<script type="application/ld\+json">(.*?)</script>',s,re.S); ld=json.loads(m.group(1)); k=0
    for n in ld['@graph']:
        if n['@type']=='WebSite': n['@id']=url+'#site'; n['url']=url; n['inLanguage']=hl
        if n['@type']=='VideoGame' and not n.get('@extra'):
            n['inLanguage']=hl; n['url']='https://maxlolgames.com/'+path+'#'+n['url'].split('#')[1]
            if cur!='fr': n['description']=LD_DESC[cur][k]
            k+=1
            if n['name']=='La Dernière Torche' and cur!='fr': n['alternateName']={'en':'The Last Torch','es':'La Última Antorcha','pt':'A Última Tocha','th':'คบเพลิงสุดท้าย','zh':'最后的火炬','ja':'最後の松明','ko':'마지막 횃불','ru':'Последний факел','id':'Obor Terakhir'}[cur]
    s=s[:m.start(1)]+json.dumps(ld,ensure_ascii=False)+s[m.end(1):]
    s=apply_games(s,cur,cur); s=apply_press(s,cur,cur); s=apply_sec(s)
    return s
fr_out=finish(fr,'fr'); open(ROOT+'index.html','w').write(fr_out)
import os
for cur,path,hl,_,_ in LANGS[1:]:
    s=fr_out
    for k,v in zip(FRK,TR[cur]):
        if v=='@@': continue
        if k not in s: print(cur,'MISSING',k[:60]); continue
        s=s.replace(k,v)
    s=s.replace('Maxlol Game, studio de jeux vidéo indépendant : La Dernière Torche, Gravity Turn, Infinite Dungeon',{'en':'Maxlol Game, indie game studio: La Dernière Torche, Gravity Turn, Infinite Dungeon','es':'Maxlol Game, estudio de juegos indie: La Dernière Torche, Gravity Turn, Infinite Dungeon','pt':'Maxlol Game, estúdio de jogos indie: La Dernière Torche, Gravity Turn, Infinite Dungeon','th':'Maxlol Game สตูดิโอเกมอินดี้: La Dernière Torche, Gravity Turn, Infinite Dungeon','zh':'Maxlol Game 独立游戏工作室：La Dernière Torche、Gravity Turn、Infinite Dungeon','ja':'Maxlol Game、インディーゲームスタジオ：La Dernière Torche、Gravity Turn、Infinite Dungeon','ko':'Maxlol Game, 인디 게임 스튜디오: La Dernière Torche, Gravity Turn, Infinite Dungeon','ru':'Maxlol Game — студия инди-игр: La Dernière Torche, Gravity Turn, Infinite Dungeon','id':'Maxlol Game, studio game indie: La Dernière Torche, Gravity Turn, Infinite Dungeon'}[cur])
    s=s.replace('content="Maxlol Game – jeux vidéo indépendants"','content="Maxlol Game – '+{'en':'indie games','es':'juegos indie','pt':'jogos indie','th':'เกมอินดี้','zh':'独立游戏','ja':'インディーゲーム','ko':'인디 게임','ru':'инди-игры','id':'game indie'}[cur]+'"')
    s=s.replace('content="fr_FR"','content="'+{'en':'en_US','es':'es_ES','pt':'pt_BR','th':'th_TH','zh':'zh_CN','ja':'ja_JP','ko':'ko_KR','ru':'ru_RU','id':'id_ID'}[cur]+'"')
    s=re.sub(r'(["\'`(])assets/',r'\1../assets/',s)
    s=re.sub(r'<html lang="fr">','<html lang="%s">'%hl,s)
    s=finish(s,cur)
    os.makedirs(ROOT+path,exist_ok=True); open(ROOT+path+'index.html','w').write(s)
sm=['<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">']
for _,path,hl,_,_ in LANGS:
    sm.append(f'  <url><loc>https://maxlolgames.com/{path}</loc><lastmod>2026-11-16</lastmod><priority>{"1.0" if not path else "0.9"}</priority>')
    for _,p2,h2,_,_ in LANGS: sm.append(f'    <xhtml:link rel="alternate" hreflang="{h2}" href="https://maxlolgames.com/{p2}"/>')
    sm.append('  </url>')
sm.append('</urlset>\n'); open(ROOT+'sitemap.xml','w').write('\n'.join(sm))
print('built')
