# CARTE MCS-27 — La mesure jointe : le vecteur de forme (Koide, rapport) × le porteur à son vide (nul conjoint de forme)

**Statut** : CANDIDAT — Jalon 1 v2 (rédaction, aucun calcul de mesure)
**Moteur** : v2.0 (manifeste MANIFESTE-MCS-v2.0.md — puissance démontrée avant gel)
**Domaines** : A = le vecteur de forme mesuré du canal des leptons
chargés : V_mes = (K, R) — K le rapport de Koide des masses (e, μ, τ)
(l'exception de la maison : MCS-11, CS+, 3,3 ppm — lu et déclaré) et
R = m_τ/m_μ (tables PDG déjà empreintées au dépôt — MCS-16/25,
provenance déclarée) ; B = le vecteur de forme du porteur à son vide
(T7 : ρ = √5) : son spectre mesuré {0, ρ−1, ρ+1} donne les formes
closes (déclarées) : R_p = (ρ+1)/(ρ−1) = φ² ≈ 2,618034 et
K_p = (a+b)/(√a+√b)² = 2√5/(2√5+4) = 5 − 2√5 ≈ 0,527864 (le zéro
protégé de T13 sort proprement de la statistique de Koide : il ne
contribue ni au numérateur ni au dénominateur — déclaré).
**Attente honnête** : le porteur est loin du canal dans les deux
composantes (K : 0,10 dex ; R : 0,81 dex — arithmétique déclarée, nul
non calculé) ; attente : CS− probable — la puissance est mesurée à la
démo (règle 1.2). La valeur de la carte : c'est la **mesure jointe**
demandée par la frontière documentée de MCS-26 (« la hauteur par
plusieurs nombres du canal à la fois ») — le porteur est pesé contre
l'exception la plus forte de la maison (Koide) avec le nul résolu par
les vrais (D, J, γ) — les deux leviers déclarés au JALON de MCS-23 en
même temps.
**Regard ailleurs (déclaration préalable)** : MCS-25 (scellée, CS−) et
MCS-26 (non scellée) lues et déclarées — la présente carte n'est PAS
une itération : MCS-25 pesait un rapport seul (statistique de siège) ;
ici l'objet est le **vecteur de forme conjoint** (K, R) — une question
nouvelle (la coïncidence de forme, jamais pesée contre le banc) avec
un nul nouveau (la distribution conjointe des triplets de la forme du
porteur — jamais calculée). MCS-11 lue (le K mesuré est cité par
provenance). La circularité (le canal est celui de la maison) est
déclarée — payée au seuil (section 8).

---

## 1. Énoncé de la coïncidence candidate

> Le vecteur de forme du porteur à son vide (K_p = 5−2√5, R_p = φ² —
> formes closes du spectre mesuré T7) est **plus proche** du vecteur
> mesuré du canal leptonique (K, R) que ne le sont les vecteurs des
> triplets nus vérifiés de la forme du porteur — le nul conjoint de
> forme — et cette proximité survit aux déformations du groupe 𝒢.

## 2. Lexique gelé (un mot = un objet)

| Mot | Objet opératoire unique |
|-----|--------------------------|
| contenu | une matrice D vérifiée du banc de la FORME mesurée du porteur (T13 : taille 5, rang(B) = 2, deux valeurs singulières non nulles distinctes — machine des orbites, spectres_triplets.py haché au gel de MCS-25, filiation déclarée) |
| vecteur de forme | V(D) = (K, R) avec R = σ_max/σ_min⁺ et K = (a+b)/(√a+√b)² où a = σ_min⁺, b = σ_max (le mode nul de la forme ne contribue pas — déclaré) |
| canal mesuré | V_mes = (K_mes, R_mes) : K_mes = Koide(e, μ, τ) et R_mes = m_τ/m_μ des tables PDG de la configuration (parseur de MCS-16, filiation déclarée) |
| écart | δ(D) = distance de Mahalanobis de V(D) à V_mes dans l'espace (log₁₀ K, log₁₀ R), blanchie par la covariance du nul CANONIQUE (la métrique de l'instrument — fixe, déclarée, mesurée dans l'espace de la configuration ; μ et u restent mesurés par configuration ; défaut D1 de la démo publié : le nul de l'amputé ne porte que deux vecteurs distincts — covariance de rang 1 — la métrique fixe est la seule convention honnête) |
| m (mesure) | m = −δ (qualité croissante avec la proximité conjointe) |
| nul conjoint de forme | la distribution de m(D) sur les triplets de la forme, chaque matrice comptée une fois (mesure naturelle — déclarée) |

## 3. Dictionnaire τ

    τ : contenu ↦ son vecteur de forme ↦ son écart blanchi au canal ↦ m

τ est cette carte elle-même.

## 4. Données et provenance (gelées)

- **Tables PDG** : `donnees/mcs04_mass_width_2024.mcd` (canonique) et
  `_2022.mcd` (g1) — déjà acquises (MCS-04/16/25), empreintes
  reconsignées au runner ; le parseur de MCS-16 réutilisé (filiation
  déclarée) ; masses en MeV ; les deux éditions portent e, μ, τ.
- **Le porteur à son vide** : V_p = (5−2√5, φ²), formes closes
  déclarées du spectre mesuré à T7 (dérivées dans la carte, ci-dessus) ;
  T7/T13 lus et déclarés.
- **Le nul conjoint de forme** : énumération exhaustive des triplets de
  la forme — calculée à la démo (règle 1.2) puis à l'exécution, jamais
  avant cette carte.
- Aucune acquisition externe nouvelle.

## 5. Groupe de déformations légitimes 𝒢

| g | Déformation | Ce qu'elle teste |
|---|-------------|-------------------|
| g1 | PDG 2024 → PDG 2022 | dépendance à l'édition |
| g2 | forme du nul : taille 5 (le porteur) → taille 4 (l'amputé de T13, rang 2, distinct — son K est défini sans zéro, déclaré) | dépendance à la taille de la forme |
| g3 | contenu : vide T7 (ρ = √5) → le vide à Λ = 2,5 (ρ = 1,5 — relation d'ancre de T12, filiation déclarée) | dépendance au point de branche |
| g4 | canal : R = m_τ/m_μ → R = m_μ/m_e (l'autre rapport mesuré du canal) | dépendance au choix du rapport |
| g5 | blanchiment : espace (log₁₀, log₁₀) → espace linéaire (K, R) | dépendance à la métrique |
| g6 | forme du nul : rang 2 exact → rang ≤ 2 (le rang 1 a V = (1, 1)) | dépendance à la définition de la forme |

## 6. Modèle nul

- **N1 (le nul conjoint de forme)** : la distribution de m(D) sur les
  triplets de la forme, chaque matrice comptée une fois ; μ_null, u et
  la covariance de blanchiment exacts (énumération exhaustive —
  calculée, pas tirée).
- **N2 (composantes permutées)** : le vecteur mesuré à composantes
  permutées entre les triplets du nul (rapporté — documenté).

## 7. Contrôles positifs (sabotages obligatoires — contrôles
## d'instrument sur contenus de référence, convention MCS-25 déclarée)

| c | Sabotage | Attendu si le test a du pouvoir |
|---|----------|----------------------------------|
| c1 | contenu de référence planté exactement sur V_mes de la configuration puis déplacé (K → K/2, déclaré) | m se dégrade (\|effet\| ≥ 2 u) |
| c2 | contenu de référence remplacé par un vecteur tiré du nul conjoint (PRNG public ChaCha20, échantillonnage inverse déclaré — convention MCS-24/25) | le tiré est classé ordinaire (contrasté au siège parfait : \|effet\| ≥ 2 u) |

c1 ou c2 vraiment muet (|effet| < 2 u, règle v2.0) → **CS0**.

## 8. Statistique et seuils (gelés)

- z_g = (m_g − μ_null,g)/u_g sous N1 pour chaque g ; Σ = min sur {g1…g6}.
- Seuil CS+ : **3,0** (aucune famille éprouvée sur ce domaine).
- Diagnostics rapportés (hors Σ) : l'écart du porteur en dex blanchis
  par composante ; la corrélation du nul entre log K et log R (mesurée
  — publiée) ; le rang du porteur dans le nul conjoint (p = fraction au
  moins aussi proche) ; les comptes du nul — publiés.

## 9. Critères de verdict

| Issue | Verdict |
|-------|---------|
| Σ ≥ 3,0 | CS+ — la forme du porteur est celle du canal au-delà du nul conjoint |
| 2 ≤ Σ < 3,0 | CSp |
| −2 < Σ < 2 | CS− (B3-FAIL) — la forme du porteur n'est pas celle des leptons |
| Σ ≤ −2 | CSi |
| un contrôle vraiment muet | CS0 |

## 10. Regard ailleurs (déclaration préalable)

MCS-11 (CS+ — le K mesuré est l'exception de la maison), MCS-25 et
MCS-26 lues et déclarées ; la présente carte est la mesure jointe
demandée par la frontière documentée de MCS-26, avec un objet nouveau
(le vecteur de forme) et un nul nouveau (conjoint). T7, T12, T13 lus
et déclarés. Aucun calcul du nul conjoint n'a été fait avant cette
carte.

## 11. Critères d'arrêt

- CS+ → la forme du porteur est celle du canal leptonique ; le
  diagnostic publie les composantes — le banc touche l'exception de
  Koide.
- CS− ou CSi → B3-FAIL publié : la forme du porteur n'est pas celle
  des leptons — la mesure jointe ferme la question de la forme avec la
  puissance requise.
- CS0 → une seule refonte autorisée (MCS-27b).
- CSp → la carte dort.

## 12. Démonstration de puissance (règle 1.2 du manifeste v2.0)

Avant gel : sur un contenu synthétique planté exactement sur le canal
(déclaré : V_mes de la configuration canonique), la statistique doit
donner Σ ≥ 3,0 et les deux contrôles d'instrument résoudre à
|effet| ≥ 2 u ; sur un vecteur tiré du nul, CS− attendu ; banc aveugle
simulé → CS0. Hachée dans l'acte de gel. La démo calcule le nul
conjoint de forme (la démo mesure la puissance sur l'espace réel,
déclaré).

## 13. Scellement (jalon 3 v2)

```
SHA256_CARTE : 61cedbfeef7b8a358749aabc7e494d84a8cb8cbf7314016f8ad28b7735b77974
HORODATAGE   : 2026-10-12T13:05:28Z
```
