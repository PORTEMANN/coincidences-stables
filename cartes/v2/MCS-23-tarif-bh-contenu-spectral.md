# CARTE MCS-23 — Tarif de Bekenstein-Hawking × contenu spectral déclaré du corpus

**Statut** : CANDIDAT — Jalon 1 v2 (rédaction, aucun calcul de mesure)
**Moteur** : v2.0 (manifeste MANIFESTE-MCS-v2.0.md — puissance démontrée avant gel)
**Domaines** : A = la densité d'entropie des horizons η = 1/(4ℏG)
(Bekenstein-Hawking, produite par l'équation d'état locale de Jacobson —
constantes G, ℏ, c de CODATA, déjà acquises à MCS-08/16, déclaré) ;
B = le contenu spectral déclaré du corpus : triplet fini (A_F = C²,
H_F = C⁷, matrice de multiplicités m = [[0,2],[2,3]], KO-dimension 6) porté
par D_GLOBAL = D_phys ⊗ I_noet + Σ Γ_k A_Ek, coupure Λ = M_P déclarée
« naturelle » par le corpus (Principes V), action spectrale Tr f(D/Λ).
**Attente honnête** : la lecture rapide donne η proche du tarif à ~0,1–0,2 dex
(le 7 déclaré face au 3π/2 requis par la normalisation gelée) — mais le nul
combinatoire de la fenêtre contient des contenus plus proches encore.
Attente : CS− ou CSi, CSp possible.
**Regard ailleurs (déclaration préalable)** : l'erratum du dépôt
spectral-triple-minimality (2026-09-06) est lu et déclaré : le compte
« 63 160 réalisations » est réfuté comme publié (0 solution sous la logique
publiée) ; le statut de la dimension 7 dépend de la table KO-6 (sous la
table usuelle L1, le lemme de parité l'exclut) ; le triplet minimal
matriciellement vérifié du corpus est C4 (H_F = C⁴, table A3b). Les pages
du corpus (C-TRIPLET-SPECTRAL, C-META-LOI, Principes V) sont lues avant
rédaction — elles sont la réclame gelée, pas les données.

---

## 1. Énoncé de la coïncidence candidate

> Le coefficient d'Einstein-Hilbert induit par le contenu spectral déclaré
> (chaîne gelée ci-dessous) reproduit le tarif des horizons η = 1/(4ℏG)
> **mieux** que les contenus spectraux libres de même fenêtre — la caisse
> déclarée du corpus encaisse au bon taux, au-delà du hasard combinatoire.

## 2. Lexique gelé (un mot = un objet)

| Mot | Objet opératoire unique |
|-----|--------------------------|
| contenu | une matrice de multiplicités m symétrique k×k (k ≤ 3), entrées ∈ {0,1,2,3}, Σm ∈ [2,24] (fenêtre Krajewski datée, CONVENTIONS.md C-BORNES) |
| N_eff | N_eff(m) = Σ_ij m_ij (proxy de dimension, même convention que le dépôt : le triplet thèse m = [[0,2],[2,3]] donne 7 = dim H_F déclarée) |
| chaîne du tarif | 1/G_ind = (2/3π)·N_eff·f₂·Λ² (normalisation Connes-Chamseddine gelée : coefficient du a₂ de Seeley-DeWitt pour Tr f(D/Λ) sur géométrie produit M₄ × F) ; f₂ = 1 (fonction test normalisée, gelée) ; Λ = M_P non réduite (canonique) |
| écart | δ(m) = log₁₀(η(m)/η_BH) = log₁₀((2/3π)·N_eff(m)·G_N·M_P²) en unités ℏ = c = 1 (G_N CODATA 2022 : 6,67430×10⁻¹¹ m³ kg⁻¹ s⁻² ; M_P = 1,2209×10¹⁹ GeV gelé) |
| m (mesure) | mesure = −|δ| (qualité croissante avec la proximité du tarif) |
| tarif requis | N_req = 3π/2 ≈ 4,712 (le N_eff qui saturera η_BH sous la chaîne gelée) |

## 3. Dictionnaire τ

    τ : matrice de multiplicités déclarée ↦ N_eff ↦ G_induite ↦ écart au tarif ↦ m

τ est cette carte elle-même.

## 4. Données et provenance (gelées)

- **Constantes** : G_N (CODATA 2022, fichier donnees/mcs08_allascii_2022.txt
  déjà acquis — MCS-08/16, empreintes reconsignées au runner) ; M_P gelée
  dans le runner (convention déclarée).
- **Contenu déclaré du corpus** : m = [[0,2],[2,3]] (C-TRIPLET-SPECTRAL,
  index.portemann.eu, lu avant rédaction — déclaré) ; triplet vérifié C4
  (ERRATUM « ce qui reste valide » — déclaré).
- **Nul** : énumération exacte de la fenêtre gelée (§2) — aucun tirage,
  distribution exacte calculée (déclaré).
- Aucune nouvelle acquisition de fichiers externes.

## 5. Groupe de déformations légitimes 𝒢

| g | Déformation | Ce qu'elle teste |
|---|-------------|-------------------|
| g1 | contenu thèse (Σm = 7) → triplet vérifié C4 (Σm = 4) | dépendance au contenu déclaré |
| g2 | Λ = M_P → Λ = M̄_P = M_P/√(8π) (réduite) | dépendance à la convention de coupure |
| g3 | G_N CODATA 2022 → CODATA 2018 (6,67408×10⁻¹¹ gelé) | dépendance à l'édition |
| g4 | table KO-6 usuelle L1 : lemme de parité — la dimension impaire est exclue, mesure recomptée sur H_F = C⁸ (plus proche pair admis, déclaré) | dépendance à la table de signes |
| g5 | fenêtre du nul : m_ij ≤ 3 → m_ij ≤ 4 (le nul s'élargit) | dépendance à la fenêtre |
| g6 | retrait d'une entrée non nulle de m au hasard (PRNG public ChaCha20) | sensibilité locale |

## 6. Modèle nul

- **N1 (contenus libres de la fenêtre)** : l'énumération exacte de toutes
  les matrices de la fenêtre gelée (§2) ; distribution exacte de m →
  μ_null, u. (Nul de complexité égale : même fenêtre, même chaîne, aucun
  tarif visé.)
- **N2 (m permutée)** : entrées de la matrice déclarée permutées (rapporté —
  Σm invariant par construction, documenté comme tel).

## 7. Contrôles positifs (sabotages obligatoires)

| c | Sabotage | Attendu si le test a du pouvoir |
|---|----------|----------------------------------|
| c1 | contenu déplacé : N_eff ×10 (déclaré) | m se dégrade (|effet| ≥ 2 u) |
| c2 | contenu remplacé par une matrice tirée du nul (PRNG) | m tombe vers μ_N1 (|effet| ≥ 2 u) |

c1 ou c2 vraiment muet (|effet| < 2 u, règle v2.0) → **CS0**.

## 8. Statistique et seuils (gelés)

- z_g = (m_g − μ_null,g)/u_g sous N1 pour chaque g ; Σ = min sur {g1…g6}.
- Seuil CS+ : **3,0** (aucune famille éprouvée par la machine sur ce
  domaine).
- Diagnostics rapportés (hors Σ) : δ canonique en dex, N_req, et le rang
  du contenu déclaré dans le nul (p = fraction des contenus de la fenêtre
  au moins aussi proches du tarif) — publié, pas moyenné.

## 9. Critères de verdict

| Issue | Verdict |
|-------|---------|
| Σ ≥ 3,0 | CS+ — la caisse déclarée encaisse au bon taux, au-delà du hasard |
| 2 ≤ Σ < 3,0 | CSp |
| −2 < Σ < 2 | CS− (B3-FAIL) — la proximité était combinatoire |
| Σ ≤ −2 | CSi — le hasard de la fenêtre fait mieux |
| un contrôle vraiment muet | CS0 |

## 10. Regard ailleurs (déclaration préalable)

Erratum 2026-09-06 du dépôt lu et déclaré (E1–E4 : compte réfuté, « sept
bandes » sans objet machine, table KO-6, C4 vérifié). Pages du corpus lues
avant rédaction (déclaré). La question « qui encaisse » est déclarée comme
métaphore du corpus ; la carte ne mesure que le tarif. Aucun calcul de
η sous la chaîne gelée n'a été effectué par la machine avant cette carte.

## 11. Critères d'arrêt

- CS+ → le contenu déclaré est exceptionnellement proche du tarif ; le
  diagnostic publie le rang dans la fenêtre.
- CS− ou CSi → la proximité était combinatoire (B3-FAIL publié) : le
  programme devra réparer l'énumération (vrais (D, J, γ) — question ouverte
  de l'erratum) avant toute MCS-23b.
- CS0 → une seule refonte autorisée (MCS-23b).
- CSp → la carte dort.

## 12. Démonstration de puissance (règle 1.2 du manifeste v2.0)

Avant gel : sur un contenu synthétique planté au tarif (N_eff = 5, l'entier
le plus proche de 3π/2 dans la fenêtre), la statistique doit donner
Σ ≥ 3,0 et les deux contrôles résoudre à |effet| ≥ 2 u ; sur un contenu
libre, CS− attendu ; banc aveugle simulé → CS0. Hachée dans l'acte de gel.

## 13. Scellement (jalon 3 v2)

```
SHA256_CARTE : null
HORODATAGE   : null
```
