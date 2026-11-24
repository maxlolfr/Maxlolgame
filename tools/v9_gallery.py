"""Étape 9 : galeries des 4 jeux construites depuis art/ (FR + EN). Idempotent : reconstruit toujours le contenu de .gal.
Les images sont réduites en WebP dans assets/g/. Usage : python3 tools/v9_gallery.py (après build_i18n.py)."""
import os, re
from PIL import Image
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + '/'
A = R + 'art/'
G = {  # slug : [(fichier source dans art/, alt FR, alt EN)]
 'gravity-turn': [('Gravity-Turn/01-banniere-logo.png', 'logo et plateau de cubes', 'logo and block board'), ('Gravity-Turn/02-visuel-plateau.png', 'le plateau pivote', 'the board turns'),
  ('Gravity-Turn/captures/01-gravity-turn-accueil.jpg', 'écran d’accueil', 'home screen'), ('Gravity-Turn/captures/02-gravity-turn-gemmes-en-partie.jpg', 'gemmes en partie', 'gems in a game'),
  ('Gravity-Turn/captures/03-gravity-turn-rotation-du-plateau.jpg', 'rotation du plateau', 'board rotation'), ('Gravity-Turn/captures/04-gravity-turn-ligne-et-gemme.jpg', 'ligne et gemme', 'line and gem'),
  ('Gravity-Turn/captures/05-gravity-turn-defi-hebdomadaire.jpg', 'défi hebdomadaire', 'weekly challenge'), ('Gravity-Turn/captures/06-gravity-turn-carte-aventure.jpg', 'carte d’aventure', 'adventure map'),
  ('Gravity-Turn/captures/07-gravity-turn-defi-du-jour.jpg', 'défi du jour', 'daily challenge'), ('Gravity-Turn/captures/08-gravity-turn-tutoriel.jpg', 'tutoriel', 'tutorial'),
  ('Gravity-Turn/captures/09-gravity-turn-quetes.jpg', 'quêtes', 'quests'), ('Gravity-Turn/captures/10-gravity-turn-apparences.jpg', 'apparences', 'appearances')],
 'la-derniere-torche': [('La-Derniere-Torche/01-dragon-forteresse.webp', 'le dragon de la forteresse', 'the fortress dragon'), ('La-Derniere-Torche/03-ultime-ysmere.webp', 'l’ultime d’Ysmère', 'Ysmère’s ultimate'),
  ('La-Derniere-Torche/04-necromancien.webp', 'le nécromancien', 'the necromancer'), ('La-Derniere-Torche/05-horloge-brisee.webp', 'l’horloge brisée', 'the broken clock'),
  ('La-Derniere-Torche/06-combat-desert.webp', 'combat dans le désert', 'desert battle'), ('La-Derniere-Torche/07-profondeurs.webp', 'les profondeurs', 'the depths'),
  ('La-Derniere-Torche/08-carte-du-donjon.webp', 'carte du donjon', 'dungeon map'), ('La-Derniere-Torche/09-journal-des-monstres.webp', 'journal des monstres', 'monster journal'),
  ('La-Derniere-Torche/10-cite-celeste.webp', 'la cité céleste', 'the celestial city'), ('La-Derniere-Torche/11-temple-de-jade.webp', 'le temple de jade', 'the jade temple'),
  ('La-Derniere-Torche/12-illustration-torche.webp', 'la torche', 'the torch')],
 'wyrmstorm': [('WYRMSTORM/01-boss-queen-frimas.webp', 'boss Reine du Givre', 'Frost Queen boss'), ('WYRMSTORM/03-vague-du-gardien.webp', 'vague du gardien', 'guardian wave'),
  ('WYRMSTORM/04-canyon-ambre-endless.webp', 'Canyon d’ambre, mode sans fin', 'Amber Canyon, endless mode'), ('WYRMSTORM/05-canyon-ambre-tirs.jpg', 'Canyon d’ambre, tirs', 'Amber Canyon, shots'),
  ('WYRMSTORM/06-canyon-ambre-bonus.jpg', 'Canyon d’ambre, bonus', 'Amber Canyon, bonus'), ('WYRMSTORM/07-canyon-ambre-vague.webp', 'Canyon d’ambre, vague', 'Amber Canyon, wave'),
  ('WYRMSTORM/08-carte-aventure.webp', 'carte d’aventure', 'adventure map'), ('WYRMSTORM/09-dragon-sylvara.webp', 'le dragon Sylvara', 'the dragon Sylvara'),
  ('WYRMSTORM/10-accueil.webp', 'écran d’accueil', 'home screen'), ('WYRMSTORM/11-illustration-dragons.webp', 'les dragons', 'the dragons'), ('WYRMSTORM/12-affiche-heros.webp', 'affiche des héros', 'heroes poster')],
 'infinite-dungeon': [('Infinite-Dungeon/01-combat-crypte.webp', 'combat dans la crypte', 'crypt battle'), ('Infinite-Dungeon/02-couverture.webp', 'couverture', 'cover art'),
  ('Infinite-Dungeon/03-illustration-camp.webp', 'le camp', 'the camp'), ('Infinite-Dungeon/04-choix-recompenses.webp', 'choix de récompenses', 'reward choice'),
  ('Infinite-Dungeon/05-equipe-devant-tour.webp', 'l’équipe devant la tour', 'the team before the tower'), ('Infinite-Dungeon/06-illustration-victoire.webp', 'victoire', 'victory'),
  ('Infinite-Dungeon/07-heroine-lyra.webp', 'l’héroïne Lyra', 'heroine Lyra')]}
NAME = {'gravity-turn': 'Gravity Turn', 'la-derniere-torche': 'La Dernière Torche', 'wyrmstorm': 'WYRMSTORM', 'infinite-dungeon': 'Infinite Dungeon'}
os.makedirs(R + 'assets/g', exist_ok=True)
for slug, items in G.items():
    cells = {'fr': [], 'en': []}
    for n, (src, fr, en) in enumerate(items, 1):
        im = Image.open(A + src).convert('RGB'); h = min(700, im.height); w = round(im.width * h / im.height)
        out = 'g/%s-%02d.webp' % (slug, n)
        im.resize((w, h), Image.LANCZOS).save(R + 'assets/' + out, 'WEBP', quality=78, method=6)
        for lang, alt in (('fr', fr), ('en', en)):
            cells[lang].append('<button type="button" data-full="/assets/%s"><img src="/assets/%s" alt="%s – %s" loading="lazy" decoding="async" width="%d" height="%d"></button>' % (out, out, NAME[slug], alt, w, h))
    for lang, rel in (('fr', 'fr/%s/index.html' % slug), ('en', '%s/index.html' % slug)):
        p = R + rel
        if not os.path.exists(p): continue
        s = open(p, encoding='utf8').read()
        new = re.sub(r'(<div class="gal"[^>]*>)(.*?)(</div>)', lambda m: m.group(1) + ''.join(cells[lang]) + m.group(3), s, count=1, flags=re.S)
        if new != s: open(p, 'w', encoding='utf8').write(new); print('galerie', rel, len(items), 'images')
