# CARTE MCS-12 — Nucléosynthèse primordiale à un paramètre × éléments légers

**Statut** : CANDIDAT — NON SCELLÉ — Jalon 1 v2 (rédaction, aucun calcul)
**Moteur** : v2.0 (manifeste MANIFESTE-MCS-v2.0.md — puissance démontrée avant gel)
**Domaines** : A = abondances primordiales mesurées (D/H, ³He/H, Y_p, ⁷Li/H) ;
B = la BBN **à un paramètre** (η baryonique fixé par le CMB, pas par les
abondances) telle que tabulée par la revue BBN du PDG — prédictions et
observations lues dans la même source publique, **figées à l'acquisition**.
**Attente honnête** : mitigée par construction. Trois accords forts (D, ³He,
⁴He) et une rupture célèbre (⁷Li, le « problème du lithium », facteur ~3 —
fait publié, pas une lecture). La question MCS : la concordance d'ensemble
(une table, un paramètre) dépasse-t-elle le hasard structurel de « univers
aléatoires », et survit-elle aux déformations ? La rupture ⁷Li est un fait
du problème ; le verdict dira si elle tue la stabilité ou si l'ensemble
tient quand même. **Aucune circularité** : η vient de Planck, pas des
abondances — seuil de base 3,0.

---

## 1. Énoncé de la coïncidence candidate

> Les quatre abondances primordiales mesurées se placent sur les valeurs
> prédites par la BBN à un paramètre (η fixé extérieurement), telles que
> tabulées par la source gelée — **au-delà de ce que produisent des univers
> aléatoires de même étendue**, et cette concordance survit aux déformations
> du groupe 𝒢, rupture ⁷Li comprise.

## 2. Lexique gelé (un mot = un objet)

| Mot | Objet opératoire unique |
|-----|--------------------------|
| élément | l'un des quatre rapports : D/H, ³He/H, Y_p (fraction massique ⁴He), ⁷Li/H |
| prédiction | la valeur tabulée par la revue BBN du PDG (édition canonique), lue à l'ouverture |
| observation | la valeur adoptée tabulée par la même revue, avec sa σ publiée |
| écart | ε(e) = log₁₀(pred(e)) − log₁₀(obs(e)) |
| m (mesure) | m = −log₁₀( RMS(ε) ) sur les éléments de la configuration |
| univers aléatoire | quadruplet tiré log-uniformément dans les étendues déclarées (section 6) |

## 3. Dictionnaire τ

    τ : abondances mesurées × prédictions BBN tabulées ↦ écarts ↦ m

τ est cette carte elle-même. Toute modification de τ après le gel = nouvelle
carte, nouveau numéro.

## 4. Données et provenance (gelées)

- **Source canonique** : revue « Big-Bang Nucleosynthesis » du PDG
  (édition 2024, pdf public — pdg.lbl.gov) : prédictions à η_CMB gelé et
  observations adoptées, avec σ publiées. Acquisition à l'ouverture,
  empreinte consignée. Aucune page n'a été lue avant la rédaction.
- **Contre-source (g1)** : la même revue, édition 2022.
- **η** : fixé par le CMB (Planck) — la carte ne l'ajuste pas ; les
  prédictions tabulées sont prises telles quelles.
- La rupture ⁷Li est un fait publié de la littérature (facteur ~3), pas
  une lecture de la table.

## 5. Groupe de déformations légitimes 𝒢

| g | Déformation | Ce qu'elle teste |
|---|-------------|-------------------|
| g1 | revue 2024 → revue 2022 | dépendance à l'édition (théorie et mesures) |
| g2 | retrait de ⁷Li (rupture déclarée) | domination de la rupture |
| g3 | retrait de ³He (mesure la moins fiable, déclarée) | domination d'un point faible |
| g4 | observations centrales → toutes à +1σ publié | dépendance aux incertitudes |
| g5 | observations centrales → toutes à −1σ publié | dépendance aux incertitudes |
| g6 | retrait d'un élément au hasard (PRNG public ChaCha20) | sensibilité locale |

## 6. Modèle nul

- **N1 (univers aléatoires)** : 10 000 quadruplets tirés log-uniformément
  dans les étendues déclarées : D/H ∈ [10⁻⁶ ; 10⁻³], ³He/H ∈ [10⁻⁶ ; 10⁻³],
  Y_p ∈ [0,05 ; 0,5], ⁷Li/H ∈ [10⁻¹¹ ; 10⁻⁸] ; m des prédictions figées sur
  chacun → μ_null, u. (Nul de complexité égale : aucune physique, même
  étendue, même effectif.)
- **N2 (prédictions permutées)** : permutation des prédictions entre
  éléments, 10 000 fois (rapporté ; teste l'assignation élément ↔ valeur).

## 7. Contrôles positifs (sabotages obligatoires)

| c | Sabotage | Attendu si le test a du pouvoir |
|---|----------|----------------------------------|
| c1 | prédictions permutées entre éléments | m s'effondre (|effet| ≥ 2 u) |
| c2 | observations remplacées par un quadruplet log-uniforme déclaré | m s'effondre vers μ_N1 (|effet| ≥ 2 u) |

c1 ou c2 vraiment muet (|effet| < 2 u, règle v2.0) → **CS0**.

## 8. Statistique et seuils (gelés)

- z_g = (m_g − μ_null,g)/u_g sous N1 pour chaque g ; Σ = min sur {g1…g6}.
- Seuil CS+ : **3,0** (aucune famille éprouvée, aucune circularité — η est
  extérieur aux abondances).
- Diagnostic rapporté (hors Σ) : les écarts ε par élément, en dex —
  dont la rupture ⁷Li, mesurée, jamais absorbée dans la moyenne sans
  être republiée.

## 9. Critères de verdict

| Issue | Verdict |
|-------|---------|
| Σ ≥ 3,0 | CS+ — la concordance d'ensemble est stable (la rupture ⁷Li reste publiée au diagnostic) |
| 2 ≤ Σ < 3,0 | CSp |
| −2 < Σ < 2 | CS− (B3-FAIL) |
| Σ ≤ −2 | CSi |
| un contrôle vraiment muet | CS0 |

## 10. Regard ailleurs (déclaration préalable)

La BBN n'a jamais été éprouvée par la machine ni le corpus. Aucune
circularité : le paramètre est fixé par le CMB. La carte mesure la
concordance d'une table figée avec des mesures figées — pas la validité de
la cosmologie, qui reste hors de portée. Sources consultées avant gel : 0.

## 11. Critères d'arrêt

- CS+ → la BBN à un paramètre est une coïncidence stable mesurée ; la
  rupture ⁷Li reste un problème ouvert, publié au diagnostic.
- CS− ou CSi → carte fermée (B3-FAIL) ; la concordance d'ensemble était
  compatible avec des univers aléatoires.
- CS0 → une seule refonte autorisée (MCS-12b).
- CSp → la carte dort.

## 12. Démonstration de puissance (règle 1.2 du manifeste v2.0)

Avant gel : sur un jeu synthétique d'observations planté sur les
prédictions à 0,02 dex près, la statistique doit donner Σ ≥ 3,0 et les
deux contrôles résoudre à |effet| ≥ 2 u ; sur un quadruplet d'univers
aléatoire, CS− attendu ; banc aveugle simulé → CS0. Hachée dans l'acte
de gel.

## 13. Scellement (jalon 3 v2)

```
SHA256_CARTE : 90f1705d3d808674755c48fde200fae629d097ad79e4afa7b2d055bc1ad5eba4
HORODATAGE   : 2026-10-11T08:32:36Z
```
