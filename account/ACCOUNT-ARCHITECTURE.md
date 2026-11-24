# Compte joueur universel Maxlol Games — architecture (prototype isolé)

## Choix
- **Supabase** (Auth + Postgres + RLS) pour l'identité et les sauvegardes cloud : compatible avec un site statique GitHub Pages (appels HTTPS directs depuis le navigateur, aucun SDK obligatoire).
- Les **achats restent dans le serveur de paiement** (`backend/`, Netlify) : c'est lui qui détient les secrets PayPal. Il ne fait confiance qu'à un **JWT Supabase vérifié** (JWKS ES256/RS256, ou secret HS256) pour rattacher une licence à un compte.
- Rien n'est imposé : **les jeux gratuits se jouent sans compte**, et un achat reste utilisable sans compte (clé de licence / jeton signé).

```
Navigateur (jeu / site)                     Supabase (gratuit)                 Netlify (gratuit)
 maxlol-account.js ── e-mail + code/lien ─► Auth (GoTrue)
        │ JWT ──────── put_save / lecture ─► Postgres + RLS (saves, historique)
        └ JWT ─────────────────────────────────────────────────────────────► /api/account/* (vérifie le JWT)
 maxlol-pay.js ───── achat PayPal ──────────────────────────────────────────► /api/orders/* + webhook PayPal
```

## Fonctions demandées
| Besoin | Réalisation | Testé |
|---|---|---|
| Connexion e-mail / lien magique | `signInEmail` (lien **et** code à 6 chiffres : le code marche quand le lien s'ouvre dans un autre navigateur) | simulation seulement |
| Bibliothèque personnelle | `/api/account/library` : achats + état + jeton frais par licence | A3 |
| Historique d'achats PayPal | idem (commande, montant, statut : COMPLETED/REFUNDED…) | A3, A5 |
| Restauration des contenus | se connecter suffit (jeton rendu par la bibliothèque) ; sinon clé / transaction+e-mail | A4 |
| Sauvegardes cloud facultatives | table `saves` (1 ligne par jeu/emplacement, 256 Ko max) | Q1–Q8, S1–S3 |
| Droits d'accès sécurisés | RLS : chacun ne lit que ses lignes ; **aucune écriture directe**, tout passe par `put_save` (contrôle de version) | Q3–Q5 |
| Sync multi-appareils | version par sauvegarde + `planSync` ; téléchargement auto seulement si le local n'a pas changé | S2, S3 |
| Migration localStorage | `migrate` = première synchro, jamais automatique, aucun écrasement | S1, P1 |
| Export / suppression | `export_my_data`, `delete_my_game_data`, `/api/account/delete` (compte Auth supprimé côté serveur) ; achats détachés, pas détruits (trace comptable) | Q9, Q10, A6 |
| Jouer sans compte | aucun code du jeu ne dépend du compte ; la synchro est un ajout | par conception |

## « Ne jamais écraser sans confirmation »
1. Premier rattachement d'un appareil avec deux sauvegardes différentes → **toujours** une question (4 choix : garder local / prendre cloud / garder les deux / annuler).
2. Modifié des deux côtés → question. Annuler ne change rien (S4).
3. Avant tout remplacement local : **copie de secours locale** (`mxl-backup:…`).
4. Avant tout remplacement cloud : l'ancienne version va dans l'**historique (5 versions)**, restaurable (Q6, S5, S8).
5. Le serveur refuse une écriture dont la version de base est périmée (course entre deux téléphones : Q2, S7).

## Contrat d'intégration pour un jeu
`adapter = { game:'torch', slot:'main', read(){ return localStorage.getItem('derniere-torche-v1') }, write(raw){ localStorage.setItem('derniere-torche-v1', raw); /* recharger l'état */ } }`
Synchroniser aux moments sûrs (menu, fin d'expédition), jamais en plein combat. Un nouveau jeu = un adapter de 4 lignes + une entrée `CATALOG` côté paiement. Pas de monnaie virtuelle commune (hors périmètre).

## Limites de l'offre gratuite Supabase (recherche du 24/11/2026, sources en réponse)
- 2 projets actifs, **500 Mo de base**, 1 Go de fichiers, 5 Go de trafic sortant, **50 000 utilisateurs actifs/mois**.
- **Mise en pause après 7 jours d'inactivité** (données conservées, service coupé jusqu'à réactivation) ; **pas de sauvegardes automatiques**.
- **E-mails d'authentification intégrés : ~2 par heure** → inutilisable en production : prévoir un SMTP externe gratuit (à choisir et vérifier au moment du réglage).
- Pro : **à partir de 25 $/mois**, 8 Go de base, 100 000 utilisateurs actifs, plus de mise en pause, sauvegardes ; ensuite ≈ 0,00325 $ par utilisateur actif au-delà de 100 000.

## Estimation des coûts (hypothèses à valider : taille réelle des sauvegardes non mesurée)
Hypothèse : sauvegarde moyenne 30 Ko, 5 versions d'historique, ~2 jeux synchronisés par joueur ⇒ ≈ 0,36 Mo/joueur (avant compression PostgreSQL).
| Joueurs avec cloud actif | Facteur limitant | Coût estimé |
|---|---|---|
| jusqu'à ~1 400 (≈ 5 000+ avec compression/historique réduit à 3) | 500 Mo de base | 0 $ |
| 1 400 → 22 000 | base 8 Go (Pro) | ≈ 25 $/mois |
| 22 000 → 100 000 | Pro + stockage supplémentaire (0,125 $/Go) | ≈ 25–75 $/mois |
| 150 000 utilisateurs actifs | + MAU au-delà de 100 000 | ≈ 25 $ + 160 $ ≈ 185 $/mois |
Trafic : une synchro ≈ 30–40 Ko ⇒ les 5 Go gratuits couvrent ≈ 130 000 synchros/mois.
**Premier mur réel : la mise en pause à 7 jours** et les **e-mails** (pas le nombre de joueurs). Parade gratuite : tâche GitHub Actions hebdomadaire qui interroge la base + SMTP externe.

## Sécurité et vie privée
- Clé `anon` publique (normale) ; clé `service_role` et `SUPABASE_SERVICE_KEY` **uniquement** dans les variables Netlify.
- JWT : audience, émetteur, rôle, expiration vérifiés ; `alg:none` et HS256 forgé refusés (A1).
- Données stockées : e-mail (Auth), profil, sauvegardes. Pas de mot de passe. Export + suppression en self-service.
- Une sauvegarde cloud n'est **pas anti-triche** (le joueur modifie sa propre sauvegarde) : acceptable en solo, à ne pas utiliser pour des classements.

## Limites connues / non testé
- **Jamais testé contre un vrai projet Supabase** : l'envoi d'e-mails, le lien magique réel et les quotas n'ont été vus qu'en simulation. Le SQL, lui, a été exécuté sur un vrai Postgres (WASM) avec les mêmes rôles/claims que Supabase.
- Synchro = remplacement de la sauvegarde entière (pas de fusion fine).
- Adapters des 7 jeux à écrire (seule La Dernière Torche est identifiée : clé `derniere-torche-v1`).
- Pages légales (confidentialité, RGPD) à publier **avant** d'ouvrir les comptes.

## Mise en route (quand tu valides)
1. Créer un projet Supabase gratuit ; exécuter `schema.sql` ; régler Auth (URL du site, redirections autorisées, SMTP).
2. Variables Netlify : `SUPABASE_URL`, `SUPABASE_JWT_SECRET` (si HS256), `SUPABASE_SERVICE_KEY`.
3. Renseigner `window.MXL_CFG = { url, anonKey, payApi }` dans le prototype pour l'essayer en réel.
