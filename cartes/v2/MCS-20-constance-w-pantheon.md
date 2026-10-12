# CARTE MCS-20 — Constance de l'énergie noire (w = −1) × résidus Pantheon+

**Statut** : CANDIDAT — Jalon 1 v2 (rédaction, aucun calcul de mesure)
**Moteur** : v2.0 (manifeste MANIFESTE-MCS-v2.0.md — puissance démontrée avant gel)
**Domaines** : A = les résidus des modules de distance des 1 701 supernovae
Pantheon+ à la courbe ΛCDM gelée (même ancrage que MCS-17 : H0 = 67,4,
M = −19,253, Ωm = 0,315 gelé — Planck) ; B = la constance de l'énergie
noire : w = −1 exact — libérer w n'améliore pas l'ajustement au-delà du
hasard structurel.
**Attente honnête** : la littérature mesure w compatible avec −1 dans
Pantheon+ ; la question MCS n'est pas la valeur de w mais la **stabilité**
de la suffisance de w = −1 sous 𝒢. Attente : CSp ou CS+.
**Regard ailleurs (déclaration préalable)** : les données Pantheon+ ont déjà
été acquises et lues (MCS-17, journal publié) — elles sont réutilisées avec
leurs empreintes reconsignées. MCS-17 a mesuré le **niveau** du résidu
bas-z (tension H0) avec une forme compacte de la courbe ; la présente carte
mesure la **forme** (suffisance de w = −1) avec l'intégrale de luminosité
complète (déclaré : la courbe de MCS-20 est l'intégrale exacte de Friedmann,
pas la forme compacte z(1+z) de MCS-17 — les deux cartes sont des objets
indépendants, scellés séparément).
**Note de correction pré-gel (déclarée)** : une première version de cette
carte mesurait la pente OLS des moyennes de bins à ordonnée libre ; sa
démonstration de puissance a échoué (σ = 1,66 < 3,1 ; contrôles muets —
la mesure diluait l'effet de w dans l'ordonnée absorbée). La mesure a été
corrigée UNE fois avant tout gel vers la statistique suffisante standard
(Δχ²), la démo v1 est conservée et publiée (demonstration_puissance_mcs20_v1).

---

## 1. Énoncé de la coïncidence candidate

> Libérer w n'améliore l'ajustement de Pantheon+ **que marginalement**
> comparé à ce qu'impose le hasard structurel (univers à w libre), et
> cette suffisance de w = −1 survit aux déformations du groupe 𝒢.

## 2. Lexique gelé (un mot = un objet)

| Mot | Objet opératoire unique |
|-----|--------------------------|
| résidu | r_i(w) = μ_obs,i − μ_th(z_i ; w) avec μ_obs = m_b_corr, μ_th = 5·log₁₀(D_L) + 25 + M, D_L = (c/H0)·(1+z)·∫₀^z dz′/E(z′), E(z) = √(Ωm(1+z)³ + (1−Ωm)(1+z)^{3(1+w)}) |
| intégrale | trapèzes cumulés sur grille fixe linspace(0 ; 2,4 ; 262145), interpolée linéairement — identique pour toutes les configurations |
| bruit | σ_i = diagonale de la covariance STATONLY gelée (corrélations ignorées — déclaré) |
| χ²(w) | χ²(w) = Σ_i r_i(w)²/σ_i² |
| meilleur w | w_best = argmin de χ²(w) sur la grille gelée linspace(−1,4 ; −0,6 ; 81 points) |
| m (mesure) | m = −Δ, Δ = χ²(−1) − χ²(w_best) ≥ 0 (qualité croissante avec la suffisance de w = −1) |
| étendue nulle | w ∈ [−1,4 ; −0,6] (déclarée, symétrique autour de −1) |

## 3. Dictionnaire τ

    τ : résidus Pantheon+ ↦ coût de w = −1 face au meilleur w libre ↦ m

τ est cette carte elle-même.

## 4. Données et provenance (gelées)

- **Pantheon+** : donnees/mcs17/pantheon_ref.dat (1 701 SNe, colonnes zCMB
  et m_b_corr) et donnees/mcs17/pantheon_STATONLY.cov — déjà acquises et
  lues à MCS-17 (regard ailleurs déclaré) ; empreintes reconsignées dans le
  runner et le journal.
- Ancrage gelé : H0 = 67,4 ; M = −19,253 ; Ωm = 0,315 (Planck, déclaré) ;
  c = 299 792,458 km/s.
- Aucune nouvelle acquisition externe.

## 5. Groupe de déformations légitimes 𝒢

| g | Déformation | Ce qu'elle teste |
|---|-------------|-------------------|
| g1 | retrait des SNe z < 0,01 | domination du bas-z |
| g2 | retrait des SNe z > 1 | domination du haut-z |
| g3 | Ωm = 0,315 → 0,30 (courbe et nul recomptés) | dépendance à l'ancrage |
| g4 | bruit gonflé σ_i × 1,2 (systématiques déclarées) | dépendance aux incertitudes |
| g5 | grille w : 81 → 41 points | dépendance à la grille |
| g6 | retrait d'une supernova au hasard (PRNG public ChaCha20) | sensibilité locale |

## 6. Modèle nul

- **N1 (univers à w libre)** : 10 000 univers synthétiques : w ~ U[−1,4 ;
  −0,6] (PRNG public) ; μ_synth = μ_th(z ; w) + N(0, σ_i) (bruit diagonal
  calé sur la covariance réelle, déclaré) ; distribution de m → μ_null, u.
  (Nul de complexité égale : même échantillon, même bruit, même grille,
  w libre.)
- **N2 (permutation des résidus à w = −1)** : rapporté.

## 7. Contrôles positifs (sabotages obligatoires)

| c | Sabotage | Attendu si le test a du pouvoir |
|---|----------|----------------------------------|
| c1 | dérive injectée : μ′ = μ_obs + μ_th(z ; −0,85) − μ_th(z ; −1) | m se dégrade (|effet| ≥ 2 u) |
| c2 | données remplacées par un univers à w libre tiré du nul | m tombe vers μ_N1 (|effet| ≥ 2 u) |

c1 ou c2 vraiment muet (|effet| < 2 u, règle v2.0) → **CS0**.

## 8. Statistique et seuils (gelés)

- z_g = (m_g − μ_null,g)/u_g sous N1 pour chaque g ; Σ = min sur {g1…g6}.
- Seuil CS+ : **3,1** (famille des tensions cosmologiques — MCS-17 à 3,1,
  consigné des deux).
- Diagnostics rapportés (hors Σ) : Δ canonique, w_best réel sur la grille
  gelée, χ²(−1)/ndl — publiés, pas moyennés.

## 9. Critères de verdict

| Issue | Verdict |
|-------|---------|
| Σ ≥ 3,1 | CS+ — la suffisance de w = −1 est stable au sens MCS |
| 2 ≤ Σ < 3,1 | CSp |
| −2 < Σ < 2 | CS− (B3-FAIL) — la suffisance était structurelle |
| Σ ≤ −2 | CSi |
| un contrôle vraiment muet | CS0 |

## 10. Regard ailleurs (déclaration préalable)

Données Pantheon+ déjà lues (MCS-17). La tension H0 (niveau bas-z) est
publiée (MCS-17, CS+) ; elle contribue au χ² de toutes les configurations
de manière constante en w et s'annule dans Δ (déclaré). Aucune mesure de
w n'a été faite par la machine avant cette carte.

## 11. Critères d'arrêt

- CS+ → la constance de l'énergie noire est stable dans Pantheon+ sous
  l'ancrage gelé ; le diagnostic publie w_best et Δ.
- CS− ou CSi → B3-FAIL publié : la suffisance de w = −1 était structurelle
  au nul déclaré.
- CS0 → une seule refonte autorisée (MCS-20b).
- CSp → la carte dort.

## 12. Démonstration de puissance (règle 1.2 du manifeste v2.0)

Avant gel : sur un univers synthétique planté à w = −1 exact (positions z
et bruit de la configuration réelle — la puissance dépend de
l'échantillon, déclaré), la statistique doit donner Σ ≥ 3,1 et les deux
contrôles résoudre à |effet| ≥ 2 u ; sur un univers à w libre, CS−
attendu ; banc aveugle simulé → CS0. Hachée dans l'acte de gel. La démo
v1 (mesure de pente, impuissante) est publiée à côté — correction
déclarée en tête de carte.

## 13. Scellement (jalon 3 v2)

```
SHA256_CARTE : null
HORODATAGE   : null
```
