# CARTE MCS-17 — Tension H0 × échantillon Pantheon+ (stabilité)

**Statut** : CANDIDAT — NON SCELLÉ — Jalon 1 v2 (rédaction, aucun calcul)
**Moteur** : v2.0 (manifeste MANIFESTE-MCS-v2.0.md — puissance démontrée avant gel)
**Domaines** : A = l'échantillon Pantheon+ de supernovae (données gelées du
dépôt mvcg : `pantheon_ref.dat` + covariance, citées par empreinte) ;
B = la tension H0 mesurée : H0_SH0ES / H0_Planck − 1 ≈ 8,4 % (pesée mvcg,
publiée).
**Attente honnête** : la tension est un fait mesuré — la question MCS est sa
**stabilité sous déformations de l'échantillon** : si elle survit à toutes
les déformations légitimes de la base de supernovae, c'est une coïncidence
stable (et le désaccord cosmologique est robuste) ; sinon, elle était un
artefact de sélection. Attente : incertaine — c'est la question ouverte.

---

## 1. Énoncé de la coïncidence candidate

> L'écart entre le module mesuré au bas-z de l'échantillon et la courbe de
> Planck gelée dépasse le hasard structurel (permutations) et survit aux
> déformations du groupe 𝒢 (sous-échantillons, fenêtres de redshift,
> sélections de qualité déclarées).

## 2. Lexique gelé (un mot = un objet)

| Mot | Objet opératoire unique |
|-----|--------------------------|
| point | une supernova de Pantheon+ (redshift z, module de distance μ, covariance C) |
| extraction | 8 bins équipopulaires en z (déclaré, geste mvcg) ; module moyen par bin |
| m (mesure) | m = écart absolu entre le module moyen du bin le plus bas en z mesuré sur la configuration et sa valeur attendue sous la courbe de Planck gelée (la tension vit au bas-z ; zéro paramètre ajusté — déclaré) |
| courbe de Planck gelée | μ_th(z) = 5·log₁₀(c·z·(1+z)/H0_Planck) + M, avec H0_Planck = 67,4 km/s/Mpc et M = −19,253 (gelés, publiés) |
| ancrage | H0_Planck = 67,4 et H0_SH0ES = 73,04 km/s/Mpc (gelés, publiés) |

## 3. Dictionnaire τ

    τ : supernovae Pantheon+ ↦ bins en z ↦ modules ↦ tension mesurée ↦ m

τ est cette carte elle-même.

## 4. Données et provenance (gelées)

- **Pantheon+** : `pantheon_ref.dat` + `pantheon_STATONLY.cov` du dépôt mvcg
  (Brout et al. 2022 — fichiers gelés du corpus, cités par empreinte,
  téléchargés à l'ouverture depuis GitHub). Aucune ligne lue avant la
  rédaction.
- La valeur 8,4 % est la pesée publiée de mvcg (déclarée, pas relue).
- Ancrages gelés : 67,4 (Planck 2018) et 73,04 (SH0ES 2022).

## 5. Groupe de déformations légitimes 𝒢

| g | Déformation | Ce qu'elle teste |
|---|-------------|-------------------|
| g1 | retrait du bin le plus extrême en z (le plus haut) | domination d'un bord |
| g2 | 8 bins → 16 bins | dépendance au binning |
| g3 | retrait des supernovae z < 0,01 (tres proches, systématiques de flux) | dépendance au plancher |
| g4 | retrait des supernovae z > 1 (queue) | dépendance à la queue |
| g5 | covariance STATONLY → STAT+SYS | dépendance aux systématiques |
| g6 | retrait d'une supernova au hasard (PRNG public ChaCha20) | sensibilité locale |

## 6. Modèle nul

- **N1 (résidus permutés)** : 10 000 permutations des résidus
  (μ_obs − μ_courbe de Planck) entre supernovae (la tendance μ(z) est
  conservée, l'assignation des résidus est détruite) ; distribution de
  m → μ_null, u.
- **N2 (pas de tension)** : modules recomputés sous une seule ancre
  (H0 moyen déclaré 70,2) avec le bruit de la covariance — distribution
  de m (rapporté).

## 7. Contrôles positifs (sabotages obligatoires)

| c | Sabotage | Attendu si le test a du pouvoir |
|---|----------|----------------------------------|
| c1 | résidus permutés entre supernovae | la tension s'effondre (|effet| ≥ 2 u) |
| c2 | tension injectée doublée (déclarée : les modules bas-z décalés pour porter H0 × 1,17) | la mesure doit la retrouver (|effet| ≥ 2 u) |

c1 ou c2 vraiment muet (|effet| < 2 u, règle v2.0) → **CS0**.

## 8. Statistique et seuils (gelés)

- z_g = (m_g − μ_null,g)/u_g sous N1 pour chaque g ; Σ = min sur {g1…g6}.
- Seuil CS+ : **3,1** = 3,0 (base) + 0,1 (famille éprouvée : le chantier
  H0 de mvcg a pesé la tension — déclaré ; l'opérateur MCS est distinct).
- Diagnostic rapporté (hors Σ) : m par ancrage (Planck seul / SH0ES seul
  comme référence) — la direction de la tension est publiée, pas moyennée.

## 9. Critères de verdict

| Issue | Verdict |
|-------|---------|
| Σ ≥ 3,1 | CS+ — la tension est stable au sens MCS (robustesse mesurée) |
| 2 ≤ Σ < 3,1 | CSp |
| −2 < Σ < 2 | CS− (B3-FAIL) — la tension était un artefact de sélection |
| Σ ≤ −2 | CSi |
| un contrôle vraiment muet | CS0 |

## 10. Regard ailleurs (déclaration préalable)

Le chantier H0 de mvcg a pesé la tension (H0 Écart : P à θ = 5 % ; fibre
H(z) : {S+:1, S−:4}) — publié, déclaré. L'opérateur MCS (stabilité sous
𝒢 de l'échantillon) n'a jamais été appliqué. Fichiers lus avant gel : 0.

## 11. Critères d'arrêt

- CS+ → la tension est robuste aux déformations de l'échantillon ;
  publiée avec les pesées mvcg en tête.
- CS− ou CSi → la tension était un artefact de sélection (B3-FAIL publié).
- CS0 → une seule refonte autorisée (MCS-17b).
- CSp → la carte dort.

## 12. Démonstration de puissance (règle 1.2 du manifeste v2.0)

Avant gel : sur un échantillon synthétique avec tension plantée (8,4 %),
la statistique doit donner Σ ≥ 3,1 et les deux contrôles résoudre à
|effet| ≥ 2 u ; sur un échantillon sans tension, CS− attendu ; banc aveugle
simulé → CS0. Hachée dans l'acte de gel.

## 13. Scellement (jalon 3 v2)

```
SHA256_CARTE : e6097a0eb7d64071f8e9e64f911782121531b6884999c893d3554b0ed868c847
HORODATAGE   : 2026-10-11T19:50:05Z
```
