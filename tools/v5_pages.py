# ================= V5 : pages commerciales par jeu (français + anglais) =================
# Contenu = uniquement ce qui est établi (site, fiches, décisions du créateur). Les points à confirmer sont listés dans le rapport.
import html as _h5
def _x(t): return _h5.escape(str(t),quote=True)
V5_SLUGS=['la-derniere-torche','wyrmstorm','gravity-turn','infinite-dungeon']
V5_KEY={'la-derniere-torche':'torch','wyrmstorm':'wyrmstorm','gravity-turn':'gt','infinite-dungeon':'id'}
V5_BASE={
 'la-derniere-torche':dict(name='La Dernière Torche',a='#FF9F2E',ink='#2A0E00',cover='assets/t-cover2.webp',pos='50% 0',price=True,version='',
   gallery=['t-desert','t-dragon','t-ultime','t-horloge','t-grotte','t-carte4','t-journal'],gw=(520,935),trailer=''),
 'wyrmstorm':dict(name='WYRMSTORM',a='#B26BFF',ink='#1B0B33',cover='assets/ws-cover.webp',pos='50% 10%',price=False,version='1.22',
   gallery=['ws-1','ws-2','ws-3','ws-4','ws-5'],gw=(390,844),trailer=''),
 'gravity-turn':dict(name='Gravity Turn',a='#4FA8FF',ink='#04152B',cover=None,pos='50% 50%',price=False,version='1.4',gallery=[],gw=(0,0),trailer=''),
 'infinite-dungeon':dict(name='Infinite Dungeon',a='#FFB547',ink='#2A1300',cover='assets/id-title.webp',pos='50% 6%',price=False,version='0.8',
   gallery=['id-camp','id-team','id-victory','id-lyra'],gw=(0,0),trailer=''),
}
V5_U={
'fr':dict(play='Jouer gratuitement',try_='Essayer gratuitement',buy='Acheter',gallery='Captures et images',trailer='Bande-annonce',soon='Bande-annonce bientôt disponible',
  feats='Les 5 points forts',info='Infos pratiques',plat='Plateformes',lang='Langues',save='Sauvegardes',upd='Mises à jour',ver='Version',faq='Questions fréquentes',
  also='Découvre aussi les autres jeux du studio',home='Accueil',games='Jeux',full='Jeu complet',demo='Démo gratuite',free='Gratuit',close='Fermer',
  worlds='Mondes',price='Prix',content='Contenu',dev='en développement',see='Voir le jeu',model='Modèle économique'),
'en':dict(play='Play for free',try_='Try for free',buy='Buy',gallery='Screenshots and images',trailer='Trailer',soon='Trailer coming soon',
  feats='Five reasons to play',info='Good to know',plat='Platforms',lang='Languages',save='Saves',upd='Updates',ver='Version',faq='FAQ',
  also="Try the studio's other games",home='Home',games='Games',full='Full game',demo='Free demo',free='Free',close='Close',
  worlds='Worlds',price='Price',content='Content',dev='in development',see='See the game',model='Business model'),
}
V5_G={
'la-derniere-torche':{
 'fr':dict(seo='La Dernière Torche – Jeu de donjon au tour par tour, essai gratuit',genre='Donjon au tour par tour',tag='Ta torche faiblit. Ton butin grossit.',
  desc="Explore jusqu'à 20 mondes avec une équipe de trois héros, pendant que ta torche perd de sa force à chaque salle. Plus il fait noir, plus les monstres frappent fort… et plus le butin grossit.",
  chips=['Essai gratuit dans le navigateur','Jeu complet : {p}, achat unique'],
  mtitle='Essai gratuit, jeu complet en achat unique',
  model=["Tu peux essayer le jeu gratuitement, sans compte, directement dans ton navigateur.","Si tu accroches, le jeu complet s'achète une seule fois ({p}) : pas d'abonnement.","L'achat se fait avec le bouton Acheter, sur la page itch.io du jeu."],
  cmp=[('Mondes','Mondes 1 à 5 (la première carte)','Les 20 mondes et leurs 20 boss'),('Prix','Gratuit','{p}, achat unique')],
  feats=[('🔥','Une torche qui s\'éteint','Quatre paliers, de Clarté à Noir total : plus il fait sombre, plus les monstres cognent. Au noir total, le butin est multiplié par trois.'),
   ('⚔️','Des combats au tour par tour','Deux rangs, Garde, faiblesses élémentaires et ultimes en plein écran : chaque tour compte.'),
   ('🛡️','8 héros, 28 costumes','Compose une équipe de trois, débloque 28 Liens entre héros. Les 8 héros ont 28 costumes et des voix pendant les combats.'),
   ('👹','20 boss qui changent de phase','À mi-vie, ils s\'enragent, jouent deux fois ou invoquent des renforts.'),
   ('♾️','Toujours une descente de plus','Ascensions, Profondeurs infinies, défi du jour et défi de la semaine.')],
  facts=dict(plat='Navigateur, mobile et ordinateur',lang='Français, anglais, espagnol, portugais',save="Automatique, sur l'appareil (dans le navigateur)",upd="Publiées en ligne ; les nouveautés sont listées sur ce site"),
  faq=[("L'essai est-il vraiment gratuit ?","Oui. La démo est gratuite, sans compte, et se joue directement dans le navigateur de ton téléphone ou de ton ordinateur."),
   ("Que contient le jeu complet en plus de la démo ?","La démo couvre les mondes 1 à 5. Le jeu complet ouvre les 20 mondes et leurs 20 boss."),
   ("Combien coûte le jeu complet ?","{p}, en achat unique, sans abonnement."),
   ("Ma progression est-elle sauvegardée ?","Oui, automatiquement, sur l'appareil que tu utilises. Si tu effaces les données de ton navigateur, la sauvegarde disparaît."),
   ("Sur quels appareils et en quelles langues ?","Sur téléphone et sur ordinateur, dans le navigateur. Le jeu est en français, anglais, espagnol et portugais."),
   ("J'ai une question sur un achat.","Contacte le studio depuis la page itch.io du jeu.")]),
 'en':dict(seo='La Dernière Torche – Turn-based dungeon crawler, free demo',genre='Turn-based dungeon crawler',tag='Your torch is dying. Your loot is growing.',
  desc="Explore up to 20 worlds with a team of three heroes while your torch loses strength in every room. The darker it gets, the harder monsters hit… and the bigger the loot grows.",
  chips=['Free demo in your browser','Full game: {p}, one-time purchase'],
  mtitle='Free demo, full game as a one-time purchase',
  model=["Try the game for free, with no account, right in your browser.","If you like it, the full game is a single purchase ({p}): no subscription.","Buy it with the Buy button, on the game's itch.io page."],
  cmp=[('Worlds','Worlds 1 to 5 (the first map)','All 20 worlds and their 20 bosses'),('Price','Free','{p}, one-time purchase')],
  feats=[('🔥','A torch that fades','Four levels, from Clarity to Total Darkness: the darker it gets, the harder monsters hit. In total darkness, loot is tripled.'),
   ('⚔️','Turn-based combat','Two rows, Guard, elemental weaknesses and full-screen ultimates: every turn counts.'),
   ('🛡️','8 heroes, 28 costumes','Build a team of three and unlock 28 Links between heroes. The 8 heroes have 28 costumes and voices during battles.'),
   ('👹','20 bosses that change phase','At half health they enrage, act twice or summon reinforcements.'),
   ('♾️','Always one more descent','Ascensions, Infinite Depths, a daily challenge and a weekly challenge.')],
  facts=dict(plat='Browser, mobile and desktop',lang='French, English, Spanish, Portuguese',save='Automatic, on your device (in the browser)',upd='Published online; news is listed on this site'),
  faq=[("Is the demo really free?","Yes. The demo is free, needs no account and plays right in your phone or computer browser."),
   ("What does the full game add to the demo?","The demo covers worlds 1 to 5. The full game opens all 20 worlds and their 20 bosses."),
   ("How much is the full game?","{p}, as a one-time purchase, with no subscription."),
   ("Is my progress saved?","Yes, automatically, on the device you use. If you clear your browser data, the save is gone."),
   ("Which devices and languages?","Phone and computer, in the browser. The game is in French, English, Spanish and Portuguese."),
   ("I have a question about a purchase.","Contact the studio from the game's itch.io page.")])},
'wyrmstorm':{
 'fr':dict(seo='WYRMSTORM – Shoot\'em up à dragons gratuit',genre="Shoot'em up à dragons",tag='Pilote, tire, fais éclore tes dragons.',
  desc="Pilote un héros et déchaîne tes dragons pour traverser le ciel, un niveau après l'autre, d'un seul pouce. Affronte 7 boss de monde et 14 gardiens animés, et fais grandir tes dragons de 7 éléments.",
  chips=['Gratuit à jouer','Boutique facultative'],mtitle='Gratuit à jouer, boutique facultative',
  model=["Tu joues gratuitement, directement dans ton navigateur, sans compte.","La boutique du jeu propose des costumes de héros et des offres : c'est facultatif.","Aujourd'hui, tu peux jouer sans rien payer. Les achats en argent réel sont prévus avec les versions mobiles."],cmp=[],
  feats=[('👆','Un seul pouce','Glisse pour piloter : ton héros tire tout seul, tu te concentres sur l\'esquive.'),
   ('🐉','Des dragons de 7 éléments','Fais éclore des œufs, fusionne et améliore tes dragons.'),
   ('👹','7 boss de monde, 14 gardiens','Des gardiens animés pièce par pièce, avec leurs propres attaques à lire et à esquiver.'),
   ('🛡️','Des héros jusqu\'au niveau 100','Fais monter tes héros en niveau et débloque leurs costumes.'),
   ('🏆','Missions, succès et saison','Raid, pass de saison, missions et succès : il y a toujours un objectif.')],
  facts=dict(plat='Navigateur, mobile',lang='Français, anglais, thaï',save="Automatique, sur l'appareil (dans le navigateur)",upd="Publiées en ligne ; les nouveautés sont listées sur ce site"),
  faq=[("WYRMSTORM est-il vraiment gratuit ?","Oui. Tu peux jouer gratuitement, sans compte, directement dans ton navigateur."),
   ("La boutique est-elle obligatoire ?","Non. Elle propose des costumes de héros et des offres facultatives."),
   ("Y a-t-il des achats en argent réel ?","Aujourd'hui, tu peux jouer sans rien payer. Les achats en argent réel sont prévus avec les versions mobiles."),
   ("Sur quels appareils ?","Sur téléphone (le jeu se joue d'un seul pouce) et sur ordinateur, dans le navigateur."),
   ("En quelles langues ?","Français, anglais et thaï."),
   ("Ma progression est-elle sauvegardée ?","Oui, automatiquement, sur l'appareil que tu utilises. Si tu effaces les données de ton navigateur, la sauvegarde disparaît.")]),
 'en':dict(seo="WYRMSTORM – Free dragon shoot'em up",genre="Dragon shoot'em up",tag='Fly, shoot, hatch your dragons.',
  desc="Pilot a hero and unleash your dragons to cross the sky one level at a time, with one thumb. Face 7 world bosses and 14 animated guardians, and grow dragons of 7 elements.",
  chips=['Free to play','Optional shop'],mtitle='Free to play, optional shop',
  model=["Play for free, right in your browser, with no account.","The in-game shop offers hero costumes and offers: it is optional.","Today you can play without paying anything. Real-money purchases are planned for the mobile versions."],cmp=[],
  feats=[('👆','One thumb is enough','Drag to fly: your hero fires on its own, so you can focus on dodging.'),
   ('🐉','Dragons of 7 elements','Hatch eggs, fuse and upgrade your dragons.'),
   ('👹','7 world bosses, 14 guardians','Guardians animated piece by piece, each with attacks to read and dodge.'),
   ('🛡️','Heroes up to level 100','Level up your heroes and unlock their costumes.'),
   ('🏆','Missions, achievements and seasons','Raid, season pass, missions and achievements: there is always a goal.')],
  facts=dict(plat='Browser, mobile',lang='French, English, Thai',save='Automatic, on your device (in the browser)',upd='Published online; news is listed on this site'),
  faq=[("Is WYRMSTORM really free?","Yes. You can play for free, with no account, right in your browser."),
   ("Is the shop required?","No. It offers hero costumes and optional offers."),
   ("Are there real-money purchases?","Today you can play without paying anything. Real-money purchases are planned for the mobile versions."),
   ("Which devices?","Phone (it plays with one thumb) and computer, in the browser."),
   ("Which languages?","French, English and Thai."),
   ("Is my progress saved?","Yes, automatically, on the device you use. If you clear your browser data, the save is gone.")])},
'gravity-turn':{
 'fr':dict(seo='Gravity Turn – Puzzle de blocs qui tournent, gratuit',genre='Puzzle de blocs qui tournent',tag='Pose. Tourne. Cascade !',
  desc="Pose des blocs gelée sur une grille de 8×8 : toutes les trois pièces, le plateau tourne d'un quart de tour et tout retombe. Une ligne qui en fait tomber une autre, c'est une cascade.",
  chips=['Gratuit','Aucun achat'],mtitle='Gratuit, sans achat',
  model=["Tu joues gratuitement, directement dans ton navigateur.","Aucun achat n'est proposé dans le jeu pour l'instant."],cmp=[],
  feats=[('🔄','Un plateau qui tourne','Toutes les trois pièces, le plateau tourne d\'un quart de tour et tout retombe.'),
   ('💥','Des cascades en chaîne','Une ligne qui en fait tomber une autre : les combos s\'enchaînent.'),
   ('🧩','84 niveaux, 7 mondes','Pierres, glace, gemmes, bombes et éclairs viennent compliquer la grille.'),
   ('📅','Défi du jour et de la semaine','Les mêmes pour tout le monde.'),
   ('🧘','Modes infini et zen','Pour jouer sans objectif, à ton rythme.')],
  facts=dict(plat='Navigateur, iPhone bientôt',lang='Français, anglais',save="Automatique, sur l'appareil (dans le navigateur)",upd="Publiées en ligne ; les nouveautés sont listées sur ce site"),
  faq=[("Gravity Turn est-il gratuit ?","Oui, et aucun achat n'est proposé dans le jeu pour l'instant."),
   ("Sur quels appareils ?","Dans le navigateur, sur téléphone et sur ordinateur. Une version iPhone est annoncée."),
   ("En quelles langues ?","Français et anglais."),
   ("Ma progression est-elle sauvegardée ?","Oui, automatiquement, sur l'appareil que tu utilises. Si tu effaces les données de ton navigateur, la sauvegarde disparaît."),
   ("Comment fonctionne la rotation ?","Toutes les trois pièces posées, le plateau tourne d'un quart de tour et les blocs retombent.")]),
 'en':dict(seo='Gravity Turn – Rotating block puzzle, free',genre='Rotating block puzzle',tag='Place. Turn. Cascade!',
  desc="Place jelly blocks on an 8×8 grid: every three pieces, the board turns a quarter and everything falls. A line that makes another one fall is a cascade.",
  chips=['Free','No purchases'],mtitle='Free, no purchases',
  model=["Play for free, right in your browser.","The game offers no purchases for now."],cmp=[],
  feats=[('🔄','A board that turns','Every three pieces, the board turns a quarter and everything falls.'),
   ('💥','Chain cascades','A line that makes another one fall: combos keep rolling.'),
   ('🧩','84 levels, 7 worlds','Stones, ice, gems, bombs and lightning complicate the grid.'),
   ('📅','Daily and weekly challenges','The same for everyone.'),
   ('🧘','Endless and zen modes','Play without a goal, at your own pace.')],
  facts=dict(plat='Browser, iPhone soon',lang='French, English',save='Automatic, on your device (in the browser)',upd='Published online; news is listed on this site'),
  faq=[("Is Gravity Turn free?","Yes, and the game offers no purchases for now."),
   ("Which devices?","In the browser, on phone and computer. An iPhone version is announced."),
   ("Which languages?","French and English."),
   ("Is my progress saved?","Yes, automatically, on the device you use. If you clear your browser data, the save is gone."),
   ("How does the rotation work?","Every three pieces you place, the board turns a quarter and the blocks fall.")])},
'infinite-dungeon':{
 'fr':dict(seo='Infinite Dungeon – Roguelite fantasy à auto-combat, gratuit',genre='Roguelite fantasy',tag='Descends. Fusionne. Survis.',
  desc="Monte une équipe de trois héros et descends le plus loin possible. Les combats se jouent seuls : ton rôle, c'est de choisir les reliques, l'équipement et les portes.",
  chips=['Gratuit','En développement (v0.8)'],mtitle='Gratuit, sans achat',
  model=["Tu joues gratuitement, directement dans ton navigateur.","Aucun achat n'est proposé dans le jeu pour l'instant. Le jeu est encore en développement (version 0.8)."],cmp=[],
  feats=[('🏰','100 étages, 10 boss','Avec un mode cauchemar et ses malédictions.'),
   ('⚔️','5 héros à combiner','Aldric, Selena, Orin, Lyra et Nyx : forme ton équipe de trois.'),
   ('🔮','Des reliques à fusionner','Reliques, équipement et synergies : c\'est toi qui bâtis la stratégie.'),
   ('🏕️','Un camp à améliorer','Entre deux descentes, améliore ton camp pour aller plus loin.'),
   ('🤖','Des combats automatiques','Les combats se jouent seuls : tu choisis les reliques, l\'équipement et les portes.')],
  facts=dict(plat='Navigateur, mobile',lang='Français, anglais',save="Automatique, sur l'appareil (dans le navigateur)",upd="Publiées en ligne ; les nouveautés sont listées sur ce site"),
  faq=[("Infinite Dungeon est-il gratuit ?","Oui, et aucun achat n'est proposé dans le jeu pour l'instant."),
   ("Le jeu est-il terminé ?","Non, c'est la version 0.8, encore en développement."),
   ("Dois-je jouer les combats ?","Non, ils se jouent seuls. Tu choisis les reliques, l'équipement et les portes."),
   ("Sur quels appareils et en quelles langues ?","Dans le navigateur, sur téléphone et ordinateur. Le jeu est en français et en anglais."),
   ("Ma progression est-elle sauvegardée ?","Oui, automatiquement, sur l'appareil que tu utilises. Si tu effaces les données de ton navigateur, la sauvegarde disparaît.")]),
 'en':dict(seo='Infinite Dungeon – Free auto-battle fantasy roguelite',genre='Fantasy roguelite',tag='Descend. Fuse. Survive.',
  desc="Build a team of three heroes and go down as far as you can. Fights play out on their own: your job is to choose the relics, the gear and the doors.",
  chips=['Free','In development (v0.8)'],mtitle='Free, no purchases',
  model=["Play for free, right in your browser.","The game offers no purchases for now. It is still in development (version 0.8)."],cmp=[],
  feats=[('🏰','100 floors, 10 bosses','With a nightmare mode and its curses.'),
   ('⚔️','5 heroes to combine','Aldric, Selena, Orin, Lyra and Nyx: build your team of three.'),
   ('🔮','Relics to fuse','Relics, gear and synergies: you build the strategy.'),
   ('🏕️','A camp to upgrade','Between two descents, upgrade your camp to go further.'),
   ('🤖','Automatic fights','Fights play out on their own: you choose the relics, the gear and the doors.')],
  facts=dict(plat='Browser, mobile',lang='French, English',save='Automatic, on your device (in the browser)',upd='Published online; news is listed on this site'),
  faq=[("Is Infinite Dungeon free?","Yes, and the game offers no purchases for now."),
   ("Is the game finished?","No, it is version 0.8, still in development."),
   ("Do I play the fights?","No, they play out on their own. You choose the relics, the gear and the doors."),
   ("Which devices and languages?","In the browser, on phone and computer. The game is in French and English."),
   ("Is my progress saved?","Yes, automatically, on the device you use. If you clear your browser data, the save is gone.")])},
}
V5_CSS='''
/* ===== V5 : pages commerciales ===== */
body.gp{--a:#FFB547;--a-ink:#2A1300}
.gp-hero{padding:clamp(22px,4vw,56px) 0 20px;background:radial-gradient(ellipse 70% 60% at 20% 0%,color-mix(in srgb,var(--a) 22%,transparent),transparent 70%)}
.gp-hero .grid{display:grid;grid-template-columns:minmax(220px,360px) 1fr;gap:clamp(20px,4vw,52px);align-items:center}
@media (max-width:760px){.gp-hero .grid{grid-template-columns:1fr}.gp-cover{max-width:300px;width:78%;margin:0 auto}}
.gp-cover{position:relative;aspect-ratio:3/4;border-radius:26px;overflow:hidden;box-shadow:0 24px 60px rgba(5,2,20,.6),0 0 0 2px var(--a)}
.gp-cover>img{width:100%;height:100%;object-fit:cover}
.gp-cover .gtc{position:absolute;inset:0}
.crumb{font-size:.85rem;color:var(--brume);margin:0 0 10px}.crumb a{color:var(--brume)}
.gp-genre{margin:0;font-size:.8rem;font-weight:800;letter-spacing:.06em;text-transform:uppercase;color:var(--a)}
.gp h1{font:400 clamp(2.3rem,7vw,3.8rem)/1.02 var(--display);margin:4px 0 6px}
.gp-tag{font:400 clamp(1.15rem,3vw,1.55rem)/1.25 var(--display);color:var(--a);margin:0 0 10px}
.gp-desc{color:var(--lavande);font-size:1.08rem;max-width:58ch;margin:0}
.chips{display:flex;flex-wrap:wrap;gap:8px;margin:16px 0 4px}
.chip{padding:6px 13px;border-radius:999px;background:rgba(255,255,255,.09);box-shadow:inset 0 0 0 1.5px color-mix(in srgb,var(--a) 55%,transparent);font-weight:800;font-size:.88rem}
.gp-cta{display:flex;flex-wrap:wrap;gap:10px;margin-top:16px}
.gb{padding:30px 0}
.gb h2{font:400 clamp(1.6rem,4vw,2.3rem)/1.1 var(--display);margin:0 0 16px}
.fgrid{display:grid;grid-template-columns:repeat(auto-fit,minmax(230px,1fr));gap:14px}
.fcard{background:var(--prune);border-radius:18px;padding:18px;box-shadow:inset 0 0 0 1px rgba(255,255,255,.07)}
.fcard .fi{font-size:1.7rem;line-height:1}.fcard h3{font:400 1.2rem/1.15 var(--display);margin:8px 0 6px}.fcard p{margin:0;color:var(--brume);font-size:.95rem}
.model{background:linear-gradient(160deg,rgba(255,255,255,.08),rgba(255,255,255,.03));border-radius:22px;padding:22px;box-shadow:inset 0 0 0 1.5px var(--a)}
.model h2{margin-bottom:10px}.model ul{margin:0;padding-left:20px;color:var(--lavande)}.model li{margin:6px 0}
.cmp{display:grid;grid-template-columns:auto 1fr 1fr;gap:1px;margin-top:16px;border-radius:14px;overflow:hidden;background:rgba(255,255,255,.12);font-size:.95rem}
.cmp>div{background:var(--prune);padding:10px 12px}.cmp .h{font-weight:800;background:rgba(255,255,255,.06)}.cmp .hf{color:var(--a)}
@media (max-width:520px){.cmp{font-size:.86rem}.cmp>div{padding:8px 9px}}
.gal{display:flex;gap:12px;overflow-x:auto;scroll-snap-type:x mandatory;padding-bottom:10px;scrollbar-width:thin}
.gal button{flex:0 0 auto;border:0;padding:0;background:none;border-radius:16px;overflow:hidden;scroll-snap-align:start;cursor:zoom-in;box-shadow:0 10px 24px rgba(5,2,20,.5)}
.gal img{height:clamp(260px,52vw,340px);width:auto;display:block}
.trailer{position:relative;aspect-ratio:16/9;border-radius:20px;overflow:hidden;background:#120C2B;display:grid;place-items:center;box-shadow:inset 0 0 0 1px rgba(255,255,255,.1);margin-bottom:18px}
.trailer>img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;opacity:.3;filter:blur(3px)}
.trailer video{position:absolute;inset:0;width:100%;height:100%;background:#000}
.trailer p{position:relative;margin:0;font-weight:800;color:var(--brume);text-align:center;padding:0 16px}
.info{display:grid;grid-template-columns:repeat(auto-fit,minmax(210px,1fr));gap:12px;margin:0}
.info div{background:var(--prune);border-radius:16px;padding:14px 16px;box-shadow:inset 0 0 0 1px rgba(255,255,255,.07)}
.info dt{font-size:.74rem;font-weight:800;letter-spacing:.06em;text-transform:uppercase;color:var(--a)}.info dd{margin:4px 0 0;font-weight:700}
.faq details{background:var(--prune);border-radius:16px;margin-bottom:10px;padding:0 16px;box-shadow:inset 0 0 0 1px rgba(255,255,255,.07)}
.faq summary{cursor:pointer;font-weight:800;padding:15px 0;list-style:none;display:flex;justify-content:space-between;gap:12px}
.faq summary::-webkit-details-marker{display:none}.faq summary::after{content:"+";color:var(--a);font-size:1.3rem;line-height:1}
.faq details[open] summary::after{content:"–"}.faq p{margin:0 0 15px;color:var(--brume)}
.more{display:grid;grid-template-columns:repeat(auto-fit,minmax(250px,1fr));gap:14px}
.rc{display:flex;gap:14px;align-items:center;background:var(--prune);border-radius:18px;padding:10px;text-decoration:none;color:inherit;box-shadow:inset 0 0 0 1px rgba(255,255,255,.07)}
.rc:hover{background:#33256a}
.rc .ri{position:relative;flex:0 0 76px;aspect-ratio:3/4;border-radius:12px;overflow:hidden;background:#120C2B}.rc .ri>img{width:100%;height:100%;object-fit:cover;object-position:50% 8%}.rc .ri .gtc{position:absolute;inset:0}
.rc b{display:block;font:400 1.15rem/1.1 var(--display)}.rc small{display:block;color:var(--brume);font-weight:700;margin-top:3px}.rc em{font-style:normal;color:var(--bonbon);font-weight:800;font-size:.85rem}
.sbar{position:fixed;left:0;right:0;bottom:0;z-index:40;display:none;gap:10px;align-items:center;padding:10px 14px calc(10px + env(safe-area-inset-bottom));background:rgba(26,18,56,.95);-webkit-backdrop-filter:blur(14px);backdrop-filter:blur(14px);border-top:1px solid rgba(255,255,255,.14);transform:translateY(115%);transition:transform .25s ease}
.sbar.show{transform:none}
.sbar .sp{font-weight:800;line-height:1.1;font-size:.78rem;color:var(--brume)}.sbar .sp b{display:block;font-size:1.05rem;color:var(--lavande)}
.sbar .btn{min-height:46px;padding:0 14px;font-size:.95rem;flex:1;justify-content:center}
@media (max-width:720px){.sbar{display:flex}body.hasbar{padding-bottom:78px}}
@media (prefers-reduced-motion:reduce){.sbar{transition:none}}
'''
def v5_fmt_price(lang,s_home):
    m=re.search(r'"torch": \{ price: "([^"]*)"',s_home); raw=m.group(1) if m else ''
    n=re.search(r'[\d]+[.,]\d+',raw);
    if not n: return raw
    v=n.group(0).replace(',','.')
    return (v.replace('.',',')+' €') if lang=='fr' else '€'+v
def v5_pref(lang): return '/fr/' if lang=='fr' else '/'
def v5_cover_html(slug,pre='/'):
    b=V5_BASE[slug]
    if b['cover']: return '<img src="%s%s" alt="%s" width="640" height="960" loading="lazy" decoding="async">'%(pre,b['cover'],_x(b['name']))
    return '<span class="gtc"><img src="%sassets/gt-jelly.webp" alt="" width="256" height="256" loading="lazy"><img class="gtl" src="%sassets/gt-logo.webp" alt="" width="720" height="241" loading="lazy"></span>'%(pre,pre)
def v5_page(slug,lang,home):
    b=V5_BASE[slug]; g=V5_G[slug][lang]; U=V5_U[lang]; key=V5_KEY[slug]; P=v5_fmt_price(lang,home); pre=v5_pref(lang)
    T=lambda t:_x(t.replace('{p}',P))
    url='https://maxlolgames.com'+pre+slug+'/'; url_fr='https://maxlolgames.com/fr/'+slug+'/'; url_en='https://maxlolgames.com/'+slug+'/'
    fix=lambda t:re.sub(r'(["\'`(])(?:\.\./)?assets/',r'\1/assets/',t)
    hd=home[:home.index('<style>')]
    links=''.join(fix(x) for x in re.findall(r'<link rel="(?:manifest|apple-touch-icon|preload|icon)"[^>]*>\n?',hd))
    csp=re.search(r'<meta http-equiv="Content-Security-Policy"[^>]*>\n?<meta name="referrer"[^>]*>',hd).group(0)
    css=fix(re.search(r'<style>(.*?)</style>',home,re.S).group(1))
    header=re.search(r'<header class="top">.*?</header>',home,re.S).group(0)
    header=re.sub(r'<button class="snd".*?</button>\s*','',header,flags=re.S)
    header=re.sub(r'href="#([a-z-]*)"',lambda m:'href="%s%s"'%(pre,('#'+m.group(1)) if m.group(1) else ''),header)
    items=[]
    for code,path,hl,name,short in LANGS:
        href=('/fr/%s/'%slug) if code=='fr' else ('/%s/'%slug) if code=='en' else '/'+path
        items.append('<a href="%s" hreflang="%s" lang="%s"%s>%s</a>'%(href,hl,hl,' aria-current="true"' if code==lang else '',name))
    lm='<details class="langmenu"><summary aria-label="Language / Langue">%s</summary><div class="lm">%s</div></details>'%(lang.upper(),''.join(items))
    header=re.sub(r'<details class="langmenu">.*?</details>',lambda m:lm,header,count=1,flags=re.S)
    footer=re.search(r'<footer>.*?</footer>',home,re.S).group(0)
    script=re.search(r"(/\* =+\n\s+BOUTIQUE.*?)/\* =+ MOTEUR D'EFFETS",home,re.S).group(1)
    if lang=='en': script=script.replace('price: "7,99 €"','price: "%s"'%P)
    img_abs='https://maxlolgames.com/'+(b['cover'] or 'assets/gt-icon.webp')
    # JSON-LD
    ld=[{"@type":"VideoGame","name":b['name'],"description":g['desc'],"url":url,"image":img_abs,"genre":g['genre'],"inLanguage":lang,"applicationCategory":"Game","operatingSystem":"Web browser",
         "author":{"@type":"Organization","name":"Maxlol Games","url":"https://maxlolgames.com/"},"publisher":{"@type":"Organization","name":"Maxlol Games","url":"https://maxlolgames.com/"},
         "offers":{"@type":"Offer","price":(re.search(r'[\d.]+','%s'%P.replace(',','.')).group(0) if b['price'] else "0"),"priceCurrency":"EUR","availability":"https://schema.org/InStock","url":url}},
        {"@type":"FAQPage","mainEntity":[{"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a.replace('{p}',P)}} for q,a in g['faq']]},
        {"@type":"BreadcrumbList","itemListElement":[{"@type":"ListItem","position":1,"name":U['home'],"item":'https://maxlolgames.com'+pre},{"@type":"ListItem","position":2,"name":b['name'],"item":url}]}]
    ldj=json.dumps({"@context":"https://schema.org","@graph":ld},ensure_ascii=False).replace('</','<\\/')
    # hero
    chips=''.join('<span class="chip">%s</span>'%T(c) for c in g['chips'])
    if b['price']:
        cta=('<a class="btn main" data-link="%s-play" href="#" target="_blank" rel="noopener">%s%s</a>'
             '<a class="btn buy" data-buy="%s" href="#" target="_blank" rel="noopener">%s%s <span class="price"></span></a>'
             '<a class="btn paypal" data-paypal="%s" href="#" target="_blank" rel="noopener">PayPal <span class="price"></span></a>')%(key,PLAYSVG,_x(U['try_']),key,BUYSVG,_x(U['buy']),key)
        bar=('<a class="btn ghost" data-link="%s-play" href="#" target="_blank" rel="noopener">%s</a><a class="btn buy" data-buy="%s" href="#" target="_blank" rel="noopener">%s <span class="price"></span></a>')%(key,_x(U['try_']),key,_x(U['buy']))
    else:
        cta='<a class="btn main" data-link="%s-play" href="#" target="_blank" rel="noopener">%s%s</a><a class="btn ghost" data-link="%s-itch" href="#" target="_blank" rel="noopener">itch.io</a>'%(key,PLAYSVG,_x(U['play']),key)
        bar='<a class="btn main" data-link="%s-play" href="#" target="_blank" rel="noopener">%s%s</a>'%(key,PLAYSVG,_x(U['play']))
    feats=''.join('<div class="fcard"><div class="fi" aria-hidden="true">%s</div><h3>%s</h3><p>%s</p></div>'%(e,_x(t),_x(d)) for e,t,d in g['feats'])
    cmp=''
    if g['cmp']:
        cmp='<div class="cmp"><div class="h">%s</div><div class="h">%s</div><div class="h hf">%s</div>'%(_x(U['content']),_x(U['demo']),_x(U['full']))+''.join('<div class="h">%s</div><div>%s</div><div>%s</div>'%(_x(a),T(c),T(d)) for a,c,d in g['cmp'])+'</div>'
    model='<section class="gb"><div class="wrap"><div class="model"><h2>%s</h2><ul>%s</ul>%s</div></div></section>'%(_x(g['mtitle']),''.join('<li>%s</li>'%T(x) for x in g['model']),cmp)
    poster=(('/assets/%s.webp'%b['gallery'][0]) if b['gallery'] else (('/'+b['cover']) if b['cover'] else '/assets/gt-bg.webp'))
    if b['trailer']: tv='<div class="trailer"><video controls preload="none" playsinline poster="%s"><source src="%s"></video></div>'%(poster,_x(b['trailer']))
    else: tv='<div class="trailer"><img src="%s" alt="" loading="lazy"><p>%s</p></div>'%(poster,_x(U['soon']))
    gal=''
    if b['gallery']:
        w,h=b['gw']; dim=(' width="%d" height="%d"'%(w,h)) if w else ''
        gal='<div class="gal" aria-label="%s">%s</div>'%(_x(U['gallery']),''.join('<button type="button" data-full="/assets/%s.webp"><img src="/assets/%s.webp" alt="%s – %d" loading="lazy" decoding="async"%s></button>'%(f,f,_x(b['name']),i+1,dim) for i,f in enumerate(b['gallery'])))
    media='<section class="gb"><div class="wrap"><h2>%s</h2>%s%s</div></section>'%(_x(U['trailer'] if not gal else U['gallery']),tv,gal)
    f=g['facts']; facts=[(U['plat'],f['plat']),(U['lang'],f['lang']),(U['save'],f['save']),(U['upd'],f['upd'])]
    if b['version']: facts.append((U['ver'],b['version']+((', '+U['dev']) if slug=='infinite-dungeon' else '')))
    info='<section class="gb"><div class="wrap"><h2>%s</h2><dl class="info">%s</dl></div></section>'%(_x(U['info']),''.join('<div><dt>%s</dt><dd>%s</dd></div>'%(_x(k),_x(v)) for k,v in facts))
    faq='<section class="gb faq"><div class="wrap"><h2>%s</h2>%s</div></section>'%(_x(U['faq']),''.join('<details><summary>%s</summary><p>%s</p></details>'%(T(q),T(a)) for q,a in g['faq']))
    rec=[]
    for s2 in V5_SLUGS:
        if s2==slug: continue
        b2=V5_BASE[s2]; g2=V5_G[s2][lang]; k2=V5_KEY[s2]
        rec.append('<a class="rc" href="%s%s/"><span class="ri">%s</span><span><b>%s</b><small>%s</small><em data-price="%s"></em></span></a>'%(pre,s2,v5_cover_html(s2),_x(b2['name']),_x(g2['genre']),k2))
    more='<section class="gb"><div class="wrap"><h2>%s</h2><div class="more">%s</div></div></section>'%(_x(U['also']),''.join(rec))
    main=('<main><section class="gp-hero"><div class="wrap"><p class="crumb"><a href="%s">%s</a> › <a href="%s#jeux">%s</a> › %s</p><div class="grid"><div class="gp-cover">%s</div><div>'
          '<p class="gp-genre">%s</p><h1>%s</h1><p class="gp-tag">%s</p><p class="gp-desc">%s</p><div class="chips">%s</div><div class="gp-cta" id="cta">%s</div></div></div></div></section>')%(pre,_x(U['home']),pre,_x(U['games']),_x(b['name']),v5_cover_html(slug),_x(g['genre']),_x(b['name']),_x(g['tag']),_x(g['desc']),chips,cta)
    main+=model+media+'<section class="gb"><div class="wrap"><h2>%s</h2><div class="fgrid">%s</div></div></section>'%(_x(U['feats']),feats)+info+faq+more+'</main>'
    js=('<script>\n'+script+'\nconst v=document.getElementById("viewer"),vi=document.getElementById("viewerImg");\n'
        'document.querySelectorAll("[data-full]").forEach(b=>b.addEventListener("click",()=>{vi.src=b.dataset.full;vi.alt=b.querySelector("img").alt;v.showModal();}));\n'
        'v.addEventListener("click",e=>{if(e.target===v)v.close()});\n'
        'const cta=document.getElementById("cta"),bar=document.getElementById("sbar");\n'
        'if(cta&&bar&&"IntersectionObserver" in window){new IntersectionObserver(es=>{bar.classList.toggle("show",!es[0].isIntersecting)}).observe(cta)}\n'
        'document.addEventListener("click",e=>{document.querySelectorAll(".mmenu[open],.langmenu[open]").forEach(d=>{if(!d.contains(e.target)||e.target.closest(".mm a"))d.open=false});});\n</script>\n')
    seo_t=g['seo']+' | Maxlol Games'
    alts='<link rel="alternate" hreflang="fr" href="%s">\n<link rel="alternate" hreflang="en" href="%s">\n<link rel="alternate" hreflang="x-default" href="%s">\n'%(url_fr,url_en,url_en)
    out=('<!DOCTYPE html>\n<html lang="%s">\n<head>\n<meta charset="utf-8">\n%s\n<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n%s'
         '<title>%s</title>\n<meta name="description" content="%s">\n<meta name="robots" content="index, follow, max-image-preview:large">\n<link rel="canonical" href="%s">\n%s'
         '<meta property="og:type" content="website">\n<meta property="og:site_name" content="Maxlol Games">\n<meta property="og:title" content="%s">\n<meta property="og:description" content="%s">\n<meta property="og:url" content="%s">\n<meta property="og:image" content="%s">\n'
         '<meta name="twitter:card" content="summary_large_image">\n<script type="application/ld+json">%s</script>\n<style>%s%s</style>\n</head>\n'
         '<body class="gp hasbar" style="--a:%s;--a-ink:%s">\n%s\n%s\n%s\n<div class="sbar" id="sbar">%s</div>\n<dialog id="viewer" aria-label="%s"><img id="viewerImg" alt=""><form method="dialog"><button>%s</button></form></dialog>\n%s</body>\n</html>\n')%(
         lang,csp,links,_x(seo_t),_x(g['desc']),url,alts,_x(seo_t),_x(g['desc']),url,_x(img_abs),ldj,css,V5_CSS,b['a'],b['ink'],header,main,footer,bar,_x(b['name']),_x(U['close']),js)
    return out
def v5_build():
    import os
    pages=[]
    for lang,path in (('fr','fr/'),('en','')):
        home=open(ROOT+path+'index.html').read()
        for slug in V5_SLUGS:
            d=ROOT+path+slug+'/'; os.makedirs(d,exist_ok=True)
            open(d+'index.html','w').write(v5_page(slug,lang,home)); pages.append(slug)
    sm=open(ROOT+'sitemap.xml').read()
    add=''
    for slug in V5_SLUGS:
        for path in ('','fr/'):
            add+='  <url><loc>https://maxlolgames.com/%s%s/</loc><lastmod>%s</lastmod><priority>0.8</priority>\n    <xhtml:link rel="alternate" hreflang="fr" href="https://maxlolgames.com/fr/%s/"/>\n    <xhtml:link rel="alternate" hreflang="en" href="https://maxlolgames.com/%s/"/>\n  </url>\n'%(path,slug,__import__("datetime").date.today().isoformat(),slug,slug)
    if 'la-derniere-torche/</loc>' not in sm: sm=sm.replace('</urlset>',add+'</urlset>')
    open(ROOT+'sitemap.xml','w').write(sm)
    print('game pages',len(pages)*2)
