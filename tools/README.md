# Outils du site

Le site est écrit en français dans `index.html`. Les dossiers `en/ es/ pt/ th/ zh/ ja/ ko/ ru/ id/` sont GÉNÉRÉS : ne pas les modifier à la main.

## Régénérer toutes les langues
Copier `build_en.py build_i18n.py v3_extra.py v4_home.py v5_pages.py v6_seo.py i18n_*.py` dans `/home/claude`, puis `python3 build_i18n.py`.
Actualités : modifier `tools/news.json` (entrée en haut de liste) puis relancer le build : accueils, page /news/ ou /fr/actualites/, flux RSS et sitemap se mettent à jour.
Codes Google/Bing : `tools/seo_config.json`. Images de partage : `python3 tools/make_og.py`. Contrôle complet : `python3 tools/seo_check.py`.
Étape finale après le build : `python3 tools/v7_css.py` (CSS partagé + cibles tactiles). Fiches jeux : `python3 tools/check_games.py` ; `"published": false` = jeu invisible partout.
Après v7 : `python3 tools/v8_legal.py` (pages juridiques, pied de page, achat) puis `python3 tools/v10_home.py` (accueil maquette 3 : hero, carrousel vedette, cartes ; sauvegarde du hero d'origine dans tools/h2cache) puis `python3 tools/v9_gallery.py` (galeries construites depuis `art/`).
Rapport d'audit : `tools/AUDIT-FINAL.md`.

## Ajouter un jeu
1. Copier `games/_exemple.json` en `games/<slug>.json` et le remplir (les langues absentes retombent sur l'anglais, puis le français).
2. Mettre les images dans `assets/` (cover = affiche verticale, webp).
3. Relancer `python3 build_i18n.py`, tester, pousser sur `main`.
Quand il y a plus de trois jeux : mettre à jour la phrase « Trois jeux, trois univers » et les descriptions dans les listes de traduction.

## Compteur de visites
Cloudflare Web Analytics : mettre le jeton dans `config.json` (`analytics_token`), relancer le build. Sans jeton, aucun compteur n'est chargé.

## Étapes 12 à 15 (héros, bannières, captures, fiches des jeux)
- `v12_heroes.py` : cartes « héros » cliquables de l'accueil (fiche : `assets/js/heroes.js`, `assets/css/heroes.css`). Images : `extract_heroes.py` (Latorche).
- `v13_banners.py` : bannières 16:9 (`assets/b/<jeu>.webp`) dans le carrousel de l'accueil.
- `v14_phone.py` : captures du cadre téléphone en fr/en/es/pt (`assets/t-<lang>-<scène>.webp`, prises dans le jeu).
- `v15_gameheroes.py` : fiches cliquables des pages Infinite Dungeon et WYRMSTORM (`assets/js/gallery-modal.js`, `gh.css`). Images : `extract_gamesheroes.py`.
- `make_og2.py` : images de partage (remplace `make_og.py` / `make_og_home.py`).

## Étapes 16 à 18 (post-traitements, à lancer dans l'ordre après v15)
- `v16_id_unavailable.py` : Infinite Dungeon « momentanément indisponible » (`UNAVAILABLE = True`).
- `v17_intro.py` : intro avec porte « touche pour entrer », sons ElevenLabs (`assets/audio/intro-*.mp3`) et musique au premier tap.
- `v18_chibi.py` : **Chibi Legends remplace Infinite Dungeon sur l'accueil** (10 langues : carrousel, carte, chiffre clé, section détaillée, JSON-LD, titres), crée les fiches `/chibi-legends-game/` et `/fr/chibi-legends-game/` (copiées du modèle WYRMSTORM), remplace la carte « autres jeux », le sitemap, la 404 et le dossier presse, et remplace la 3e jaquette du mur de l'intro. La démo jouable reste dans `/chibi-legends/` (PWA, ne pas toucher). Infinite Dungeon garde sa fiche.
  Images : `assets/cl-cover.webp`, `assets/cl-icon.webp`, `assets/b/chibi-legends.webp`, captures `assets/cl-<fr|en>-<combat|heroes|team|skills|quests|album|shop>.webp` + miniatures `assets/th/cl-*`. Originaux : `art/Chibi-Legends/`. Partage : `python3 -I tools/make_og2.py`.
- `v20_infinite_dungeon.py` : réintègre Infinite Dungeon au catalogue après v18 et v19 et réactive les liens itch.io.
- `v21_prices.py` : à lancer EN DERNIER (après v19 et les v20) : prix 4,99 € Chibi Legends + WYRMSTORM (PayPal.me maxlolfr2) et pastille « Démo gratuite » sur les cartes payantes. Les JSON de `games/` portent aussi ce prix.
- `v22_clean.py` : à lancer EN DERNIER (après v21) : retire taxes/TVA (encart d'achat, mentions légales) et remplit la livraison (code par e-mail PayPal sous 48 h).
