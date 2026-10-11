# CARTE MCS-09 — Loi de Titius-Bode × demi-grands axes planétaires

**Statut** : CANDIDAT — NON SCELLÉ — Jalon 1 v2 (rédaction, aucun calcul)
**Moteur** : v2.0 (manifeste MANIFESTE-MCS-v2.0.md — puissance démontrée avant gel)
**Domaines** : A = demi-grands axes des corps du système solaire (tables
publiques NASA/JPL) ; B = la loi de Titius-Bode **historique, figée par
l'histoire** : a_n = 0,4 + 0,3·2ⁿ UA.
**Attente honnête** : échec global probable. La loi est célèbre pour ses deux
ruptures (Neptune, 1789 années après sa formulation, mesurée à 30,07 UA contre
38,8 prédits ; Pluton à 39,48 contre 77,2) autant que pour ses réussites
(Uranus et Cérès, prédites puis trouvées). La question MCS n'est pas « la loi
est-elle vraie ? » mais : la structure résiduelle dépasse-t-elle le hasard
structurel, et les ruptures tuent-elles la stabilité sous 𝒢 ?

---

## 1. Énoncé de la coïncidence candidate

> Les demi-grands axes des corps de la liste figée (section 4) se placent sur
> la loi historique a_n = 0,4 + 0,3·2ⁿ UA — **paramètres gelés en 1772, aucun
> réajustement** — au-delà de ce que produit le hasard structurel, et cette
> conformité survit aux déformations du groupe 𝒢.

## 2. Lexique gelé (un mot = un objet)

| Mot | Objet opératoire unique |
|-----|--------------------------|
| corps | l'un des 10 corps de la liste figée (section 4) |
| prédiction | a_pred gelée : Mercure 0,4 ; Vénus 0,7 ; Terre 1,0 ; Mars 1,6 ; Cérès 2,8 ; Jupiter 5,2 ; Saturne 10,0 ; Uranus 19,6 ; Neptune 38,8 ; Pluton 77,2 (UA) |
| écart relatif | e(c) = (a_obs(c) − a_pred(c)) / a_pred(c) |
| m (mesure) | m = −log₁₀( RMS(e) ) sur les corps de la configuration |
| loi plate | nul de complexité égale : séquences croissantes quelconques sans loi |

## 3. Dictionnaire τ

    τ : demi-grands axes mesurés ↦ écarts relatifs à la loi figée ↦ m

τ est cette carte elle-même. Toute modification de τ après le gel = nouvelle
carte, nouveau numéro.

## 4. Données et provenance (gelées)

- **Liste figée des 10 corps et de leurs indices** (déclarée, historique) :
  Mercure (n = −∞, a_pred = 0,4), Vénus (0), Terre (1), Mars (2), Cérès (3),
  Jupiter (4), Saturne (5), Uranus (6), Neptune (7), Pluton (8).
- **Mesures** : demi-grands axes publics — source primaire : NASA Planetary
  Fact Sheets (NSSDC) ; contre-source (g1) : JPL Solar System Dynamics.
  Acquisition à l'ouverture, empreintes consignées. Aucune valeur n'a été
  lue dans ces tables avant la rédaction (les ruptures connues sont des
  faits historiques publiés, pas une lecture de la table).
- **Déclaration de circularité historique** : la loi a été ajustée en
  1766/1772 sur Mercure…Saturne (6 corps de la liste) ; Uranus (1781) et
  Cérès (1801) sont des prédictions réussies, Neptune (1846) et Pluton (1930)
  des ruptures. Le regard ailleurs (section 10) le paie.

## 5. Groupe de déformations légitimes 𝒢

| g | Déformation | Ce qu'elle teste |
|---|-------------|-------------------|
| g1 | source primaire (NSSDC) → contre-source (JPL SSD) | dépendance à la table |
| g2 | retrait de Neptune (rupture historique déclarée) | domination d'une rupture |
| g3 | retrait de Pluton (rupture + requalification 2006) | domination d'une rupture |
| g4 | retrait de Cérès (le « gap » comblé a posteriori) | domination d'une réussite |
| g5 | retrait de Mercure (indice n = −∞ singulier) | dépendance au point singulier |
| g6 | retrait d'un corps au hasard (PRNG public ChaCha20) | sensibilité locale |

## 6. Modèle nul

- **N1 (séquences libres)** : 10 000 séquences de 10 demi-grands axes triés,
  tirés log-uniformes dans l'étendue réelle déclarée [0,39 ; 39,8] UA ;
  m de la loi figée sur chacune → μ_null, u. (C'est le nul de complexité
  égale : aucune loi, même étendue, même effectif.)
- **N2 (écarts permutés)** : permutation des écarts relatifs entre corps,
  10 000 fois (rapporté ; teste l'assignation corps ↔ index, pas la loi).

## 7. Contrôles positifs (sabotages obligatoires)

| c | Sabotage | Attendu si le test a du pouvoir |
|---|----------|----------------------------------|
| c1 | indices décalés d'un rang (prédictions doublées : a_pred → 0,4+0,3·2^{n+1}) | m s'effondre (|effet| ≥ 2 u) |
| c2 | corps remplacés par une séquence log-uniforme déclarée | m s'effondre vers μ_N1 (|effet| ≥ 2 u) |

c1 ou c2 vraiment muet (|effet| < 2 u, règle v2.0) → **CS0**.

## 8. Statistique et seuils (gelés)

- z_g = (m_g − μ_null,g)/u_g sous N1 pour chaque g (effectif de la
  configuration) ; Σ = min sur {g1…g6}.
- Diagnostic rapporté (hors Σ) : m calculé séparément sur la cohorte
  « connue en 1772 » (6 corps) et la cohorte « post-1772 » (Uranus, Cérès,
  Neptune, Pluton).
- Seuil CS+ : **3,2** = 3,0 (base) + 0,1 (famille des réseaux géométriques
  déjà éprouvée par MCS-04) + 0,1 (ajustement historique partiel déclaré).

## 9. Critères de verdict

| Issue | Verdict |
|-------|---------|
| Σ ≥ 3,2 | CS+ |
| 2 ≤ Σ < 3,2 | CSp |
| −2 < Σ < 2 | CS− (B3-FAIL) |
| Σ ≤ −2 | CSi |
| un contrôle vraiment muet | CS0 |

## 10. Regard ailleurs (déclaration préalable)

La famille « loi harmonique / réseau géométrique » a été éprouvée par MCS-04
(CS− publié : non spécifique au pas près). La présente carte teste une loi
**figée par l'histoire** (pas par la machine) — opérateur identique, objet
différent. L'ajustement historique partiel (6 corps connus à la formulation)
est déclaré et payé au seuil (section 8). Tables consultées avant gel : 0.

## 11. Critères d'arrêt

- CS− ou CSi → carte fermée ; la loi de Titius-Bode est close comme
  coïncidence stable (son statut historique de curiosité reste ce qu'il est).
- CS0 → une seule refonte autorisée (MCS-09b).
- CSp → la carte dort.
- CS+ → surprise publiée avec la circularité historique en tête de lecture.

## 12. Démonstration de puissance (règle 1.2 du manifeste v2.0)

Avant gel : sur un système synthétique planté sur la loi figée à 1 % près,
la statistique doit donner Σ ≥ 3,2 et les deux contrôles résoudre à
|effet| ≥ 2 u ; sur une séquence croissante sans loi, CS− attendu ; banc
aveugle simulé → CS0. Hachée dans l'acte de gel.

## 13. Scellement (jalon 3 v2)

```
SHA256_CARTE : 8f8387ec24b55c2a5525700047438caf4a352718c42199951a2b95d8c063399c
HORODATAGE   : 2026-10-11T04:17:04Z
```
