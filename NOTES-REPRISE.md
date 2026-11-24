# Reprise — maxlolgames.com (état au 24 nov. 2026, soir)
Répondre en français. Max travaille uniquement depuis le téléphone ; Claude fait tout (commit, push, vérification en ligne).
Production = branche `main` (GitHub Pages). Push : `git fetch origin main`, rebase/merge, `git -c push.negotiate=true push origin HEAD:main`. Une autre session pousse aussi (Chibi Legends) : toujours fetch avant.

## Chaîne de génération (tools/, voir tools/README.md)
build_en/i18n → v7_css → v8_legal → v9_gallery → v10_home → v11_gamepages → v12 héros → v13 bannières → v14 captures téléphone → v15 fiches héros → v16 ID indisponible → v17 intro → **v18 Chibi Legends**. Tous idempotents. Contrôle : `python3 -I tools/seo_check.py` (doit donner 0 erreur / 0 avertissement). Partage : `python3 -I tools/make_og2.py`.

## Fait aujourd'hui
- Bannières, héros cliquables, captures téléphone traduites, images de partage, fiches héros/dragons, intro v2 avec sons ElevenLabs.
- Infinite Dungeon : « momentanément indisponible », retiré de l'accueil ; sa fiche reste en ligne.
- **Chibi Legends remplace ID sur l'accueil (10 langues)** : carrousel, cartes, chiffre « 130 entrées de bestiaire ». Section détaillée = `tools/games/chibi-legends-rpg.json` (autre session, prix 3,99 €). Démo jouable : `/chibi-legends/` (PWA, ne pas toucher, ni `/chibi-test/`).
- Fiches Chibi Legends FR/EN : `/chibi-legends-game/`, `/fr/chibi-legends-game/` (captures `assets/cl-<fr|en>-*.webp`, originaux `art/Chibi-Legends/`). **En noindex et hors sitemap** (Max veut Chibi caché des moteurs pour l'instant).

## À trancher / à fournir par Max
- Prix de Chibi Legends : 3,99 € (accueil) vs « gratuit » (politique de confidentialité).
- Bannière 16:9 de Chibi Legends : actuelle = recadrage agrandi de l'affiche ; proposer un prompt ChatGPT/Gemini (indiquer lequel est meilleur, image de référence en fichier).
- Infos légales manquantes (marqueurs dans tools/legal/facts.json), choix du paiement (PayPal.me maxlolfr2 pour l'instant), pages légales hors FR/EN en anglais.
- Max a envoyé `Maxlol-Games-32-visuels.zip` (export de la galerie ID/Torche/WYRMSTORM) sans consigne : demander quoi en faire.

## Prochaine étape demandée
**Refonte graphique du site** (nouvelle fenêtre). Rien à changer sur maxlolgames.com avant validation de Max si possible via le site test Netlify `maxlolgames-test`.
Règles : annonce + estimation de coût + liste de tâches dès le début ; barre de progression et coût en tokens dans chaque réponse ; demander l'accord avant de générer des sons payants hors site.
