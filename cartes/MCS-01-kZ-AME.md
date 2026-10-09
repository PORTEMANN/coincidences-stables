# CARTE MCS-01 — k(Z) contre la vallée de stabilité β

**Statut** : CANDIDAT — NON SCELLÉ — Jalon 1 (rédaction, aucun calcul)
**Domaines** : A = constante de structure fine α (constante sans dimension) ;
B = masses nucléaires / vallée de stabilité β (tables AME).
**Attente honnête** : carte probablement destinée à CS−. Son intérêt est de
fermer proprement, ou de produire le premier point d'ancrage numérique.

---

## 1. Énoncé de la coïncidence candidate

Le corpus propose une loi **à zéro paramètre libre** liant la vallée de
stabilité β à α :

    k(Z) = − (1 / (1000·α)) · ln(Z) + 3/2

avec 1/(1000·α) ≈ 1,37036 (α⁻¹ = 137,035999…).

La carte teste si la courbe N/Z prédite par cette loi, **sans aucun ajustement**,
décrit la vallée de stabilité mieux que les modèles nuls de complexité égale
ou supérieure, et si cette performance survit aux déformations du groupe 𝒢.

## 2. Lexique gelé (un mot = un objet)

| Mot | Objet opératoire unique |
|-----|--------------------------|
| vallée de stabilité | ensemble des nucléides « stables » : demi-vie > 10⁹ ans OU nucléide observationnellement stable selon NuDat 3 |
| N/Z observé | (A − Z)/Z pour l'isotope stable le plus lourd à Z donné ; si plusieurs stables, moyenne pondérée par abondance |
| loi candidate | k(Z) ci-dessus, pente ET ordonnée à l'origine fixées ; **aucun paramètre ajustable** |
| nul de complexité égale | toute loi à 0 paramètre libre (ex. N/Z = 1 ; N/Z = 1 + a·Z^(2/3) avec a fixé par la formule de Weizsäcker sans réajustement) |
| nul de complexité supérieure | loi à paramètres ajustés sur le sous-ensemble d'apprentissage uniquement : a·ln(Z)+b (2 param.), a·Z^b+c (3 param.), polynôme degré 2 (3 param.) |
| résidu | r(Z) = (N/Z)_observé(Z) − (N/Z)_prédit(Z) |
| m (mesure) | −log₁₀( RMS(r) ), qualité croissante avec la précision |

## 3. Dictionnaire τ

    τ : α  ↦  loi k(Z)  ↦  prédiction N/Z(Z) pour Z = 1 … 92

τ est cette carte elle-même. Toute modification de τ après le gel = nouvelle
carte, nouveau numéro, nouveau regard ailleurs.

## 4. Données et provenance (gelées au jalon 3)

- **Apprentissage des nuls ajustés** : AME2012 (nucléides stables, Z = 1…82).
- **Test hors-échantillon** : AME2020 (mêmes critères), incluant Z = 83…92.
- **Contre-données** : AME2003 (version ancienne, test de stabilité temporelle),
  JEFF-3.3 (chaîne de compilation indépendante).
- α : CODATA 2018 (valeur fixée, non réajustée à CODATA 2022 — déformation g5).

Aucune donnée de test n'a servi à écrire la loi candidate (règle d'anti-circularité
du manifeste, §8).

## 5. Groupe de déformations légitimes 𝒢

| g | Déformation | Ce qu'elle teste |
|---|-------------|-------------------|
| g1 | AME2012 → AME2020 (hors-échantillon strict) | surapprentissage des nuls |
| g2 | AME2020 → AME2003 | dépendance à la version des tables |
| g3 | AME → JEFF-3.3 | dépendance à la chaîne d'évaluation |
| g4 | retrait des Z magiques (2, 8, 20, 28, 50, 82) | la loi ne serait qu'un effet de couches |
| g5 | CODATA 2018 → CODATA 2022 pour α | sensibilité à α |
| g6 | nucléides pairs-Z seuls / impairs-Z seuls | artefact de parité |
| g7 | isotope le plus lourd → moyenne des stables | convention de N/Z |
| g8 | Z = 1…92 → Z = 20…92 (retrait des légers) | domination des petits Z |

## 6. Modèle nul

Distribution de m sous l'hypothèse « la loi candidate n'est qu'une courbe lisse
parmi d'autres » :

- **N1 (permutation)** : permuter les N/Z observés entre Z, 10 000 fois,
  recalculer m de la loi candidate à chaque fois → μ_null, u.
- **N2 (famille concurrente)** : les trois nuls de complexité supérieure ajustés
  sur AME2012, évalués sur AME2020 ; la candidate doit battre le **meilleur**
  d'entre eux hors-échantillon (pas la moyenne).
- **N3 (formes lisses aléatoires)** : 10 000 lois a·ln(Z)+b avec (a,b) tirés
  uniformément dans a ∈ [−3, 0], b ∈ [0, 4] ; la candidate à 0 paramètre doit
  se situer hors du quantile 99 % de cette famille **à complexité moindre**.

## 7. Contrôles positifs (sabotages obligatoires)

| c | Sabotage | Comportement attendu si le test a du pouvoir |
|---|----------|------------------------------------------------|
| c1 | permuter Z ↔ N dans les données | la candidate doit être détruite (z chute sous −2) |
| c2 | remplacer α par α/2 dans la pente | dégradation significative de m |
| c3 | supprimer le terme coulombien de la convention Weizsäcker utilisée pour les nuls physiques | les nuls physiques doivent se dégrader — sinon N2 est aveugle |

Si c1 ou c2 échoue à dégrader : **CS0**, test impuissant, carte à refondre.

## 8. Statistique et seuils (gelés)

- z_g = (m_g − μ_null,g) / u_g, calculé sous N1 pour chaque g ∈ 𝒢.
- Σ = min sur {g1…g8} des z_g.
- La candidate doit en outre satisfaire N2 : m_candidate > m_meilleur_nul_ajusté
  sur AME2020, avec marge ≥ 0,05 en unités de m (gelé).
- Correction du regard ailleurs : seuil CS+ porté de 3 à 3,2 si plus de
  5 familles de formes ont été essayées avant cette carte (déclaré : 3 familles
  — constante, logarithme libre, puissance — donc seuil maintenu à 3).

## 9. Critères de verdict

| Issue | Verdict |
|-------|---------|
| Σ ≥ 3 et marge N2 tenue | CS+ |
| 2 ≤ Σ < 3, ou Σ ≥ 3 sans marge N2 | CSp |
| −2 < Σ < 2 | CS− (publication B3-FAIL) |
| Σ ≤ −2 | CSi |
| c1 ou c2 muet | CS0 |

## 10. Regard ailleurs (déclaration préalable)

Familles essayées avant gel : 3. Variantes de la loi candidate essayées : 1
(celle-ci). Sous-ensembles de données examinés avant gel : 0 (rédaction sur
spécifications des tables, pas sur les chiffres).

## 11. Critères d'arrêt

- CS− ou CSi → carte fermée, publication, pas de variante « réparée » dans
  cette campagne (fermer, ne pas ajouter).
- CS0 → une seule refonte autorisée (MCS-01b), nouveau regard ailleurs déclaré.
- CSp → aucune revendication ; la carte dort jusqu'à une table AME ultérieure.

## 12. Scellement (jalon 3)

```
SHA256_CARTE : 45185f63459fcf9e580a0a86725110a9bdf462aa1754b56321259a73ca34c0e1
HORODATAGE   : 2026-10-09T13:31:46Z
```
