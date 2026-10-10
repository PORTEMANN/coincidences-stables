# CARTE SÉMANTIQUE DES VERDICTS — Machine à Coïncidences Stables

**Date** : 2026-10-10 · **Périmètre** : campagne v0.1 (jalon 4 : MCS-01/02/03,
moteur figé) + campagne v2.0 (jalons 1–4 v2 : MCS-04 à 07) + carte de
calibration MCS-08 (Benford × CODATA, CS+) + verdicts du corpus
mobilisés par les cartes (mvcg, M1/M1b, bifurcations, EEG P44/P47/P51).

Cette carte ne classe pas les verdicts par numéro mais par **ce qu'ils
signifient** : quel type de correspondance était testé, et quel mode de
fermeture (ou de suspension) la réalité a choisi.

---

## 1. La carte en une image

```
                        CORRESPONDANCE TESTÉE
                                │
        ┌───────────────────────┼───────────────────────────┐
   structurelle            de forme globale            de dépendance
   (invariants,            (loi harmonique,            (proximité × succès,
    spectres)               décroissance)               frontière)
        │                       │                           │
   MCS-01  MCS-02          MCS-04   MCS-06              MCS-07
    CSi     CSi             CS−      CS−                 CS−
   (inversion stable)  (non spécifique / sous seuil)  (portée par la
                                                        frontière elle-même)

        │                       │
   MCS-03 : CS0            MCS-05 : CS0
   (matériau insuffisant)  (mesure sous le nul — test impuissant)

   calibration (régularité connue vraie) :
   MCS-08 : CS+ — Benford × CODATA (Σ = 5,24) — l'étalon
```

## 2. Les cinq modes de fermeture (la lecture sémantique)

### A. Inversion stable (CSi) — la réalité fait *pire* que le hasard
- **MCS-01** (loi kZ × masses AME) : Σ = −6,93. La loi numérique candidate est
  activement contredite par les masses mesurées, sous toutes les déformations.
- **MCS-02** (invariants ASH × signaux EEG/ECG/cellules/roulements) :
  Σ = −25,10. Les invariants structurels séparent *moins bien* que des
  surrogates de même spectre.

*Signification* : ces correspondances ne sont pas seulement absentes — elles
sont **anti-stables**. Le monde, dans ces deux domaines, se range du côté
opposé à la loi proposée. C'est le verdict le plus fort que la machine rende.

### B. Forme réelle mais non spécifique (CS−) — mieux que le hasard, pas au pas près
- **MCS-04** (zoo particulaire × tempérament égal) : le canonique bat un réseau
  aléatoire (z = 2,28) mais n'importe quel pas voisin convient (g5 : −0,43).

*Signification* : il y a une régularité grossière (les masses s'ordonnent en
log), mais elle ne porte **aucune information au niveau du demi-ton**. La loi
précise était une illusion de sélection : le vague survit, le précis meurt.

### C. Dépendance portée par la frontière elle-même (CS−)
- **MCS-07** (M1 : distance à r₁₂ × taux de succès) : la relation existe sur
  le corpus (z0 = 2,38) mais disparaît quand on retire les trois chantiers de
  la frontière (z = 0,55).

*Signification* : l'inversion M1 est une **propriété des points-frontière**,
pas une loi du corpus. La mesure reste publiée et vraie ; elle n'est pas une
coïncidence stable — elle ne généralise pas hors de ses propres témoins.

### D. Tendance vraie, sous le seuil (CS−)
- **MCS-06** (loi des bifurcations v2) : ρ = −0,853 sur l'axe physique, stable
  sous g1–g5 (2,10 ≤ z ≤ 2,37), mais le seuil 3,1 n'est jamais approché, et la
  carte incluait dans Σ un tirage du nul (g6 — défaut de conception publié).
  Point de méthode confirmé : l'axe conventionnel est libre (|ρ_conv| = 0,135).

*Signification* : la décroissance de la dérivabilité avec la complexité est
**visible mais pas démontrable** à cette taille d'échantillon. La conjecture
reste catégorie II — étiquetée, non promue.

### E. Test impuissant (CS0) — la machine refuse de trancher
- **MCS-03** (KO6/E8 × groupes finis SU(2)) : les trois contrôles muets — le
  matériau (15 paires) ne résout pas les sabotages ponctuels.
- **MCS-05** (agrégation centroïde EEG) : la mesure réelle est *sous* le nul
  IAAFT (0,457 < 0,493) ; le contrôle par permutation ne peut pas dégrader ce
  qui est déjà en dessous (c1 = 1,82 u < 2 u).

*Signification* : le moteur v2.0 distingue « la correspondance est fausse » de
« le test ne peut pas voir ». Les deux cartes sont **suspendues, pas closes** —
une seule refonte chacune (MCS-03b, MCS-05b).

### F. Confirmation (CS+) — l'étalon de calibration
- **MCS-08** (loi de Benford × constantes CODATA 2022) : Σ = 5,24 ≥ 3,0 —
  z de 5,24 à 10,93 sous toutes les déformations (édition 2018, retrait des
  constantes exactes du SI, échelle eV, **base 12**, demi-table, retrait
  aléatoire) ; contrôles à 8,41 u et 7,32 u.

*Signification* : la machine sait reconnaître une régularité vraie — y compris
en base 12, ce qui confirme que la loi détectée est celle du monde, pas de la
notation. Ce CS+ n'est pas une découverte (Benford était connu) : c'est
l'**étalon** qui donne leur valeur discriminante aux six fermetures et
suspensions précédentes.

## 3. Ce qui survit (confirmations MCS et pesées locales du corpus)

| Survivant | Statut | Portée |
|-----------|--------|--------|
| **Benford × CODATA (MCS-08)** | **CS+ — Σ = 5,24** | étalon de calibration : l'opérateur reconnaît une régularité vraie |
| Contacts harmoniques mvcg : μ, Z, charm | S+ locaux publiés | pesées par contact, PAS une loi globale (MCS-04 l'a mesuré) |
| P-He : He est gaz noble | tranchée 5/5 | une bifurcation physique à bas Z, décidée |
| M1/M1b : inversion à r₁₂ | mesurée et répliquée | vraie sur les points-frontière, instable sous 𝒢 (MCS-07) |
| Frontière r₁₂ (P31–P33, P39) | cartographiée | la limite du dérivable existe ; sa « loi » reste conjecture |

## 4. Ce que la carte dit du monde

1. **Une coïncidence stable confirmée (MCS-08, calibration) sur 8 cartes** —
   2 inversions, 3 fermetures, 2 suspensions, 1 étalon. Le CS+ de calibration
   mesure la machine ; les fermetures mesurent le monde.
2. **Les correspondances numériques précises entre domaines éloignés meurent
   toutes au même endroit** : la déformation qui change l'échelle, le pas ou
   l'ancre (MCS-01 g, MCS-04 g5). Le monde contient des régularités
   grossières ; il ne contient pas, dans ce qui a été testé, de réseaux
   précis cachés.
3. **L'EEG comme source de lois zéro-paramètre est quadruplement fermé**
   (P44, P47, P51, MCS-05/CS0) — la famille doit dormir.
4. **Les vraies frontières trouvées sont internes au corpus** (r₁₂, M1) :
   la machine éclaire d'abord ses propres limites de dérivabilité.
5. **L'honnêteté du dispositif est mesurée, pas affirmée** : deux CS0
   informatifs (dont un produit par la règle signe-robuste v2.0 là où v0.1
   aurait rendu un faux verdict), un défaut de conception publié (MCS-06, g6).

---

*Carte rédigée après clôture du jalon 4 v2, mise à jour après MCS-08. Toute
carte future (MCS-09+) ajoutera un point à cette carte, jamais ne révisera un
point existant — les fermetures sont définitives, les suspensions attendent
leur refonte unique.*
