# RAPPORT — Jalon 4 v2 : ouverture des cartes MCS-04 à MCS-07

**Date** : 2026-10-10 · **Moteur** : v2.0 (scellé, empreinte globale d23216f5…)
**Campagne précédente** : jalon 4 (MCS-01/02/03) close — v0.1 figée.
**Journal** : `journal/JALON-4V2-OUVERTURE.jsonl` (18 records chaînés, genèse
GENESIS-MCS-J4V2, lié au gel des cartes d53b0c23…).

## Protocole rappelé

Quatre cartes rédigées au jalon 1 v2, puissance démontrée sur synthétique pour
chacune (règle 1.2 — 4/4 SCELLABLE, journal haché dans l'acte de gel), gelées
au jalon 3 v2 (empreintes pré-gel consignées dans `scellement/GEL-CARTES-V2.json`,
blocs nuls conservés pour vérification octet par octet), puis ouvertes ici :
acquisition publique consignée, runner figé et haché **avant** exécution,
**une seule exécution par carte**, verdicts publiés quel que soit le résultat.

## Verdicts

| Carte | Question | Σ | Contrôles (u) | Verdict |
|-------|----------|-----|----------------|---------|
| MCS-04 | zoo particulaire × tempérament égal | −0,43 | c1 = 4,45 ; c2 = 2,15 | **CS−** |
| MCS-05 | agrégation centroïde EEG (F17) | −1,71 | c1 = 1,82 (muet) ; c2 = 22,35 | **CS0** |
| MCS-06 | loi des bifurcations v2 | 0,90 | c1 = 7,91 ; c2 = 12,55 | **CS−** |
| MCS-07 | économie de l'information (M1) | 0,55 | c1 = 2,41 ; c2 = 4,72 | **CS−** |

## Lectures

### MCS-04 — la loi harmonique n'est pas une coïncidence stable globale
Le canonique dépasse le nul N1 (z = 2,28 — mieux qu'un réseau aléatoire de pas
voisin), mais le maillon faible est g5 (changement de pas 2^(1/11)/2^(1/13),
z = −0,43) : l'accord ne tient pas au pas du tempérament égal, il est
compatible avec un réseau de pas voisin quelconque. Les pesées locales mvcg
(S+ sur μ/Z/charm) restent ce qu'elles sont ; la correspondance **globale**
est close (B3-FAIL publié).

### MCS-05 — test impuissant sur BCICIV-2a (CS0)
L'accuracy centroïde réelle (0,457) est sous le nul IAAFT (0,493) — aucune
information de phase lisible, cohérent avec les échecs P44/P47/P51. Mais le
contrôle c1 (étiquettes permutées) est muet (|effet| = 1,82 u < 2 u) : la
permutation ne dégrade pas assez une mesure déjà sous le nul. Règle v2.0 :
CS0, carte suspendue — une seule refonte autorisée (MCS-05b). Le pipeline
lui-même est validé par c2 (récupération d'un ERD synthétique à 22,4 u).

### MCS-06 — la loi des bifurcations v2 n'atteint pas le seuil
Tendance réelle (ρ_phys = −0,853 sur 14 bifurcations physiques, z0 = 2,34,
stable sous g1–g5 entre 2,10 et 2,37) mais en deça du seuil 3,1 même au
canonique ; l'axe conventionnel est libre comme attendu (|ρ_conv| = 0,135
< 0,5). Maillon faible : g6 (0,90) — la carte scellée inclut dans Σ une
permutation des types, c'est-à-dire un tirage du nul N1 ; ce défaut de
conception est publié (la démonstration de puissance testait la statistique,
pas le minimum complet à six déformations — leçon pour la règle 1.2).
Verdict : CS−. La conjecture reste catégorie II, étiquetée.

### MCS-07 — l'inversion M1 n'est pas stable sous déformations
La relation « proximité à la frontière r₁₂ × taux de succès » est réelle sur
le corpus (z0 = 2,38) mais portée par les points-frontière eux-mêmes : leur
retrait (g3) effondre la mesure (z = 0,55). Verdict : CS−. La mesure M1 reste
un résultat du corpus ; elle n'est pas une coïncidence stable au sens MCS.

## Ce que le moteur v2.0 a changé

- **Aucun CS0 parasite de convention de signe** (cf. MCS-01/02 au jalon 4) :
  la règle signe-robuste a fonctionné — les deux CS0 possibles étaient
  informatifs (MCS-05 : impuissance réelle, pas artefact de signe).
- **La règle 1.2 a tenu** : les quatre statistiques ont résolu leurs contrôles
  sur synthétique avant gel ; en exécution réelle, trois cartes sur quatre
  ont eu des contrôles vivants — le quatrième (MCS-05, c1) a été détecté
  comme muet et a suspendu la carte au lieu de produire un faux CS−.
- **Limite mesurée** : la démonstration de puissance porte sur la statistique,
  pas sur le minimum complet du groupe 𝒢 (MCS-06, g6). Une version future de
  la règle 1.2 devra exiger la démonstration sur le 𝒢 complet.

## Reproductibilité

- Données publiques : PDG `mass_width_2024.mcd` / `mass_width_2022.mcd`
  (pdg.lbl.gov), BCICIV-2a (bbci.de, zip sha256 65fe93cb…), artefacts M1/M1b
  du corpus (GitHub blob SHA consignés), table de bifurcations
  (`donnees/mcs06_bifurcations.json`, 15 batteries justifiées test par test).
- Runners hachés avant exécution (`code/mcs0{4,5,6,7}_runner.py`) ; un crash
  avant tout résultat (MCS-05 v1) est consigné au journal avec le correctif.
- PRNG public : clé = SHA-256("MCS-J4V2|" + empreinte_carte + "|" +
  empreinte_données), ChaCha20-IETF — toute personne peut rejouer.

*Verdicts publiés quel que soit le résultat : 3 CS−, 1 CS0. La machine a
encore une fois produit des fermetures, pas des confirmations.*
