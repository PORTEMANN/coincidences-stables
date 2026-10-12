# CARTE MCS-26 — Le siège du vide × le canal neutrinos mesuré (nul réel spectral des masses²)

**CORRECTION PRÉ-GEL DÉCLARÉE (unique, précédents MCS-20/25)** : la
démo v1 (nul réel spectral complet de la fenêtre) est impuissante —
σ = 2,05 < 3,0, c2 = 1,18 u : à un seul rapport mesuré, le nul complet
a toujours une queue de sièges algébriques chanceux (leçon MCS-23) —
elle est publiée (validation/journal_puissance_mcs26_v1.jsonl et son
journal). La correction est le **nul de forme** : la correspondance est
déclarée par la forme spectrale mesurée du porteur (T13 : un mode nul
protégé + deux modes massifs, taille 5, rang 2, deux valeurs
singulières distinctes) — le nul pertinent est l'ensemble des triplets
de la fenêtre ayant exactement cette forme (déclaré, mesuré à la démo
v2) ; la déformation g2 passe à la forme de l'amputé (taille 4, rang 2
— T13) et g6 au rang ≤ 2 (dépendance à la définition de la forme).

**Statut** : CANDIDAT — Jalon 1 v2 (rédaction, aucun calcul de mesure)
**Moteur** : v2.0 (manifeste MANIFESTE-MCS-v2.0.md — puissance démontrée avant gel)
**Domaines** : A = le canal mesuré des splittings neutriniques :
R_ν = Δm²_31/Δm²_21 (NuFIT — acquisition déclarée du 12/10/2026 :
tables des paramètres épinglées et hachées dans donnees/mcs26/ :
v5.2 (2022), v5.3 (03/2024), v6.0 (09/2024) — provenance nu-fit.org,
analyse globale à trois saveurs) ; B = le contenu spectral du banc : le
porteur à son vide (T7 : ρ = √5 à Λ = 3 — mesuré, publié) dont le
rapport de masses² des deux modes massifs est la forme close
q = ((ρ+1)/(ρ−1))² = φ⁴ = (7+3√5)/2 ≈ 6,8541 (déclarée) ; le zéro
protégé (T13) est le mode sans masse — la forme mesurée du porteur
{0, ρ−1, ρ+1} est celle d'un secteur neutrino à hiérarchie normale
minimale (déclaré — c'est la règle de forme de la correspondance).
**Attente honnête** : le vide est loin du canal (0,69 dex) ; le nul
réel contient des valeurs algébriques proches du tarif par combinatoire
(leçon de MCS-23, déclarée) ; attente : CS− probable — la puissance est
mesurée à la démo (règle 1.2). La valeur de la carte : fermer le
dernier canal mesuré déclaré de la frontière de MCS-24 (après le canal
leptonique, MCS-25) avec le nul réel spectral des masses² — et mesurer
la consistance de la chaîne d'ancre (le point de la branche du porteur
qui siègerait exactement R_ν existe : ρ ≈ 1,42 — publié en diagnostic
avec son Λ_sel — la seconde ancre dirait alors TOUTE la chaîne).
**Regard ailleurs (déclaration préalable)** : MCS-24 (scellée, CSi) et
MCS-25 (scellée, CS−) lues et déclarées — la présente carte est la
suite déclarée de la frontière (« neutrinos, échelle de Majorana, ou
cosmologie ») ; les deux autres candidats sont fermés par argument
déclaré (l'échelle de Majorana n'est pas mesurée — absence de donnée ;
la constante cosmologique vit dans le slot projeté hors des équations
— verdict T12 : elle ne peut pas ancrer la coupure dans cette
architecture). T6, T7, T12, T13 lus et déclarés. La circularité de
recherche (la forme du porteur a été mesurée avant cette carte) est
déclarée — payée au seuil (section 8).

---

## 1. Énoncé de la coïncidence candidate

> Le rapport de masses² des deux modes massifs du porteur à son vide
> (q = φ⁴ — forme close du spectre mesuré T7, au carré) est **plus
> proche** du rapport mesuré des splittings neutriniques R_ν que ne le
> sont les rapports de masses² des triplets nus vérifiés de la fenêtre
> — le nul réel spectral — et cette proximité survit aux déformations
> du groupe 𝒢.

## 2. Lexique gelé (un mot = un objet)

| Mot | Objet opératoire unique |
|-----|--------------------------|
| contenu | une matrice D vérifiée du banc (machine des orbites de T1, réimplémentation déclarée — spectres_triplets.py haché dans l'acte de gel de MCS-25, filiation déclarée) de taille n ∈ [2 ; 7] (fenêtre canonique déclarée) |
| rapport de masses² | q(D) = r(D)² = (σ_max/σ_min⁺)² (mêmes conventions que MCS-25 : σ_min⁺ > TOL·σ_max, TOL = 1e-9 figé ; rang 1 → r := 1) |
| canal | R_ν = Δm²_31/Δm²_21 de la configuration NuFIT (analyse « without SK-atm », ordre normal — déclaré : le zéro protégé du porteur est une hiérarchie normale minimale ; les deux éditions gelées portent les deux splittings dans cette variante) |
| écart | δ = log₁₀(q/R_ν) (signé) |
| m (mesure) | m = −\|δ\| (qualité croissante avec la proximité du canal) |
| nul réel de forme | la distribution de m(D) sur les triplets vérifiés de la fenêtre ayant la FORME mesurée du porteur (T13 : taille 5, rang(B) = 2, deux valeurs singulières non nulles distinctes — un mode nul, deux paires massives), chaque matrice comptée une fois (mesure naturelle — déclarée ; correction unique) |

## 3. Dictionnaire τ

    τ : contenu ↦ son rapport de masses² ↦ son écart au canal ↦ m

τ est cette carte elle-même.

## 4. Données et provenance (gelées)

- **NuFIT** : `donnees/mcs26/nufit_v60.tbl-parameters.pdf` (canonique —
  v6.0, données de septembre 2024, variante IC19 « without SK-atm »,
  ordre normal : Δm²_21 = 7,49×10⁻⁵ eV², Δm²_31 = +2,534×10⁻³ eV²) et
  `donnees/mcs26/nufit_v52.tbl-parameters.pdf` (g1 — v5.2, 2022, même
  variante : 7,41×10⁻⁵ et +2,511×10⁻³) — acquisition déclarée du
  12/10/2026 (nu-fit.org), empreintes reconsignées au runner ; la
  table v5.3 (03/2024) est épinglée avec elles (réserve déclarée,
  non utilisée).
- **Le porteur à son vide** : q = (7+3√5)/2, forme close déclarée du
  spectre mesuré à T7 ; le zéro protégé est mesuré à T13 ; lus et
  déclarés.
- **Le nul réel spectral** : énumération exhaustive des matrices
  vérifiées de la fenêtre (machine hachée au gel de MCS-25) — calculée
  à la démo (règle 1.2) puis à l'exécution, jamais avant cette carte.
- Aucune autre acquisition externe.

## 5. Groupe de déformations légitimes 𝒢

| g | Déformation | Ce qu'elle teste |
|---|-------------|-------------------|
| g1 | NuFIT 6.0 → NuFIT 5.2 (même variante, déclarée) | dépendance à l'édition |
| g2 | forme du nul : taille 5 (le porteur) → taille 4 (l'amputé de T13, rang 2, distinct) | dépendance à la taille de la forme |
| g3 | contenu : rapport de masses² (φ⁴) → rapport de masses (φ² ≈ 2,618) | dépendance à l'avatar du contenu |
| g4 | contenu : vide T7 (Λ = 3, ρ = √5) → le vide à Λ = 2,5 (ρ = 1,5, q = 25 — relation d'ancre de T12, filiation déclarée) | dépendance au point de branche |
| g5 | métrique d'écart : \|log₁₀\| → écart relatif \|q−R\|/R | dépendance à la métrique |
| g6 | forme du nul : rang 2 exact → rang ≤ 2 (le rang 1 a q = 1) | dépendance à la définition de la forme |

## 6. Modèle nul

- **N1 (le nul réel de forme)** : la distribution de m(D) sur les
  triplets de la forme déclarée, chaque matrice comptée une fois ;
  μ_null, u exacts (énumération exhaustive — calculée, pas tirée).
- **N2 (bornes de mesure)** : R_ν aux bornes ±1σ de l'édition (les
  splittings ont ~3 % d'incertitude — la demi-largeur moyenne est
  déclarée) ; rapporté — documenté.

## 7. Contrôles positifs (sabotages obligatoires — contrôles
## d'instrument sur contenus de référence, convention MCS-25 déclarée)

| c | Sabotage | Attendu si le test a du pouvoir |
|---|----------|----------------------------------|
| c1 | contenu de référence planté exactement sur R_ν de la configuration puis déplacé (× 8, déclaré) | m se dégrade (\|effet\| ≥ 2 u) |
| c2 | contenu de référence remplacé par un rapport tiré du nul (PRNG public ChaCha20, échantillonnage inverse déclaré — convention MCS-24/25) | le tiré est classé ordinaire (contrasté au siège parfait : \|effet\| ≥ 2 u) |

c1 ou c2 vraiment muet (|effet| < 2 u, règle v2.0) → **CS0**.

## 8. Statistique et seuils (gelés)

- z_g = (m_g − μ_null,g)/u_g sous N1 pour chaque g ; Σ = min sur {g1…g6}.
- Seuil CS+ : **3,0** (aucune famille éprouvée sur ce domaine).
- Diagnostics rapportés (hors Σ) : l'écart du vide en dex ; le point de
  siège exact de la branche (ρ_ν = (√R_ν+1)/(√R_ν−1) et son Λ_sel par
  la relation d'ancre de T12 sur S⁴(1) — la chaîne complète que
  demanderait la seconde ancre) ; le rang du vide dans le nul réel
  (p = fraction au moins aussi proche) ; les comptes du nul par taille
  — publiés.

## 9. Critères de verdict

| Issue | Verdict |
|-------|---------|
| Σ ≥ 3,0 | CS+ — le vide du porteur siège le canal neutrino au-delà du nul réel |
| 2 ≤ Σ < 3,0 | CSp |
| −2 < Σ < 2 | CS− (B3-FAIL) — le canal neutrino ne contient pas l'ancre |
| Σ ≤ −2 | CSi |
| un contrôle vraiment muet | CS0 |

## 10. Regard ailleurs (déclaration préalable)

MCS-24 (CSi) et MCS-25 (CS−) lues et déclarées — la leçon (pas de
cadran, la forme d'abord) est appliquée : l'objet est un rapport de
masses², sans échelle, et la correspondance est déclarée par la forme
mesurée du porteur (T13). La leçon de MCS-23 est déclarée : le nul
réel contient des proximités combinatoires — c'est elle que le nul
mesure. Le nul réel spectral des masses² a été calculé une première
fois à la démo v1 (impuissante, publiée — correction déclarée en tête
de carte) ; aucune mesure du contenu n'a été faite.

## 11. Critères d'arrêt

- CS+ → le vide du porteur siège le canal neutrino ; le diagnostic
  publie la chaîne d'ancre complète (ρ_ν, Λ_sel) — la seconde ancre
  existe et dit tout.
- CS− ou CSi → B3-FAIL publié : les trois candidats déclarés de la
  frontière de MCS-24 sont fermés (leptonique par MCS-25, neutrinos
  ici, Majorana/cosmologie par argument déclaré) — la frontière reste
  ouverte, documentée.
- CS0 → une seule refonte autorisée (MCS-26b).
- CSp → la carte dort.

## 12. Démonstration de puissance (règle 1.2 du manifeste v2.0)

Démo v1 (nul réel spectral complet) : IMPUISSANTE — σ = 2,05, c2 =
1,18 u — publiée. Démo v2 (la présente carte corrigée — nul de forme)
avant gel : sur un contenu synthétique planté exactement sur le canal
(déclaré : R_ν de la configuration canonique), la statistique doit
donner Σ ≥ 3,0 et les deux contrôles d'instrument résoudre à
|effet| ≥ 2 u ; sur un rapport tiré du nul, CS− attendu ; banc aveugle
simulé → CS0. Hachée dans l'acte de gel. La démo calcule le nul réel
de forme (la démo mesure la puissance sur l'espace réel, déclaré).

## 13. Scellement (jalon 3 v2)

```
SHA256_CARTE : null
HORODATAGE   : null
```
