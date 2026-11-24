# Inscrire le site (depuis ton téléphone)
## Google Search Console
1. Ouvre search.google.com/search-console, connecte-toi, « Ajouter une propriété » → **Préfixe d'URL** → `https://maxlolgames.com/`.
2. Méthode de validation : **Balise HTML**. Copie la valeur de `content="…"` et envoie-la moi : je la place dans `tools/seo_config.json` et je republie.
3. Quand c'est validé : menu « Sitemaps » → ajoute `sitemap.xml`.
4. « Inspection d'URL » : colle les 4 pages de jeux et `/news/`, puis « Demander une indexation ».
## Bing Webmaster Tools
1. bing.com/webmasters → connecte-toi → **Importer depuis Google Search Console** (le plus simple, après l'étape Google).
2. Vérifie que le sitemap `https://maxlolgames.com/sitemap.xml` est bien présent.
## Ensuite
Dis-moi chaque nouveauté (jeu, version, prix) : j'ajoute une ligne dans `tools/news.json` et tout se met à jour (accueil, actualités, flux RSS, sitemap).
