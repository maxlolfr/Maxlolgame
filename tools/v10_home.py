"""Étape 10 : accueil « maquette 3 » (hero titre sur image, carrousel vedette, stats avec icônes, cartes verticales).
Post-traitement idempotent des 10 accueils, qui réutilise les textes déjà présents (aucune nouvelle traduction sauf les libellés
précédent/suivant). Usage : python3 tools/v10_home.py (après build_i18n.py, v7_css.py, v8_legal.py)."""
import os, re
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + '/'
PAGES = ['index.html'] + [l + '/index.html' for l in ('fr', 'es', 'pt', 'th', 'zh', 'ja', 'ko', 'ru', 'id')]
PREVNEXT = {'en': ('Previous game', 'Next game'), 'fr': ('Jeu précédent', 'Jeu suivant'), 'es': ('Juego anterior', 'Juego siguiente'),
            'pt': ('Jogo anterior', 'Próximo jogo'), 'th': ('เกมก่อนหน้า', 'เกมถัดไป'), 'zh': ('上一个游戏', '下一个游戏'),
            'ja': ('前のゲーム', '次のゲーム'), 'ko': ('이전 게임', '다음 게임'), 'ru': ('Предыдущая игра', 'Следующая игра'),
            'id': ('Game sebelumnya', 'Game berikutnya')}
ICONS = [  # flamme, épée, couches
 '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M12 2c1 3.5-1.5 5-3 7.2C7.5 11.3 7 13 8 15c-2-.5-3.5-2.3-3.5-4.8C4.5 6.5 8 5.5 8.5 2.5 10 3.5 11 3 12 2Zm4.5 8.5c1.2 1.6 2 3.2 1.5 5.4C17.3 19 14.8 21 12 21s-5-1.8-5-4.2c0-1.4.7-2.5 1.7-3.4.2 1.2 1 2 2 2 0-2.2 1.2-3.3 2.2-4.3.7-.7 1.2-1.5 1.1-2.6 1.4.4 2 1.3 2.5 2Z"/></svg>',
 '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M14.5 4.5 20 3l-1.5 5.5L9 18l-3-3zM6 15l-3 3 3 3 3-3M5 14l5 5"/></svg>',
 '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="m12 3 9 5-9 5-9-5z"/><path d="m3 13 9 5 9-5"/><path d="m3 17.5 9 5 9-5" opacity=".6"/></svg>']
ARROW = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 12h14M13 6l6 6-6 6"/></svg>'
CH = lambda d: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="%s"/></svg>' % d


def split_lead(t):
    if re.search(r'。', t):
        i = t.index('。') + 1
        return t[:i - 1], t[i:].strip()
    m = re.search(r'\.\s+', t)
    if m:
        return t[:m.start()], t[m.end():]
    return '', t


def build(path):
    p = R + path
    if not os.path.exists(p):
        return False
    s = open(p, encoding='utf8').read()
    lang = path.split('/')[0] if '/' in path else 'en'
    pre = '../' if '/' in path else ''
    orig = s
    # 0) nettoyage d'une version précédente (idempotent) : on repart du hero d'origine conservé dans <!--h2-orig-->
    if 'class="hero hero2"' in s:
        cache = R + 'tools/h2cache/' + path.replace('/', '_')
        if not os.path.exists(cache):
            raise SystemExit('hero2 sans sauvegarde : ' + path)
        hero_old = open(cache, encoding='utf8').read()
        s = re.sub(r'<section class="hero hero2".*?</section>', lambda _m: hero_old, s, count=1, flags=re.S)
        s = re.sub(r'<section class="fcar".*?</section>\s*', '', s, count=1, flags=re.S)
        s = re.sub(r'<script data-h2>.*?</script>\s*', '', s, flags=re.S)
        s = re.sub(r'<span class="ni" aria-hidden="true">.*?</span>', '', s, flags=re.S)
        s = re.sub(r'<span class="nt">(<b data-count="\d+">\d+</b><span>.*?</span>)</span>', r'\1', s, flags=re.S)
    hm = re.search(r'<section class="hero" id="hero".*?</section>', s, re.S)
    if not hm:
        return False
    hero_old = hm.group(0)
    h1 = re.search(r'<h1 id="titre" class="sr">.*?</h1>', hero_old, re.S).group(0)
    txt = re.search(r'<div class="hero-text">\s*<p>(.*?)</p>', hero_old, re.S).group(1)
    sign = re.search(r'<p class="sign">(.*?)</p>', hero_old, re.S)
    main_btn = re.search(r'<a class="btn main" href="#jeux">(.*?)</a>', hero_old, re.S).group(1).strip()
    about = re.search(r'<a class="opt" href="#apropos">(.*?)</a>', s, re.S)
    about = about.group(1) if about else main_btn
    eyebrow, lead = split_lead(txt)
    new_hero = ('<section class="hero hero2" id="hero" aria-labelledby="titre">\n'
                '    <canvas class="fxc" id="heroFx" aria-hidden="true"></canvas>\n'
                '    <div class="fan" id="fan" aria-hidden="true"></div>\n'
                '    <div class="wrap">\n      ' + h1 + '\n'
                + ('      <p class="eyebrow">%s</p>\n' % eyebrow if eyebrow else '')
                + '      <p class="h-title" aria-hidden="true">Maxlol <span>Games</span></p>\n'
                '      <div class="hero-text"><p>' + lead + '</p>' + ('<p class="sign">%s</p>' % sign.group(1) if sign else '') + '</div>\n'
                '      <div class="cta"><a class="btn main" href="#jeux">' + main_btn + ' ' + ARROW + '</a>'
                '<a class="btn ghost" href="#apropos">' + about + '</a></div>\n'
                '    </div>\n  </section>')
    # carrousel à partir des cartes de la boutique
    store = re.search(r'<div class="store">(.*?)</div>\s*</div>\s*</section>', s, re.S)
    arts = re.findall(r'<article class="scard.*?</article>', store.group(1), re.S) if store else []
    slides = []
    for a in arts:
        a = re.sub(r'<a class="btn (?:buy|paypal)".*?</a>', '', a, flags=re.S)
        a = re.sub(r'<span class="sstar".*?</span>', '', a)
        a = a.replace('<article class="scard feat"', '<article class="fslide"').replace('<article class="scard"', '<article class="fslide"')
        a = re.sub(r'<h3 class="sname">(.*?)</h3>', r'<p class="sname">\1</p>', a, flags=re.S)
        slides.append(a)
    label = re.search(r'<h2 id="jeux-t">(.*?)</h2>', s).group(1)
    pv, nx = PREVNEXT[lang]
    fcar = ('<section class="fcar" aria-roledescription="carousel" aria-label="%s">\n    <div class="fc-wrap">\n'
            '      <button class="fc-nav fc-prev" type="button" aria-label="%s">%s</button>\n'
            '      <div class="fc-track" id="fcTrack">%s</div>\n'
            '      <button class="fc-nav fc-next" type="button" aria-label="%s">%s</button>\n    </div>\n'
            '    <div class="fc-dots" id="fcDots" aria-hidden="true">%s</div>\n  </section>\n\n  '
            % (label, pv, CH('M15 5l-7 7 7 7'), ''.join(slides), nx, CH('M9 5l7 7-7 7'), '<i></i>' * len(slides)))
    os.makedirs(R + 'tools/h2cache', exist_ok=True)
    open(R + 'tools/h2cache/' + path.replace('/', '_'), 'w', encoding='utf8').write(hero_old)
    s = s.replace(hero_old, new_hero + '\n\n  ' + fcar, 1)
    # icônes des stats
    for i, ic in enumerate(ICONS):
        s = re.sub(r'(<div class="num reveal">)(?!<span class="ni")(.*?<b data-count="%s")' % ('20', '84', '100')[i],
                   lambda m: m.group(1) + '<span class="ni" aria-hidden="true">' + ic + '</span><span class="nt">' + m.group(2), s, count=1, flags=re.S)
    s = re.sub(r'(<span class="nt"><b data-count="\d+">\d+</b><span>.*?</span>)(</div>)', r'\1</span>\2', s)
    # lien CSS
    css = '<link rel="stylesheet" href="%sassets/css/home2.css">' % ('../' if '/' in path else '/')
    if 'home2.css' not in s:
        s = re.sub(r'(<link rel="stylesheet" href="[^"]*home\.[a-f0-9]+\.css">)', r'\1\n' + css, s, count=1)
    # script carrousel
    js = ('<script data-h2>(function(){var t=document.getElementById("fcTrack");if(!t)return;var d=document.querySelectorAll("#fcDots i"),'
          'n=t.children.length,i=0,timer;function w(){return t.children[0].getBoundingClientRect().width+14}'
          'function go(k){i=(k+n)%n;t.scrollTo({left:i*w(),behavior:"smooth"})}'
          'function mark(){var k=Math.round(t.scrollLeft/w());i=Math.max(0,Math.min(n-1,k));d.forEach(function(e,j){e.className=j===i?"on":""})}'
          't.addEventListener("scroll",function(){clearTimeout(timer);timer=setTimeout(mark,60)},{passive:true});'
          'document.querySelector(".fc-prev").onclick=function(){go(i-1)};document.querySelector(".fc-next").onclick=function(){go(i+1)};'
          'd.forEach(function(e,j){e.onclick=function(){go(j)}});mark()})();</script>')
    s = re.sub(r'(<footer)', js + '\n\\1', s, count=1)
    if s != orig:
        open(p, 'w', encoding='utf8').write(s)
    return True


if __name__ == '__main__':
    ok = [pg for pg in PAGES if build(pg)]
    print('accueils traités :', len(ok), ok)
