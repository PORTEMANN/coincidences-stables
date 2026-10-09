# Rapport de validation synthetique — jalon 2

Graine maitresse : `20261009` — PRNG numpy (synthetique ; les campagnes
scellees utiliseront ChaCha20-IETF, conformement au manifeste).

## Resultats

| Scenario | Verite connue | Attendu | Obtenu | Conforme |
|----------|---------------|---------|--------|----------|
| SYN-A_correspondance_plantee | — | CS+ | CS+ | oui |
| SYN-B_artefact_spectral | — | CS- | CS- | oui |
| SYN-C_loi_fausse | — | CS- | CS- | oui |
| SYN-D_loi_plantee | — | CS+ | CS+ | oui |
| SYN-E_banc_aveugle | — | CS0 | CS0 | oui |

## Controles positifs du banc (calibration)

- c1 (scramble FT sur PAC plante) : effet = 26.25 u_null
- c2 (injection d'un PAC connu dans du bruit) : effet = 25.08 u_null
- seuil de pouvoir gele : >= 2.0 u_null

## Detail par scenario

### SYN-A_correspondance_plantee

- verdict : **CS+** — structure de phase inter-domaines stable (vit sur donnees, meurt sous IAAFT)
- Sigma = 13.603 (seuil 3.3)
- z par deformation : g1_iaaft = 20.17, g2_renversement = 20.17, g5_fenetre_4s = 13.60, g8_500Hz = 22.03

### SYN-B_artefact_spectral

- verdict : **CS-** — ni (a) ni (b) : artefact probable
- Sigma = -1.086 (seuil 3.3)
- z par deformation : g1_iaaft = 1.14, g2_renversement = 1.14, g5_fenetre_4s = -1.09, g8_500Hz = 1.52

### SYN-C_loi_fausse

- verdict : **CS-** — artefact probable ; publication B3-FAIL
- Sigma = 0.525 (seuil 3.0)
- z par deformation : g1_complet = 0.67, g2_pairs = 0.74, g3_impairs = 0.78, g4_Zge20 = 0.52

### SYN-D_loi_plantee

- verdict : **CS+** — coincidence stable : survit a toutes les deformations
- Sigma = 5.371 (seuil 3.0)
- z par deformation : g1_complet = 7.09, g2_pairs = 6.46, g3_impairs = 7.17, g4_Zge20 = 5.37

### SYN-E_banc_aveugle

- verdict : **CS0** — controles positifs muets : ['c1_scramble_FT'] ; test impuissant
- Sigma = 5.000 (seuil 3.3)
- z par deformation : g1 = 5.00, g2 = 5.00, g3 = 5.00, g4 = 5.00

## Honnetete du banc

1. Pour les scenarios spectraux, la mesure validee est m = couplage
   phase-amplitude moyen (I4). C'est un substitut : il exerce Sigma, la
   double contrainte IAAFT, les controles et le journal. La mesure
   exacte de la carte MCS-02 (Wasserstein inter-domaines) reste gelee
   pour le jalon 4 et n'a pas ete executee ici.
2. Le nul de g2 (renversement temporel) reutilise la distribution nulle
   de base : par stationnarite des surrogates, elles coincident.
3. Pour les scenarios de lois (SYN-C/D), le nul est la famille de lois
   lisses aleatoires (N3-like de la carte MCS-01) : une permutation seule
   est trop faible pour des donnees monotones et ferait paraitre une
   mauvaise loi 'stable'. La regle de marge N2 de la carte (battre le
   meilleur nul ajuste hors-echantillon) reste a exercer au jalon 4.
4. SYN-E demontre que le verdict CS0 prime sur Sigma : une statistique
   aveugle avec Sigma = 5 est refusee. La regle 'controles muets => CS0'
   est cablee dans l'operateur, pas dans l'interpretation.

## Integrite

- journal chaine SHA-256 : integre, 7 enregistrements (`journal_synthetique.jsonl`).

## Portee

Jalon 2 valide le moteur de verdict. Il ne valide ni les donnees, ni
les cartes, ni la physique. Prochain jalon : gel (SHA-256 des cartes
et du code, chainage, horodatage). Aucune donnee reelle avant.
