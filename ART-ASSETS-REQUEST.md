# ART-ASSETS-REQUEST — Refonte « Maxlol Signature »

Le site fonctionne avec les illustrations existantes. Ces 3 images amélioreraient le résultat (aucune ne bloque la mise en ligne).
Moteur conseillé pour chacune : **ChatGPT Image** (meilleur pour garder le style et le cadrage des personnages). Fournir les références en fichiers.

| # | Priorité | Fichier | Emplacement | Taille / ratio | Poids max | Format | Fond transparent |
|---|----------|---------|-------------|----------------|-----------|--------|------------------|
| 1 | Haute | `cl-cover.webp` (nouvelle jaquette Chibi Legends) | `assets/cl-cover.webp` | 640×960, 2:3 | 90 Ko | WebP | non |
| 2 | Haute | `chibi-legends.webp` (bannière 16:9) | `assets/b/chibi-legends.webp` | 1600×900, 16:9 | 140 Ko | WebP | non |
| 3 | Moyenne | `studio-heroes.webp` (illustration groupe pour « À propos ») | `assets/studio-heroes.webp` | 900×600, 3:2 | 100 Ko | WebP | oui (PNG puis WebP alpha) |

Contexte : la jaquette actuelle de Chibi Legends est la même image que La Dernière Torche. Il faut une vraie jaquette propre au jeu, dans le style chibi du jeu.
Zones libres pour le texte HTML : bannière 16:9 = laisser le tiers gauche calme (sombre) pour le titre.

## Prompt 1 — jaquette Chibi Legends (2:3)
À rédiger avec les héros chibi réels du jeu (images de référence : `art/Chibi-Legends/`). Demande : affiche verticale 2:3, équipe de 3 héros chibi au premier plan en pleine action, monde fantasy lumineux, titre « Chibi Legends » en haut en lettres rondes dorées, palette violet nuit / or / turquoise, style identique aux captures du jeu, aucun texte autre que le titre.

## Prompt 2 — bannière 16:9 Chibi Legends
Même univers que la jaquette, composition horizontale 16:9, héros sur le tiers droit, tiers gauche en dégradé violet sombre sans détail, ambiance fantasy colorée, aucun texte.

## Prompt 3 — illustration studio (fond transparent)
Groupe des héros emblématiques de La Dernière Torche (références : `assets/t-cover2.webp`), 3 personnages côte à côte, torche allumée, éclairage chaud, fond transparent, aucun texte.

*Les prompts complets, un par bloc à copier, seront fournis dans le chat au moment de les générer.*
