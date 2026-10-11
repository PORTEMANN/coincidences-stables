# CARTE MCS-05b — Asymétrie ERD × classes motrices (F17, REFONTE UNIQUE)

**Statut** : REFONTE — NON SCELLÉ — Jalon 1 v2 (rédaction, aucun calcul)
**Refonte de** : MCS-05 (gelée au jalon 3 v2, ouverte : **CS0** — la mesure
centroïde était *sous* le nul IAAFT (0,457 < 0,493) et le contrôle par
permutation d'étiquettes ne pouvait pas dégrader une mesure déjà sous le
nul : c1 = 1,82 u, muet ; suspension publiée).
**Moteur** : v2.0.
**Domaines** : A = EEG d'imagerie motrice (BCICIV-2a, déjà acquis et
empreinté — réutilisation consignée) ; B = classes motrices (gauche/droite).
**Attente honnête** : **CS− attendu** — trois échecs mesurés dans le corpus
(P44, P47, P51) et la suspension CS0 de MCS-05. La fonction de la refonte :
convertir la suspension en fermeture propre si le signal est absent, ou la
surprise s'il est présent. La refonte corrige la cécité de la mesure, pas
la question.

---

## 1. Ce que la refonte change — et ne change pas

**Inchangé** : la question (existe-t-il une information lisible entre essais
et classes d'imagerie motrice, stable sous 𝒢 ?), les données (BCICIV-2a),
la fenêtre et les canaux de la famille, le verdict attendu.

**Changé (l'opérateur)** : la mesure centroïde (accuracy) vivait sous le
plancher du hasard (0,5) : sous le nul, elle ne pouvait plus tomber. La
refonte mesure l'**asymétrie ERD**, centrée sur zéro — sans plancher :

- indice d'un essai : E = (P_μ(ipsilatéral) − P_μ(contralatéral)) /
  (P_μ(ipsi) + P_μ(contra)), P_μ = puissance de la bande mu (8–12 Hz)
  sur la fenêtre 2–4 s post-cue, aux canaux C3/C4, latéralité
  déduite de l'étiquette (gauche → ipsi = C3 ; droite → ipsi = C4) ;
  l'ERD atténue le contralatéral : E > 0 attendu si l'ERD existe ;
- m = moyenne de E sur tous les essais de tous les sujets (signe déclaré :
  m > 0 attendu si l'ERD existe).

Le point méthodologique de la refonte : m = 0 est le point sans signal —
la mesure peut tomber DES DEUX côtés du nul, le contrôle c1 (étiquettes
permutées) retrouve un pouvoir.

## 2. Lexique gelé (un mot = un objet)

| Mot | Objet opératoire unique |
|-----|--------------------------|
| essai | un segment EEG BCICIV-2a (canaux C3/C4, fenêtre 2–4 s post-cue, 250 Hz) |
| bande mu | 8–12 Hz (puissance par périodogramme, zéro paramètre) |
| E (essai) | (P_contra − P_ipsi) / (P_contra + P_ipsi) selon l'étiquette déclarée |
| m (mesure) | moyenne de E sur les essais de la configuration |
| nul de complexité égale | surrogates IAAFT (spectre identique, phase détruite) |

## 3. Dictionnaire τ

    τ : essais EEG ↦ asymétrie mu contralatérale ↦ m

τ est MCS-05 avec l'opérateur corrigé. Toute modification après le gel =
nouvelle carte, nouveau numéro.

## 4. Données et provenance (gelées)

- **BCICIV-2a** (Graz, 9 sujets, sessions d'entraînement étiquetées) —
  déjà acquis pour MCS-05 (zip sha256 65fe93cb… et 9 fichiers GDF
  empreintés au journal du jalon 4 v2) ; réutilisation re-consignée.
- Déclaration d'usage antérieur conservée de MCS-05 (P44, P47, P51 +
  suspension MCS-05) : le regard ailleurs le paie (section 10).

## 5. Groupe de déformations légitimes 𝒢

| g | Déformation | Ce qu'elle teste |
|---|-------------|-------------------|
| g1 | hémisphères permutés (C3 ↔ C4 par essai, exclu du min, rapporté) | latéralité ou générique ? |
| g2 | fenêtre 2–4 s → 1–3 s | dépendance à la fenêtre |
| g3 | bande mu 8–12 Hz → 8–13 Hz | dépendance à la bande |
| g4 | retrait du sujet A03 (déclaré à MCS-05) | domination d'un sujet |
| g5 | canaux C3/C4 → C3/C4 avec référence Cz soustraite | dépendance à la référence |
| g6 | retrait d'un sujet au hasard (PRNG public ChaCha20) | sensibilité locale |

## 6. Modèle nul

- **N1 (hémisphères permutés)** : réassignation aléatoire C3 ↔ C4 par essai,
  10 000 fois ; la contralatéralité est détruite, tout le reste est conservé
  → μ_null, u. (La mesure est une mesure de *puissance* : un surrogate IAAFT
  conserve le spectre et ne peut pas la tuer — le nul honnête est la
  permutation des hémisphères, déclaré.)
- **N2 (étiquettes permutées)** : permutation des étiquettes, 1 000 fois.
- **N3 (bruit de même DSP)** : bruit filtré de même DSP par sujet.

## 7. Contrôles positifs (sabotages obligatoires) — règle de la refonte

| c | Sabotage | Attendu si le test a du pouvoir |
|---|----------|----------------------------------|
| c1 | étiquettes permutées | m → 0 (rapporté : vivant SSI un signal est présent — voir ci-dessous) |
| c2 | injection d'une asymétrie mu synthétique déclarée dans du bruit réel (essais réels remplacés par bruit + mu atténué d'un côté selon des étiquettes factices) : le pipeline doit retrouver ces étiquettes | récupération ≫ hasard (|effet| ≥ 2 u) |

**Règle déclarée de la refonte** : c2 muet → **CS0** (le pipeline est
aveugle : verdict d'impuissance). c1 muet n'est **pas** un CS0 : sur
données sans signal, c1 est muet par construction — c'était la cécité de
MCS-05 ; c1 est publié comme diagnostic de présence du signal, pas comme
déclencheur. (Déviation déclarée à la règle générale des deux contrôles —
la justification est la suspension elle-même.)

## 8. Statistique et seuils (gelés)

- z_g = (m_g − μ_null,g)/u_g sous N1 pour chaque g ; Σ = min sur {g2…g6}
  (g1 exclu du minimum, rapporté — double contrainte).
- Double contrainte : (a) Σ ≥ 3,3 sur données réelles ; (b) sous permutation
  des hémisphères, m s'effondre (z_effondrement ≤ −2).
- Seuil CS+ : **3,3** (famille EEG : trois échecs mesurés + la suspension
  de MCS-05, payés — gelé à MCS-05, conservé).

## 9. Critères de verdict

| Issue | Verdict |
|-------|---------|
| (a) et (b) | CS+ (surprise — la famille EEG dormait) |
| (a) sans (b) | CS− déguisé → **CS−** (latéralité générique) |
| (b) sans (a) | CSp |
| ni (a) ni (b) | **CS− — verdict attendu : F17 close pour cette famille** |
| Σ ≤ −2 | CSi |
| c2 vraiment muet | CS0 — le pipeline reste aveugle après sa seule refonte |

## 10. Regard ailleurs (déclaration préalable de la refonte)

Quatre mesures EEG déjà publiées : P44, P47, P51 (B3-FAIL) et MCS-05 (CS0).
La refonte les paie toutes au seuil (3,3 conservé). C'est l'unique refonte
autorisée : aucune MCS-05c n'existera.

## 11. Critères d'arrêt

- CS− ou CSi → fermeture propre : la question « information lisible entre
  essais et classes, zéro paramètre » est close pour la famille BCICIV-2a
  (quatre mesures + une refonte — publié B3-FAIL).
- CS0 → le pipeline est déclaré aveugle après sa seule refonte (publié).
- CSp → la carte dort à nouveau.
- CS+ → surprise ; publication avec les trois échecs en tête de lecture.

## 12. Démonstration de puissance (règle 1.2 du manifeste v2.0)

Avant gel : sur un EEG synthétique avec ERD planté, la statistique doit
donner Σ ≥ 3,3 et c2 résoudre à |effet| ≥ 2 u ; sur bruit sans structure,
CS− attendu ; pipeline aveugle simulé → CS0. Hachée dans l'acte de gel.

## 13. Scellement (jalon 3 v2)

```
SHA256_CARTE : 33ae9f7194d345cb83de45006de8c0ff0fd58fd7c1d50a56600111a87f166e0d
HORODATAGE   : 2026-10-11T14:43:09Z
```
