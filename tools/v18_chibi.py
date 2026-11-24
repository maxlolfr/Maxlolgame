# ================= V18 : Chibi Legends remplace Infinite Dungeon sur l'accueil (10 langues) + fiches FR/EN =================
# Post-traitement idempotent, à lancer APRÈS v17. Infinite Dungeon garde sa fiche (avec « momentanément indisponible »)
# mais disparaît de l'accueil, du carrousel, des cartes, des stats et des listes « autres jeux ».
# La démo jouable vit dans /chibi-legends/ (PWA, ne pas toucher) ; la fiche de présentation est /chibi-legends-game/ (EN) et /fr/chibi-legends-game/ (FR).
import re, json, os, glob, html as H
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + '/'
A, INK = '#FFB547', '#2A1300'
PLAYSVG = '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M8 5.5v13a1 1 0 0 0 1.5.86l10.5-6.5a1 1 0 0 0 0-1.72L9.5 4.64A1 1 0 0 0 8 5.5z"/></svg>'
NAME = 'Chibi Legends'
PLAYURL = '/chibi-legends/'

GENRE = {'en': 'Idle action RPG', 'fr': "RPG d'action idle", 'es': 'RPG de acción idle', 'pt': 'RPG de ação idle', 'th': 'RPG แอ็กชันไอเดิล', 'zh': '放置动作角色扮演', 'ja': '放置アクションRPG', 'ko': '방치형 액션 RPG', 'ru': 'Idle экшен-RPG', 'id': 'RPG aksi idle'}
SHORT = {
 'en': 'Build a team of chibi heroes and watch them fight on their own, world after world. Upgrade them, find loot, unleash their ultimates.',
 'fr': 'Forme une équipe de héros chibi et regarde-les combattre tout seuls, monde après monde. Améliore-les, trouve du butin, lance leurs ultimes.',
 'es': 'Forma un equipo de héroes chibi y míralos luchar solos, mundo tras mundo. Mejóralos, encuentra botín y lanza sus definitivas.',
 'pt': 'Monte uma equipe de heróis chibi e veja-os lutar sozinhos, mundo após mundo. Melhore-os, ache itens e solte os ultimates.',
 'th': 'สร้างทีมฮีโร่จิบิแล้วดูพวกเขาต่อสู้เอง โลกแล้วโลกเล่า อัปเกรด หาไอเทม และปล่อยท่าไม้ตาย',
 'zh': '组建Q版英雄队伍,看他们一个世界接一个世界自动战斗。升级、找战利品、释放大招。',
 'ja': 'ちびキャラの英雄チームを作り、ワールドごとに自動で戦う姿を見守ろう。強化、戦利品探し、必殺技の発動。',
 'ko': '치비 영웅 팀을 만들고 월드마다 알아서 싸우는 모습을 지켜보세요. 강화하고, 전리품을 찾고, 궁극기를 발동하세요.',
 'ru': 'Собери команду чиби-героев и смотри, как они сами сражаются мир за миром. Улучшай их, ищи добычу, запускай ультимейты.',
 'id': 'Bangun tim pahlawan chibi dan lihat mereka bertarung sendiri, dunia demi dunia. Tingkatkan, cari loot, dan lepas ultimate.'}
PLAY = {'en': 'Play the demo', 'fr': 'Jouer à la démo', 'es': 'Jugar a la demo', 'pt': 'Jogar a demo', 'th': 'เล่นเดโม', 'zh': '试玩', 'ja': 'デモを遊ぶ', 'ko': '데모 플레이', 'ru': 'Играть в демо', 'id': 'Mainkan demo'}
STAT = {'en': 'entries in the Chibi Legends bestiary', 'fr': 'entrées dans le bestiaire de Chibi Legends', 'es': 'entradas en el bestiario de Chibi Legends', 'pt': 'entradas no bestiário de Chibi Legends',
        'th': 'รายการในสมุดสัตว์ประหลาดของ Chibi Legends', 'zh': '条 Chibi Legends 图鉴', 'ja': '件の Chibi Legends 図鑑エントリー', 'ko': '개의 Chibi Legends 도감 항목', 'ru': 'записей в бестиарии Chibi Legends', 'id': 'entri di bestiari Chibi Legends'}
ABOUT = {'en': 'chibi heroes that fight on their own, world after world. Playable demo.', 'fr': 'des héros chibi qui combattent seuls, monde après monde. Démo jouable.', 'es': 'héroes chibi que luchan solos, mundo tras mundo. Demo jugable.',
         'pt': 'heróis chibi que lutam sozinhos, mundo após mundo. Demo jogável.', 'th': 'ฮีโร่จิบิที่ต่อสู้เอง โลกแล้วโลกเล่า เดโมเล่นได้', 'zh': 'Q版英雄自动战斗,一个世界接一个世界。可试玩。',
         'ja': 'ワールドごとに自動で戦うちびキャラの英雄。デモ版あり。', 'ko': '월드마다 알아서 싸우는 치비 영웅. 플레이 가능한 데모.', 'ru': 'чиби-герои, которые сами сражаются мир за миром. Доступно демо.', 'id': 'pahlawan chibi yang bertarung sendiri, dunia demi dunia. Demo bisa dimainkan.'}
T = {k: dict(genre=GENRE[k], short=SHORT[k], play=PLAY[k], stat=STAT[k], about='<li>⚔️ <b>Chibi Legends</b>: %s</li>' % ABOUT[k]) for k in GENRE}


# Infinite Dungeon retiré de l'accueil : « Cinq jeux, cinq univers » (ajouté avec Chibi Legends) redevient « Quatre jeux, quatre univers ».
LEAD = [('Cinq jeux, cinq univers.', 'Quatre jeux, quatre univers.'), ('Five games, five worlds.', 'Four games, four worlds.'), ('Cinco juegos, cinco mundos.', 'Cuatro juegos, cuatro mundos.'),
        ('Cinco jogos, cinco universos.', 'Quatro jogos, quatro universos.'), ('5つのゲーム、5つの世界。', '4つのゲーム、4つの世界。'), ('다섯 개의 게임, 다섯 개의 세계.', '네 개의 게임, 네 개의 세계.'),
        ('Пять игр, пять миров.', 'Четыре игры, четыре мира.'), ('Lima game, lima dunia.', 'Empat game, empat dunia.'), ('ห้าเกม ห้าโลก', 'สี่เกม สี่โลก'), ('五款游戏，五个世界。', '四款游戏，四个世界。')]


def _e(t): return H.escape(str(t), quote=True)


def gamelink(lang): return '/fr/chibi-legends-game/' if lang == 'fr' else '/chibi-legends-game/'


def home_lang(path):
    m = re.match(r'(fr|es|pt|th|zh|ja|ko|ru|id)/index\.html$', path)
    return m.group(1) if m else 'en'


def rc_card(lang):
    t = T['fr' if lang == 'fr' else 'en']
    return ('<a class="rc" href="%s"><span class="ri"><img src="/assets/cl-cover.webp" alt="%s" width="640" height="960" loading="lazy" decoding="async"></span>'
            '<span><b>%s</b><small>%s</small><em data-price="chibi-legends-rpg"></em></span></a>') % (gamelink(lang), NAME, NAME, _e(t['genre']))


# ---------- accueils ----------
def patch_home(path):
    p = R + path
    s = open(p, encoding='utf8').read()
    if 'infinite-dungeon' not in s and 'Infinite Dungeon' not in s:
        return False
    lang = home_lang(path); t = T[lang]; L = gamelink(lang); o = s

    def see_label(block):
        m = re.search(r'<a class="btn ghost" href="[^"]*infinite-dungeon/">([^<]*)</a>', block)
        return m.group(1) if m else 'See the game'

    def swap_article(cls):
        nonlocal s
        for m in list(re.finditer(r'<article class="%s".*?</article>' % cls, s, re.S)):
            b = m.group(0)
            if 'infinite-dungeon' not in b: continue
            see = see_label(b)
            b = re.sub(r'href="[^"]*infinite-dungeon/"', 'href="%s"' % L, b)
            b = b.replace('Infinite Dungeon', NAME)
            b = b.replace('assets/b/infinite-dungeon.webp', 'assets/b/chibi-legends.webp').replace('data-price="id"', 'data-price="chibi-legends-rpg"').replace('assets/id-title.webp', 'assets/cl-cover.webp')
            b = re.sub(r'<p class="sgenre">[^<]*</p>', '<p class="sgenre">%s</p>' % _e(t['genre']), b)
            b = re.sub(r'<p class="sdesc">[^<]*</p>', '<p class="sdesc">%s</p>' % _e(t['short']), b)
            b = re.sub(r'<div class="sact">.*?</div></div></article>$', lambda _m: '<div class="sact"><a class="btn main" href="%s">%s</a><a class="btn ghost" href="%s">%s</a></div></div></article>' % (PLAYURL, _e(t['play']), L, see), b, flags=re.S)
            s = s.replace(m.group(0), b)
    swap_article('fslide'); swap_article('scard')

    s = re.sub(r'<b data-count="100">100</b><span>[^<]*Infinite Dungeon[^<]*</span>', lambda _m: '<b data-count="130">130</b><span>%s</span>' % _e(t['stat']), s)

    a = s.find('<!-- ===== Infinite Dungeon')
    if a >= 0:   # la section détaillée de Chibi Legends existe déjà (tools/games/chibi-legends-rpg.json) : on retire celle d'Infinite Dungeon
        s = s[:a] + s[s.index('</section>', a) + 10:].lstrip('\n')

    def fix_ld(m):
        try: d = json.loads(m.group(2))
        except Exception: return m.group(0)
        def walk(x):
            if isinstance(x, dict):
                if x.get('name') == 'Infinite Dungeon' and x.get('@type') == 'VideoGame':
                    x['name'] = NAME; x['url'] = 'https://maxlolgames.com' + L
                    x['image'] = 'https://maxlolgames.com/assets/og/chibi-legends.jpg'; x['description'] = t['short']
                    x.pop('offers', None); x.pop('isAccessibleForFree', None); x.pop('genre', None)
                for v in x.values(): walk(v)
            elif isinstance(x, list):
                for v in x: walk(v)
        walk(d)
        return m.group(1) + json.dumps(d, ensure_ascii=False) + m.group(3)
    s = re.sub(r'(<script type="application/ld\+json">)(.*?)(</script>)', fix_ld, s, flags=re.S)

    for _a, _b in LEAD: s = s.replace(_a, _b)
    s = s.replace('assets/b/chibi-legends-rpg.webp', 'assets/b/chibi-legends.webp')
    head_end = s.find('</head>')
    s = s[:head_end].replace('Infinite Dungeon', NAME) + s[head_end:]
    s = re.sub(r'(<h1 id="titre" class="sr">[^<]*?)Infinite Dungeon', lambda _m: _m.group(1) + NAME, s)
    s = re.sub(r'<li>⚔️ <b>Infinite Dungeon</b>.*?</li>', lambda _m: t['about'], s, flags=re.S)
    if s != o:
        open(p, 'w', encoding='utf8').write(s); return True
    return False


def patch_rc(path):
    p = R + path
    s = open(p, encoding='utf8').read()
    if 'class="rc"' in s and 'infinite-dungeon/">' in s:
        lang = 'fr' if path.startswith('fr/') else 'en'
        n = re.sub(r'<a class="rc" href="[^"]*infinite-dungeon/">.*?</a>', lambda m: rc_card(lang), s, flags=re.S)
        if n != s:
            open(p, 'w', encoding='utf8').write(n); return True
    return False


FAQ = {
 'en': [("Can I try Chibi Legends now?", "Yes. The demo is playable right now in your browser, with no account."),
        ("Do I have to play every fight?", "No. Your heroes fight on their own. You upgrade them, equip gear and unleash the ultimates when you want to."),
        ("Does my team earn anything while I am away?", "Yes. Your team keeps earning gold when you are away, up to 8 hours."),
        ("How long is the game?", "There are 20 worlds and 400 levels, with a boss every 5 levels, and the climb goes on beyond. Rebirth lets you restart stronger, so there is always a new run to try."),
        ("Why replay it?", "Eight heroes make 70 possible teams, 28 duo links change how fights play out, loot goes up to Mythic, and there are 22 relics, Ember talents and 130 bestiary entries to complete."),
        ("Which devices?", "Phone and computer, in the browser."),
        ("Which languages?", "French, English, Spanish, Portuguese and Thai."),
        ("Is my progress saved?", "Yes, on your device. There is no account and no server: clearing your browser data erases the save.")],
 'fr': [("Puis-je essayer Chibi Legends tout de suite ?", "Oui. La démo se joue dès maintenant dans le navigateur, sans compte."),
        ("Faut-il jouer chaque combat ?", "Non. Tes héros combattent seuls. Tu les améliores, tu les équipes et tu lances les ultimes quand tu veux."),
        ("Mon équipe gagne-t-elle quelque chose quand je suis absent ?", "Oui. Ton équipe continue de gagner de l’or quand tu n’es pas là, jusqu’à 8 heures."),
        ("Combien de temps dure le jeu ?", "Il y a 20 mondes et 400 niveaux, avec un boss tous les 5 niveaux, et la montée continue au-delà. La renaissance permet de repartir plus fort : il y a toujours une nouvelle partie à tenter."),
        ("Pourquoi y rejouer ?", "Huit héros donnent 70 équipes possibles, 28 liens de duo changent les combats, le butin monte jusqu’au Mythique, et il reste 22 reliques, des talents de Braises et 130 fiches de bestiaire à compléter."),
        ("Sur quels appareils ?", "Téléphone et ordinateur, dans le navigateur."),
        ("Dans quelles langues ?", "Français, anglais, espagnol, portugais et thaï."),
        ("Ma progression est-elle sauvegardée ?", "Oui, sur ton appareil. Il n’y a ni compte ni serveur : vider les données du navigateur efface la sauvegarde.")],
}
P = {
 'en': dict(title="Chibi Legends – Idle Dungeon Action RPG | Maxlol Games",
   desc="Idle action RPG: build a team of chibi heroes, watch them fight world after world, upgrade them and unleash ultimates. Playable demo in your browser.",
   ogalt="Chibi Legends key art: the heroes climbing the dungeon stairs", home='Home', games='Games', genre='Idle action RPG',
   tag="Your heroes fight. You build the team.", d="Chibi Legends is an idle action RPG: you build the team, your heroes do the fighting. Recruit 8 heroes, pick 4, pair them in duos and climb 400 levels across 20 worlds, each guarded by a boss that changes tactics mid-fight. Upgrade, equip, learn skills, then be reborn stronger. Even when you are away, your team keeps earning gold.",
   chips=['Playable demo', 'No account needed'], play='Play the demo', gal='Screenshots and images',
   alts=['auto-battle in the Forgotten Crypt', 'the heroes list', 'companions', 'skills and ultimates', 'daily quests', 'bestiary', 'the daily merchant'],
   why='Reasons to play',
   cards=[('⚔️', 'Heroes that fight for you', '8 heroes, a team of 4 (70 line-ups), 3 skills and an ultimate each. You pick who fights and when the ultimates fire.'),
          ('🤝', '28 duo links', 'Put the right two heroes side by side and their ultimates charge a link gauge: when it is full, a combined attack with its own cutscene.'),
          ('🌍', '20 worlds, 400 levels', 'From the Forgotten Crypt to the Heart of the Night. A boss every 5 levels, and the climb goes on past level 400.'),
          ('👹', '20 bosses that change tactics', 'Each boss announces a big attack, then switches to a second phase at half health: bone wall, rage, summons, regeneration, a second life…'),
          ('📖', '130 monsters in the bestiary', '104 monsters, 20 bosses and 6 elites. Six elements, weaknesses, resistances and 10 behaviours (poison, vampirism, dodge, theft…). Complete entries for +1% gold each.'),
          ('🎒', 'Loot, relics and rebirth', '6 gear slots, 5 rarities up to Mythic, 22 permanent relics, Ember talents and rebirth to start over stronger.'),
          ('⏳', 'It earns while you are away', 'Your team keeps earning gold when you are not playing, up to 8 hours. Daily quests, achievements and a daily merchant bring you back.'),
          ('🎧', 'Music and voices', 'A jukebox of 16 tracks unlocked world by world, voices for the heroes, a pause menu and an audio mixer.')],
   know='Good to know', info=[('Platforms', 'Browser, mobile'), ('Languages', 'French, English, Spanish, Portuguese, Thai'), ('Saves', 'Automatic, on your device'), ('Version', '1.8.1')],
   faq='FAQ', other="Try the studio's other games", more=[('/la-derniere-torche/', 'assets/t-cover2.webp', 'La Dernière Torche', 'Turn-based dungeon crawler', 'torch', 640, 960),
    ('/wyrmstorm/', 'assets/ws-cover.webp', 'WYRMSTORM', "Dragon shoot'em up", 'wyrmstorm', 640, 960), ('/gravity-turn/', 'assets/gt-cover.webp', 'Gravity Turn', 'Rotating block puzzle', 'gt', 540, 720)]),
 'fr': dict(title="Chibi Legends – RPG d’action idle en donjon | Maxlol Games",
   desc="RPG d’action idle : forme une équipe de héros chibi, regarde-la combattre monde après monde, améliore-la et lance les ultimes. Démo jouable dans le navigateur.",
   ogalt="Illustration de Chibi Legends : les héros montent l’escalier du donjon", home='Accueil', games='Jeux', genre="RPG d'action idle",
   tag="Tes héros se battent. Tu bâtis l’équipe.", d="Chibi Legends est un RPG d’action idle : tu bâtis l’équipe, tes héros se battent. Recrute 8 héros, choisis-en 4, associe-les en duos et grimpe 400 niveaux répartis sur 20 mondes, chacun gardé par un boss qui change de tactique en plein combat. Améliore, équipe, apprends des sorts, puis renais plus fort. Même quand tu n’es pas là, ton équipe continue de gagner de l’or.",
   chips=['Démo jouable', 'Sans compte'], play='Jouer à la démo', gal='Captures et images',
   alts=['combat automatique dans la Crypte oubliée', 'la liste des héros', 'les compagnons', 'compétences et ultimes', 'les quêtes quotidiennes', 'le bestiaire', 'le marchand du jour'],
   why='Pourquoi y jouer',
   cards=[('⚔️', 'Des héros qui se battent pour toi', '8 héros, une équipe de 4 (70 compositions), 3 sorts et un ultime chacun. Tu choisis qui combat et quand les ultimes partent.'),
          ('🤝', '28 liens de duo', 'Place les bons héros côte à côte : leurs ultimes chargent une jauge de lien, et quand elle est pleine, une attaque combinée se déclenche avec sa cinématique.'),
          ('🌍', '20 mondes, 400 niveaux', 'De la Crypte oubliée au Cœur de la Nuit. Un boss tous les 5 niveaux, et la montée continue au-delà du niveau 400.'),
          ('👹', '20 boss qui changent de tactique', 'Chaque boss annonce une grande attaque, puis passe en 2e phase à mi-vie : muraille d’os, rage, invocations, régénération, seconde vie…'),
          ('📖', '130 monstres au bestiaire', '104 monstres, 20 boss et 6 élites. Six éléments, faiblesses, résistances et 10 comportements (poison, vampirisme, esquive, vol…). Chaque fiche complétée rapporte +1 % d’or.'),
          ('🎒', 'Butin, reliques et renaissance', '6 emplacements d’équipement, 5 raretés jusqu’au Mythique, 22 reliques permanentes, talents de Braises et renaissance pour repartir plus fort.'),
          ('⏳', 'Ça rapporte même absent', 'Ton équipe continue de gagner de l’or quand tu ne joues pas, jusqu’à 8 heures. Quêtes du jour, succès et marchand du jour te font revenir.'),
          ('🎧', 'Musiques et voix', 'Un jukebox de 16 musiques débloquées monde après monde, des voix pour les héros, un menu pause et un mixeur audio.')],
   know='À savoir', info=[('Plateformes', 'Navigateur, mobile'), ('Langues', 'Français, anglais, espagnol, portugais, thaï'), ('Sauvegarde', 'Automatique, sur ton appareil'), ('Version', '1.8.1')],
   faq='FAQ', other="Essaie les autres jeux du studio", more=[('/fr/la-derniere-torche/', 'assets/t-cover2.webp', 'La Dernière Torche', 'Donjon au tour par tour', 'torch', 640, 960),
    ('/fr/wyrmstorm/', 'assets/ws-cover.webp', 'WYRMSTORM', "Shoot'em up à dragons", 'wyrmstorm', 640, 960), ('/fr/gravity-turn/', 'assets/gt-cover.webp', 'Gravity Turn', 'Puzzle de blocs qui tournent', 'gt', 540, 720)]),
}
ORDER = ['combat', 'heroes', 'team', 'skills', 'quests', 'album', 'shop']


def build_gamepage(lang):
    tp = R + ('fr/wyrmstorm/index.html' if lang == 'fr' else 'wyrmstorm/index.html')
    s = open(tp, encoding='utf8').read()
    q = P[lang]; faq = FAQ[lang]; base = '/fr/' if lang == 'fr' else '/'
    page = 'https://maxlolgames.com' + gamelink(lang)
    ldm = re.search(r'(<script type="application/ld\+json">)(.*?)(</script>)', s, re.S)
    d = json.loads(ldm.group(2))
    for g in d['@graph']:
        ty = g.get('@type')
        if ty == 'VideoGame':
            g.update({'@id': page + '#game', 'name': NAME, 'description': q['desc'], 'url': page, 'image': 'https://maxlolgames.com/assets/og/chibi-legends.jpg',
                      'genre': q['genre'], 'inLanguage': ['fr', 'en']})
            g.pop('offers', None); g.pop('isAccessibleForFree', None)
        elif ty == 'FAQPage':
            g['mainEntity'] = [{"@type": "Question", "name": a, "acceptedAnswer": {"@type": "Answer", "text": b}} for a, b in faq]
        elif ty == 'BreadcrumbList':
            g['itemListElement'][-1].update({'name': NAME, 'item': page})
    s = s[:ldm.start()] + ldm.group(1) + json.dumps(d, ensure_ascii=False) + ldm.group(3) + s[ldm.end():]
    head_end = s.index('</head>'); head = s[:head_end]; rest = s[head_end + 7:]
    old_title = re.search(r'<title>(.*?)</title>', head).group(1)
    old_desc = re.search(r'<meta name="description" content="(.*?)">', head).group(1)
    old_alt = re.search(r'<meta property="og:image:alt" content="(.*?)">', head).group(1)
    head = head.replace(old_title, _e(q['title'])).replace(old_desc, _e(q['desc'])).replace(old_alt, _e(q['ogalt']))
    head = head.replace('/wyrmstorm/', '/chibi-legends-game/').replace('og/wyrmstorm.jpg', 'og/chibi-legends.jpg')
    head = re.sub(r'<link rel="stylesheet" href="/assets/css/(heroes|gh)\.css">\n?', '', head)
    head += '\n<link rel="stylesheet" href="/assets/css/chibi.css">'
    head = re.sub(r'<meta name="robots" content="[^"]*">', '<meta name="robots" content="noindex, follow">', head)
    head = re.sub(r'<link rel="canonical"[^>]*>\n?|<link rel="alternate" hreflang=[^>]*>\n?', '', head)
    s = head + '</head>' + rest
    s = s.replace('--a:#B26BFF;--a-ink:#1B0B33', '--a:%s;--a-ink:%s' % (A, INK))
    s = s.replace('/wyrmstorm/', '/chibi-legends-game/')
    play = '<a class="btn main" href="%s">%s%s</a>' % (PLAYURL, PLAYSVG, _e(q['play']))
    gal = ''.join('<button type="button" data-full="/assets/cl-%s-%s.webp"><img src="/assets/cl-%s-%s.webp" alt="%s – %s" loading="lazy" decoding="async" width="324" height="700"></button>' % (lang, n, lang, n, NAME, _e(q['alts'][i])) for i, n in enumerate(ORDER))
    cards = ''.join('<div class="fcard"><div class="fi" aria-hidden="true">%s</div><h3>%s</h3><p>%s</p></div>' % (i, _e(a), _e(b)) for i, a, b in q['cards'])
    info = ''.join('<div><dt>%s</dt><dd>%s</dd></div>' % (_e(a), _e(b)) for a, b in q['info'])
    faqh = ''.join('<details><summary>%s</summary><p>%s</p></details>' % (_e(a), _e(b)) for a, b in faq)
    more = ''.join('<a class="rc" href="%s"><span class="ri"><img src="/%s" alt="%s" width="%d" height="%d" loading="lazy" decoding="async"></span><span><b>%s</b><small>%s</small><em data-price="%s"></em></span></a>' % (u, im, _e(n), w, h, _e(n), _e(g), k) for u, im, n, g, k, w, h in q['more'])
    main = ('<main><section class="gp-hero gp2 gp-chibi-legends-game"><div class="wrap"><p class="crumb"><a href="%s">%s</a> › <a href="%s#jeux">%s</a> › %s</p>'
            '<div class="grid"><div class="gp-cover"><img src="/assets/cl-cover.webp" alt="%s" width="640" height="960" loading="lazy" decoding="async"></div>'
            '<div><p class="gp-genre">%s</p><h1>%s</h1><p class="gp-tag">%s</p><p class="gp-desc">%s</p><div class="chips">%s</div><div class="gp-cta" id="cta">%s</div></div></div></div></section>\n'
            '<section class="gb"><div class="wrap"><h2>%s</h2><div class="gal" aria-label="%s">%s</div></div></section>'
            '<section class="gb"><div class="wrap"><h2>%s</h2><div class="fgrid">%s</div></div></section>'
            '<section class="gb"><div class="wrap"><h2>%s</h2><dl class="info">%s</dl></div></section>'
            '<section class="gb faq"><div class="wrap"><h2>%s</h2>%s</div></section>'
            '<section class="gb"><div class="wrap"><h2>%s</h2><div class="more">%s</div></div></section></main>') % (
        base, q['home'], base, q['games'], NAME, NAME, _e(q['genre']), NAME, _e(q['tag']), _e(q['d']),
        ''.join('<span class="chip">%s</span>' % _e(c) for c in q['chips']), play,
        _e(q['gal']), _e(q['gal']), gal, _e(q['why']), cards, _e(q['know']), info, q['faq'], faqh, _e(q['other']), more)
    s = re.sub(r'<main>.*?</main>', lambda m: main, s, count=1, flags=re.S)
    s = re.sub(r'<div class="sbar" id="sbar">.*?</div>', lambda m: '<div class="sbar" id="sbar">%s</div>' % play, s, count=1, flags=re.S)
    s = re.sub(r'<script type="application/json"[^>]*>.*?</script>\n?', '', s, flags=re.S)
    s = re.sub(r'<script src="/assets/js/gallery-modal\.js" defer></script>\n?', '', s)
    s = re.sub(r'(<dialog id="viewer" aria-label=")[^"]*(")', lambda m: m.group(1) + NAME + m.group(2), s)
    out = R + gamelink(lang).strip('/') + '/index.html'
    os.makedirs(os.path.dirname(out), exist_ok=True)
    open(out, 'w', encoding='utf8').write(s)


def patch_misc():
    p = R + 'sitemap.xml'; s = open(p, encoding='utf8').read()
    if 'chibi-legends-game' in s:   # retire une ancienne entrée
        s = re.sub(r'  <url><loc>https://maxlolgames.com/(?:fr/)?chibi-legends-game/</loc>.*?</url>\n', '', s, flags=re.S); open(p, 'w', encoding='utf8').write(s)
    if False:
        def u(loc):
            return ('  <url><loc>https://maxlolgames.com/%s</loc><lastmod>2026-11-24</lastmod><priority>0.8</priority>\n'
                    '    <xhtml:link rel="alternate" hreflang="fr" href="https://maxlolgames.com/fr/chibi-legends-game/"/>\n    <xhtml:link rel="alternate" hreflang="en" href="https://maxlolgames.com/chibi-legends-game/"/>\n'
                    '    <xhtml:link rel="alternate" hreflang="x-default" href="https://maxlolgames.com/chibi-legends-game/"/>\n  </url>\n') % loc
        s = s.replace('</urlset>', u('chibi-legends-game/') + u('fr/chibi-legends-game/') + '</urlset>'); open(p, 'w', encoding='utf8').write(s)
    p = R + '404.html'; s = open(p, encoding='utf8').read()
    n = s.replace('<a href="/fr/infinite-dungeon/">Infinite Dungeon</a>', '<a href="/fr/chibi-legends-game/">Chibi Legends</a>').replace('<a href="/infinite-dungeon/">Infinite Dungeon</a>', '<a href="/chibi-legends-game/">Chibi Legends</a>')
    if n != s: open(p, 'w', encoding='utf8').write(n)
    p = R + 'press/index.html'; s = open(p, encoding='utf8').read(); o = s
    s = re.sub(r'<p><b>Infinite Dungeon</b>:[^<]*<a href="[^"]*">Play</a></p>', lambda m: '<p><b>Chibi Legends</b>: chibi dungeon RPG with auto-battle, free playable demo. <a href="https://maxlolgames.com/chibi-legends/">Play</a></p>', s)
    s = s.replace('../assets/id-icon.webp', '../assets/cl-icon.webp').replace('Infinite Dungeon icon', 'Chibi Legends icon')
    s = s.replace('../assets/id-title.webp', '../assets/cl-cover.webp').replace('Infinite Dungeon poster', 'Chibi Legends poster')
    if s != o: open(p, 'w', encoding='utf8').write(s)


def main():
    from PIL import Image, ImageFilter   # bannière 16:9 : bande des héros de la jaquette
    Image.open(R + 'assets/cl-cover.webp').convert('RGB').crop((0, 410, 640, 770)).resize((1600, 900), Image.LANCZOS).filter(ImageFilter.UnsharpMask(radius=2, percent=60, threshold=2)).save(R + 'assets/b/chibi-legends.webp', quality=84, method=6)
    # l'intro affiche un mur de jaquettes : la 3e (Infinite Dungeon) devient Chibi Legends
    Image.open(R + 'assets/cl-cover.webp').convert('RGB').resize((240, 360), Image.LANCZOS).save(R + 'assets/intro/i3.webp', quality=80, method=6)
    open(R + 'assets/css/chibi.css', 'w', encoding='utf8').write(
        '#chibi-legends{--a:%s;--a-ink:%s}\n#chibi-legends.bgon .bg{background-image:url(/assets/b/chibi-legends.webp)}\n'
        '#chibi-legends .bg::after{background:linear-gradient(90deg,rgba(20,8,30,.96) 0%%,rgba(20,8,30,.88) 45%%,rgba(20,8,30,.55) 100%%)}\n'
        '@media (max-width:860px){#chibi-legends .bg::after{background:linear-gradient(rgba(20,8,30,.75),rgba(20,8,30,.95) 40%%)}}\n'
        '.gp-chibi-legends-game{--gp-bg:url(/assets/b/chibi-legends.webp)}\n.gp-chibi-legends-game .gp-cover img{object-position:50%% 0}\n'
        '.gal button img{background:#120c20}\n' % (A, INK))
    n = 0
    for f in ['index.html'] + [l + '/index.html' for l in ('fr', 'es', 'pt', 'th', 'zh', 'ja', 'ko', 'ru', 'id')]:
        if os.path.exists(R + f): n += patch_home(f)
    for lang in ('en', 'fr'): build_gamepage(lang)
    r = 0
    for f in glob.glob(R + '**/index.html', recursive=True):
        rel = os.path.relpath(f, R)
        if rel.startswith(('tools/', 'chibi-', 'prototype/', 'art/', 'node_modules/')) or 'infinite-dungeon' in rel: continue
        r += patch_rc(rel)
    patch_misc()
    print('v18 : %d accueils modifiés, 2 fiches Chibi Legends, %d cartes « autres jeux »' % (n, r))


if __name__ == '__main__':
    main()
