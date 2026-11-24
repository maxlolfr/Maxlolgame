# Outils du site

Le site est écrit en français dans `index.html`. Les dossiers `en/ es/ pt/ th/ zh/ ja/ ko/ ru/ id/` sont GÉNÉRÉS : ne pas les modifier à la main.

## Régénérer toutes les langues
Copier `build_en.py build_i18n.py v3_extra.py v4_home.py v5_pages.py v6_seo.py i18n_*.py` dans `/home/claude`, puis `python3 build_i18n.py`.
Actualités : modifier `tools/news.json` (entrée en haut de liste) puis relancer le build : accueils, page /news/ ou /fr/actualites/, flux RSS et sitemap se mettent à jour.
Codes Google/Bing : `tools/seo_config.json`. Images de partage : `python3 tools/make_og.py`. Contrôle complet : `python3 tools/seo_check.py`.
Étape finale après le build : `python3 tools/v7_css.py` (CSS partagé + cibles tactiles). Fiches jeux : `python3 tools/check_games.py` ; `"published": false` = jeu invisible partout.
Après v7 : `python3 tools/v8_legal.py` (pages juridiques, pied de page, achat) puis `python3 tools/v9_gallery.py` (galeries construites depuis `art/`).
Rapport d'audit : `tools/AUDIT-FINAL.md`.

## Ajouter un jeu
1. Copier `games/_exemple.json` en `games/<slug>.json` et le remplir (les langues absentes retombent sur l'anglais, puis le français).
2. Mettre les images dans `assets/` (cover = affiche verticale, webp).
3. Relancer `python3 build_i18n.py`, tester, pousser sur `main`.
Quand il y a plus de trois jeux : mettre à jour la phrase « Trois jeux, trois univers » et les descriptions dans les listes de traduction.

## Compteur de visites
Cloudflare Web Analytics : mettre le jeton dans `config.json` (`analytics_token`), relancer le build. Sans jeton, aucun compteur n'est chargé.
