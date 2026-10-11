# CARTE MCS-13 — Résonances orbitales × systèmes planétaires multiples

**Statut** : CANDIDAT — NON SCELLÉ — Jalon 1 v2 (rédaction, aucun calcul)
**Moteur** : v2.0 (manifeste MANIFESTE-MCS-v2.0.md — puissance démontrée avant gel)
**Domaines** : A = périodes orbitales des planètes des systèmes multiples
(NASA Exoplanet Archive, table des systèmes planétaires) ; B = l'ensemble
figé des rapports rationnels simples R = {2:1, 3:2, 4:3, 5:4, 6:5, 3:1,
4:1, 5:2, 5:3} (résonances de moyen mouvement d'ordre bas, déclaré).
**Attente honnête** : mitigée, et la littérature le sait : l'excès mesuré
de paires vit **juste à côté** des résonances exactes (légèrement au large),
pas dessus. La carte teste le regroupement *sur* les rapports rationnels
simples — pas l'excès adjacent. Le diagnostic déclaré (section 8) mesurera
séparément le signe des écarts (au large / au strict). Attente : CSp ou CS−
sur la mesure stricte ; l'éventuel CS+ serait une surprise intéressante.

---

## 1. Énoncé de la coïncidence candidate

> Les rapports de périodes des paires adjacentes des systèmes planétaires
> multiples se placent sur les rapports rationnels simples de R **au-delà de
> ce que produit le hasard structurel** (même distribution de périodes, ordre
> détruit), et ce regroupement survit aux déformations du groupe 𝒢.

## 2. Lexique gelé (un mot = un objet)

| Mot | Objet opératoire unique |
|-----|--------------------------|
| système | un système planétaire de la table avec ≥ 2 planètes à période mesurée |
| paire | deux planètes adjacentes en période (r = P_ext/P_int > 1) |
| R | l'ensemble figé de rapports rationnels simples (en-tête) |
| écart | δ(r) = min sur ρ ∈ R de |r − ρ| / ρ |
| m (mesure) | m = −log₁₀( RMS(δ) ) sur les paires de la configuration |
| ordre détruit | périodes d'un même système permutées puis re-triées (nul) |

## 3. Dictionnaire τ

    τ : périodes des systèmes multiples ↦ rapports adjacents ↦ écarts à R ↦ m

τ est cette carte elle-même. Toute modification de τ après le gel = nouvelle
carte, nouveau numéro.

## 4. Données et provenance (gelées)

- **NASA Exoplanet Archive** : table des systèmes planétaires (paramètres
  composites ; champs : hôte, période orbitale, nombre de planètes du
  système) — acquisition à l'ouverture (service public de la base),
  empreinte consignée. Aucune ligne lue avant la rédaction.
- **Liste figée** : tous les systèmes avec ≥ 2 planètes à période mesurée ;
  les déformations filtrent selon les critères déclarés de la section 5.
- Aucune circularité : R est générique (rationnels d'ordre bas), non
  ajusté sur l'échantillon ; l'excès « à côté des résonances » est un fait
  publié de la littérature, déclaré, pas une lecture de la base.

## 5. Groupe de déformations légitimes 𝒢

| g | Déformation | Ce qu'elle teste |
|---|-------------|-------------------|
| g1 | systèmes ≥ 2 planètes → ≥ 3 planètes | dépendance à la richesse des chaînes |
| g2 | retrait du système apportant le plus de paires (déclaré à l'exécution, publié) | domination d'un système |
| g3 | R complet → résonances de premier ordre seules (p/q avec p = q+1) | dépendance à l'ensemble cible |
| g4 | retrait des paires avec r > 4 (grandes séparations) | dépendance à l'étendue |
| g5 | écart relatif → seuil absolu déclaré : m recompté en fraction de paires à δ < 1 % (m = fraction, mesure alternative déclarée) | dépendance à la métrique |
| g6 | retrait d'une paire au hasard (PRNG public ChaCha20) | sensibilité locale |

## 6. Modèle nul

- **N1 (ordre détruit)** : 10 000 permutations intra-système des périodes
  (re-triées après permutation) ; rapports adjacents et m recomputés →
  μ_null, u. C'est le nul de complexité égale : même distribution de
  périodes, même architecture de systèmes, ordre libre.
- **N2 (périodes libres)** : périodes tirées log-uniformément dans
  l'étendue observée de la table (déclarée à l'exécution), regroupées en
  systèmes de mêmes tailles ; m recomputé (rapporté).

## 7. Contrôles positifs (sabotages obligatoires)

| c | Sabotage | Attendu si le test a du pouvoir |
|---|----------|----------------------------------|
| c1 | rapports déplacés au point milieu entre leur rationnel le plus proche et le suivant de R (sabotage maximal déclaré) | m s'effondre (|effet| ≥ 2 u) |
| c2 | paires remplacées par des rapports log-uniformes déclarés | m s'effondre vers μ_N1 (|effet| ≥ 2 u) |

c1 ou c2 vraiment muet (|effet| < 2 u, règle v2.0) → **CS0**.

## 8. Statistique et seuils (gelés)

- z_g = (m_g − μ_null,g)/u_g sous N1 pour chaque g ; Σ = min sur {g1…g6}.
- Seuil CS+ : **3,0** (aucune famille éprouvée, aucune circularité).
- Diagnostics rapportés (hors Σ) : distribution **signée** des écarts au
  rapport le plus proche (excès au large / au strict — la nuance publiée de
  la littérature) ; histogramme des rapports rationnels atteints.

## 9. Critères de verdict

| Issue | Verdict |
|-------|---------|
| Σ ≥ 3,0 | CS+ — le regroupement sur résonances est stable au sens MCS |
| 2 ≤ Σ < 3,0 | CSp |
| −2 < Σ < 2 | CS− (B3-FAIL) |
| Σ ≤ −2 | CSi |
| un contrôle vraiment muet | CS0 |

## 10. Regard ailleurs (déclaration préalable)

Les résonances orbitales n'ont jamais été éprouvées par la machine ni le
corpus. La nuance « excès à côté des résonances » est déclarée et isolée
dans le diagnostic — la mesure stricte et la nuance ne se confondront pas.
Bases consultées avant gel : 0.

## 11. Critères d'arrêt

- CS+ → le regroupement sur rapports simples est une coïncidence stable ;
  le diagnostic d'écart signé est publié en tête de lecture.
- CS− ou CSi → carte fermée (B3-FAIL) ; le regroupement sur R était
  structurel.
- CS0 → une seule refonte autorisée (MCS-13b).
- CSp → la carte dort.

## 12. Démonstration de puissance (règle 1.2 du manifeste v2.0)

Avant gel : sur des systèmes synthétiques plantés sur les rapports de R à
1 % près, la statistique doit donner Σ ≥ 3,0 et les deux contrôles résoudre
à |effet| ≥ 2 u ; sur des périodes libres ordonnées, CS− attendu ; banc
aveugle simulé → CS0. Hachée dans l'acte de gel.

## 13. Scellement (jalon 3 v2)

```
SHA256_CARTE : bef50920b091937166e3b919c89fc032ea85a97cbc1da5d799a508f009ea0363
HORODATAGE   : 2026-10-11T09:33:28Z
```
