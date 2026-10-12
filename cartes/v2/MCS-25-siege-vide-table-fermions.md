# CARTE MCS-25 — Le siège du vide : rapport spectral du porteur × le canal mesuré des leptons chargés (nul réel spectral)

**CORRECTION PRÉ-GEL DÉCLARÉE (unique, précédent MCS-20)** : la démo v1
(table complète des 8 fermions, 28 rapports) est impuissante — plafond
mesuré σ = 1,46 : la table complète est trop dense pour résoudre un
siège — elle est publiée (validation/demonstration_puissance_mcs25_v1.py
et son journal). La correction est la **règle de forme spectrale** : le
porteur a exactement deux modes massifs (et un mode nul) ; l'arène
mesurée portant exactement deux rapports de masses indépendants déjà
pesés par la maison est le **canal des leptons chargés** {e, μ, τ}
(précédent MCS-11, déclaré). Les contrôles deviennent des contrôles
d'instrument sur contenus de référence (déclaré — sinon toute carte à
attente négative basculerait CS0 par construction). La table complète
reste publiée dans les diagnostics.

**Statut** : CANDIDAT — Jalon 1 v2 (rédaction, aucun calcul de mesure)
**Moteur** : v2.0 (manifeste MANIFESTE-MCS-v2.0.md — puissance démontrée avant gel)
**Domaines** : A = le canal mesuré des leptons chargés {e, μ, τ}
(PDG 2024 canonique / PDG 2022 — tables déjà empreintées au dépôt,
MCS-11/16, déclaré) — les deux rapports indépendants μ/e et τ/μ (et
leur produit τ/e) ; B = le contenu spectral du banc : le porteur à son
vide (T7 : ρ = √5 à Λ = 3 — mesuré, publié) dont le rapport spectral
est la forme close r = (√5+1)/(√5−1) = (3+√5)/2 = φ² ≈ 2,618034
(déclarée).
**Attente honnête** : le canal leptonique est loin (son plus petit
rapport est μ/e ≈ 206,8) ; la valeur du porteur au vide (φ² ≈ 2,618)
siégera mal ; le nul réel spectral concentre ses rapports entre 1 et
quelques dizaines (argument structurel déclaré, nul calculé à la démo).
Attente : CS− probable — la carte mesure si la table des leptons
contient une ancre pour le porteur ; sa valeur est le premier
branchement du nul réel SPECTRAL (matrices énumérées, pas seulement
comptées) sur une mesure — la campagne E de la stratégie du
12/10/2026 — et, si le verdict est négatif, la fermeture publiée du
porteur comme phénoménologie (frontière déclarée de MCS-24 : « une
seconde ancre mesurée »).
**Regard ailleurs (déclaration préalable)** : MCS-24 (scellée, CSi)
lue et déclarée — la présente carte est la suite de sa frontière avec
un objet nouveau (un rapport, SANS cadran — la leçon de MCS-24 est
appliquée) et un nul nouveau (spectral). MCS-16 lue (sa table PDG est
réutilisée — provenance). T7, T9, T12 lus et déclarés. La circularité
de recherche (la table est celle du corpus, le vide du porteur a été
mesuré avant cette carte) est déclarée — payée au seuil (section 8).

---

## 1. Énoncé de la coïncidence candidate

> Le rapport spectral du porteur à son vide (r = φ² — forme close du
> spectre mesuré T7 : {0, ±(ρ−1), ±(ρ+1)} à ρ = √5) siège dans la
> table mesurée des rapports de masses de fermions **plus près** que
> ne le font les rapports spectraux des triplets nus vérifiés de la
> fenêtre — le nul réel spectral — et cette proximité survit aux
> déformations du groupe 𝒢.

## 2. Lexique gelé (un mot = un objet)

| Mot | Objet opératoire unique |
|-----|--------------------------|
| contenu | une matrice D vérifiée du banc (machine des orbites de T1, réimplémentation déclarée, filiation MCS-24) de taille n ∈ [2 ; 6] (fenêtre canonique déclarée) |
| rapport spectral | r(D) = σ_max/σ_min⁺ des valeurs singulières du bloc hors-chiral B ; σ_min⁺ = plus petite valeur singulière > TOL·σ_max (TOL = 1e-9 figé) ; rang 1 → r := 1 (convention déclarée) |
| table | le canal des leptons chargés {e, μ, τ} (valeurs PDG de la table .mcd de la configuration) — les 3 rapports {μ/e, τ/μ, τ/e} (règle de forme spectrale : le porteur a deux modes massifs, le canal a deux rapports indépendants — correction déclarée) |
| siège | s(x) = min sur les rapports R de la table de \|log₁₀(x/R)\| (en dex) |
| m (mesure) | m = −s (qualité croissante avec la proximité du siège) |
| nul réel spectral | la distribution de s(D) sur TOUTES les matrices vérifiées de la fenêtre, chaque matrice comptant une fois (la mesure naturelle — les comptes de MCS-24 sont ces nombres de matrices, déclaré) |

## 3. Dictionnaire τ

    τ : contenu ↦ son rapport spectral ↦ son siège dans la table ↦ m

τ est cette carte elle-même.

## 4. Données et provenance (gelées)

- **Table PDG** : `donnees/mcs04_mass_width_2024.mcd` (canonique) et
  `donnees/mcs04_mass_width_2022.mcd` (g1) — déjà acquises (MCS-04/16),
  empreintes reconsignées au runner ; le parseur de MCS-16 réutilisé
  (filiation déclarée) ; masses en MeV ; les deux éditions portent e,
  μ, τ (déclaré).
- **Le porteur à son vide** : r = (3+√5)/2, forme close déclarée du
  spectre mesuré à T7 (ρ = √5 à Λ = 3) ; lu et déclaré.
- **Le nul réel spectral** : énumération exhaustive des matrices
  vérifiées de la fenêtre — calculée à la démo (règle 1.2) puis à
  l'exécution, jamais avant la carte.
- Aucune acquisition externe nouvelle.

## 5. Groupe de déformations légitimes 𝒢

| g | Déformation | Ce qu'elle teste |
|---|-------------|-------------------|
| g1 | PDG 2024 → PDG 2022 (les deux éditions portent e, μ, τ — déclaré) | dépendance à l'édition |
| g2 | fenêtre du nul n ≤ 6 → n ≤ 7 | dépendance à la fenêtre |
| g3 | contenu : vide T7 (ρ = √5) → ρ = 1,5 (vide déplacé, r = 5) | dépendance au vide mesuré |
| g4 | contenu : vide T7 → le point Λ = 6 de la branche (ρ = √32, r = (√32+1)/(√32−1) — relation d'ancre de T12, filiation déclarée) | dépendance au point de branche |
| g5 | métrique de siège : \|log₁₀\| → écart relatif \|x−R\|/R | dépendance à la métrique |
| g6 | poids du nul : chaque matrice compte une fois → poids uniforme par taille | dépendance à la mesure du nul |

## 6. Modèle nul

- **N1 (le nul réel spectral)** : la distribution de s(D) sur les
  matrices vérifiées de la fenêtre, chaque matrice comptée une fois ;
  μ_null, u exacts (énumération exhaustive — calculée, pas tirée).
- **N2 (masses permutées)** : les 3 masses du canal permutées, la table
  de rapports reconstruite (rapporté — documenté).

## 7. Contrôles positifs (sabotages obligatoires — contrôles
## d'instrument sur contenus de référence, correction déclarée)

| c | Sabotage | Attendu si le test a du pouvoir |
|---|----------|----------------------------------|
| c1 | contenu de référence planté exactement sur une entrée de la table (déclaré : μ/e de la configuration) puis déplacé au centre géométrique du plus grand intervalle logarithmique de la table | le siège se dégrade (\|effet\| ≥ 2 u) |
| c2 | contenu de référence remplacé par un rapport tiré du nul (PRNG public ChaCha20, échantillonnage inverse déclaré — convention MCS-24) | le tiré est classé ordinaire (contrasté au siège parfait : \|effet\| ≥ 2 u) |

c1 ou c2 vraiment muet (|effet| < 2 u, règle v2.0) → **CS0**.

## 8. Statistique et seuils (gelés)

- z_g = (m_g − μ_null,g)/u_g sous N1 pour chaque g ; Σ = min sur {g1…g6}.
- Seuil CS+ : **3,0** (aucune famille éprouvée sur ce domaine).
- Diagnostics rapportés (hors Σ) : le siège du porteur en dex ; le
  siège du porteur dans la table complète des fermions (publié — la
  table de la démo v1) ; la table des meilleurs sièges du nul ; le rang
  du porteur dans le nul réel spectral (p = fraction au moins aussi
  bien siègee) ; les comptes du nul par taille — publiés.

## 9. Critères de verdict

| Issue | Verdict |
|-------|---------|
| Σ ≥ 3,0 | CS+ — le vide du porteur siège dans la table au-delà du nul réel |
| 2 ≤ Σ < 3,0 | CSp |
| −2 < Σ < 2 | CS− (B3-FAIL) — le vide du porteur n'est pas phénoménologie |
| Σ ≤ −2 | CSi |
| un contrôle vraiment muet | CS0 |

## 10. Regard ailleurs (déclaration préalable)

MCS-24 (scellée, CSi) lue et déclarée — sa leçon (pas de cadran) est
appliquée : le présent objet est un rapport, sans échelle. MCS-16 lue
(table et parseur réutilisés, provenance déclarée) ; la présente carte
n'est pas une itération de MCS-16 : la question est différente (un
contenu du banc contre une table, pas des règles contre des masses) et
le nul est nouveau (réel spectral). T7 (le vide mesuré), T9 (le MS
corrigé), T12 (la relation d'ancre) lus et déclarés. Le nul réel
spectral a été calculé une première fois à la démo v1 (impuissante,
publiée — correction déclarée en tête de carte) ; aucune mesure du
contenu n'a été faite.

## 11. Critères d'arrêt

- CS+ → le vide du porteur siège dans la table mesurée ; le banc touche
  la phénoménologie ; le diagnostic publie quel rapport siège.
- CS− ou CSi → B3-FAIL publié : la table des fermions chargés ne
  contient pas d'ancre pour le porteur — la seconde ancre demandée par
  la frontière de MCS-24 devra venir d'ailleurs (déclaré : neutrinos,
  échelle de Majorana, ou cosmologie).
- CS0 → une seule refonte autorisée (MCS-25b).
- CSp → la carte dort.

## 12. Démonstration de puissance (règle 1.2 du manifeste v2.0)

Démo v1 (table complète des fermions) : IMPUISSANTE — plafond mesuré
σ = 1,46 — publiée (validation/demonstration_puissance_mcs25_v1.py et
son journal). Démo v2 (la présente carte corrigée) avant gel : sur un
contenu synthétique planté exactement sur une entrée de la table
(déclaré : le rapport μ/e de la configuration — présent dans toutes
les configurations du groupe), la statistique doit donner Σ ≥ 3,0 et
les deux contrôles d'instrument résoudre à |effet| ≥ 2 u ; sur un
rapport tiré du nul, CS− attendu ; banc aveugle simulé → CS0. Hachée
dans l'acte de gel. La démo calcule le nul réel spectral (fenêtre
canonique n ≤ 6 — la démo mesure la puissance sur l'espace réel,
déclaré ; g2 à n = 7 mesuré à l'exécution, coût déclaré).

## 13. Scellement (jalon 3 v2)

```
SHA256_CARTE : e1e4e0728fa3b2849e25f906c8bf1fd0c1d68f9a417bb71a96a91be5bf40b546
HORODATAGE   : 2026-10-12T11:08:46Z
```
