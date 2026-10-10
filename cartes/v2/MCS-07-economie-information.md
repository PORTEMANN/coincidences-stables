# CARTE MCS-07 — Économie de l'information à la frontière r₁₂ (inversion M1)

**Statut** : CANDIDAT — NON SCELLÉ — Jalon 1 v2 (rédaction, aucun calcul)
**Moteur** : v2.0 (manifeste MANIFESTE-MCS-v2.0.md — puissance démontrée avant gel)
**Domaines** : A = chantiers du corpus (P0–P48, métriques publiées) ;
B = distance à la frontière r₁₂ × taux de succès des confrontations externes.
**Attente honnête** : l'inversion est déjà mesurée et répliquée dans le corpus
(M1/M1b : réfutée structurellement). La carte teste si la relation
« proximité à la frontière × taux de succès externe » est une **coïncidence
stable sous déformations**, ou un artefact du choix de métrique.

---

## 1. Énoncé de la coïncidence candidate

Le corpus a mesuré (M1, répliqué par M1b) que le taux de succès des
confrontations externes **s'effondre** au voisinage de la frontière r₁₂
(τ : 0,60 contre 1,00) alors que le ratio informationnel brut y est plus
élevé (ρ₁ médiane 0,898 vs 0,275). La correspondance candidate :

> La distance d'un chantier à la frontière r₁₂ (déclarée par chantier) prédit
> son taux de succès aux confrontations externes — relation négative, stable
> sous 𝒢, au-delà du hasard structurel.

## 2. Lexique gelé (un mot = un objet)

| Mot | Objet opératoire unique |
|-----|--------------------------|
| chantier | l'un des chantiers du corpus de la liste figée (section 4) |
| distance à la frontière | δ(c) = distance déclarée du chantier c à la frontière r₁₂ (proche / lointain, codée 0/1 par la liste figée — déclarée, pas recomputée) |
| taux de succès | τ(c) = fraction de confrontations externes réussies du chantier, recomputée des artefacts publiés |
| m (mesure) | corrélation de Spearman entre δ et τ sur la liste figée (signe : − attendu) ; m = −ρ(δ, τ) (qualité croissante avec l'inversion mesurée) |
| nul de complexité égale | relation monotone libre entre δ et τ sans ajustement |

## 3. Dictionnaire τ

    τ : chantiers figés ↦ (δ déclarée, τ recomputée) ↦ m

τ est cette carte elle-même.

## 4. Données et provenance (gelées)

- **Liste figée** : les chantiers du corpus avec métriques publiées
  (noetic-machine-complete, `data/` + M1) — la liste exacte et les δ sont
  écrites dans le runner avec leurs empreintes ; entièrement local (aucune
  acquisition externe : les artefacts sont ceux du dépôt publié).
- **Métriques** : τ recomputé des verdicts publiés (succès de confrontation
  externe par chantier, table M1) ; proxy de Kolmogorov (taille gzip des
  artefacts) pour la déformation g2.
- Anti-circularité : M1/M1b ont mesuré la relation ; la carte la teste comme
  coïncidence stable sous 𝒢 — déclaré au regard ailleurs.

## 5. Groupe de déformations légitimes 𝒢

| g | Déformation | Ce qu'elle teste |
|---|-------------|-------------------|
| g1 | τ recomputé → τ avec dénominateurs V2 alternatifs (déclarés M1) | dépendance au dénominateur |
| g2 | taille SLOC → taille gzip (proxy M1b) | dépendance à la métrique de taille |
| g3 | retrait des chantiers P31–P33 (ceux de la frontière elle-même) | domination des points-frontière |
| g4 | δ binaire → δ à trois niveaux (proche/moyen/lointain, déclaré) | granularité de la distance |
| g5 | Spearman → Kendall τ de corrélation | dépendance au coefficient |
| g6 | retrait d'un chantier au hasard (PRNG public) | sensibilité locale |

## 6. Modèle nul

- **N1 (permutation)** : permutation des δ entre chantiers, 10 000 fois.
- **N2 (τ aléatoires)** : τ uniformes sur [0,1] ; distribution de m.
- **N3 (relations monotones aléatoires)** : 10 000 relations décroissantes
  aléatoires entre δ et τ tirées par le PRNG.

## 7. Contrôles positifs (sabotages obligatoires)

| c | Sabotage | Attendu si le test a du pouvoir |
|---|----------|----------------------------------|
| c1 | δ permutées entre chantiers | m s'effondre vers N1 (|effet| ≥ 2 u) |
| c2 | étiquettes δ inversées (proche ↔ lointain) | la relation doit s'inverser (|effet| ≥ 2 u) |

c1 ou c2 vraiment muet → **CS0**.

## 8. Statistique et seuils (gelés)

- z_g = (m_g − μ_null,g)/u_g sous N1 ; Σ = min sur {g1…g6}.
- Regard ailleurs : M1/M1b publiés (inversion mesurée et répliquée) ; seuil
  CS+ : **3,1** (une famille de mesures déjà publiée, déclarée).

## 9. Critères de verdict

| Issue | Verdict |
|-------|---------|
| Σ ≥ 3,1 | CS+ |
| 2 ≤ Σ < 3,1 | CSp |
| −2 < Σ < 2 | CS− (B3-FAIL) |
| Σ ≤ −2 | CSi |
| un contrôle vraiment muet | CS0 |

## 10. Regard ailleurs (déclaration préalable)

M1 et M1b sont publiés dans le corpus (réfutation avec inversion, répliquée).
La carte n'ajoute aucune mesure nouvelle hors celles déclarées à la section 4
— elle teste la **stabilité sous déformations** de la relation publiée, pas
la relation elle-même. Une seule famille essayée (celle-ci).

## 11. Critères d'arrêt

- CS− ou CSi → la relation M1 est close comme coïncidence instable (la
  mesure M1 elle-même reste ce qu'elle est : un résultat du corpus, mais non
  une coïncidence stable au sens MCS).
- CS0 → une seule refonte autorisée (MCS-07b).
- CSp → la carte dort.

## 12. Démonstration de puissance (règle 1.2 du manifeste v2.0)

Avant gel : sur une liste synthétique de chantiers avec relation plantée
(δ proche → τ bas), la statistique doit résoudre les contrôles à |effet| ≥ 2 u
et donner Σ ≥ 3,1 ; sans relation, CS− attendu. Hachée dans l'acte de
scellement.

## 13. Scellement (jalon 3 v2)

```
SHA256_CARTE : 426ee08b718e6d693a41d5718b4c251e1a00a4296ef645b6c4872b443e4be05f
HORODATAGE   : 2026-10-10T18:31:16Z
```
