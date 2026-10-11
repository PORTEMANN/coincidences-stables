# CARTE MCS-16 — Ratios de masses gelés du corpus × masses mesurées

**Statut** : CANDIDAT — NON SCELLÉ — Jalon 1 v2 (rédaction, aucun calcul)
**Moteur** : v2.0 (manifeste MANIFESTE-MCS-v2.0.md — puissance démontrée avant gel)
**Domaines** : A = masses mesurées (PDG 2024/2022, CODATA 2022/2018 —
tables déjà empreintées au dépôt) ; B = **la liste figée des six règles de
ratios du corpus** (mvcg, chantier LOI-HARMONIQUE — bilan gelé cité par
empreinte ; chaque règle a déjà été pesée *ponctuellement* par mvcg, mot
S+/P publié — la MCS mesure la **stabilité d'ensemble sous 𝒢**, opérateur
différent).
**Attente honnête** : mitigée, comme Titius-Bode : deux règles sub-% (muon,
Z), deux à ~1 % (up, charm), deux en zone grise (strange, bottom, ~12 %).
Le RMS sera dominé par les deux P — la question est de savoir si
l'ensemble dépasse le hasard structurel et si la zone grise tue la
stabilité, comme Neptune tuait Titius-Bode. Attente : CSp ou CS−.

---

## 1. Énoncé de la coïncidence candidate

> Les six règles figées du corpus (section 4) prédisent les masses mesurées
> **au-delà de ce que produit le hasard structurel** (mêmes règles, masses
> permutées ou libres), et l'accord d'ensemble survit aux déformations du
> groupe 𝒢.

## 2. Lexique gelé (un mot = un objet)

| Mot | Objet opératoire unique |
|-----|--------------------------|
| règle | l'une des six formules figées de la section 4 (aucune constante recalibrée) |
| écart | ε(i) = log₁₀(prédit_i / mesuré_i) pour le ratio i |
| m (mesure) | m = −log₁₀( RMS(ε) ) sur les règles de la configuration |
| α | constante de structure fine de la table CODATA de la configuration |
| masses | tables PDG de la configuration ; quarks en MS-bar à 2 GeV (déclaré) |

## 3. Dictionnaire τ

    τ : règles figées du corpus ↦ masses prédites ↦ écarts aux masses mesurées ↦ m

τ est cette carte elle-même.

## 4. Les six règles figées (citées du bilan gelé de mvcg)

| # | Nom mvcg | Règle figée | Mot mvcg |
|---|----------|-------------|----------|
| 1 | LH_Muon_Quinte | m_μ = m_e·(3/2)/α | S+ (0,59 %) |
| 2 | LH_Z_Diagonale | m_Z = m_p/(α·√2) | S+ (0,30 %) |
| 3 | LH_Strange_Quarte | m_s = m_p/9 | P (12,1 %) |
| 4 | LH_Bottom_G6 | m_b = 4·m_c^corps/2^{1/12} (m_c^corps = 1 251,029 MeV gelé — chaîne interne déclarée) | P (13,0 %) |
| 5 | LH_Up_G3 | m_u = (m_p/18)·√α/2 | S+ (3,1 %) |
| 6 | LH_Charm_G5 | m_c = 24·m_p/18 | S+ (1,5 %) |

La provenance : bilan du chantier LOI-HARMONIQUE de mvcg (document gelé,
cité par empreinte dans le runner). **Circularité déclarée** : les règles
furent trouvées sur ces masses (recherche) — payée au seuil (section 8).

## 5. Données et provenance (gelées)

- **PDG** `mass_width_2024.mcd` (canonique) et `mass_width_2022.mcd` (g1) ;
  **CODATA** `allascii_2022.txt` (α, canonique) et `allascii_2018.txt` (g2) —
  les quatre tables sont déjà acquises et empreintées au dépôt (campagnes
  MCS-04/MCS-08) ; réutilisation re-consignée. Aucune règle n'a été
  recalculée depuis ces tables avant la rédaction.
- Le bilan mvcg est cité par empreinte ; les règles sont écrites dans le
  runner **avant** tout calcul, avec leurs mots mvcg.

## 6. Groupe de déformations légitimes 𝒢

| g | Déformation | Ce qu'elle teste |
|---|-------------|-------------------|
| g1 | PDG 2024 → PDG 2022 (ratios disponibles dans les deux éditions, déclaré) | dépendance à l'édition |
| g2 | α CODATA 2022 → CODATA 2018 | dépendance à α |
| g3 | retrait de la règle muon (la plus précise) | domination d'un S+ |
| g4 | retrait de la règle bottom (la pire) | domination d'un P |
| g5 | retrait des deux règles P (strange + bottom) | la zone grise porte-t-elle tout ? |
| g6 | retrait d'une règle au hasard (PRNG public ChaCha20) | sensibilité locale |

## 7. Modèle nul

- **N1 (assignation permutée)** : 10 000 permutations des masses mesurées
  entre les six règles ; distribution de m → μ_null, u.
- **N2 (masses libres)** : masses tirées log-uniformément dans l'étendue
  du zoo déclarée [0,5 MeV ; 173 GeV] ; distribution de m (rapporté).

## 8. Statistique, contrôles et seuils (gelés)

- z_g = (m_g − μ_null,g)/u_g sous N1 pour chaque g ; Σ = min sur {g1…g6}.
- Contrôles positifs : **c1** masses permutées entre règles (l'assignation
  s'effondre, |effet| ≥ 2 u attendu) ; **c2** constantes des six règles
  altérées de ×1,05 (déclaré) — m se dégrade (|effet| ≥ 2 u).
  c1 ou c2 vraiment muet (|effet| < 2 u, règle v2.0) → **CS0**.
- Seuil CS+ : **3,2** = 3,0 (base) + 0,1 (famille éprouvée : MCS-04, CS−
  publié) + 0,1 (circularité : règles trouvées sur les masses).
- Diagnostic rapporté (hors Σ) : ε par règle (l'information honnête :
  quelles règles tiennent — la frontière grise est nommée, pas moyennée).

## 9. Critères de verdict

| Issue | Verdict |
|-------|---------|
| Σ ≥ 3,2 | CS+ — la récolte du corpus est stable au sens MCS |
| 2 ≤ Σ < 3,2 | CSp |
| −2 < Σ < 2 | CS− (B3-FAIL) |
| Σ ≤ −2 | CSi |
| un contrôle vraiment muet | CS0 |

## 10. Regard ailleurs (déclaration préalable)

La famille « loi harmonique globale » a été tuée par MCS-04 (CS− publié :
non spécifique au pas près). Les six règles sont des contacts **locaux**
tenus sous mvcg (opérateur ponctuel) — la présente carte mesure leur
stabilité d'ensemble sous 𝒢, opérateur distinct déclaré. La circularité
(recherche des règles sur les masses) est payée au seuil.

## 11. Critères d'arrêt

- CS+ → la récolte tient sous 𝒢 ; publiée avec la circularité en tête.
- CS− ou CSi → les règles locales étaient du hasard structurel à seuil
  local (B3-FAIL) — les mots mvcg restent ce qu'ils sont (verdicts
  ponctuels, non stabilité).
- CS0 → une seule refonte autorisée (MCS-16b).
- CSp → la carte dort.

## 12. Démonstration de puissance (règle 1.2 du manifeste v2.0)

Avant gel : sur des masses synthétiques plantées sur les six règles à
0,5 % près, la statistique doit donner Σ ≥ 3,2 et les deux contrôles
résoudre à |effet| ≥ 2 u ; sur des masses libres, CS− attendu ; banc
aveugle simulé → CS0. Hachée dans l'acte de gel.

## 13. Scellement (jalon 3 v2)

```
SHA256_CARTE : fd0b290b655ddd225d91dd1f97b0b4872d94bb5a078b13ab5bbeb28f3a938ed1
HORODATAGE   : 2026-10-11T18:55:51Z
```
