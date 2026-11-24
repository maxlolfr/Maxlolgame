# Audit sécurité PayPal — Maxlol Games (24/11/2026)

## 1. Architecture AVANT
- Site : pages statiques GitHub Pages. PayPal = **un simple lien PayPal.me** (`paypal.me/maxlolfr2/7.99EUR`) ; aucun backend, aucune API PayPal, aucun webhook.
- Jeu La Dernière Torche (repo `Latorche`) : « démo » et « complet » sont **deux builds** choisis par la constante `D.DEMO` (mondes 1–5 seulement si `true`). Aucun mécanisme d'achat, de licence ni de vérification. Le passage démo → complet se fait par un code de sauvegarde `LDS1:` (base64 du JSON, **non signé**).
- Un « Pass Confort » (1,99 $ / 69 THB) est annoncé dans le jeu : « paiement bientôt ». Désactivé dans le catalogue serveur.

## 2. Constats (existant)
| # | Gravité | Constat |
|---|---|---|
| A | **Critique** | Aucune livraison automatisée : PayPal.me ne notifie personne. Rien ne prouve qu'un paiement a eu lieu. |
| B | **Critique (à vérifier)** | Le dépôt du jeu contient `D.DEMO=false` et `D.ADMIN=true` (mode admin : « tout débloquer », +or). Si ce build est celui publié sur la-derniere-torche.netlify.app, le « jeu gratuit » est en réalité le jeu complet avec un mode triche. Le site n'a pas pu être consulté depuis mon environnement. Le commentaire du code dit « METTRE false pour la version en vente ». |
| C | Élevée | Code de sauvegarde `LDS1:` non signé : on peut y modifier or, héros, progression (le flag `admin` est remis à false à l'import, mais pas le reste). |
| D | Élevée | Compte PayPal **personnel** : l'API Commandes/Webhooks exige un compte **Business**. Impossible d'automatiser ou de vérifier un paiement avec le compte actuel. |
| E | Moyenne | Pas de restauration d'achat, pas de remboursement géré. |
| F | Faible | Aucune clé secrète PayPal trouvée dans les dépôts (bon point). |

## 3. Architecture APRÈS (`backend/`, commune à tous les jeux)
Netlify Functions + Netlify Blobs (offre gratuite), site Netlify séparé `maxlol-pay`. Le site GitHub Pages reste inchangé.
- `POST /api/orders/create` : le client envoie seulement un **id produit** ; prix/devise/destinataire viennent du **catalogue serveur**.
- `POST /api/orders/capture` : capture serveur, puis contrôle de statut COMPLETED, montant, devise, produit, destinataire. Livraison idempotente.
- `POST /api/paypal-webhook` : signature vérifiée via l'API PayPal `verify-webhook-signature` (corps brut), événements dédupliqués. Gère COMPLETED, PENDING, DENIED/DECLINED, REFUNDED, REVERSED.
- Licence : clé `MXL-XXXX-XXXX-XXXX-XXXX` **dérivée** (HMAC) — jamais stockée en clair ; jeton d'accès **ES256 signé** (14 jours), vérifié dans le navigateur avec la clé publique.
- Restauration : clé de licence, ou **ID de transaction PayPal + e-mail PayPal**. Limitation de tentatives par IP.
- `licence.accountId` prévu pour le futur **compte joueur universel** (Prompt 4) : rattachement unique licence → compte.
- Client commun `assets/maxlol-pay.js` + pages `pay/return/` et `pay/cancel/`.
- Secrets : variables d'environnement Netlify uniquement ; aucune clé dans le dépôt/le client ; réponses d'erreur génériques.

## 4. Les 10 points demandés
1 Création/capture serveur : OK (S1, S3). 2 Secrets : OK (S21). 3 Validation prix/devise/produit/destinataire : OK (S1, S2, S9). 4 COMPLETED avant livraison : OK (S3, S6, S7, S8). 5 Webhooks : OK (S12) — via API PayPal. 6 Double livraison/réutilisation : OK (S4, S5, S11, S12). 7 Restauration : OK (S16, S17). 8 Annulé/refusé/pending/remboursé : OK (S6–S8, S14, S15). 9 localStorage : OK côté jeton (S19, C1, C2) — **limite ci-dessous**. 10 Association compte/récupération : clé + transaction/e-mail OK (S16) ; compte universel préparé (S20).

## 5. Tests exécutés : 26/26 réussis (voir tableau dans la réponse)
**Important : ils tournent contre un simulateur PayPal local** (même contrat REST), pas contre le vrai Sandbox : aucun identifiant Sandbox n'est disponible dans mon environnement. `test/run-sandbox.mjs` rejoue création/capture contre le vrai Sandbox dès que les identifiants sont fournis. Bugs trouvés par les tests et corrigés : contrôle produit trop permissif ; verrou de capture non atomique.

## 6. Limites restantes (honnêtes)
- Le jeu est du JavaScript côté client : un jeton signé empêche de **fabriquer** un achat, mais un joueur déterminé peut **modifier le code** (`D.DEMO`). Seule protection forte : servir les mondes 6–20 (paquets `www/packs`) **depuis le serveur, sur présentation du jeton**. À faire si tu veux aller plus loin.
- Le mode admin du jeu doit être désactivé (`D.ADMIN=false`) dans tout build public.
- Code de sauvegarde `LDS1:` à signer côté serveur (ou à limiter) si la triche sur la progression compte.
- Un remboursement coupe l'accès au prochain `refresh` en ligne ou à l'expiration du jeton (14 jours max).
- Limitation de débit simple (par IP/heure) ; à renforcer si abus.
- Non testé : Sandbox réel, appel HTTP de bout en bout sur Netlify (seulement fumée locale des règles d'origine/CORS).

## 7. Avant mise en production (rien n'est déployé)
Compte PayPal Business ; app Sandbox puis Live ; webhook configuré ; variables Netlify ; clé publique figée dans le site ; CSP du site (`connect-src`) ; boutons du site basculés de PayPal.me vers `MaxlolPay.buy('torch-full')`.
