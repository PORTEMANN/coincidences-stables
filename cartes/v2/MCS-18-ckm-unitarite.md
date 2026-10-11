# CARTE MCS-18 — Unitarité CKM (première ligne) × mesures PDG

**Statut** : CANDIDAT — NON SCELLÉ — Jalon 1 v2 (rédaction, aucun calcul)
**Moteur** : v2.0 (manifeste MANIFESTE-MCS-v2.0.md — puissance démontrée avant gel)
**Domaines** : A = les trois éléments de la première ligne de la matrice CKM
mesurés (|V_ud|, |V_us|, |V_ub| — revue CKM du PDG, éditions 2024/2022) ;
B = l'unitarité : |V_ud|² + |V_us|² + |V_ub|² = 1 (théorème du modèle
standard — la question est la **stabilité de l'écart mesuré** sous 𝒢).
**Attente honnête** : l'écart mesuré (~0,15 %, le « déficit de la première
ligne ») est une discussion connue (~2 σ) ; mvcg a pesé le contact (P au
cheveu du S+, δ/U = 1,14 — publié). La question MCS : l'écart survit-il aux
déformations (éditions, bornes, retraits) au-delà du hasard structurel ?
Attente : CSp ou CS− (l'écart est faible et les incertitudes le portent).

---

## 1. Énoncé de la coïncidence candidate

> L'écart mesuré |V_ud|² + |V_us|² + |V_ub|² − 1 est **plus petit** que ce
> que produit le hasard structurel (éléments tirés dans les étendues
> déclarées), et cette proximité de l'unité survit aux déformations du
> groupe 𝒢 — la première ligne est unitaire au-delà du hasard.

## 2. Lexique gelé (un mot = un objet)

| Mot | Objet opératoire unique |
|-----|--------------------------|
| élément | |V_ud|, |V_us| ou |V_ub| lu dans la revue CKM du PDG de la configuration |
| écart | Δ = | |V_ud|² + |V_us|² + |V_ub|² − 1 | |
| m (mesure) | m = −log₁₀(Δ) sur la configuration (qualité croissante avec la proximité de 1) |
| étendue | V_ud ∈ [0,95 ; 0,99], V_us ∈ [0,20 ; 0,25], V_ub ∈ [0,003 ; 0,005] (déclarées) |

## 3. Dictionnaire τ

    τ : éléments mesurés ↦ écart à l'unité ↦ m

τ est cette carte elle-même.

## 4. Données et provenance (gelées)

- **Revue CKM du PDG** (éditions 2024 et 2022, pdf publics — pdg.lbl.gov) :
  les trois éléments avec leurs σ publiées, lus à l'ouverture, empreintes
  consignées. Aucune page lue avant la rédaction.
- Le déficit ~0,15 % est une discussion publiée de la littérature (déclaré,
  pas une lecture de la revue). Le contact mvcg (P, δ/U = 1,14) est cité.

## 5. Groupe de déformations légitimes 𝒢

| g | Déformation | Ce qu'elle teste |
|---|-------------|-------------------|
| g1 | revue 2024 → revue 2022 | dépendance à l'édition |
| g2 | éléments centraux → tous à +1σ publié | dépendance aux incertitudes |
| g3 | éléments centraux → tous à −1σ publié | dépendance aux incertitudes |
| g4 | retrait de V_ub (le plus petit — Δ recompté sur deux éléments) | domination du petit |
| g5 | retrait de V_ud (le plus grand — Δ recompté sur deux éléments) | domination du grand |
| g6 | retrait d'un élément au hasard (PRNG public ChaCha20) | sensibilité locale |

## 6. Modèle nul

- **N1 (éléments libres)** : 10 000 triplets tirés uniformément dans les
  étendues déclarées ; distribution de m → μ_null, u. (Nul de complexité
  égale : aucune unitarité, mêmes étendues, même effectif.)
- **N2 (éléments permutés)** : les trois éléments mesurés permutés entre
  leurs rôles, 10 000 fois (rapporté).

## 7. Contrôles positifs (sabotages obligatoires)

| c | Sabotage | Attendu si le test a du pouvoir |
|---|----------|----------------------------------|
| c1 | V_us déplacé de 5 % dans le sens qui l'éloigne de l'unité (déclaré) | m se dégrade (|effet| ≥ 2 u) |
| c2 | éléments remplacés par un triplet libre déclaré | m s'effondre vers μ_N1 (|effet| ≥ 2 u) |

c1 ou c2 vraiment muet (|effet| < 2 u, règle v2.0) → **CS0**.

## 8. Statistique et seuils (gelés)

- z_g = (m_g − μ_null,g)/u_g sous N1 pour chaque g ; Σ = min sur {g1…g6}.
- Seuil CS+ : **3,0** (aucune famille éprouvée par la machine sur ce
  domaine ; la mesure mvcg est ponctuelle, publiée — l'opérateur MCS est
  distinct).
- Diagnostic rapporté (hors Σ) : Δ en unités de σ combinée publiée —
  la tension en σ est publiée, pas moyennée.

## 9. Critères de verdict

| Issue | Verdict |
|-------|---------|
| Σ ≥ 3,0 | CS+ — l'unitarité de la première ligne est stable au sens MCS |
| 2 ≤ Σ < 3,0 | CSp |
| −2 < Σ < 2 | CS− (B3-FAIL) |
| Σ ≤ −2 | CSi |
| un contrôle vraiment muet | CS0 |

## 10. Regard ailleurs (déclaration préalable)

Le contact CKM de mvcg (P, δ/U = 1,14) est publié, déclaré. L'unitarité
n'a jamais été éprouvée sous 𝒢 par la machine. Revues lues avant gel : 0.

## 11. Critères d'arrêt

- CS+ → l'unitarité est stable ; le déficit résiduel est publié en σ au
  diagnostic, avec la tension nommée.
- CS− ou CSi → la proximité de l'unité était structurelle (B3-FAIL publié).
- CS0 → une seule refonte autorisée (MCS-18b).
- CSp → la carte dort.

## 12. Démonstration de puissance (règle 1.2 du manifeste v2.0)

Avant gel : sur un triplet synthétique planté unitaire à 0,1 % près, la
statistique doit donner Σ ≥ 3,0 et les deux contrôles résoudre à
|effet| ≥ 2 u ; sur un triplet libre, CS− attendu ; banc aveugle simulé
→ CS0. Hachée dans l'acte de gel.

## 13. Scellement (jalon 3 v2)

```
SHA256_CARTE : null
HORODATAGE   : null
```
