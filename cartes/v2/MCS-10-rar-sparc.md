# CARTE MCS-10 — Relation d'accélération radiale × galaxies SPARC

**Statut** : CANDIDAT — NON SCELLÉ — Jalon 1 v2 (rédaction, aucun calcul)
**Moteur** : v2.0 (manifeste MANIFESTE-MCS-v2.0.md — puissance démontrée avant gel)
**Domaines** : A = courbes de rotation et contenus baryoniques des galaxies
(base publique SPARC, Lelli, McGaugh & Schombert 2016) ; B = la relation
d'accélération radiale figée par sa publication : g_RAR(g) = g / (1 − e^{−√(g/g†)}),
avec g† = 1,2 × 10⁻¹⁰ m/s² **gelée, aucun réajustement**.
**Attente honnête** : la relation est publiée comme serrée (dispersion
≈ 0,13 dex sur l'échantillon) — mais elle a été **ajustée sur cet échantillon**
(circularité déclarée, payée au seuil), et une partie du signal est
cinématiquement non indépendante (diagnostic déclaré). La question MCS :
la serréité survit-elle aux déformations du groupe 𝒢 — coupures de qualité,
choix de masse stellaire, géométrie ? CS+ possible ; ce serait le premier
CS+ non trivial de la machine.

---

## 1. Énoncé de la coïncidence candidate

> Pour les galaxies de la liste figée (section 4), l'accélération observée
> g_obs = V²/r est donnée par la fonction universelle figée g_RAR(g_bar) —
> g† gelée à sa valeur publiée — avec une dispersion résiduelle **plus faible
> que ce que produit le hasard structurel**, et cette serréité survit aux
> déformations du groupe 𝒢.

## 2. Lexique gelé (un mot = un objet)

| Mot | Objet opératoire unique |
|-----|--------------------------|
| point | un point de courbe de rotation (r, V_obs, V_gas, V_disk, V_bul) d'une galaxie de la liste |
| g_obs | V_obs² / r |
| g_bar | (|V_gas|·V_gas + Υ_d·|V_disk|·V_disk + Υ_b·|V_bul|·V_bul) / r, avec Υ_d = 0,5 et Υ_b = 0,7 (conventions SPARC déclarées, canaux canoniques) |
| résidu | ε = log₁₀(g_obs) − log₁₀(g_RAR(g_bar)), restreint aux points où g_bar > 0 |
| m (mesure) | m = −log₁₀( RMS(ε) ) sur les points de la configuration |
| loi plate | nul de complexité égale : pas de relation — appariements libres |

## 3. Dictionnaire τ

    τ : courbes de rotation + profils baryoniques ↦ (g_obs, g_bar) ↦ m

τ est cette carte elle-même. Toute modification de τ après le gel = nouvelle
carte, nouveau numéro.

## 4. Données et provenance (gelées)

- **SPARC** (Spitzer Photometry and Accurate Rotation Curves ; Lelli,
  McGaugh & Schombert 2016, AJ 152, 157 — base publique, fichiers de
  modèles de masse par galaxie) — acquisition à l'ouverture, empreintes
  consignées. Aucune ligne de la base n'a été lue avant la rédaction.
- **Liste figée** : toutes les galaxies du fichier de modèles de masse
  (la liste exacte est lue à l'exécution ; les déformations la filtrent
  selon les critères déclarés de la section 5).
- **Déclaration de circularité** : g† a été ajustée sur cet échantillon en
  2016 ; elle est gelée ici à sa valeur publiée (aucun réajustement) et la
  circularité est payée au seuil (section 8).
- **Déclaration de non-indépendance cinématique** : g_obs et g_bar partagent
  la courbe de rotation via V_disk ; la composante indépendante est le gaz.
  Diagnostic rapporté (hors Σ) : la relation mesurée sur la composante
  gazeuse seule (g_bar → g_gas seul).

## 5. Groupe de déformations légitimes 𝒢

| g | Déformation | Ce qu'elle teste |
|---|-------------|-------------------|
| g1 | galaxies de qualité Q = 1 seulement (drapeau publié de la base) | dépendance à la qualité des courbes |
| g2 | Υ_d : 0,5 → 0,7 (autre convention publiée) | dépendance à la masse stellaire |
| g3 | retrait des galaxies d'inclinaison < 30° (géométrie mal contrainte) | dépendance géométrique |
| g4 | retrait des points r < 1 kpc (centres, bulbes complexes) | dépendance radiale |
| g5 | retrait des galaxies dont la distance n'est pas de qualité « étoile » (colonne déclarée de la base) | dépendance aux distances |
| g6 | retrait d'une galaxie au hasard (PRNG public ChaCha20) | sensibilité locale |

## 6. Modèle nul

- **N1 (appariements permutés)** : 10 000 permutations des profils
  baryoniques entre galaxies (V_obs conservé, profils gaz/disque/bulge
  réassignés à d'autres galaxies) ; distribution de m → μ_null, u.
- **N2 (radii permutés)** : permutation des rayons au sein de chaque galaxie,
  10 000 fois (rapporté).

## 7. Contrôles positifs (sabotages obligatoires)

| c | Sabotage | Attendu si le test a du pouvoir |
|---|----------|----------------------------------|
| c1 | radii permutés au sein de chaque galaxie (appariement point à point détruit) | m s'effondre vers N2 (|effet| ≥ 2 u) |
| c2 | échelle d'accélération doublée (g† → 2,4 × 10⁻¹⁰) | m se dégrade (|effet| ≥ 2 u) |

c1 ou c2 vraiment muet (|effet| < 2 u, règle v2.0) → **CS0**.

## 8. Statistique et seuils (gelés)

- z_g = (m_g − μ_null,g)/u_g sous N1 pour chaque g ; Σ = min sur {g1…g6}.
- Seuil CS+ : **3,1** = 3,0 (base) + 0,1 (ajustement historique de g† sur
  l'échantillon, déclaré).
- Diagnostics rapportés (hors Σ) : relation sur g_gas seul ; dispersion par
  galaxie (médiane des RMS intra-galaxie).

## 9. Critères de verdict

| Issue | Verdict |
|-------|---------|
| Σ ≥ 3,1 | CS+ — premier CS+ non trivial ; la RAR est stable au sens MCS |
| 2 ≤ Σ < 3,1 | CSp |
| −2 < Σ < 2 | CS− (B3-FAIL) |
| Σ ≤ −2 | CSi |
| un contrôle vraiment muet | CS0 |

## 10. Regard ailleurs (déclaration préalable)

La RAR n'a jamais été éprouvée par la machine ni le corpus. L'ajustement
historique de g† sur l'échantillon est déclaré et payé au seuil. Le débat
MOND/ΛCDM est extérieur à la carte : la machine mesure la **stabilité** de
la correspondance, pas son interprétation. Bases consultées avant gel : 0.

## 11. Critères d'arrêt

- CS+ → la RAR est une coïncidence stable mesurée ; publication avec la
  circularité et le diagnostic cinématique en tête de lecture.
- CS− ou CSi → carte fermée (B3-FAIL) ; la serréité publiée était un
  artefact de sélection ou de construction.
- CS0 → une seule refonte autorisée (MCS-10b).
- CSp → la carte dort.

## 12. Démonstration de puissance (règle 1.2 du manifeste v2.0)

Avant gel : sur un échantillon synthétique de galaxies plantées sur la
relation figée (dispersion 0,13 dex déclarée), la statistique doit donner
Σ ≥ 3,1 et les deux contrôles résoudre à |effet| ≥ 2 u ; sur des
appariements libres, CS− attendu ; banc aveugle simulé → CS0. Hachée dans
l'acte de gel.

## 13. Scellement (jalon 3 v2)

```
SHA256_CARTE : c9c9d6fdf4841ffe4e2cf37b2e447372a4ef48bad502ff58abc053aadf668089
HORODATAGE   : 2026-10-11T06:53:31Z
```
