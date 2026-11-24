#!/usr/bin/env python3 -I
"""v19 — Charte « Maxlol Signature — Gaming Premium ».
À lancer en DERNIER (après v18). Idempotent.
 1. charge assets/css/signature.css en dernier sur toutes les pages qui ont une feuille de style du site ;
 2. accueils (10 langues) : ajoute une miniature de jeu devant chaque actualité.
Usage : python3 -I tools/v19_signature.py [--check]
"""
import re, sys, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
VERSION = "9"
LINK = '<link rel="stylesheet" href="/assets/css/signature.css?v=%s">' % VERSION
SKIP = ("chibi-legends/", "chibi-test/", "backend/", "art/", "tools/", ".git/")

THUMBS = [  # (fragment dans l'URL de l'actu, image)
    ("wyrmstorm", "/assets/ws-cover.webp"),
    ("derniere-torche", "/assets/t-icon.webp"),
    ("torch", "/assets/t-icon.webp"),
    ("gravity", "/assets/gt-icon.webp"),
    ("chibi", "/assets/cl-icon.webp"),
    ("infinite", "/assets/id-icon.webp"),
]
DEFAULT_THUMB = "/assets/icon-192.png"

def thumb_for(href):
    h = href.lower()
    for frag, img in THUMBS:
        if frag in h:
            return img
    return DEFAULT_THUMB

def add_css(s):
    s = re.sub(r'\n?<link rel="stylesheet" href="/assets/css/signature\.css[^"]*">', "", s)
    ms = list(re.finditer(r'<link rel="stylesheet" href="/assets/css/[^"]+">', s))
    if not ms:
        return s
    e = ms[-1].end()
    return s[:e] + "\n" + LINK + s[e:]

def add_thumbs(s):
    def li(m):
        block = m.group(0)
        if "nthumb" in block:
            return block
        href = re.search(r'<a href="([^"]*)"', block)
        img = thumb_for(href.group(1) if href else "")
        return block.replace("<li>", '<li><img class="nthumb" src="%s" alt="" width="56" height="56" loading="lazy" decoding="async">' % img, 1)
    return re.sub(r'<li><time.*?</li>', li, s, flags=re.S) if 'class="nl"' in s else s

def main():
    check = "--check" in sys.argv
    changed = 0
    for p in sorted(ROOT.rglob("*.html")):
        rel = p.relative_to(ROOT).as_posix()
        if rel.startswith(SKIP):
            continue
        s = p.read_text(encoding="utf-8")
        n = add_css(s)
        if "/assets/css/home2.css" in n:
            n = add_thumbs(n)
        if n != s:
            changed += 1
            if not check:
                p.write_text(n, encoding="utf-8")
    print(("à modifier : " if check else "modifié : ") + str(changed) + " fichiers")

if __name__ == "__main__":
    main()
