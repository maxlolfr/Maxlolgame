"""Restore the playable Infinite Dungeon prototype after v18_chibi.py."""
import json
import re
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOMAIN = "https://maxlolgames.com"
PLAY_URL = "https://maxlolfr.itch.io/infinite-dungeon"
OLD_PLAY_URL = "https://maxlolfr.github.io/Stepquest/infinite-dungeon-v08/"
NAME = "Infinite Dungeon"
OLD_COUNT = [
    "Four games, four worlds.", "Quatre jeux, quatre univers.", "Cuatro juegos, cuatro mundos.",
    "Quatro jogos, quatro universos.", "สี่เกม สี่โลก", "四款游戏，四个世界。",
    "4つのゲーム、4つの世界。", "네 개의 게임, 네 개의 세계.",
    "Четыре игры, четыре мира.", "Empat game, empat dunia.",
]
# Genre, short pitch, demo button and catalogue count.
COPY = {
    "en": ("Fantasy roguelite", "Choose three heroes, climb 100 floors and face 10 bosses in automatic battles.", "Play the demo", "Five games, five worlds."),
    "fr": ("Roguelite fantasy", "Choisis trois héros, gravis 100 étages et affronte 10 boss en combat automatique.", "Jouer à la démo", "Cinq jeux, cinq univers."),
    "es": ("Roguelite de fantasía", "Elige tres héroes, sube 100 pisos y enfréntate a 10 jefes en combates automáticos.", "Jugar a la demo", "Cinco juegos, cinco mundos."),
    "pt": ("Roguelite de fantasia", "Escolha três heróis, suba 100 andares e enfrente 10 chefes em combates automáticos.", "Jogar a demo", "Cinco jogos, cinco universos."),
    "th": ("โร้กไลต์แฟนตาซี", "เลือกฮีโร่สามคน ไต่หอคอย 100 ชั้น และสู้กับบอส 10 ตัวด้วยการต่อสู้อัตโนมัติ", "เล่นเดโม", "ห้าเกม ห้าโลก"),
    "zh": ("奇幻轻度肉鸽", "选出三位英雄，登上百层高塔，在自动战斗中挑战十位首领。", "试玩", "五款游戏，五个世界。"),
    "ja": ("ファンタジー・ローグライト", "3人の英雄を選び、100階の塔を登ってオートバトルで10体のボスに挑もう。", "デモを遊ぶ", "5つのゲーム、5つの世界。"),
    "ko": ("판타지 로그라이트", "영웅 3명을 골라 100층 탑을 오르고 자동 전투로 보스 10명을 상대하세요.", "데모 플레이", "다섯 개의 게임, 다섯 개의 세계."),
    "ru": ("Фэнтезийный рогалик", "Выбери трёх героев, пройди 100 этажей башни и победи 10 боссов в автобоях.", "Играть в демо", "Пять игр, пять миров."),
    "id": ("Roguelite fantasi", "Pilih tiga pahlawan, daki menara 100 lantai, dan hadapi 10 bos dalam pertarungan otomatis.", "Mainkan demo", "Lima game, lima dunia."),
}


def page_path(lang):
    return "/fr/infinite-dungeon/" if lang == "fr" else "/infinite-dungeon/"


def play_link(label):
    return f'<a class="btn main" href="{PLAY_URL}" target="_blank" rel="noopener">{escape(label)}</a>'


def restore_home(html, lang, old_count):
    genre, pitch, play, count = COPY[lang]
    path = page_path(lang)
    if 'data-game="infinite-dungeon"' in html:
        return html

    for card_class, image, width, height, title_tag in (
        ("fslide", "/assets/b/infinite-dungeon.webp", 1600, 900, "p"),
        ("scard", "/assets/id-title.webp", 640, 960, "h3"),
    ):
        pattern = rf'(<article class="{card_class}"[^>]*>.*?</article>)(?=</div>)'
        template = next(match for match in re.finditer(pattern, html, re.S)
                        if 'chibi-legends-game/"' in match[0])
        label = re.search(r'<a class="btn ghost" href="[^"]*chibi-legends-game/">([^<]+)</a>', template[0])[1]
        card = (
            f'<article class="{card_class}" data-game="infinite-dungeon" style="--a:#F0B94A">'
            f'<a class="simg" href="{path}" aria-label="{NAME}"><img src="{image}" alt="{NAME}" '
            f'width="{width}" height="{height}" loading="lazy" decoding="async"></a>'
            f'<div class="sbody"><p class="sgenre">{escape(genre)}</p>'
            f'<{title_tag} class="sname"><a href="{path}">{NAME}</a></{title_tag}>'
            f'<p class="sdesc">{escape(pitch)}</p><div class="sact">{play_link(play)}'
            f'<a class="btn ghost" href="{path}">{label}</a></div></div></article>'
        )
        html = html[:template.end()] + '\n        ' + card + html[template.end():]

    html = re.sub(r'(<div class="fc-dots" id="fcDots"[^>]*>)(?:<i></i>)+(</div>)',
                  lambda m: m[1] + '<i></i>' * 5 + m[2], html)
    html = html.replace(old_count, count)
    html = re.sub(r'(<h1 id="titre"[^>]*>)([^<]+)(</h1>)',
                  lambda m: m[1] + m[2] + ", " + NAME + m[3], html)

    def add_game(match):
        data = json.loads(match[2])
        game = {
            "@type": "VideoGame", "@id": DOMAIN + path + "#game", "name": NAME,
            "url": DOMAIN + path, "description": pitch, "genre": genre,
            "image": DOMAIN + "/assets/og/infinite-dungeon.jpg",
            "isAccessibleForFree": True, "publisher": {"@id": DOMAIN + "/#studio"},
        }
        catalogue = next(node for node in data["@graph"] if node["@type"] == "ItemList")
        items = catalogue["itemListElement"]
        items.append({"@type": "ListItem", "position": len(items) + 1, "item": game})
        return match[1] + json.dumps(data, ensure_ascii=False) + match[3]

    return re.sub(r'(<script type="application/ld\+json">)(.*?)(</script>)', add_game, html, count=1, flags=re.S)


def restore_game_page(html, lang):
    play = "Jouer gratuitement sur itch.io" if lang == "fr" else "Play free on itch.io"
    html = re.sub(r'<span class="btn main unavail"[^>]*>[^<]+</span>', play_link(play), html)
    html = re.sub(r'<p class="unavail-note">[^<]+</p>', "", html)
    html = re.sub(r'<a class="btn main"[^>]*data-link="id-play"[^>]*>.*?</a>', play_link(play), html, flags=re.S)
    html = html.replace(OLD_PLAY_URL, PLAY_URL)
    for before, after in {
        "descend 100 floors": "climb 100 floors",
        "descends 100 étages": "gravis 100 étages",
        "descends le plus loin possible": "gravis le plus d’étages possible",
        "Version 0.8, in development.": "Playable prototype v1.5 on itch.io.",
        "Version 0.8, en développement.": "Prototype jouable v1.5 sur itch.io.",
        "Version 0.8.": "Prototype jouable v1.5 sur itch.io.",
        "Descend. Fuse. Survive.": "Climb. Fuse. Survive.",
        "Descends. Fusionne. Survis.": "Gravis la tour. Fusionne. Survis.",
        "In development (v0.8)": "Playable prototype (v1.5)",
        "En développement (v0.8)": "Prototype jouable (v1.5)",
        "The game offers no purchases for now. It is still in development (version 0.8).": "The playable prototype is free on itch.io.",
        "Aucun achat n&#x27;est proposé dans le jeu pour l&#x27;instant. Le jeu est encore en développement (version 0.8).": "Le prototype jouable est gratuit sur itch.io.",
        "0.8, in development": "1.5, playable prototype",
        "0.8, en développement": "1.5, prototype jouable",
        "No, it is version 0.8, still in development.": "The current playable build is prototype v1.5.",
        "Non, c&#x27;est la version 0.8, encore en développement.": "La version actuellement jouable est le prototype v1.5.",
        "version 0.8": "prototype v1.5",
    }.items():
        html = html.replace(before, after)
    return html


def update(rel_path, transform):
    path = ROOT / rel_path
    original = path.read_text(encoding="utf-8")
    changed = transform(original)
    if changed != original:
        path.write_text(changed, encoding="utf-8")


def add_related_game(html, lang):
    path = page_path(lang)
    if f'<a class="rc" href="{path}"' in html:
        return html
    cards = list(re.finditer(r'<a class="rc" href="[^"]+">.*?</a>', html, re.S))
    last = cards[-1].end()
    genre = escape(COPY[lang][0])
    card = (f'<a class="rc" href="{path}"><span class="ri"><img src="/assets/id-title.webp" '
            f'alt="{NAME}" width="640" height="960" loading="lazy" decoding="async"></span>'
            f'<span><b>{NAME}</b><small>{genre}</small></span></a>')
    return html[:last] + '\n' + card + html[last:]


if __name__ == "__main__":
    for lang, old_count in zip(COPY, OLD_COUNT, strict=True):
        home = "index.html" if lang == "en" else f"{lang}/index.html"
        update(home, lambda html: restore_home(html, lang, old_count).replace(OLD_PLAY_URL, PLAY_URL))
    for lang in ("en", "fr"):
        update(page_path(lang).lstrip("/") + "index.html", lambda html: restore_game_page(html, lang))
        folder = "fr/" if lang == "fr" else ""
        for slug in ("la-derniere-torche", "wyrmstorm", "gravity-turn", "chibi-legends-game"):
            update(f"{folder}{slug}/index.html", lambda html: add_related_game(html, lang))
    update("tools/source_fr.html", lambda html: html.replace(OLD_PLAY_URL, PLAY_URL))
    update("press/index.html", lambda html: html if 'href="/infinite-dungeon/"' in html else html.replace(
        '<div class="grid">', '<p><b>Infinite Dungeon</b>: free fantasy roguelite prototype with a 100-floor tower and automatic battles. '
        '<a href="/infinite-dungeon/">Official game page</a> · <a href="' + PLAY_URL + '">Play on itch.io</a></p>\n<div class="grid">', 1
    ))
