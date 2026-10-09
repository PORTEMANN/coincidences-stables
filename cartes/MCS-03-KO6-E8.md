# CARTE MCS-03 — KO-6 / triples spectraux ↔ 2I ⊂ E₈, |2I| = 120

**Statut** : CANDIDAT — NON SCELLÉ — Jalon 1 (rédaction, aucun calcul)
**Domaines** : A = géométrie non commutative (triple spectral du modèle standard,
KO-dimension 6) ; B = théorie des groupes (sous-groupes finis, E₈).
**Attente honnête** : **carte de calibration négative**. Le corpus a déjà
partiellement enterré cette correspondance. Sa fonction est de démontrer que la
MCS sait tuer une belle coïncidence — un banc qui ne peut pas produire CS− sur
MCS-03 ne peut pas être cru sur MCS-02.

---

## 1. Énoncé de la coïncidence candidate

Deux faits mathématiques indépendants :

- le triple spectral fini du modèle standard (algèbre réelle
  A_F = ℂ ⊕ ℍ ⊕ M₃(ℂ)) est sélectionné par des conditions de minimalité en
  KO-dimension 6 (Connes–Chamseddine) ;
- le groupe icosaédrique binaire 2I, d'ordre 120, admet un plongement dans E₈
  (via 2I ⊂ SU(2) et la chaîne McKay / sous-algèbres de E₈), et 120 est aussi
  le nombre de racines de H₄, groupe de Coxeter lié à l'icosien.

Correspondance candidate : il existerait un **invariant combinatoire commun**
entre les conditions KO-6 et le pont 120 ↔ E₈ — c'est-à-dire que les mêmes
contraintes qui sélectionnent A_F sélectionneraient la chaîne 2I ⊂ SU(2) ⊂ … ⊂ E₈.

La carte transforme ce « il existerait » en objet testable : une fonction de
comptage définie ci-dessous doit prendre des valeurs corrélées sur les deux
familles, au-delà de ce que produisent les familles de comparaison.

## 2. Lexique gelé (un mot = un objet)

| Mot | Objet opératoire unique |
|-----|--------------------------|
| triple KO-6 minimal | A_F = ℂ ⊕ ℍ ⊕ M₃(ℂ) avec représentation, opérateur de Dirac fini D_F, structure réelle J_F satisfaisant les axiomes de Connes en KO-dimension 6 ; conditions de sélection : ordre 1, orientabilité, Poincaré fini, minimalité (Connes 2006 ; Chamseddine–Connes 2007) |
| chaîne icosienne | 2I ⊂ SU(2), |2I| = 120 ; plongement de H₄ dans E₈ (Moody–Patera) : les 120 racines de H₄ s'envoient sur 120 des 240 racines de E₈ |
| invariant C | pour une algèbre finie A : C(A) = nombre de couples (p, q) de représentations irréductibles avec dim(p)·dim(q) ≤ dim(A) satisfaisant la condition d'ordre 1 avec un D_F auto-adjoint |
| m (mesure) | corrélation de Spearman entre le vecteur C sur la famille KO et le vecteur C sur la famille des groupes, restreinte aux objets minimaux de chaque famille |
| minimalité côté groupes | groupe fini G ⊂ SU(2) ou système de racines exceptionnel, sans quotient propre préservant le plongement dans E₈ |

## 3. Dictionnaire τ

    τ : conditions KO-6 (ordre 1, orientabilité, minimalité)
        ↦  fonction de comptage C restreinte aux algèbres finies réelles
        ↔  fonction de comptage C restreinte aux sous-groupes finis de SU(2) et systèmes exceptionnels

La correspondance prétend que le maximum de C côté algèbres (atteint en A_F)
correspond au maximum de C côté groupes (atteint en 2I / E₈).

## 4. Données et provenance

Pas de données expérimentales : les « données » sont des énumérations
mathématiques exhaustives, fixées par référence :

- algèbres finies réelles involutives de dimension ≤ 32 (énumération standard) ;
- sous-groupes finis de SU(2) (classification ADE : cycliques, dihédraux, T, O, I
  et leurs binaires) ;
- systèmes de racines exceptionnels G₂, F₄, E₆, E₇, E₈ et plongements de H₃, H₄
  (tables Moody–Patera 1993 ; Connes–Chamseddine 2007).

## 5. Groupe de déformations légitimes 𝒢

| g | Déformation | Ce qu'elle teste |
|---|-------------|-------------------|
| g1 | E₈ → E₇ / E₆ / D₁₆ | la coïncidence serait-elle « tout grand groupe marche » ? |
| g2 | 2I → groupe cyclique Z₁₂₀ (même ordre 120) | la coïncidence serait-elle un pur comptage d'ordre ? |
| g3 | règle de comptage C : seuil dim(A) → 2·dim(A) | fragilité à la convention de comptage |
| g4 | KO-6 → KO-2 / KO-7 | la dimension mod 8 serait-elle interchangeable ? |
| g5 | algèbres réelles → complexes | dépendance au corps |
| g6 | plongement H₄ ⊂ E₈ de Moody–Patera → plongement alternatif | unicité de la chaîne |

## 6. Modèle nul

- **N1 (carquois aléatoires)** : 10 000 algèbres finies aléatoires de même
  distribution de dimensions que la famille KO ; distribution de m.
- **N2 (comptage d'ordre)** : la seule quantité |G| est conservée, la structure
  est détruite (tirages uniformes parmi groupes d'ordre ≤ 240) — si la
  correspondance survit à N2, elle était un comptage d'ordres, pas une structure.
- **N3 (permutation)** : permutation des maxima entre les deux familles.

## 7. Contrôles positifs (sabotages obligatoires)

| c | Sabotage | Attendu si le test a du pouvoir |
|---|----------|----------------------------------|
| c1 | casser 2I : le remplacer par I (ordre 60) dans la chaîne | m doit chuter sous −2 |
| c2 | intervertir les maxima de C entre familles (forcer A_F ↔ T au lieu de 2I) | m doit chuter |
| c3 | retirer la condition d'ordre 1 de la définition de C | si m ne change pas, C ne mesure pas ce qu'il prétend : **CS0** |

c1 ou c2 muet → CS0. c3 muet → CS0 immédiat (l'invariant est vide).

## 8. Statistique et seuils (gelés)

- z_g = (m_g − μ_null,g) / u_g sous N1 pour chaque g.
- Σ = min sur {g1…g6}.
- Regard ailleurs : familles de correspondances E₈ déjà enterrées dans le
  corpus : 2 (pont 120 ↔ E₈ nu ; correspondance dimensions KO). Seuil CS+
  relevé de 3 à 3,4 (déclaré et gelé ici).
- Seuil CS0 renforcé pour cette carte : un seul contrôle positif muet suffit
  (carte de calibration, exigence maximale).

## 9. Critères de verdict

| Issue | Verdict |
|-------|---------|
| Σ ≥ 3,4 | CS+ (surprise majeure ; publication avec relecture externe exigée) |
| 2 ≤ Σ < 3,4 | CSp |
| −2 < Σ < 2 | **CS− — verdict attendu ; sa production propre est le succès de la carte** |
| Σ ≤ −2 | CSi |
| un contrôle muet | CS0 → le banc entier est suspect ; geler MCS-01 et MCS-02 jusqu'à refonte |

## 10. Regard ailleurs (déclaration préalable)

Variantes de la correspondance essayées dans le corpus avant cette carte : 2
(déclarées ci-dessus). Invariants candidats avant C : 3 (comptage de racines,
signature de K-theory, dimension des représentations). Aucun calcul n'a été fait
pour cette carte elle-même.

## 11. Critères d'arrêt

- CS− ou CSi : publication B3-FAIL, fermeture définitive de la ligne KO-6 ↔ E₈
  dans le corpus. Aucune variante.
- CS0 : **le banc est déclaré aveugle** ; suspension des verdicts sur toutes les
  autres cartes jusqu'à démonstration que la cécité est locale à MCS-03.
- CS+ : ne rien conclure seul ; exiger une réplication par un tiers avant toute
  mention publique hors B3.

## 12. Scellement (jalon 3)

```
SHA256_CARTE : e5b082c87c996842c707e06a66d98008c62c9dfc114ee33a35ff5da7dc0a1f70
HORODATAGE   : 2026-10-09T13:31:46Z
```
