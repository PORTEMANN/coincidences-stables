# CARTE MCS-14 — Loi de rang figée × groupes d'espace cristallographiques

**Statut** : CANDIDAT — NON SCELLÉ — Jalon 1 v2 (rédaction, aucun calcul)
**Moteur** : v2.0 (manifeste MANIFESTE-MCS-v2.0.md — puissance démontrée avant gel)
**Domaines** : A = structures cristallines réalisées et publiées
(Crystallography Open Database — base ouverte) ; B = la loi de rang
**figée** : N(r) = N_tot / (H₂₃₀ · r) pour les 230 groupes d'espace triés
par effectif décroissant (loi de Zipf d'exposant α = 1, **aucun paramètre
ajusté** — N_tot est le total de la configuration, H₂₃₀ = Σ 1/r est fixe).
**Attente honnête** : mitigée. La concentration est un fait notoire
(quelques groupes hébergent l'essentiel des structures publiées : la mesure
canonique dépassera sûrement le nul uniforme) — mais la loi de rang à
exposant figé 1 n'a aucune raison de survivre aux sous-ensembles (systèmes
cristallins, époques), dont les distributions diffèrent par construction.
La question est la stabilité de la forme, pas l'existence de la
concentration. Attente : CSp ou CS−.

---

## 1. Énoncé de la coïncidence candidate

> Les effectifs des 230 groupes d'espace dans la base ouverte suivent la loi
> de rang figée N(r) = N_tot / (H₂₃₀ · r) **au-delà de ce que produit le
> hasard structurel** (partitions aléatoires uniformes de même total), et
> cette forme survit aux déformations du groupe 𝒢.

## 2. Lexique gelé (un mot = un objet)

| Mot | Objet opératoire unique |
|-----|--------------------------|
| groupe | l'un des 230 groupes d'espace (notation Hermann-Mauguin de la base) |
| effectif | nombre de structures de la configuration hébergées par le groupe |
| rang r | rang du groupe par effectif décroissant (1 = le plus peuplé) |
| loi figée | N_zipf(r) = N_tot / (H₂₃₀ · r), H₂₃₀ = Σ_{r=1..230} 1/r |
| écart | ε(r) = log₁₀(N_obs(r) + 1) − log₁₀(N_zipf(r) + 1) (le +1 est gelé) |
| m (mesure) | m = −log₁₀( RMS(ε) ) sur les 230 rangs |

## 3. Dictionnaire τ

    τ : structures de la base ↦ effectifs par groupe ↦ rangs ↦ m

τ est cette carte elle-même. Toute modification de τ après le gel = nouvelle
carte, nouveau numéro.

## 4. Données et provenance (gelées)

- **Crystallography Open Database** (crystallography.net — base ouverte) :
  comptage des structures par groupe d'espace, acquisition à l'ouverture,
  empreinte consignée. Aucune requête n'a été faite avant la rédaction.
- **Liste figée** : les 230 groupes d'espace (l'effectif de chacun est lu à
  l'exécution ; les groupes vides comptent comme vides, déclaré).
- La concentration des groupes d'espace est un fait notoire de la
  littérature cristallographique, déclaré — pas une lecture de la base.

## 5. Groupe de déformations légitimes 𝒢

| g | Déformation | Ce qu'elle teste |
|---|-------------|-------------------|
| g1 | sous-ensemble système monoclinique seul | la forme tient-elle par système ? |
| g2 | sous-ensemble système cubique seul | la forme tient-elle par système ? |
| g3 | retrait du groupe de rang 1 (le dominant, publié à l'exécution) | domination d'un groupe |
| g4 | exposant figé α = 1 → α = 0,5 (loi plus molle déclarée) | dépendance à l'exposant |
| g5 | retrait des structures datées > 2000 (colonne année de la base, déclarée) | dépendance à l'époque |
| g6 | retrait d'un groupe au hasard, rangs recomptés (PRNG public ChaCha20) | sensibilité locale |

## 6. Modèle nul

- **N1 (partitions uniformes)** : 10 000 partitions du même total de
  structures sur 230 groupes (multinomiale uniforme) ; rangs recomputés,
  m recomputé → μ_null, u. (Nul de complexité égale : aucune loi, même
  total, mêmes 230 cases.)
- **N2 (rangs permutés)** : permutation des effectifs entre rangs, 10 000
  fois (rapporté ; teste l'ordonnancement, pas la concentration).

## 7. Contrôles positifs (sabotages obligatoires)

| c | Sabotage | Attendu si le test a du pouvoir |
|---|----------|----------------------------------|
| c1 | rangs inversés (tri croissant : le groupe le moins peuplé pris pour rang 1) | m s'effondre (|effet| ≥ 2 u) |
| c2 | exposant doublé (α = 2, déclaré) | m se dégrade (|effet| ≥ 2 u) |

c1 ou c2 vraiment muet (|effet| < 2 u, règle v2.0) → **CS0**.

## 8. Statistique et seuils (gelés)

- z_g = (m_g − μ_null,g)/u_g sous N1 pour chaque g ; Σ = min sur {g1…g6}.
- Seuil CS+ : **3,0** (aucune famille éprouvée, aucune circularité).
- Diagnostics rapportés (hors Σ) : l'exposant α ajusté (hors mesure,
  publié à titre indicatif) pour la configuration canonique et pour chaque
  sous-ensemble de la section 5 ; les dix groupes de tête.

## 9. Critères de verdict

| Issue | Verdict |
|-------|---------|
| Σ ≥ 3,0 | CS+ — la loi de rang figée est stable au sens MCS |
| 2 ≤ Σ < 3,0 | CSp |
| −2 < Σ < 2 | CS− (B3-FAIL) |
| Σ ≤ −2 | CSi |
| un contrôle vraiment muet | CS0 |

## 10. Regard ailleurs (déclaration préalable)

La distribution des groupes d'espace n'a jamais été éprouvée par la machine
ni le corpus. La famille « loi de rang / Zipf » n'a pas été éprouvée non
plus (elle est en réserve comme second étalon de calibration — la présente
carte n'est pas la calibration : sa forme est contestable, l'étalon ne
l'est pas). Bases consultées avant gel : 0.

## 11. Critères d'arrêt

- CS+ → la forme de rang figée est une coïncidence stable ; publiée avec
  les exposants ajustés en diagnostic.
- CS− ou CSi → carte fermée (B3-FAIL) ; la forme figée était une
  approximation instable d'une concentration réelle.
- CS0 → une seule refonte autorisée (MCS-14b).
- CSp → la carte dort.

## 12. Démonstration de puissance (règle 1.2 du manifeste v2.0)

Avant gel : sur une base synthétique plantée sur la loi figée (α = 1
exact, bruit 10 %), la statistique doit donner Σ ≥ 3,0 et les deux
contrôles résoudre à |effet| ≥ 2 u ; sur une partition uniforme, CS−
attendu ; banc aveugle simulé → CS0. Hachée dans l'acte de gel.

## 13. Scellement (jalon 3 v2)

```
SHA256_CARTE : c2202d9245cf30470d9a85d2f0fff653039511331c9834a558f51b5734ab2ff5
HORODATAGE   : 2026-10-11T10:24:29Z
```
