import re, json
SRC='/home/claude/maxlolgame/index.html'; OUT='/home/claude/maxlolgame/en/index.html'
s=open(SRC).read()
R=[
# head
('<html lang="fr">','<html lang="en">'),
('<title>Maxlol Games – Jeux indépendants : La Dernière Torche, Gravity Turn, Infinite Dungeon</title>','<title>Maxlol Games – Indie games: La Dernière Torche, Gravity Turn, Infinite Dungeon</title>'),
("Maxlol Games, studio indépendant de jeux mobiles : La Dernière Torche (donjon au tour par tour, 20 boss), Gravity Turn (puzzle de blocs qui tournent) et Infinite Dungeon (roguelite). À jouer dans le navigateur et sur itch.io.","Maxlol Games, an indie game studio: La Dernière Torche (\"The Last Torch\", a dungeon crawler about a fading torch), Gravity Turn (rotating block puzzle) and Infinite Dungeon (roguelite). Play on mobile, in your browser and on itch.io."),
('content="Maxlol Games – jeux vidéo indépendants"','content="Maxlol Games – indie games"'),
('content="fr_FR"','content="en_US"'),
("La Dernière Torche, Gravity Turn, Infinite Dungeon — Studio indépendant de jeux mobiles : donjons, boss et puzzles, jouables tout de suite dans le navigateur.","La Dernière Torche, Gravity Turn, Infinite Dungeon — Independent mobile game studio: dungeons, bosses and puzzles, playable instantly in your browser."),
("Des jeux faits main, pensés d'abord pour le téléphone.</p>","Handmade games, designed for the phone first."),  # placeholder; fixed below
('<meta property="og:description" content="Studio indépendant de jeux mobiles : donjons, boss et puzzles, jouables tout de suite dans le navigateur.">','<meta property="og:description" content="Independent mobile game studio: dungeons, bosses and puzzles, playable instantly in your browser.">'),
('<meta property="og:url" content="https://maxlolgames.com/">','<meta property="og:url" content="https://maxlolgames.com/en/">'),
('<link rel="canonical" href="https://maxlolgames.com/">','<link rel="canonical" href="https://maxlolgames.com/en/">'),
('<link rel="alternate" hreflang="fr" href="https://maxlolgames.com/">','<link rel="alternate" hreflang="fr" href="https://maxlolgames.com/">\n<link rel="alternate" hreflang="en" href="https://maxlolgames.com/en/">\n<link rel="alternate" hreflang="x-default" href="https://maxlolgames.com/">'),
# intro / nav
('maxlolfr présente','maxlolfr presents'),('Touche pour passer','Tap to skip'),
('aria-label="Maxlol Games, retour en haut"','aria-label="Maxlol Games, back to top"'),
('aria-label="Menu"','aria-label="Menu"'),
('<a class="opt" href="#jeux">Jeux</a>','<a class="opt" href="#jeux">Games</a>'),
('>Nouveau</a>','>New</a>'),('>À propos</a>','>About</a>'),
('aria-label="Activer la musique"','aria-label="Turn music on"'),
# hero
("Studio indépendant de jeux mobiles. Des donjons à conquérir, des boss à abattre, des puzzles qui font tourner la tête. Jouable tout de suite dans le navigateur, sans téléchargement.","Independent mobile game studio. Dungeons to conquer, bosses to slay, puzzles that turn your head. Play instantly in your browser, no download needed."),
('Créés par maxlolfr','Made by maxlolfr'),
('Découvrir La Dernière Torche','Discover La Dernière Torche'),('Tous les jeux','All games'),('Ma page itch.io','My itch.io page'),
('Touche une lettre pour la faire rebondir.','Tap a letter to make it bounce.'),
('Les jeux en chiffres','The games in numbers'),
('boss dans La Dernière Torche','bosses in La Dernière Torche'),('niveaux dans Gravity Turn','levels in Gravity Turn'),('étages dans Infinite Dungeon','floors in Infinite Dungeon'),
('<h2 id="jeux-t">Les jeux</h2>','<h2 id="jeux-t">The games</h2>'),
("Trois jeux, trois univers. Tous se jouent dans le navigateur, sur téléphone comme sur ordinateur.","Three games, three worlds. All of them play in your browser, on phone or computer."),
('Nouveau, essai gratuit','New, free trial'),('Puzzle de blocs qui tourne','Rotating block puzzle'),('Roguelite fantasy</span></a>','Fantasy roguelite</span></a>'),
# torche
('alt="La Dernière Torche : un héros brandit sa torche dans le noir"','alt="La Dernière Torche: a hero raises a torch in the dark"'),
('Déplace ton doigt ou ta souris : la torche éclaire le donjon.','Move your finger or mouse: the torch lights the dungeon.'),
('Donjon au tour par tour','Turn-based dungeon crawler'),
('Explore. Remplis ton sac. Ressors avant le noir.','Explore. Fill your bag. Get out before the dark.'),
("Trois héros. Une seule torche, qui perd de sa force à chaque salle. Plus il fait noir, plus les monstres frappent fort, et plus le butin grossit. Sors à temps avec ton sac : si tu tombes, tu en perds 80 %.","Three heroes. One torch, which weakens with every room. The darker it gets, the harder monsters hit and the bigger the loot grows. Get out in time with your bag: if you fall, you lose 80% of it."),
('aria-label="Les quatre paliers de la torche"','aria-label="The four torch levels"'),
('<b>Clarté</b><span>Tout est visible</span>','<b>Clarity</b><span>Everything is visible</span>'),
('<b>Pénombre</b><span>Monstres plus forts</span>','<b>Twilight</b><span>Stronger monsters</span>'),
('<b>Ténèbres</b><span>Leurs intentions se cachent</span>','<b>Darkness</b><span>Their intentions are hidden</span>'),
('<b>Noir total</b><span>Embuscades, butin ×3</span>','<b>Pitch black</b><span>Ambushes, loot ×3</span>'),
("Combats au tour par tour sur deux rangs, avec Garde, faiblesses élémentaires et ultimes en plein écran","Turn-based combat on two rows, with Guard, elemental weaknesses and full-screen ultimates"),
("28 Liens : deux héros à 100 % d'ultime unissent leurs pouvoirs","28 Links: two heroes at 100% ultimate join their powers"),
("Des boss qui changent de phase à mi-vie : enragés, doubles actions, invocations","Bosses that change phase at half health: enraged, double actions, summons"),
("Combat, élite, coffre, marchand, repos, événements, et le Trésor noir caché dans l'obscurité","Fights, elites, chests, merchants, rest stops, events, and the Black Treasure hidden in the dark"),
("Ascensions, Profondeurs infinies, défi du jour et défi de la semaine","Ascensions, Infinite Depths, daily challenge and weekly challenge"),
('<dt>Essai</dt><dd>Gratuit, dans le navigateur</dd>','<dt>Trial</dt><dd>Free, in your browser</dd>'),
('<dt>Plateformes</dt><dd>Navigateur, mobile et ordinateur</dd>','<dt>Platforms</dt><dd>Browser, mobile and computer</dd>'),
('<dt>Jeu complet</dt>','<dt>Full game</dt>'),
('</svg>Acheter <span class="price">','</svg>Buy <span class="price">'),
('Essayer gratuitement','Try it for free'),
('aria-label="Captures de La Dernière Torche qui défilent"','aria-label="Scrolling screenshots of La Dernière Torche"'),
("Capture d'écran de La Dernière Torche : le désert","La Dernière Torche screenshot: the desert"),
("Capture d'écran de La Dernière Torche : le dragon","La Dernière Torche screenshot: the dragon"),
("Capture d'écran de La Dernière Torche : le boss ultime","La Dernière Torche screenshot: the ultimate boss"),
("Capture d'écran de La Dernière Torche : l'horloge","La Dernière Torche screenshot: the clock"),
("Capture d'écran de La Dernière Torche : la grotte","La Dernière Torche screenshot: the cave"),
("Capture d'écran de La Dernière Torche : la carte, suite","La Dernière Torche screenshot: the map"),
("Capture d'écran de La Dernière Torche : le journal","La Dernière Torche screenshot: the journal"),
('<span>mondes et 20 boss</span>','<span>worlds and 20 bosses</span>'),('<span>héros à recruter</span>','<span>heroes to recruit</span>'),
('<span>monstres dans le journal</span>','<span>monsters in the journal</span>'),('<span>niveaux par héros</span>','<span>levels per hero</span>'),
('aria-label="Images de La Dernière Torche"','aria-label="La Dernière Torche images"'),
('alt="Le nécromancien et son armée de squelettes"','alt="The necromancer and his skeleton army"'),
('alt="Combat contre le dragon de la forteresse"','alt="Fighting the fortress dragon"'),
('alt="Attaque ultime d\'Ysmère"','alt="Ysmère\'s ultimate attack"'),
('alt="Le temple du Désert des Rois"','alt="The temple of the Desert of Kings"'),
('alt="Combat dans le Désert des Rois"','alt="Fighting in the Desert of Kings"'),
('alt="Combat dans l\'Horlogerie"','alt="Fighting in the Clockworks"'),
('alt="Combat dans les Profondeurs"','alt="Fighting in the Depths"'),
('alt="Carte des donjons"','alt="The dungeon map"'),('alt="Journal des monstres"','alt="The monster journal"'),
('<h3>Les 8 héros</h3>','<h3>The 8 heroes</h3>'),
('<span>Chevalier</span>','<span>Knight</span>'),('<span>Paladine</span>','<span>Paladin</span>'),('<span>Archère</span>','<span>Archer</span>'),
('<span>Voleuse</span>','<span>Thief</span>'),('<span>Artificier nain</span>','<span>Dwarf engineer</span>'),('<span>Chamane</span>','<span>Shaman</span>'),('<span>Nécromancien</span>','<span>Necromancer</span>'),
('aria-label="Les 20 boss de La Dernière Torche"','aria-label="The 20 bosses of La Dernière Torche"'),
# gt
('Puzzle mobile <span','Mobile puzzle <span'),
("Pose des blocs gelée sur une grille de 8 sur 8. Toutes les trois pièces, le plateau tourne d'un quart de tour et tout retombe. Une ligne qui en fait tomber une autre, c'est une cascade.","Place jelly blocks on an 8 by 8 grid. Every three pieces, the board turns a quarter turn and everything falls. A line that makes another one fall is a cascade."),
("84 niveaux répartis en 7 mondes, avec pierres, glace, gemmes, bombes et éclairs","84 levels across 7 worlds, with stones, ice, gems, bombs and lightning"),
("Un défi du jour et un défi de la semaine, les mêmes pour tout le monde","A daily and a weekly challenge, the same for everyone"),
("Modes infini et zen pour jouer sans objectif","Endless and zen modes to play without a goal"),
('<dt>Version</dt><dd>1.3</dd>','<dt>Version</dt><dd>1.3</dd>'),
('<dd>Navigateur, iPhone bientôt</dd>','<dd>Browser, iPhone soon</dd>'),
('<dt>Langues</dt><dd>Français, anglais</dd>','<dt>Languages</dt><dd>French, English</dd>'),
('Jouer à Gravity Turn','Play Gravity Turn'),('Voir sur itch.io','See on itch.io'),
# id
("Affiche d'Infinite Dungeon : les cinq héros devant la tour du donjon","Infinite Dungeon poster: the five heroes in front of the dungeon tower"),
('Roguelite fantasy <span','Fantasy roguelite <span'),
("Monte une équipe de trois héros et descends le plus loin possible. Les combats se jouent seuls : ton rôle, c'est de choisir les reliques, l'équipement et les portes.","Build a team of three heroes and go down as far as you can. Fights play out on their own: your job is to choose the relics, the gear and the doors."),
("100 étages et 10 boss, avec un mode cauchemar et ses malédictions","100 floors and 10 bosses, with a nightmare mode and its curses"),
("5 héros à combiner : Aldric, Selena, Orin, Lyra et Nyx","5 heroes to combine: Aldric, Selena, Orin, Lyra and Nyx"),
("Reliques à fusionner, synergies, et un camp à améliorer entre deux descentes","Relics to merge, synergies, and a camp to upgrade between runs"),
('<dt>Joueurs</dt><dd>Solo</dd>','<dt>Players</dt><dd>Solo</dd>'),
('<dd>Navigateur, mobile</dd>','<dd>Browser, mobile</dd>'),
('<dd>0.8, en développement</dd>','<dd>0.8, in development</dd>'),
("Images d'Infinite Dungeon","Infinite Dungeon images"),
('alt="Le camp des héros autour du feu"','alt="The heroes\' camp around the fire"'),('alt="L\'équipe devant le donjon"','alt="The team in front of the dungeon"'),
('alt="Écran de victoire"','alt="Victory screen"'),('alt="Lyra, l\'archère"','alt="Lyra, the archer"'),
('Jouer à Infinite Dungeon','Play Infinite Dungeon'),
# misc alts
("L'équipe de héros d'Infinite Dungeon","The hero team of Infinite Dungeon"),("Jelly, la mascotte de Gravity Turn","Jelly, the Gravity Turn mascot"),
("Icône de Gravity Turn","Gravity Turn icon"),("Icône d'Infinite Dungeon","Infinite Dungeon icon"),
# about
('<h2 id="ap-t">Qui fait ces jeux ?</h2>','<h2 id="ap-t">Who makes these games?</h2>'),
("Maxlol Games, c'est le studio d'une seule personne : maxlolfr. Je conçois, je code et j'équilibre chaque jeu moi-même, avec l'aide de l'IA pour les images et les sons.","Maxlol Games is a one-person studio: maxlolfr. I design, code and balance every game myself, with AI help for images and sounds."),
("Chaque jeu est d'abord pensé pour une main sur un iPhone, puis adapté à l'ordinateur. Les nouvelles versions sortent ici et sur itch.io dès qu'elles sont jouables.","Every game is designed first for one hand on an iPhone, then adapted to computers. New versions come out here and on itch.io as soon as they are playable."),
('<h2>Suivre mes jeux</h2>','<h2>Follow my games</h2>'),
('Télécharger et suivre les sorties','Download and follow new releases'),('Le code et les versions de test','Code and test builds'),
('<b>Écrire</b><span>Un retour, un bug, une idée</span>','<b>Write</b><span>Feedback, a bug, an idea</span>'),
('par maxlolfr</span>','by maxlolfr</span>'),
("Images et musiques des jeux : maxlolfr. Polices Lilita One et Nunito (licence OFL).","Game images and music: maxlolfr. Lilita One and Nunito fonts (OFL license)."),
('Touche 🔊 pour la musique','Tap 🔊 for music'),
('aria-label="Image agrandie"','aria-label="Enlarged image"'),('<button>Fermer</button>','<button>Close</button>'),
# JS
('textContent = "Bientôt"','textContent = "Soon"'),('"Gratuit"','"Free"'),
('"Couper la musique"','"Turn music off"'),('"Activer la musique"','"Turn music on"'),
('price: "7,99 €"','price: "€7.99"'),
]
# fix placeholder
R=[r for r in R if r[0]!="Des jeux faits main, pensés d'abord pour le téléphone.</p>"]
for a,b in R:
    if a not in s: print("MISSING:",a[:70]); continue
    s=s.replace(a,b)
# h1
s=s.replace('Maxlol Games, studio de jeux vidéo indépendant : La Dernière Torche, Gravity Turn, Infinite Dungeon','Maxlol Games, indie game studio: La Dernière Torche, Gravity Turn, Infinite Dungeon')
s=s.replace('<h1 id="titre" class="sr">','<h1 id="titre" class="sr">')
# og:description FR remains in head? replace explicit
s=s.replace('content="Handmade games','content="Handmade games')
# JSON-LD (en)
m=re.search(r'<script type="application/ld\+json">(.*?)</script>',s,re.S); ld=json.loads(m.group(1))
for n in ld['@graph']:
    if n['@type']=='WebSite': n['url']=n['@id']='https://maxlolgames.com/en/'; n['@id']='https://maxlolgames.com/en/#site'; n['inLanguage']='en'
    if n['@type']=='VideoGame':
        n['inLanguage']='en'; n['url']=n['url'].replace('maxlolgames.com/#','maxlolgames.com/en/#')
        n['description']={"La Dernière Torche":"Turn-based dungeon crawler for mobile: your torch fades with every room, 20 bosses to beat.","Gravity Turn":"Mobile puzzle: place the blocks, the board rotates, cascades chain.","Infinite Dungeon":"Auto-battle fantasy roguelite: 100 floors, 10 bosses, teams of 3 heroes."}[n['name']]
        if n['name']=='La Dernière Torche': n['alternateName']='The Last Torch'
s=s[:m.start(1)]+json.dumps(ld,ensure_ascii=False)+s[m.end(1):]
# assets paths
s=re.sub(r'(["\'`(])assets/',r'\1../assets/',s)
s=s.replace('<a class="lang" href="en/" hreflang="en" lang="en" aria-label="View the site in English">EN</a>','<a class="lang" href="../" hreflang="fr" lang="fr" aria-label="Voir le site en français">FR</a>')
open(OUT,'w').write(s)
# remaining French check
body=re.sub(r'url\(data:[^)]*\)','',s)
fr=set(re.findall(r'>([^<>{}]*[éèàçêôûù][^<>{}]*)<',body))
print('left FR text:',[x.strip()[:60] for x in fr][:40])
