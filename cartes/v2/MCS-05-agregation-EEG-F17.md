# CARTE MCS-05 — Agrégation dérivée d'essais EEG × classes motrices (F17)

**Statut** : CANDIDAT — NON SCELLÉ — Jalon 1 v2 (rédaction, aucun calcul)
**Moteur** : v2.0 (manifeste MANIFESTE-MCS-v2.0.md — puissance démontrée avant gel)
**Domaines** : A = EEG d'imagerie motrice par essais (BCICIV-2a) ;
B = classes motrices (gauche / droite).
**Attente honnête** : carte à haut risque. La famille EEG du corpus cumule
trois échecs mesurés (P44, P47, P51 — B3-FAIL publiés). La frontière F17 est
ouverte. Cette carte pose la question une fois, globalement, sous déformations
et double contrainte de phase — puis se ferme.

---

## 1. Énoncé de la coïncidence candidate

Le corpus a mesuré que les règles zéro-paramètre par essai unique échouent
(P44 : 0,540 et 0,520 contre seuil 0,60) et que le vote par agrégation est
insuffisant (P47 : 0,5926 < seuil figé). La correspondance candidate est plus
faible et plus précise :

> L'agrégation centroïde (moyenne des essais par classe, zéro paramètre
> ajusté) produit une séparation des classes motrices **supérieure à ce que
> produisent les surrogates à spectre identique** — c'est-à-dire qu'il existe
> une information de phase lisible entre essais et classes, stable sous 𝒢.

## 2. Lexique gelé (un mot = un objet)

| Mot | Objet opératoire unique |
|-----|--------------------------|
| essai | un segment EEG d'imagerie motrice BCICIV-2a (run d'entraînement, canal C3/Cz/C4, fenêtre 2–4 s post-cue) |
| agrégation centroïde | moyenne arithmétique des essais d'une même classe, par canal ; aucun paramètre |
| séparation | accuracy du centroïde euclidien (split par essais, 70/30, graine publique) |
| m (mesure) | accuracy de l'agrégation centroïde sur le split de test |
| domaine | un sujet |

## 3. Dictionnaire τ

    τ : essais EEG ↦ agrégation centroïde ↦ séparation des classes

τ est cette carte elle-même.

## 4. Données et provenance (gelées)

- **BCICIV-2a** (BNCI, 9 sujets, imagerie motrice, données publiques
  d'entraînement) — acquisition par le runner, empreintes consignées.
- Fenêtre : 2–4 s post-cue ; canaux C3, Cz, C4 ; 250 Hz natif.
- **Déclaration d'usage antérieur** : BCICIV-2a a servi à P44 (règles
  réfutées) — la présente carte n'utilise pas ces verdicts pour construire τ
  (l'agrégation centroïde est antérieure et générique) ; le regard ailleurs
  (section 10) le déclare.

## 5. Groupe de déformations légitimes 𝒢

| g | Déformation | Ce qu'elle teste |
|---|-------------|-------------------|
| g1 | surrogates IAAFT (100/fenêtre, exclu du min, rapporté) | phase ou spectre ? |
| g2 | fenêtre 2–4 s → 1–3 s | dépendance à la fenêtre |
| g3 | canaux C3/Cz/C4 → C3/C4 seuls | dépendance spatiale |
| g4 | retrait du sujet le plus lisible (déclaré au gel : mesuré P44 = A03) | domination d'un sujet |
| g5 | référence moyenne commune → référence Cz | dépendance à la référence |
| g6 | split 70/30 → 50/50 | dépendance au split |

## 6. Modèle nul

- **N1 (IAAFT)** : nul central — m sur surrogates (100/fenêtre) → μ_null, u.
- **N2 (étiquettes permutées)** : permutation des étiquettes de classe,
  1 000 fois ; m doit s'effondrer vers la moyenne N2.
- **N3 (bruit de même DSP)** : bruit filtré de même DSP moyenne par sujet.

## 7. Contrôles positifs (sabotages obligatoires)

| c | Sabotage | Attendu si le test a du pouvoir |
|---|----------|----------------------------------|
| c1 | permutation des étiquettes de classe | m s'effondre vers N2 (|effet| ≥ 2 u attendu) |
| c2 | injection d'un ERD synthétique (mu 10 Hz) dans du bruit pur, modulé par des étiquettes factices déclarées | le pipeline doit retrouver ces étiquettes : récupération ≫ hasard (|effet| ≥ 2 u) |

c1 ou c2 vraiment muet (|effet| < 2 u) → **CS0**.

## 8. Statistique et seuils (gelés)

- z_g = (m_g − μ_null,g)/u_g sous N1 pour chaque g ; Σ = min sur {g2…g6}
  (g1 IAAFT exclu du minimum, rapporté séparément — double contrainte).
- Double contrainte : (a) Σ ≥ 3,3 sur données réelles ; (b) sous IAAFT,
  m s'effondre (z_effondrement ≤ −2).
- Regard ailleurs : famille EEG déjà trois échecs mesurés (P44, P47, P51) ;
  seuil CS+ : **3,3** (identique à MCS-02, déclaré).

## 9. Critères de verdict

| Issue | Verdict |
|-------|---------|
| (a) et (b) | CS+ |
| (a) sans (b) | CS− déguisé → **CS−** (spectrale, générique) |
| (b) sans (a) | CSp |
| ni (a) ni (b) | CS− |
| Σ ≤ −2 | CSi |
| un contrôle vraiment muet | CS0 |

## 10. Regard ailleurs (déclaration préalable)

Trois échecs EEG mesurés avant gel (P44, P47, P51 — publiés) : les règles
zéro-paramètre par essai sont réfutées, le vote par agrégation insuffisant,
les invariants ASH ne séparent pas le sommeil. Cette carte pose une question
**distincte et plus faible** (existe-t-il une information de phase lisible,
stable sous 𝒢 ?) — pas une réparation des règles réfutées (fermer, ne pas
ajouter). Jeux de données examinés avant gel : 1 (celui-ci, déclaré).

## 11. Critères d'arrêt

- CS− ou CSi → carte fermée ; F17 reste ouverte dans le corpus mais la
  question « agrégation centroïde sous déformations » est close (B3-FAIL).
- CS0 → une seule refonte autorisée (MCS-05b).
- CSp → la carte dort.

## 12. Démonstration de puissance (règle 1.2 du manifeste v2.0)

Avant gel : sur un EEG synthétique avec ERD planté (gauche/droite), la
statistique doit donner Σ ≥ 3,3 et les contrôles résoudre à |effet| ≥ 2 u ;
sur bruit coloré sans structure, CS− attendu ; banc aveugle simulé → CS0.
Hachée dans l'acte de scellement.

## 13. Scellement (jalon 3 v2)

```
SHA256_CARTE : 177b86c1af4cfa2f3af64f0dd012dac25b786d98c1f636f3a19712c1d8a892be
HORODATAGE   : 2026-10-10T18:31:16Z
```
