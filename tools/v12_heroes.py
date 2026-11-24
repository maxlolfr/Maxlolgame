"""Étape 12 : rend les cartes « Les 8 héros » cliquables (fiche : tenues, planche de poses). Idempotent.
Usage : python3 tools/v12_heroes.py (après v10_home.py). Images : tools/extract_heroes.py."""
import os, re
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + '/'
HEROES = ['aldric', 'selena', 'orin', 'lyra', 'nyx', 'brann', 'ysmere', 'necro']
HINT = {'en': 'Tap a hero to see their outfits and poses.', 'fr': 'Touche un héros pour voir ses tenues et ses poses.', 'es': 'Toca un héroe para ver sus trajes y poses.',
        'pt': 'Toque em um herói para ver seus trajes e poses.', 'th': 'แตะฮีโร่เพื่อดูชุดและท่าทางของเขา', 'zh': '点击英雄，查看他的服装和姿势。',
        'ja': 'ヒーローをタップすると、衣装とポーズが見られます。', 'ko': '영웅을 누르면 의상과 포즈를 볼 수 있어요.', 'ru': 'Нажми на героя, чтобы увидеть его наряды и позы.',
        'id': 'Ketuk pahlawan untuk melihat kostum dan posenya.'}
PAGES = ['index.html'] + [l + '/index.html' for l in ('fr', 'es', 'pt', 'th', 'zh', 'ja', 'ko', 'ru', 'id')]
n = 0
for path in PAGES:
    p = R + path
    s = open(p, encoding='utf8').read(); o = s
    lang = path.split('/')[0] if '/' in path else 'en'
    m = re.search(r'(<div class="wrap t-heroes reveal">\s*<h3>.*?</h3>)(?:\s*<p class="t-hint">.*?</p>)?\s*<ul>(.*?)</ul>', s, re.S)
    if not m:
        print('liste héros introuvable :', path); continue
    items = re.findall(r'<li>(?:<button[^>]*>.*?<span class="hc-t"><b>(.*?)</b><span>(.*?)</span></span>.*?</button>|<b>(.*?)</b><span>(.*?)</span>)</li>', m.group(2), re.S)
    lis = []
    for i, it in enumerate(items):
        name, role = (it[0], it[1]) if it[0] else (it[2], it[3])
        lis.append('<li><button type="button" class="hc" data-i="%d" aria-haspopup="dialog"><img class="hc-face" src="/assets/heroes/face_%s.webp" alt="" width="48" height="48" loading="lazy" decoding="async">'
                   '<span class="hc-t"><b>%s</b><span>%s</span></span><i class="hc-go" aria-hidden="true">›</i></button></li>' % (i, HEROES[i], name, role))
    assert len(lis) == 8, (path, len(lis))
    new = m.group(1) + '\n      <p class="t-hint">' + HINT[lang] + '</p>\n      <ul>' + ''.join(lis) + '</ul>'
    s = s.replace(m.group(0), new, 1)
    if 'heroes.css' not in s:
        s = re.sub(r'(<link rel="stylesheet" href="[^"]*home2\.css">)', r'\1\n<link rel="stylesheet" href="%sassets/css/heroes.css">' % ('../' if '/' in path else '/'), s, count=1)
    if 'js/heroes.js' not in s:
        s = re.sub(r'(<footer)', '<script src="/assets/js/heroes.js" defer></script>\n\\1', s, count=1)
    if s != o:
        open(p, 'w', encoding='utf8').write(s); n += 1
print('accueils traités :', n)
