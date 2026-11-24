"""Étape 14 : captures du cadre téléphone de l'accueil dans la langue de la page (jeu disponible en fr/en/es/pt ; autres langues -> en).
Images : assets/t-<en|es|pt>-<scène>.webp (captures du jeu en langue, 520x935). La page FR garde ses captures d'origine. Idempotent."""
import os, re
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + '/'
S = ['fight', 'map', 'world', 'doors', 'heroes', 'camp', 'shop']
W = {'en': ['a fight', 'the world map', 'a dungeon', 'choosing a door', 'your heroes', 'the camp', 'the shop'],
     'es': ['un combate', 'el mapa', 'una mazmorra', 'elegir una puerta', 'tus héroes', 'el campamento', 'la tienda'],
     'pt': ['uma luta', 'o mapa', 'uma masmorra', 'escolher uma porta', 'seus heróis', 'o acampamento', 'a loja'],
     'th': ['การต่อสู้', 'แผนที่โลก', 'ดันเจี้ยน', 'การเลือกประตู', 'เหล่าฮีโร่', 'แคมป์', 'ร้านค้า'],
     'zh': ['战斗', '世界地图', '地下城', '选择房门', '你的英雄', '营地', '商店'],
     'ja': ['戦闘', 'ワールドマップ', 'ダンジョン', '扉の選択', 'ヒーロー', 'キャンプ', 'ショップ'],
     'ko': ['전투', '월드 맵', '던전', '문 선택', '영웅', '캠프', '상점'],
     'ru': ['бой', 'карта мира', 'подземелье', 'выбор двери', 'ваши герои', 'лагерь', 'магазин'],
     'id': ['pertarungan', 'peta dunia', 'dungeon', 'memilih pintu', 'pahlawanmu', 'kemah', 'toko']}
SRC = {'en': 'en', 'es': 'es', 'pt': 'pt'}
n = 0
for lang in ['en', 'es', 'pt', 'th', 'zh', 'ja', 'ko', 'ru', 'id']:
    path = 'index.html' if lang == 'en' else lang + '/index.html'
    p = R + path; s = open(p, encoding='utf8').read()
    m = re.search(r'(<div class="phone-in" id="trailer">)(.*?)(</div>)', s, re.S)
    first = re.search(r'alt="([^"]*)"', m.group(2)).group(1)
    pre = re.match(r'(.*?:)\s*', first) if ':' in first else None
    prefix = (pre.group(1) if pre else 'La Dernière Torche :') + ' '
    g = SRC.get(lang, 'en'); imgs = []
    for i, sc in enumerate(S):
        alt = prefix + W[lang][i]; u = 'assets/t-%s-%s.webp' % (g, sc)
        if '/' in path: u = '../' + u
        if i == 0: imgs.append('<img loading="lazy" decoding="async" src="%s" alt="%s" class="on" width="520" height="935">' % (u, alt))
        else: imgs.append('<img data-src="%s" decoding="async" alt="%s" width="520" height="935" loading="lazy">' % (u, alt))
    new = m.group(1) + '\n          ' + '\n          '.join(imgs) + '\n        ' + m.group(3)
    if new != m.group(0): s = s.replace(m.group(0), new, 1); open(p, 'w', encoding='utf8').write(s); n += 1
print('accueils traités :', n)
