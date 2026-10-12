# CARTE MCS-21 — Tension S₈ × familles CMB / lentilles faibles

**Statut** : CANDIDAT — Jalon 1 v2 (rédaction, aucun calcul de mesure)
**Moteur** : v2.0 (manifeste MANIFESTE-MCS-v2.0.md — puissance démontrée avant gel)
**Domaines** : A = les mesures publiées de S₈ = σ₈√(Ωm/0,3) du CMB primaire
et des lentilles faibles (valeurs gelées dans le runner avec leurs
sources) ; B = la concordance ΛCDM : les deux familles mesurent le même
paramètre.
**Attente honnête** : la tension est célèbre (~2–3 σ historiquement) mais
sa géographie bouge (KiDS-Legacy 2025 converge vers le CMB ; DES reste
bas — revue 2026 citée au runner). La question MCS : l'écart entre les
deux familles survit-il aux déformations (éditions, bornes, retraits)
au-delà du hasard structurel ? Attente : CSp ou CS+.

---

## 1. Énoncé de la coïncidence candidate

> L'écart mesuré entre les S₈ du CMB primaire et ceux des lentilles
> faibles est **plus grand** que ce que produit le hasard structurel
> (concordance gaussienne autour de la moyenne commune), et cette
> séparation survit aux déformations du groupe 𝒢 — la tension S₈ est
> stable au sens MCS.

## 2. Lexique gelé (un mot = un objet)

| Mot | Objet opératoire unique |
|-----|--------------------------|
| mesure | une valeur S₈ publiée avec ses bornes, gelée dans le runner avec sa source |
| famille | CMB = {Planck 2018, ACT DR6} ; lentilles = {KiDS-1000, DES-Y3, HSC-Y3} (canonique) |
| erreur symétrisée | σ = (borne haute + borne basse)/2 (gelé) |
| moyenne de famille | moyenne pondérée inverse-variance des mesures de la famille |
| T | T = |μ̄_CMB − μ̄_lens| / √(σ̄_CMB² + σ̄_lens²) |
| m (mesure) | m = T (séparation croissante avec la tension) |

## 3. Dictionnaire τ

    τ : mesures S₈ publiées ↦ séparation des familles en σ combinée ↦ m

τ est cette carte elle-même.

## 4. Données et provenance (gelées)

Valeurs gelées dans le runner, chacune avec sa source publique citée
(vérifiées avant rédaction) :

- **CMB** : Planck 2018 (Planck Collaboration 2020) S₈ = 0,834 ± 0,016 ;
  ACT DR6 lentille+BAO+BBN (Madhavacheril et al. 2024) S₈ = 0,840 ± 0,028.
- **Lentilles** : KiDS-1000 (Asgari et al. 2021) S₈ = 0,759 +0,024/−0,021 ;
  DES-Y3 cosmic shear (Amon/Secco et al. 2022) S₈ = 0,759 +0,025/−0,023 ;
  HSC-Y3 (Li/Dalal et al. 2023) S₈ = 0,769 +0,031/−0,034.
- **Éditions déclarées pour les déformations** : Combined CMB 2026
  (Planck+ACT+SPT, revue 2026) S₈ = 0,836 +0,012/−0,013 ; KiDS-Legacy
  (Wright et al. 2025) S₈ = 0,815 +0,016/−0,021.

Aucune acquisition de fichiers : les valeurs sont gelées dans le runner
avec leurs sources (convention MCS-16). Le suspense mvcg sur le secteur
sombre est déclaré au registre des campagnes.

## 5. Groupe de déformations légitimes 𝒢

| g | Déformation | Ce qu'elle teste |
|---|-------------|-------------------|
| g1 | KiDS-1000 → KiDS-Legacy (édition du même relevé) | dépendance à l'édition lentilles |
| g2 | Planck 2018 → Combined CMB 2026 | dépendance à l'édition CMB |
| g3 | erreurs symétrisées → bornes hautes | dépendance aux incertitudes |
| g4 | erreurs symétrisées → bornes basses | dépendance aux incertitudes |
| g5 | retrait de HSC-Y3 (la plus haute des lentilles) | domination d'un point |
| g6 | retrait d'une mesure au hasard (PRNG public ChaCha20) | sensibilité locale |

## 6. Modèle nul

- **N1 (concordance gaussienne)** : 10 000 tirages : chaque mesure tirée de
  N(μ_pool, σ_i), μ_pool = moyenne pondérée globale des valeurs réelles de
  la configuration ; distribution de T → μ_null, u. (Nul de complexité
  égale : mêmes erreurs, même effectif, une seule valeur vraie.)
- **N2 (étiquettes permutées)** : les étiquettes de famille permutées,
  rapporté (faible effectif, déclaré).

## 7. Contrôles positifs (sabotages obligatoires)

| c | Sabotage | Attendu si le test a du pouvoir |
|---|----------|----------------------------------|
| c1 | famille lentilles alignée sur μ̄_CMB (tension supprimée, déclaré) | T s'effondre (|effet| ≥ 2 u) |
| c2 | écarts à μ_pool doublés dans le sens observé (tension doublée, déclaré) | T augmente (|effet| ≥ 2 u) |

c1 ou c2 vraiment muet (|effet| < 2 u, règle v2.0) → **CS0**.

## 8. Statistique et seuils (gelés)

- z_g = (m_g − μ_null,g)/u_g sous N1 pour chaque g ; Σ = min sur {g1…g6}.
- Seuil CS+ : **3,1** (famille des tensions cosmologiques — MCS-17 à 3,1,
  consigné des deux).
- Diagnostic rapporté (hors Σ) : T canonique en σ et contribution de
  chaque mesure (poids), publiés sans moyennage inter-familles caché.

## 9. Critères de verdict

| Issue | Verdict |
|-------|---------|
| Σ ≥ 3,1 | CS+ — la tension S₈ est stable au sens MCS |
| 2 ≤ Σ < 3,1 | CSp |
| −2 < Σ < 2 | CS− (B3-FAIL) — la séparation était structurelle au nul |
| Σ ≤ −2 | CSi |
| un contrôle vraiment muet | CS0 |

## 10. Regard ailleurs (déclaration préalable)

La tension S₈ est une discussion publique (déclarée) ; la revue 2026
citée au runner documente la convergence de KiDS-Legacy et la persistance
de DES — la carte mesurera la stabilité de l'écart, pas son explication.
Aucune valeur n'a été lue dans les sources avant la rédaction au-delà des
citations vérifiées du §4.

## 11. Critères d'arrêt

- CS+ → la tension S₈ est stable ; le diagnostic publie la géographie de
  l'écart par mesure.
- CS− ou CSi → B3-FAIL publié : la tension était structurelle au nul de
  concordance déclaré.
- CS0 → une seule refonte autorisée (MCS-21b).
- CSp → la carte dort.

## 12. Démonstration de puissance (règle 1.2 du manifeste v2.0)

Avant gel : sur un jeu synthétique planté avec une tension de 3,5 σ entre
deux familles de trois mesures (erreurs des valeurs réelles), la
statistique doit donner Σ ≥ 3,1 et les deux contrôles résoudre à
|effet| ≥ 2 u ; sur un jeu concordant, CS− attendu ; banc aveugle simulé
→ CS0. Hachée dans l'acte de gel.

## 13. Scellement (jalon 3 v2)

```
SHA256_CARTE : 48d55fcc28a714859f50af1b0e4aa8ec388f914b6d404b16d5171ee5f4cb909b
HORODATAGE   : 2026-10-12T03:54:41Z
```
