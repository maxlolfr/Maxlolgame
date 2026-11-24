"""Étape 15 : section cliquable « héros » sur les pages jeu Infinite Dungeon (5 héros + tenue) et WYRMSTORM (7 dragons, pilotes, évolutions). FR + EN. Idempotent.
Images : tools/extract_gamesheroes.py -> assets/hid, assets/hws. Comportement : assets/js/gallery-modal.js, style : assets/css/heroes.css + gh.css."""
import os, re, json
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + '/'
T = {'fr': dict(base='Tenue de base', outfits='Tenues', sheet='Planche de poses', close='Fermer', atk='Attaque', skill='Compétence', hit='Touché', ko='K.O.', win='Victoire', ult='Ultime'),
     'en': dict(base='Default outfit', outfits='Outfits', sheet='Pose sheet', close='Close', atk='Attack', skill='Skill', hit='Hit', ko='Down', win='Victory', ult='Ultimate')}
IDH = [('aldric', 'Aldric', 'Chevalier', 'Knight', 'Armure de l’Aube', 'Dawn Armor'), ('selena', 'Séléna', 'Paladine', 'Paladin', 'Prêtresse des étoiles', 'Star Priestess'),
       ('orin', 'Orin', 'Mage', 'Mage', 'Archimage du givre', 'Frost Archmage'), ('lyra', 'Lyra', 'Archère', 'Archer', 'Garde-chasse d’automne', 'Autumn Gamekeeper'),
       ('nyx', 'Nyx', 'Voleuse', 'Rogue', 'Ombre écarlate', 'Scarlet Shade')]
WSD = [('water', 'Azuréon', 'Eau', 'Water'), ('fire', 'Pyralis', 'Feu', 'Fire'), ('ice', 'Givrhal', 'Glace', 'Ice'), ('nature', 'Sylvaria', 'Nature', 'Nature'),
       ('storm', 'Voltaris', 'Foudre', 'Lightning'), ('shadow', 'Nyxar', 'Ombre', 'Shadow'), ('light', 'Solarion', 'Lumière', 'Light')]
TXT = {('id', 'fr'): ('Les 5 héros', 'Touche un héros pour voir sa tenue et ses poses.'), ('id', 'en'): ('The 5 heroes', 'Tap a hero to see their outfit and poses.'),
       ('ws', 'fr'): ('Les 7 dragons et leurs pilotes', 'Touche un dragon pour voir son pilote et ses évolutions.'), ('ws', 'en'): ('The 7 dragons and their pilots', 'Tap a dragon to see its pilot and evolutions.')}
def data(game, l):
    t = T[l]; i = 0 if l == 'fr' else 1
    if game == 'id':
        H = []
        for k, name, rf, re_, cf, ce in IDH:
            p = '/assets/hid/%s_' % k
            H.append(dict(name=name, role=(rf, re_)[i], thumb=p + 'i0.webp', variants=[
                dict(label=t['base'], thumb=p + 'i0.webp', frames=[p + 'i%d.webp' % n for n in range(4)], poses=[[t['atk'], p + 'atk.webp'], [t['skill'], p + 'skill.webp'], [t['hit'], p + 'hit.webp'], [t['ko'], p + 'ko.webp'], [t['win'], p + 'win.webp']], extra=[[t['ult'], p + 'ult.webp']]),
                dict(label=(cf, ce)[i], thumb=p + 'ci0.webp', frames=[p + 'ci0.webp'], poses=[[t['atk'], p + 'catk.webp'], [t['skill'], p + 'cskill.webp'], [t['hit'], p + 'chit.webp']])]))
        return dict(sq=False, ui=dict(outfits=t['outfits'], sheet=t['sheet'], close=t['close']), heroes=H)
    ev = ('Évolution', 'Evolution'); pil = ('Pilote — forme', 'Pilot — form')
    H = []
    for k, name, ef, ee in WSD:
        p = '/assets/hws/%s_' % k
        poses = [[('Dragon', 'Dragon')[i], p + 'd0.webp'], ['%s 1' % ev[i], p + 'd1.webp'], ['%s 2' % ev[i], p + 'd2.webp'], [('Apparence', 'Skin')[i], p + 'sk.webp']]
        extra = [[('Pilote de dos', 'Pilot from behind')[i], p + 'pb.webp']]
        H.append(dict(name=name, role=(ef, ee)[i], thumb=p + 'p1.webp', variants=[dict(label='%s %d' % (pil[i], n), thumb=p + 'p%d.webp' % n, frames=[p + 'p%d.webp' % n], poses=poses, extra=extra) for n in (1, 2, 3)]))
    return dict(sq=True, ui=dict(outfits=('Évolutions du pilote', 'Pilot evolutions')[i], sheet=('Le dragon', 'The dragon')[i], close=t['close']), heroes=H)
n = 0
for game, slug in [('id', 'infinite-dungeon'), ('ws', 'wyrmstorm')]:
    for l, path in [('en', slug + '/index.html'), ('fr', 'fr/' + slug + '/index.html')]:
        p = R + path; s = open(p, encoding='utf8').read(); o = s
        s = re.sub(r'<section class="gh">.*?</section>\n?', '', s, flags=re.S); s = re.sub(r'<script type="application/json" id="hm-data">.*?</script>\n?', '', s, flags=re.S); s = re.sub(r'<script src="/assets/js/gallery-modal.js" defer></script>\n?', '', s)
        d = data(game, l); title, hint = TXT[(game, l)]
        lis = ''.join('<li><button type="button" class="hc" data-i="%d" aria-haspopup="dialog"><img class="hc-face" src="%s" alt="" width="48" height="48" loading="lazy" decoding="async"%s>'
                      '<span class="hc-t"><b>%s</b><span>%s</span></span><i class="hc-go" aria-hidden="true">›</i></button></li>'
                      % (i, h['thumb'], '' if game == 'ws' else ' style="object-fit:cover;object-position:50% 15%"', h['name'], h['role']) for i, h in enumerate(d['heroes']))
        sec = '<section class="gh"><div class="wrap"><h2>%s</h2><p class="t-hint">%s</p><ul>%s</ul></div></section>\n' % (title, hint, lis)
        i = s.index('<div class="gal"'); j = s.rfind('<section', 0, i); s = s[:j] + sec + s[j:]
        if 'css/heroes.css' not in s: s = s.replace('<link rel="stylesheet" href="/assets/css/gp2.css">', '<link rel="stylesheet" href="/assets/css/gp2.css">\n<link rel="stylesheet" href="/assets/css/heroes.css">\n<link rel="stylesheet" href="/assets/css/gh.css">', 1)
        js = '<script type="application/json" id="hm-data">%s</script>\n<script src="/assets/js/gallery-modal.js" defer></script>\n' % json.dumps(d, ensure_ascii=False, separators=(',', ':'))
        s = s.replace('<footer', js + '<footer', 1)
        if s != o: open(p, 'w', encoding='utf8').write(s); n += 1
print('pages traitées :', n)
