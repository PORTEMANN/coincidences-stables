# CARTE MCS-19 — Plancher KSS × viscosités mesurées (⁴He, gaz unitaire, QGP)

**Statut** : CANDIDAT — NON SCELLÉ — Jalon 1 v2 (rédaction, aucun calcul)
**Moteur** : v2.0 (manifeste MANIFESTE-MCS-v2.0.md — puissance démontrée avant gel)
**Domaines** : A = η/s mesuré de systèmes fluides quantiques (⁴He liquide,
gaz unitaire, plasma quark-gluon — valeurs publiées, citées avec sources
gelées dans le runner) ; B = le plancher de Kovtun–Son–Starinets :
η/s ≥ ℏ/(4π k_B) (borne conjecturée 2005, gelée).
**Attente honnête** : le suspense est publié par mvcg : le QGP s'approche
du plancher (1–3 planchers) sans le saturer, le ⁴He s'en tient loin (~9
planchers), le gaz unitaire entre les deux — la machine mesurera si
l'approche du plancher est stable sous 𝒢. Attente : incertaine.

---

## 1. Énoncé de la coïncidence candidate

> Les η/s mesurés des fluides quantiques de la liste figée s'approchent du
> plancher KSS **au-delà de ce que produit le hasard structurel** (valeurs
> libres dans l'étendue déclarée), et l'approche survit aux déformations du
> groupe 𝒢 (choix de systèmes, de mesures, de convention du plancher).

## 2. Lexique gelé (un mot = un objet)

| Mot | Objet opératoire unique |
|-----|--------------------------|
| système | l'un des trois fluides de la liste figée : ⁴He liquide, gaz unitaire, QGP |
| mesure | la valeur η/s publiée du système, citée avec sa source (runner, gelée) |
| plancher | η/s ≥ ℏ/(4π k_B) = 0,0796 (KSS 2005, gelé) |
| m (mesure) | e = min_systèmes(η/s)/0,0796 − 1 (signé) ; m = −log₁₀(|e|) si e > 0 ; si e ≤ 0 (violation du plancher) : m = −log₁₀(|e|) − 2 (décalage déclaré : toute violation est pire que toute approche) |
| étendue | η/s ∈ [0,05 ; 5] (déclarée) |

## 3. Dictionnaire τ

    τ : η/s mesurés des fluides figés ↦ distance au plancher ↦ m

τ est cette carte elle-même.

## 4. Données et provenance (gelées)

- **Valeurs publiées**, citées dans le runner avec leurs sources
  (⁴He : mesures publiées du plan d'expérience ; gaz unitaire : mesure
  publiée ; QGP : extraction publiée RHIC/LHC) — aucune acquisition externe
  au-delà de ces citations ; les valeurs sont gelées dans le runner avant
  calcul, avec leurs sources.
- Le suspense KSS de mvcg est publié, déclaré (KSS ⁴He : S− à 780 % ;
  KSS/QGP : S− à 100 % — la borne inférieure déclarée du plasma ne sature
  pas le plancher).

## 5. Groupe de déformations légitimes 𝒢

| g | Déformation | Ce qu'elle teste |
|---|-------------|-------------------|
| g1 | retrait du QGP (le plus proche) | domination du meilleur point |
| g2 | retrait du ⁴He (le plus lointain) | domination du pire |
| g3 | plancher ℏ/4πk_B → ℏ/2πk_B (convention déclarée) | dépendance à la convention |
| g4 | mesures centrales → bornes hautes publiées | dépendance aux incertitudes |
| g5 | mesures centrales → bornes basses publiées | dépendance aux incertitudes |
| g6 | retrait d'un système au hasard (PRNG public ChaCha20) | sensibilité locale |

## 6. Modèle nul

- **N1 (valeurs libres)** : 10 000 triplets η/s tirés log-uniformément dans
  [0,05 ; 5] ; distribution de m → μ_null, u. (Nul de complexité égale :
  aucune borne, même étendue, même effectif.)
- **N2 (systèmes permutés)** : les mesures permutées entre systèmes,
  10 000 fois (rapporté — identité sur min : documenté comme tel).

## 7. Contrôles positifs (sabotages obligatoires)

| c | Sabotage | Attendu si le test a du pouvoir |
|---|----------|----------------------------------|
| c1 | le système le plus proche est remplacé par une valeur à 10 planchers (déclaré) | m s'effondre (|effet| ≥ 2 u) |
| c2 | le plancher est doublé (déclaré) | m se dégrade (|effet| ≥ 2 u) |

c1 ou c2 vraiment muet (|effet| < 2 u, règle v2.0) → **CS0**.

## 8. Statistique et seuils (gelés)

- z_g = (m_g − μ_null,g)/u_g sous N1 pour chaque g ; Σ = min sur {g1…g6}.
- Seuil CS+ : **3,0** (aucune famille éprouvée par la machine sur ce
  domaine ; les pesées mvcg sont ponctuelles, publiées — l'opérateur MCS
  est distinct).
- Diagnostic rapporté (hors Σ) : (η/s)/plancher par système — le suspense
  est publié par système, pas moyenné.

## 9. Critères de verdict

| Issue | Verdict |
|-------|---------|
| Σ ≥ 3,0 | CS+ — l'approche du plancher est stable au sens MCS |
| 2 ≤ Σ < 3,0 | CSp |
| −2 < Σ < 2 | CS− (B3-FAIL) — l'approche était structurelle |
| Σ ≤ −2 | CSi |
| un contrôle vraiment muet | CS0 |

## 10. Regard ailleurs (déclaration préalable)

Le suspense KSS/QGP et les pesées ⁴He/Bertsch de mvcg sont publiés,
déclarés. La saturation n'a jamais été éprouvée sous 𝒢 par la machine.
Sources lues avant gel : 0.

## 11. Critères d'arrêt

- CS+ → l'approche du plancher est stable ; le non-saturation du QGP reste
  publié au diagnostic (le plancher est approché, pas saturé — les deux
  sont mesurés).
- CS− ou CSi → B3-FAIL publié.
- CS0 → une seule refonte autorisée (MCS-19b).
- CSp → la carte dort.

## 12. Démonstration de puissance (règle 1.2 du manifeste v2.0)

Avant gel : sur un triplet synthétique planté au plancher (1,05 plancher),
la statistique doit donner Σ ≥ 3,0 et les deux contrôles résoudre à
|effet| ≥ 2 u ; sur un triplet libre, CS− attendu ; banc aveugle simulé
→ CS0. Hachée dans l'acte de gel.

## 13. Scellement (jalon 3 v2)

```
SHA256_CARTE : null
HORODATAGE   : null
```
