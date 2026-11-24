# SEO technique — maxlolgames.com (24/11/2026)

## État initial (audit)
Déjà en place : robots.txt + sitemap, canonical et hreflang sur les accueils (10 langues), Open Graph + JSON-LD Organization/WebSite, image 1200×630 pour l'accueil, un seul h1 par page, 404 en noindex.
Manques trouvés : pas d'image de partage par jeu ; titres/descriptions trop longs (jusqu'à 311 car.) dans 8 langues ; JSON-LD de l'accueil limité à 1 jeu avec une ancre ; liens du bloc actualités vers des ancres seulement ; pas de page ni de flux d'actualités ; sitemap sans actualités ; robots.txt n'écartait pas les dossiers techniques (backend, account, pay, tools) ; page presse sans balises de partage ; 20 balises `<img>` inutiles dans l'intro ; 4 images de cartes sans texte alternatif ; pas d'emplacement pour les codes Google/Bing.

## Corrigé (gratuit, sans changement de design)
- Pages indexables dédiées par jeu (fr + en), titres 56–66 car., descriptions ≤ 158 car., mots-clés naturels (RPG de donjon, roguelite, puzzle, shoot'em up).
- Images de partage 1200×630 par jeu (`assets/og/`), avec dimensions, type et texte alternatif ; twitter:card large.
- Données structurées : Organization (identifiant unique), VideoGame (offre gratuite + offre payante pour la Torche, langues réelles), ItemList des jeux sur l'accueil, FAQPage, BreadcrumbList, Blog/BlogPosting. Aucun faux avis ni note.
- hreflang : accueils = 10 langues (réciproques) ; jeux et actualités = fr/en seulement (seules vraies traductions) + x-default.
- Titres et descriptions courts dans les 10 langues pour l'accueil.
- Actualités : `tools/news.json` → bloc de l'accueil, page `/news/` et `/fr/actualites/`, flux `/feed.xml` et `/fr/feed.xml`, sitemap.
- Sitemap régénéré (21 URL, lastmod réels), robots.txt (dossiers techniques exclus), 404 avec liens, page presse complétée.
- Doublons : intro réduite de 40 à 20 images dans le HTML (le reste est dupliqué par le script).
- Emplacements prêts pour les codes de vérification Google / Bing (`tools/seo_config.json`).

## Contrôle automatique (`python3 tools/seo_check.py`)
21 pages : 0 erreur, 0 avertissement (canonical = URL du sitemap, hreflang réciproques, JSON-LD valide, images de partage 1200×630, liens internes, alt, h1, robots/sitemap cohérents, flux RSS valides). Rendu testé sur iPhone/Android/ordinateur : aucune erreur JS, aucun débordement.

## Limites / à faire côté propriétaire
- Search Console et Bing : inscription impossible sans ton compte (voir SEO-GUIDE.md).
- Le CSS reste dans chaque page (design en fichier unique) : le sortir dans un fichier partagé réduirait chaque page d'environ la moitié, mais touche au design : non fait.
- Pas de vidéo/bande-annonce : donc pas de balisage VideoObject. Pas d'avis : donc pas de notes.
- Pages de jeux et actualités uniquement en fr/en : les 8 autres langues pointent vers l'accueil traduit.
- HTTPS forcé et redirection www → domaine nu : à vérifier dans les réglages GitHub Pages / DNS (non vérifiable depuis mon environnement).
- Le classement Google ne peut pas être garanti ; l'indexation prend de quelques jours à quelques semaines.
