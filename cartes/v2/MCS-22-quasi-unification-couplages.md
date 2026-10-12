# CARTE MCS-22 — Quasi-unification des couplages SM × running gelé

**Statut** : CANDIDAT — Jalon 1 v2 (rédaction, aucun calcul de mesure)
**Moteur** : v2.0 (manifeste MANIFESTE-MCS-v2.0.md — puissance démontrée avant gel)
**Domaines** : A = les trois couplages de jauge du modèle standard mesurés
à M_Z (α̂_em, sin²θ_W, α_s — PDG, éditions 2024/2022, valeurs gelées dans
le runner avec sources) ; B = la quasi-unification : les trois droites de
running 1-loop (coefficients SM gelés, normalisation SU(5) gelée) se
croisent presque — la question est la **stabilité de la quasi-fermeture**
sous 𝒢, pas son existence.
**Attente honnête** : la littérature sait que le SM manque l'unification
(la SUSY la répare) ; MCS-18 et MCS-19 ont montré que les mesures sur
trois nombres manquent de pouvoir — cette carte utilise une mesure
continue (le gap au croisement), mais le nul peut recouvrir le signal.
Attente : incertaine, non scellure possible.

---

## 1. Énoncé de la coïncidence candidate

> Le gap résiduel des trois couplages au croisement des deux premiers est
> **plus petit** que ce que produit le hasard structurel (couplages libres
> dans les étendues déclarées, même running), et cette fermeture survit
> aux déformations du groupe 𝒢 — la quasi-unification SM est stable au
> sens MCS.

## 2. Lexique gelé (un mot = un objet)

| Mot | Objet opératoire unique |
|-----|--------------------------|
| couplages | y₁ = 1/α₁ = (3/5)·cos²θ_W·α̂_em⁻¹ ; y₂ = 1/α₂ = sin²θ_W·α̂_em⁻¹ ; y₃ = 1/α_s (normalisation SU(5) gelée) |
| running | y_i(t) = y_i(M_Z) − (b_i/2π)·t, t = ln(μ/M_Z), b = (41/10 ; −19/6 ; −7) (SM 1-loop, gelé) |
| croisement | t₁₂ = (y₁₀ − y₂₀)/((b₁ − b₂)/2π) |
| gap | g = |y₃(t₁₂) − y₁(t₁₂)| |
| m (mesure) | m = −g (qualité croissante avec la fermeture) |
| étendue nulle | α̂_em⁻¹ ∈ [120 ; 140], sin²θ_W ∈ [0,20 ; 0,27], α_s ∈ [0,09 ; 0,15] (déclarées) |

## 3. Dictionnaire τ

    τ : couplages mesurés à M_Z ↦ running gelé ↦ gap au croisement ↦ m

τ est cette carte elle-même.

## 4. Données et provenance (gelées)

Constantes gelées dans le runner, sources publiques vérifiées avant
rédaction (convention MCS-16 : aucune acquisition de fichiers) :

- **Canonique (PDG 2024)** : α̂_em⁽⁵⁾(M_Z)⁻¹ = 127,930 ± 0,008 (revue
  Standard Model PDG 2024) ; sin²θ_W(M_Z) MS-bar = 0,23129 ± 0,00004
  (fit global PDG 2024) ; α_s(M_Z) = 0,1180 ± 0,0009 (moyenne mondiale
  PDG 2024) ; M_Z = 91,1880 GeV.
- **Édition déclarée pour g1 (PDG 2022)** : α̂_em⁽⁵⁾(M_Z)⁻¹ = 127,951 ±
  0,009 ; sin²θ_W(M_Z) MS-bar = 0,23122 ± 0,00004 ; α_s inchangé (valeur
  2022 non gelée — déclaré).
- **Convention déclarée pour g5** : sin²θ_W on-shell = 1 − m_W²/m_Z² avec
  m_W = 80,3692 GeV (PDG 2024, gelé).

## 5. Groupe de déformations légitimes 𝒢

| g | Déformation | Ce qu'elle teste |
|---|-------------|-------------------|
| g1 | constantes → édition PDG 2022 | dépendance à l'édition |
| g2 | constantes → toutes à +1σ publié | dépendance aux incertitudes |
| g3 | constantes → toutes à −1σ publié | dépendance aux incertitudes |
| g4 | gap mesuré au croisement t₁₃ au lieu de t₁₂ | dépendance à la référence |
| g5 | sin²θ_W MS-bar → on-shell (convention gelée) | dépendance au schéma |
| g6 | perturbation aléatoire des trois constantes dans ±0,5σ (PRNG public ChaCha20) | sensibilité locale |

## 6. Modèle nul

- **N1 (couplages libres)** : 10 000 triplets tirés uniformément dans les
  étendues déclarées ; même running gelé ; distribution de m → μ_null, u.
  (Nul de complexité égale : trois couplages, même loi d'évolution, aucune
  unification.)
- **N2 (couplages permutés entre rôles)** : rapporté (croisements hors
  fenêtre possibles, documenté comme tel).

## 7. Contrôles positifs (sabotages obligatoires)

| c | Sabotage | Attendu si le test a du pouvoir |
|---|----------|----------------------------------|
| c1 | α_s déplacée de +15 % (déclaré) | le gap augmente, m se dégrade (|effet| ≥ 2 u) |
| c2 | constantes remplacées par un triplet libre du nul | m tombe vers μ_N1 (|effet| ≥ 2 u) |

c1 ou c2 vraiment muet (|effet| < 2 u, règle v2.0) → **CS0**.

## 8. Statistique et seuils (gelés)

- z_g = (m_g − μ_null,g)/u_g sous N1 pour chaque g ; Σ = min sur {g1…g6}.
- Seuil CS+ : **3,0** (aucune famille éprouvée par la machine sur ce
  domaine).
- Diagnostics rapportés (hors Σ) : échelle du croisement μ₁₂ en GeV, gap
  canonique, et gap relatif g/y₁(t₁₂) — publiés sans moyennage.

## 9. Critères de verdict

| Issue | Verdict |
|-------|---------|
| Σ ≥ 3,0 | CS+ — la quasi-unification SM est stable au sens MCS |
| 2 ≤ Σ < 3,0 | CSp |
| −2 < Σ < 2 | CS− (B3-FAIL) — la quasi-fermeture était structurelle |
| Σ ≤ −2 | CSi |
| un contrôle vraiment muet | CS0 |

## 10. Regard ailleurs (déclaration préalable)

La non-unification du SM et la réparation SUSY sont publiées (déclaré) ;
la revue PDG citée au runner documente la prédiction α_s(M_Z) = 0,13 ±
0,01 sous unification SUSY. Les contacts mvcg sur les constantes sont
déclarés au registre. Aucun running n'a été calculé par la machine avant
cette carte.

## 11. Critères d'arrêt

- CS+ → la quasi-fermeture est stable ; le diagnostic publie μ₁₂ et le
  gap résiduel.
- CS− ou CSi → B3-FAIL publié : la quasi-unification était structurelle
  aux étendues déclarées.
- CS0 → une seule refonte autorisée (MCS-22b).
- CSp → la carte dort.

## 12. Démonstration de puissance (règle 1.2 du manifeste v2.0)

Avant gel : sur un triplet synthétique planté exactement unifié (α_s
ajustée pour fermer le gap, déclaré), la statistique doit donner Σ ≥ 3,0
et les deux contrôles résoudre à |effet| ≥ 2 u ; sur un triplet libre,
CS− attendu ; banc aveugle simulé → CS0. Hachée dans l'acte de gel.

## 13. Scellement (jalon 3 v2)

```
SHA256_CARTE : null
HORODATAGE   : null
```
