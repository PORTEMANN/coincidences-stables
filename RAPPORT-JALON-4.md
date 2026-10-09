# RAPPORT JALON 4 — Ouverture sur données réelles

**Date** : 2026-10-09 — **Exécution unique par carte**, verdicts publiés quelle
soit l'issue. **Journal chaîné** : `journal/JALON-4-OUVERTURE.jsonl` (chaque
record inclut le hash du précédent ; vérifié à chaque étape). **Chaînage** :
le premier record lie la tête du scellement jalon 3
(`e611625f…`).

| Carte | Verdict moteur brut | Verdict final déclaré | Σ |
|-------|--------------------|-----------------------|---|
| MCS-01 — k(Z) vs vallée β | CS0 (artefact de signe) | **CSi** | −6,93 |
| MCS-02 — invariants ASH vivant/non vivant | CS0 (artefact de signe) | **CSi** | −25,10 |
| MCS-03 — KO-6 ↔ E₈ (calibration négative) | CS0 (matériel) | **CS0** | −1,95 (suspendu) |

---

## 1. Doctrine d'exécution (rappel)

- Chaque runner est écrit, haché (SHA-256) et consigné au journal **avant** son
  exécution unique. Toute modification ultérieure = nouveau hash, nouvelle
  entrée de journal (l'historique est publié, jamais effacé).
- PRNG : **graine publique déterministe**
  `clé = SHA-256("MCS-J4|" + empreinte_carte + "|" + empreinte_données)` → flot
  ChaCha20-IETF (RFC 8439, nonce nulle). Aucune graine secrète : l'exigence est
  la reproductibilité. L'ordre des tirages est publié dans chaque runner.
- Le journal JSONL est chaîné par hachage (chaque record inclut le hash du
  précédent) ; il ne peut pas être réécrit sans casser la chaîne.
- Déviations déclarées et publiées (jamais silencieuses) — elles sont listées
  ci-dessous.

## 2. Acquisition des données

- **AME2012 / AME2003 / NUBASE2012 / NUBASE2003** : l'origine IAEA
  (www-nds.iaea.org) est protégée par Cloudflare pour les requêtes directes et
  la Wayback Machine était inaccessible. Acquisition via le **miroir officiel
  AMDC/IMP-CAS** (même centre de données), avec **recoupement indépendant** de
  l'origine IAEA par navigateur : 4/4 noyaux témoins identiques (¹²C, ¹⁶O,
  ⁵⁶Fe, ²⁰⁸Pb), 3 353/3 353 et 3 179/3 179 lignes parsées, A = N+Z cohérent.
- **JEFF-3.3 (contre-données)** : fichier combiné de décroissance
  `JEFF33-rdd_all.asc` (45 Mo, 3 084 demi-vies) via la plateforme officielle
  DOI de la NEA Data Bank (data.oecd-nea.org). Contrôles : n = 614,6 s ;
  ²³⁸U = 1,41·10¹⁷ s ✓.
- **EEG (MCS-02)** : la carte prévoyait OpenNeuro ds003778 « ou équivalent
  déclaré au gel » ; ds003778 est un protocole de mémoire, pas un repos yeux
  ouverts. Substitution déclarée : **ds004584 « EEG Rest eyes open »**
  (49 contrôles sains, 63/64 canaux dont Cz et O1, 500 Hz, CC0) ; 20 sujets
  tirés par le PRNG public, 3 fenêtres disjointes de 10 s par sujet.
- **ECG** : PhysioNet nsrdb, 18 enregistrements, dérivation ECG1 (= lead II
  documenté), 60 segments de 10 s tirés.
- **Allen Cell Types** : 10 cellules humaines (sur 413 candidates avec NWB),
  60 fenêtres de 10 s sur 52 sweeps ≥ 12 s de contenu réel (50 kHz).
- **CWRU Bearing** : 1 HP : 12 fichiers (98, 106, 119, 131, 170, 175, 186, 210,
  214, 223, 3002, 3006) ; 3 HP : 11 fichiers — 216.mat et 3009-3012.mat
  inexistants (HTTP 404), déclaré. 60 fenêtres par régime, offsets à résolution
  échantillon (fichiers ~12 s).
- Le tirage des fenêtres est fixé par `code/jalon4_acquisition_mcs02.py`
  (publié, haché) et consigné dans `donnees/MANIFESTE-ACQUISITION-MCS02.json`.

## 3. MCS-01 — k(Z) contre la vallée de stabilité β : **CSi**

Runner `code/mcs01_runner.py` (hash `1b59bf38…`).

- La loi candidate k(Z) = −(1/(1000α))·ln Z + 3/2 est **anti-alignée** avec la
  vallée β dans les 9 configurations (AME2020, AME2003, JEFF-3.3, retraits
  magiques/pairs/impairs/légers, CODATA 2018/2022, deux conventions de N/Z) :
  z de −4,5 à −6,9 ; **Σ = −6,93 ≤ −2**.
- Falsification convergente des trois familles de nuls : N1 (z ≈ −7), N2 (les
  nuls ajustés battent la candidate : marge −0,84), N3 (la candidate est *sous*
  le quantile 99 % des lois lisses aléatoires : 0,379 < 0,434).
- Contrôle c1 (Z↔N) : la candidate s'ajuste sur les données **miroir** à
  +45,6 u — effet de 52,6 u en valeur absolue ; c2 (α→α/2) : +53,0 u. Le banc
  est extrêmement puissant ; le CS0 moteur est un artefact de la convention
  signée (effet attendu positif alors que la candidate partait déjà détruite).
- Note de transparence : le commentaire de la carte « 1/(1000α) ≈ 1,37036 »
  est arithmetiquement faux (0,137036) ; la **formule** gelée a été exécutée.
  La conclusion est robuste à cette ambiguïté.
- **Carte fermée** (section 11 : fermer, ne pas ajouter ; la refonte MCS-01b
  n'est pas engagée).

## 4. MCS-02 — Invariants ASH à travers signaux vivants et non vivants : **CSi**

Runner `code/mcs02_runner.py` (hash final `bb0b2067…`).

- Sur les 8 configurations (base, renversement, O1, 3 HP, 4 s, sans I4, sujets
  tournés, 500 Hz), la séparation des domaines dans l'espace (I1..I4) est très
  **supérieure** à celle des surrogates IAAFT : z de −7,1 à −25,1 ;
  **Σ = −25,10 ≤ −2**.
- Double contrainte : (a) Σ < 3,3 ; (b) les surrogates IAAFT ne s'effondrent
  pas (z_effondrement = +22,6) — ils se **rapprochent**. Ni (a) ni (b), et
  Σ ≤ −2 : **CSi**.
- N2 (bruit de même DSP moyenne de domaine) reproduit m réel (−2,33 contre
  −2,28) : la séparation est essentiellement **spectrale, donc générique** ;
  la structure de phase écarte encore davantage les domaines.
- Contrôles : c1 (mélange d'étiquettes) : m tombe à −0,3624, à 0,05 u de la
  moyenne N3 (−0,3583) — l'attente « s'effondre vers N3 » est exactement
  remplie (effet de 97 u ; convention signée inopérante car la candidate
  partait inversée) ; c2 (injection PAC, après correction du dosage déclarée
  en CODE_MCS02_V3) : **+2,08 u, vivant** ; c3 (métronome) : I3 = 0 vs 0,252
  (ECG), 0,88 u — classé à part (rapporté).
- **La couche ASH dans sa forme actuelle est close** (section 11). Publication
  B3-FAIL.

## 5. MCS-03 — KO-6 / triples spectraux ↔ 2I ⊂ E₈ : **CS0** (banc local aveugle)

Runner `code/mcs03_runner.py` (hash `483c2bda…`).

- Machinerie intégralement calculée et auto-vérifiée : tables de caractères
  (centre de l'algèbre de groupe ; complétude Σd² = |G|, orthogonalité),
  indicateur de Frobenius-Schur, décomposition de Wedderburn réelle — la table
  de 2I est reproduite exactement, celle de I (A₅) aussi.
- Σ = −1,95 (qui aurait lu CS−, la cible de calibration) est **suspendu** :
  les trois contrôles sont matériellement muets (c1 : +0,04 u ; c2 : −0,44 u ;
  c3 : +0,62 u). La statistique (Spearman sur 15 paires) ne résout pas un
  sabotage point-par-point. Le CS0 est matériellement correct.
- La prémisse de la correspondance est déjà factuellement fausse sous
  l'invariant déclaré : C(A_F) = 2 alors que max(C_ALG) = 6 ; C(2I) = 12 alors
  que max(C_GRP) = 14.
- **Localité de la cécité démontrée** (exigée par la carte section 11) : cause
  structurelle identifiée (corrélation de rangs, 15 points) ; MCS-01 et MCS-02
  montrent des contrôles de 53 u et 97 u sur d'autres statistiques. Les
  verdicts des autres cartes tiennent.
- **Ligne KO-6 ↔ E₈ fermée comme non-testable par cet invariant** (pas comme
  CS−). Aucune refonte dans cette campagne.

## 6. Historique complet des échecs et corrections (publication symétrique)

1. IAEA derrière Cloudflare (curl) ; Wayback inaccessible (curl **et**
   navigateur) → miroir AMDC/IMP-CAS + recoupement navigateur.
2. Acquisition MCS-02 v1 : 17 fenêtres Allen nulles (sweeps zero-paddés) →
   exécution arrêtée avant terme ; pool reconstruit sur plages non nulles.
3. Acquisition v1bis : doublons massifs CWRU (offsets entiers en secondes) →
   offsets à résolution échantillon.
4. Runner MCS-02 v1 : crash après g1 (bug tuple) → correction, nouveau hash.
5. Runner MCS-02 v2 : contrôle c2 sous-dosé (injection non mise à l'échelle,
   signaux µV) → exécution complète mais c2 muet ; v3 avec dosage fort,
   tout le reste bit à bit identique (vérifié 3 fois sur g1).
6. PRNG ChaCha20 pur Python trop lent (~100 ms/surrogate) → vectorisation
   numpy (×18), **flot prouvé bit à bit identique** (RFC 8439 + recoupement
   20×100 blocs).
7. Manifeste d'acquisition : crash JSON (int64 numpy) → convertisseur déclaré.

Aucun de ces épisodes n'a été effacé du journal : chacun est consigné dans le
record correspondant.

## 7. Reproductibilité

- Journal : `journal/JALON-4-OUVERTURE.jsonl` — vérification :
  `JournalChaine.verifier(chemin, genesis="GENESIS-MCS-J4-OUVERTURE")`
  (retourne `(True, n)` sur les n records chaînés).
- Empreintes données : MCS-01 `57caec6e…`, MCS-02 `afe3efea…`,
  MCS-03 (calculée sur énumérations) `764dfb6f…`.
- Runners : MCS-01 `1b59bf38…`, MCS-02 `bb0b2067…`, MCS-03 `483c2bda…` ;
  PRNG partagé `970eeb1b…` ; script d'acquisition (hash final dans le journal).
- Résultats complets : `resultats/mcs01_resultats.json`,
  `resultats/mcs02_resultats.json`, `resultats/mcs03_resultats.json`.
- Les données brutes (~700 Mo) ne sont pas versionnées (sources publiques :
  AMDC/IMP-CAS, IAEA, NEA, OpenNeuro, PhysioNet, Allen, CWRU) ; leurs
  empreintes sont dans le journal et les manifestes.
