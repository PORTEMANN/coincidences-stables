# CARTE MCS-02 — Invariants spectraux ASH à travers signaux vivants et non vivants

**Statut** : CANDIDAT — NON SCELLÉ — Jalon 1 (rédaction, aucun calcul)
**Domaines** : A = signaux physiologiques (EEG, ECG, électrophysiologie
cellulaire) ; B = signaux non vivants (vibrations mécaniques).
**Attente honnête** : carte à haut risque d'apophénie. Sa fonction première est
de discipliner la notion de « signature spectrale » : démontrer soit qu'elle est
spécifique, soit qu'elle est générique à tout signal complexe.

---

## 1. Énoncé de la coïncidence candidate

Le corpus (couche ASH) suggère qu'un vecteur d'invariants spectraux prend des
valeurs comparables sur des signaux vivants et non vivants. La carte teste une
version précise et faible de cette idée :

> Le vecteur d'invariants spectraux I = (I1, I2, I3, I4), calculé par un pipeline
> gelé, sépare-t-il les domaines entre eux **moins** que ne le prédisent les
> surrogates à spectre de puissance identique ?

Autrement dit : y a-t-il dans la **structure de phase** (pas dans le spectre de
puissance) une information inter-domaines stable ? Si les surrogates IAAFT
reproduisent le rapprochement, la coïncidence est générique : CS−.

## 2. Lexique gelé (un mot = un objet)

| Mot | Objet opératoire unique |
|-----|--------------------------|
| pipeline ASH | : rééchantillonnage 1000 Hz → fenêtres de 10 s sans recouvrement → retrait de tendance linéaire → Welch (segments 4 s, recouvrement 50 %) |
| I1 (pente 1/f) | pente β de la régression log-log de la DSP sur 1–40 Hz |
| I2 (entropie spectrale) | entropie de Shannon de la DSP normalisée sur 1–40 Hz, divisée par log(nb de bins) |
| I3 (harmonicité) | fraction de l'énergie des pics (prominence > 3σ) dont les rapports de fréquences sont entiers à ±2 % près |
| I4 (couplage phase-amplitude) | indice de modulation (Tort) entre phase 4–8 Hz et amplitude 30–45 Hz |
| domaine | l'un des quatre corpus ci-dessous |
| m (mesure) | séparation inter-domaines : m = −d_W(moyennes de domaines), où d_W est la distance de Wasserstein-2 moyenne entre paires de domaines dans l'espace I standardisé. m grand = domaines proches |

## 3. Dictionnaire τ

    τ : signal brut  ↦  pipeline ASH  ↦  I = (I1, I2, I3, I4) ∈ ℝ⁴  ↦  distance inter-domaines

τ inclut le pipeline. Toute modification du pipeline après gel = nouvelle carte.

## 4. Données et provenance (gelées au jalon 3)

- **EEG** : repos yeux ouverts, OpenNeuro ds003778 (ou équivalent déclaré au gel),
  20 sujets, 3 fenêtres par sujet, canal Cz et O1.
- **ECG** : PhysioNet MIT-BIH Normal Sinus Rhythm, 18 enregistrements, dérivée II.
- **Électrophysiologie cellulaire** : Allen Cell Types Database, potentiels de
  membrane de cellules humaines (sous-ensemble déclaré au gel).
- **Vibration** : Case Western Reserve University Bearing Data, charge 1 HP,
  accéléromètre DE.
- 60 fenêtres par domaine, tirées selon une graine déclarée **au gel** (la graine
  de tirage fait partie du manifeste scellé, pas de cette carte).

## 5. Groupe de déformations légitimes 𝒢

| g | Déformation | Ce qu'elle teste |
|---|-------------|-------------------|
| g1 | surrogates IAAFT (100 par fenêtre) | la coïncidence tient-elle à la phase ou au spectre ? |
| g2 | renversement temporel | irréversibilité : la coïncidence serait-elle un artéfact de stationnarité ? |
| g3 | EEG canal Cz → O1 | dépendance au site d'électrode |
| g4 | vibration charge 1 HP → 3 HP | dépendance au régime mécanique |
| g5 | fenêtres 10 s → 4 s | dépendance à la résolution spectrale |
| g6 | retrait de la bande 4–8 Hz de I4 | la coïncidence serait-elle portée par un seul invariant ? |
| g7 | permutation des sujets EEG entre sessions | structure inter-individuelle |
| g8 | rééchantillonnage 1000 Hz → 500 Hz | dépendance à la fréquence d'échantillonnage |

## 6. Modèle nul

- **N1 (surrogates IAAFT)** : pour chaque fenêtre, 100 surrogates à spectre de
  puissance conservé et phase randomisée ; distribution de m sur surrogates →
  μ_null, u. **C'est le nul central** : si la coïncidence est une propriété du
  spectre, elle doit y survivre ; si elle est une propriété de la phase, elle
  doit y mourir — et la carte exige qu'elle y meure pour les surrogates tout en
  vivant pour les données (double contrainte, voir §9).
- **N2 (signaux synthétiques)** : bruit filtré de même DSP moyenne par domaine,
  sans structure de phase.
- **N3 (mélange)** : fenêtres réassignées à des domaines aléatoires (permutation
  des étiquettes de domaine) → m doit s'effondrer.

## 7. Contrôles positifs (sabotages obligatoires)

| c | Sabotage | Attendu si le test a du pouvoir |
|---|----------|----------------------------------|
| c1 | mélanger les étiquettes de domaine | m s'effondre vers N3 |
| c2 | injecter dans l'EEG un couplage phase-amplitude artificiel connu | I4 doit le détecter (sinon I4 est aveugle) |
| c3 | remplacer l'ECG par un métronome synthétique à 1 Hz + bruit | I3 doit le classer hors-cluster (démonstration que le test peut distinguer la trivialité) |

c1 ou c2 muet → **CS0**.

## 8. Statistique et seuils (gelés)

- z_g = (m_g − μ_null,g) / u_g sous N1, pour chaque g ∈ 𝒢.
- Σ = min sur {g2…g8} des z_g. **g1 (IAAFT) est exclu du minimum** car il porte
  la double contrainte (voir §9) ; il est rapporté séparément.
- Regard ailleurs : 4 invariants choisis parmi 11 candidats déclarés (pente,
  entropie, harmonicité, PAC, Hjorth ×3, exposant de Hurst, largeur de bande
  dominante, SEF95, ratio θ/β). Seuil CS+ relevé de 3 à 3,3 (correction gelée
  pour 11 familles examinées : méthode Bonferroni ramollie, log(11)/log(2) ≈ 3,46
  → ajustement fixé à 3,3 par convention déclarée ici).

## 9. Critères de verdict

La carte exige une **double contrainte** :

- (a) Σ ≥ 3,3 sur les données réelles ;
- (b) sous g1 (IAAFT), m_surrogate s'effondre : z_IAAFT ≤ −2 (la coïncidence
  meurt avec la phase).

| Issue | Verdict |
|-------|---------|
| (a) et (b) | CS+ : structure de phase inter-domaines stable |
| (a) sans (b) | CS− déguisé → verdict **CS−** : la coïncidence était spectrale, donc générique |
| (b) sans (a) | CSp |
| ni (a) ni (b) | CS− |
| Σ ≤ −2 sur données réelles | CSi |
| c1 ou c2 muet | CS0 |

## 10. Regard ailleurs (déclaration préalable)

Invariants candidats examinés : 11 (liste en §8). Pipelines examinés : 1
(celui-ci). Jeux de données écartés avant rédaction : 2 (EEG mouvement — trop
d'artefacts ; vibration aéronautique — non public).

## 11. Critères d'arrêt

- Verdict « (a) sans (b) » : publication immédiate comme démonstration que la
  couche ASH mesurait le spectre, pas la phase. Fermeture de la couche ASH
  dans sa forme actuelle (fermer, ne pas ajouter).
- CS0 : une seule refonte du pipeline autorisée (MCS-02b).
- CS+ : publication avec distributions nulles complètes ; aucune interprétation
  ontologique (manifeste §8).

## 12. Scellement (jalon 3)

```
SHA256_CARTE : 0aa840f23ca4516ae5f76342be950694d0dcd4c204e02ea7ad0c8b1f08fa167a
HORODATAGE   : 2026-10-09T13:31:46Z
```
