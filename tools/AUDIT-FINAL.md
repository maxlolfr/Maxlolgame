# Audit final Maxlol Games — Prompt 6 (24/11/2026)

Branche : `audit-final-prompt6` (issue de `refonte-boutique` @ 097f0a4). Rien n'est déployé en production.
Site de préproduction : http://maxlolgames-test.netlify.app (protégé par connexion Netlify, noindex) — **non mis à jour** par ce prompt.

## Verdict : NO GO pour la mise en production (3 bloquants, voir ci-dessous)

## Ce qui a réellement été testé (et comment)
- Playwright **Chromium** (émulation mobile) : 28 pages × 8 largeurs (320, 375, 390, 430, 768, 1024, 1280, 1920) = 224 chargements.
- Playwright **WebKit** (moteur de Safari, **simulation Linux ≠ vrai Safari iPhone**) : 28 pages × 4 largeurs (320, 390, 430, 768) = 112 chargements.
- Lighthouse 13 mobile (simulé), serveur local **sans compression gzip**, 3 pages avant/après.
- Contrôle des liens : 550 liens internes + 9 liens externes. Contrôle HTTP direct de la production.
- Comparaison pixel à pixel avant/après (10 pages × 2 tailles).

## Scores Lighthouse mobile (labo, avant → après)
| Page | Perf | Access. | Bonnes pratiques | SEO | LCP | CLS | TBT |
|---|---|---|---|---|---|---|---|
| /fr/ | 94 → 100 | 100 | 100 | 100 | 1,3 → 1,2 s | 0 | 280 → 30 ms |
| /fr/wyrmstorm/ | 97 → 97 | 100 | 100 | 100 | 2,6 s (> 2,5) | 0 | 40 → 0 ms |
| /news/ | 100 → 100 | 100 | 100 | 100 | 1,0 → 0,9 s | 0 | 0 |
Poids transféré /fr/wyrmstorm : 870 → 627 Ko. INP : non mesurable (pas de données réelles).

## Résultats
- Erreurs JavaScript : 24 → **0**. Erreurs réseau / 404 : 0. Liens internes cassés : 0 / 550. Débordement horizontal de page : 0.
- Cibles tactiles < 40 px (pages × résolutions) : 161 → 81 (reste : liens de texte dans les paragraphes, tolérés WCAG 2.2 AA ≥ 24 px).

## Bugs critiques (bloquent la validation commerciale)
1. **HTTP sans redirection HTTPS** : `http://maxlolgames.com/` répond 200. Action (propriétaire) : GitHub > dépôt > Settings > Pages > cocher « Enforce HTTPS ».
2. **Paiement non sécurisé** : tous les boutons Acheter sont des liens `paypal.me/maxlolfr2/<montant>EUR` écrits en dur. Le prix est modifiable dans l'URL, aucun déblocage automatique, aucune vérification du paiement, remboursement/restauration manuels. Le backend `maxlol-pay` (prix côté serveur, licences signées) existe dans `backend/` mais **aucune page ne l'utilise** et la clé publique `MAXLOL_PAY_PUBKEY` n'est définie nulle part. Aucun test Sandbox possible (pas d'identifiants) : tous les scénarios Sandbox demandés = **non réalisés**.
3. **Infinite Dungeon ne se lance pas** : `https://maxlolfr.github.io/Stepquest/infinite-dungeon-v08/` renvoie **404** (Pages hors ligne, probablement dépôt passé en privé). Les autres jeux répondent 200 (Gravity Turn, La Dernière Torche, WYRMSTORM, itch.io).

## Bugs majeurs
- Pages `/pay/return/` et `/pay/cancel/` publiées avec des `%s` non remplacés (page vide + erreur JS) → **corrigé**.
- WYRMSTORM : LCP mobile 2,6 s (objectif 2,5 s) — à optimiser (image d'en-tête).

## Bugs mineurs
- 81 cibles tactiles restantes < 40 px (liens de texte).
- `backend/public/` sans balise viewport (page technique, non indexée).
- Une balise `<img>` sans `src` (emplacement masqué de la visionneuse).
- `chibi-legends/` et `chibi-test/` : copies de 220 Mo chacune (doublon).

## Corrections effectuées
- Pages de paiement reconstruites (aucun texte injecté via innerHTML ; identifiant de commande validé par regex).
- CSS mutualisé : 20 blocs inline (≈ 750 Ko) → 3 fichiers `assets/css/*.<empreinte>.css` (cache long). Design identique : 6 pages desktop identiques au pixel près ; écarts restants = animations / chargement différé.
- Correctifs tactiles (menu, langue, son, fil d'Ariane, liens de pied/de cartes ≥ 44 px) sur mobile uniquement.
- Étape `tools/v7_css.py` (idempotente, à lancer après `build_i18n.py`).
- Jeux : champ `"published": false` (jamais généré : ni catalogue, ni page, ni sitemap, ni flux), modèle `games/_exemple.json` complet (modèle économique, achat, bannière, logo, bande-annonce facultative, SEO), validateur `tools/check_games.py`.

## Chibi Legends
Non indexé (balise noindex, absent du sitemap, aucun lien public). Mais **joignable par URL** en production (200) : noindex n'est pas une protection d'accès. S'il est réellement confidentiel, il faut le retirer du dépôt public ou le mettre derrière un accès protégé.

## La Dernière Torche — démo
Jeu en ligne (la-derniere-torche.netlify.app) : `DEMO = true` (mondes 1 à 5 gratuits), `ADMIN = false` → configuration publique correcte. Le dépôt source (DEMO=false, ADMIN=true) est la version complète/test : ne jamais la déployer telle quelle.

## Tests non réalisables / non réalisés
Vrai Safari iPhone et vrai Chrome Android (aucun appareil) ; orientation paysage ; paiements Sandbox (tous scénarios) ; sauvegardes, anciens saves, comptes joueurs, synchro (non testés dans les jeux) ; galeries/plein écran et changements de langue par clic ; Google Search Console ; en-têtes HTTP (GitHub Pages ne permet pas de les définir : CSP par balise meta seulement) ; cookies/consentement ; INP réel.

## Notes /100 (estimations d'après les mesures ci-dessus)
Design 85 · Ergonomie 78 · Compatibilité mobile 80 · Performances 92 · Sécurité 50 · Référencement 88 · Efficacité commerciale 60 · Maintenabilité 82.

## Recommandations
1. Activer « Enforce HTTPS » (1 clic). 2. Brancher `MaxlolPay` (ou retirer les prix PayPal.me modifiables) avant de vendre. 3. Rendre Infinite Dungeon jouable (hébergement gratuit Netlify) ou masquer son bouton Jouer. 4. Retirer/protéger Chibi Legends. 5. Optimiser l'image d'en-tête de WYRMSTORM. 6. Tester sur ton Honor Magic V5 et sur un iPhone avant GO.

## Fichiers modifiés
`pay/return/index.html`, `pay/cancel/index.html`, 22 pages HTML (CSS externalisé), `press/index.html`, `assets/css/*` (3 nouveaux), `tools/v7_css.py`, `tools/v3_extra.py`, `tools/check_games.py`, `tools/games/_exemple.json`, `tools/AUDIT-FINAL.md`.
