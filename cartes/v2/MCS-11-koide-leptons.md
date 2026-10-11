# CARTE MCS-11 — Formule de Koide × masses des leptons chargés

**Statut** : CANDIDAT — NON SCELLÉ — Jalon 1 v2 (rédaction, aucun calcul)
**Moteur** : v2.0 (manifeste MANIFESTE-MCS-v2.0.md — puissance démontrée avant gel)
**Domaines** : A = masses mesurées de l'électron, du muon et du tau
(PDG 2024/2022, CODATA 2022/2018 — tables déjà empreintées au dépôt) ;
B = la formule de Koide **figée par sa publication (1982)** :
K = (m_e + m_μ + m_τ) / (√m_e + √m_μ + √m_τ)² = 2/3, **aucun paramètre**.
**Attente honnête** : incertaine, et c'est le test. La proximité publiée est
réelle (~3 × 10⁻⁵ en écart relatif) mais la formule n'a que **trois points** —
et elle a été *trouvée* sur ces trois masses (circularité intégrale déclarée,
payée au seuil). Le nul structurel sur n = 3 est le juge : s'il produit
souvent d'aussi bonnes proximités, la carte dort ou meurt ; sinon, la machine
aura mesuré une coïncidence exceptionnelle sans l'expliquer.

---

## 1. Énoncé de la coïncidence candidate

> Pour les masses mesurées des trois leptons chargés, la formule figée de
> Koide vaut 2/3 **au-delà de ce que produit le hasard structurel** sur des
> triplets de masses de même hiérarchie, et cette proximité survit aux
> déformations du groupe 𝒢.

## 2. Lexique gelé (un mot = un objet)

| Mot | Objet opératoire unique |
|-----|--------------------------|
| triplet | les masses (m_e, m_μ, m_τ) lues dans une table de la configuration |
| K | (m_e + m_μ + m_τ) / (√m_e + √m_μ + √m_τ)² — sans dimension, symétrique |
| cible | 2/3, gelée (publication 1982, aucun réajustement) |
| m (mesure) | m = −log₁₀( |K − 2/3| / (2/3) ) — qualité croissante avec la proximité |
| hiérarchie | masses triées, tirées log-uniformément dans l'étendue déclarée [0,5 ; 2000] MeV |

## 3. Dictionnaire τ

    τ : masses des trois leptons chargés ↦ K ↦ m

τ est cette carte elle-même. Toute modification de τ après le gel = nouvelle
carte, nouveau numéro.

## 4. Données et provenance (gelées)

- **Tables** (déjà acquises et empreintées au dépôt lors des campagnes
  MCS-04 et MCS-08, réutilisées avec re-consignation des empreintes) :
  PDG `mass_width_2024.mcd` (canonique), PDG `mass_width_2022.mcd` (g1),
  CODATA `allascii_2022.txt` (g2), CODATA `allascii_2018.txt` (g3).
- **Déclaration de circularité intégrale** : la formule a été trouvée sur
  ces trois masses (1982) ; elle n'a jamais prédit une quatrième particule
  (l'extension aux quarks est un autre chantier, non couvert). Payée au
  seuil (section 8). Aucun calcul de K n'a été effectué avant la rédaction ;
  la proximité ~10⁻⁵ est un fait de la littérature, pas une mesure faite ici.
- **Fragilité déclarée** : n = 3. Le z final est une rareté de queue de nul,
  pas une preuve de loi — la lecture le rappellera quelle que soit l'issue.

## 5. Groupe de déformations légitimes 𝒢

| g | Déformation | Ce qu'elle teste |
|---|-------------|-------------------|
| g1 | PDG 2024 → PDG 2022 | dépendance à l'édition de la mesure |
| g2 | PDG 2024 → CODATA 2022 | dépendance à l'autorité de mesure |
| g3 | CODATA 2022 → CODATA 2018 | double changement d'autorité et d'édition |
| g4 | masses centrales → toutes à +1σ publié | dépendance aux incertitudes |
| g5 | masses centrales → toutes à −1σ publié | dépendance aux incertitudes |
| g6 | MeV → unités atomiques (m_e ≡ 1, déclaré) | invariance d'échelle (INERTE par construction — rapportée) |

## 6. Modèle nul

- **N1 (triplets hiérarchiques libres)** : 10 000 triplets de masses triés,
  tirés log-uniformément dans [0,5 ; 2000] MeV ; distribution de m → μ_null, u.
  C'est le nul de complexité égale : aucune formule, même hiérarchie déclarée,
  même effectif (n = 3).
- **N2 (panel de rationnels)** : m recalculé pour un panel de cibles simples
  {1/3, 1/2, 2/3, 3/4, 4/5, φ − 1} (diagnostic rapporté, hors Σ : 2/3 est-il
  le meilleur rationnel simple, ou l'un parmi d'autres ?).

## 7. Contrôles positifs (sabotages obligatoires)

| c | Sabotage | Attendu si le test a du pouvoir |
|---|----------|----------------------------------|
| c1 | triplet remplacé par un tirage log-uniforme déclaré | m s'effondre vers μ_N1 (|effet| ≥ 2 u) |
| c2 | cible 2/3 → 3/4 (rationnel déclaré) | m se dégrade (|effet| ≥ 2 u) |

c1 ou c2 vraiment muet (|effet| < 2 u, règle v2.0) → **CS0**.

## 8. Statistique et seuils (gelés)

- z_g = (m_g − μ_null,g)/u_g sous N1 pour chaque g ; Σ = min sur {g1…g6}.
- Seuil CS+ : **3,1** = 3,0 (base) + 0,1 (découverte historique de la formule
  sur l'échantillon testé — circularité intégrale déclarée).
- Diagnostic rapporté (hors Σ) : le panel N2 de la section 6.

## 9. Critères de verdict

| Issue | Verdict |
|-------|---------|
| Σ ≥ 3,1 | CS+ — la proximité est exceptionnelle sous le nul ; publiée SANS explication revendiquée |
| 2 ≤ Σ < 3,1 | CSp |
| −2 < Σ < 2 | CS− (B3-FAIL) — la proximité était banale pour des triplets hiérarchiques |
| Σ ≤ −2 | CSi |
| un contrôle vraiment muet | CS0 |

## 10. Regard ailleurs (déclaration préalable)

La famille « loi harmonique des masses » a été éprouvée par MCS-04 (CS−,
opérateur différent : réseau vs formule rationnelle). La formule de Koide
n'a jamais été éprouvée par la machine ni le corpus. Tables consultées avant
gel : 0 (les masses elles-mêmes sont des constantes publiques connues ;
l'écart à 2/3 n'a pas été calculé avant la rédaction).

## 11. Critères d'arrêt

- CS+ → la coïncidence est mesurée comme exceptionnelle ; publication avec
  la circularité intégrale et la fragilité n = 3 en tête de lecture.
- CS− ou CSi → carte fermée (B3-FAIL) ; la formule rejoint les curiosités
  banales de la littérature.
- CS0 → une seule refonte autorisée (MCS-11b).
- CSp → la carte dort.

## 12. Démonstration de puissance (règle 1.2 du manifeste v2.0)

Avant gel : sur un triplet synthétique planté sur K = 2/3 à 10⁻⁶ près, la
statistique doit donner Σ ≥ 3,1 et les deux contrôles résoudre à
|effet| ≥ 2 u ; sur un triplet log-uniforme, CS− attendu ; banc aveugle
simulé → CS0. Hachée dans l'acte de gel.

## 13. Scellement (jalon 3 v2)

```
SHA256_CARTE : 7eaad89022d57ab342590196dc79c9ac880792c7879c07ea50e1e29fd2efbe21
HORODATAGE   : 2026-10-11T08:13:01Z
```
