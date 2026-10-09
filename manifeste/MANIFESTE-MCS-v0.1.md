# MANIFESTE MCS — v0.1 (CANDIDAT, NON SCELLÉ)

**Machine à Coïncidences Stables / Machine des Points Fixes inter-domaines**
Date de rédaction : 2026-10-09
Statut : JALON 1 — cartes rédigées, rien n'est gelé, aucun test n'a été exécuté.

---

## 1. Objet de la machine

La MCS n'est ni une ontologie ni un instrument de métrologie. Elle arbitre des
**correspondances entre domaines indépendants**. Sa question unique :

> Une correspondance déclarée τ : A → B survit-elle aux déformations qui
> devraient la détruire si elle n'était qu'un artefact de langage ?

Elle hérite de la doctrine du corpus :

- **fermer, ne pas ajouter** — une carte morte est une frontière mesurée ;
- **un mot = un objet** — chaque terme a une définition opératoire unique, gelée dans la carte ;
- **échecs publiés** — les verdicts négatifs ont la même valeur documentaire que les positifs (B3-FAIL) ;
- **séparation carte/banc** — le carnet propose, le banc dispose ; le banc ne connaît que des cartes hashées.

La MCS ne prononce jamais « c'est vrai ». Elle prononce « cette compression
résiste anormalement » (CS+), « elle est locale » (CSp), « elle est un artefact
probable » (CS−), « elle s'inverse » (CSi), ou « le test est impuissant » (CS0).

## 2. Opérateur

Soit une correspondance candidate τ : A → B et un groupe de déformations
légitimes 𝒢 déclaré dans la carte. Pour chaque déformation g ∈ 𝒢, une statistique
de marge normalisée :

    z_g(τ) = ( m_g(τ) − μ_null,g ) / u_g

où m_g est la mesure de qualité de la correspondance sous g, μ_null,g la
moyenne du modèle nul sous g, u_g son incertitude (écart-type du nul).

La stabilité est le **maillon le plus faible** :

    Σ(τ) = min_{g ∈ 𝒢} z_g(τ)

Une seule déformation légitime qui casse la correspondance tue la carte.
La moyenne des preuves est interdite : elle permettrait à une coïncidence
forte sur un axe de compenser une mort sur un autre.

## 3. Taxonomie des verdicts

| Condition            | Verdict | Sens                                              |
|----------------------|---------|---------------------------------------------------|
| Σ ≥ 3                | **CS+** | coïncidence stable : survit à tout 𝒢               |
| 2 ≤ Σ < 3            | **CSp** | stabilité locale ; hors-échantillon non démontré   |
| −2 < Σ < 2           | **CS−** | artefact probable ; publication B3-FAIL obligatoire |
| Σ ≤ −2               | **CSi** | inversion stable ; publication prioritaire         |
| contrôles positifs muets | **CS0** | test impuissant ; aucune conclusion, carte à refondre |

Règle d'impuissance : si un contrôle positif (sabotage qui *doit* casser une
correspondance réelle) ne la casse pas, le test est aveugle. Verdict CS0,
quel que soit Σ.

## 4. Constitution (règles non amendables sans changement de version majeure)

1. **Dictionnaire gelé.** τ est écrite avant tout calcul. Aucune retouche après
   observation des résidus.
2. **Un mot = un objet.** Chaque carte contient un lexique ; tout terme non
   défini dans le lexique est interdit dans la carte.
3. **Modèle nul déclaré.** Pour chaque carte : ce que le hasard structurel peut
   produire seul (permutations, bootstrap par blocs, surrogates IAAFT, modèles
   de même complexité en degrés de liberté).
4. **Contrôles positifs obligatoires.** Au moins deux sabotages par carte, qui
   doivent casser la correspondance si le test a du pouvoir.
5. **Regard ailleurs.** Chaque carte déclare le nombre de familles de formes et
   de variantes essayées ; les seuils sont corrigés en conséquence avant ouverture.
6. **Seuils gelés.** Tous les seuils (θ, tailles d'effet, fenêtres, jeux de
   données) sont fixés au gel, avant la première exécution du banc.
7. **Publication symétrique.** CS− et CSi sont publiés avec le même soin que CS+.

## 5. Registre des cartes (jalon 1)

| ID      | Titre                                        | Domaines A × B                          | Attente honnête |
|---------|----------------------------------------------|------------------------------------------|-----------------|
| MCS-01  | k(Z) contre la vallée de stabilité           | constante α × masses nucléaires (AME)    | à fermer        |
| MCS-02  | Invariants spectraux ASH inter-signaux       | EEG × ECG × vibration × électrophys.     | à discipliner   |
| MCS-03  | KO-6 / triples spectraux ↔ 2I ⊂ E₈, \|2I\|=120 | géométrie non commutative × théorie des groupes | calibration négative |

## 6. Séquence des jalons

- **Jalon 1 (présent document)** : manifeste + cartes, sans code. Lexiques,
  dictionnaires τ, groupes 𝒢, nuls, contrôles positifs, seuils.
- **Jalon 2** : implémentation de Σ = min z_g et des générateurs de nuls,
  testée sur données synthétiques à vérité connue (démontrer que le banc tue
  les artefacts et détecte les correspondances plantées).
- **Jalon 3** : gel — calcul des SHA-256 des cartes et du code, chaînage du
  journal, horodatage. Aucune exécution sur données réelles avant ce point.
- **Jalon 4** : ouverture — exécution unique, verdicts, publication quelle
  que soit l'issue.

## 7. Politique de publication

Tout verdict est publié avec : la carte hashée, le code hashé, le journal
chaîné, les distributions nulles, les contrôles positifs, et la valeur de Σ
par déformation (pas seulement le minimum). Un CS+ publié sans ses z_g
complets est invalide.

## 8. Limites de portée

- La MCS ne dit rien sur la conscience, la noétique ou l'ontologie. Une
  coïncidence stable est une **invitation à chercher une loi commune**, pas
  la preuve qu'elle existe.
- Aucune carte ne peut porter sur des données déjà utilisées pour construire
  sa propre correspondance (circularity interdite ; voir règle de hors-échantillon
  dans chaque carte).
- La MCS ne modifie pas `mvcg` : elle est un opérateur distinct, sur un objet
  distinct (passages entre langages, non contacts métrologiques).

## 9. Scellement (à remplir au jalon 3)

```
SHA256_MANIFESTE : 3c5d50bec884571fb41b6c4a5fb3739b8b70fb7458f3651e3297a3ae3e1fce78
SHA256_MCS-01    : 45185f63459fcf9e580a0a86725110a9bdf462aa1754b56321259a73ca34c0e1
SHA256_MCS-02    : 0aa840f23ca4516ae5f76342be950694d0dcd4c204e02ea7ad0c8b1f08fa167a
SHA256_MCS-03    : e5b082c87c996842c707e06a66d98008c62c9dfc114ee33a35ff5da7dc0a1f70
SHA256_CODE      : 892cd28ee5aad1f31dae866abed9d61dee06c4dc2737e8c813acf426f96db0a9
CHAINE_JOURNAL   : e611625fafa6e760358371d4c33f6021f0dd42bec5d15a28a64a490f10b9d22f
HORODATAGE       : 2026-10-09T13:31:46Z
```

---

*Rédigé à la croisée des « coïncidences stables ». Ce manifeste est un candidat :
tant que le bloc 9 est à null, tout peut encore mourir proprement.*
