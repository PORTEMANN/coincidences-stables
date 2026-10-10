# MANIFESTE MCS — v2.0 (CANDIDAT, NON SCELLÉ)

**Machine à Coïncidences Stables — moteur v2.0**
Date de rédaction : 2026-10-09 (soir)
Statut : JALON 1 v2.0 — successeur du manifeste v0.1 (gelé, jalon 3 accompli,
jalon 4 publié). Ce document NE rouvre aucune carte fermée.

---

## 0. Succession

La v0.1 reste ce qu'elle est : gelée le 2026-10-09T13:31:46Z, exécutée au
jalon 4, trois cartes closes (MCS-01 : CSi ; MCS-02 : CSi ; MCS-03 : CS0).
Journal de preuve : `journal/JALON-4-OUVERTURE.jsonl` (20 records chaînés,
tête `9171759e…`). La v2.0 est un **moteur successeur** : elle change la règle
d'impuissance et ajoute une exigence de puissance avant gel, rien d'autre.
Toute carte écrite sous v2.0 est une carte nouvelle (nouveau numéro, nouveau
regard ailleurs).

## 1. Ce que le jalon 4 a appris au moteur (motivations, records cités)

### 1.1 — La règle d'impuissance doit être robuste au signe

En v0.1, la règle (§3) — « un contrôle positif qui ne casse pas la
correspondance rend le test aveugle » — était implémentée comme un effet
**signé** ≥ +2 u. Le jalon 4 a produit deux cas où cette convention signée
déclarait aveugle un banc qui mesurait un effet énorme :

- MCS-01, contrôle c1 (Z↔N) : effet = **−52,6 u** — la candidate, déjà
  détruite (z = −6,9), s'*alignait* sur les données miroir (+45,6 u). Le banc
  mesurait ±53 u (c2 : +53,0 u). [records RESULTAT_MCS01, LECTURE_MCS01]
- MCS-02, contrôle c1 (mélange d'étiquettes) : effet = **−96,9 u** —
  l'effondrement *vers N3* était exact (m_c1 = −0,3624 vs moyenne N3 =
  −0,3583, à 0,05 u), mais de signe inverse à la convention car la candidate
  partait inversée. [records RESULTAT_MCS02, LECTURE_MCS02]

Les deux lectures opérateur (publiées, consignées) ont déclaré CSi matériel ;
le moteur brut rendait CS0. Cette divergence moteur/opérateur est un défaut de
conception, pas une doctrine : en v2.0, **la puissance d'un contrôle est
|effet| en unités u_null ; un contrôle est muet ssi |effet| < 2 u**. La
direction (conforme / inverse à l'attente déclarée dans la carte) est un
**diagnostic publié séparément**, jamais confondu avec la puissance.

### 1.2 — La puissance se démontre avant le gel

MCS-03 a montré une cécité **structurelle** : la statistique (corrélation de
Spearman sur 15 paires) ne pouvait pas résoudre un sabotage point-par-point
(c1 : +0,04 u ; c2 : −0,44 u ; c3 : +0,62 u — tous |effet| < 2 u). Le verdict
CS0 était matériellement correct, et la cécité a été démontrée locale à cette
statistique [record LECTURE_MCS03]. En v2.0 : **toute carte jointe une
démonstration de puissance sur synthétique** — la statistique choisie doit
résoudre chacun de ses contrôles à |effet| ≥ 2 u sur données synthétiques à
vérité connue, avant le gel ; la démonstration est hachée dans l'acte de
scellement. Une carte sans démonstration de puissance ne peut pas être
scellée. C'est une règle de rédaction (jalon 1), non amendable autrement que
par une v3.0.

### 1.3 — Ce qui a tenu (inchangé)

Σ = min z_g (maillon le plus faible, moyenne interdite) ; taxonomie
CS+/CSp/CS−/CSi/CS0 ; double contrainte pour les cartes spectrales (vivre sur
données réelles, mourir sous IAAFT) ; journal chaîné SHA-256 ; exécution
unique avec runner haché avant exécution ; PRNG à graine publique dérivée
(ChaCha20-IETF, RFC 8439) ; publication symétrique des échecs ; séparation
carte/banc ; « un mot = un objet » ; « fermer, ne pas ajouter ».

## 2. Opérateur (inchangé)

    z_g(τ) = ( m_g(τ) − μ_null,g ) / u_g
    Σ(τ)   = min_{g ∈ 𝒢} z_g(τ)

## 3. Taxonomie des verdicts (v2.0)

| Condition | Verdict | Sens |
|-----------|---------|------|
| Σ ≥ seuil gelé | **CS+** | coïncidence stable |
| 2 ≤ Σ < seuil | **CSp** | stabilité locale |
| −2 < Σ < 2 | **CS−** | artefact probable ; B3-FAIL obligatoire |
| Σ ≤ −2 | **CSi** | inversion stable ; publication prioritaire |
| un contrôle positif avec \|effet\| < 2 u | **CS0** | test impuissant |

Règle d'impuissance v2.0 : un contrôle est aveugle ssi son effet n'atteint pas
2 u_null **en valeur absolue**. La direction est rapportée dans le verdict
(`directions_controles` : conforme / inverse / faible) — une direction inverse
sur un banc puissant est une information sur la candidate (souvent : elle est
inversée), pas une preuve d'aveuglement.

## 4. Constitution v2.0 (non amendable sans changement de version majeure)

Les règles 1–7 de la v0.1 tiennent. Ajout :

8. **Puissance démontrée avant gel.** Chaque carte jointe une démonstration
   synthétique de résolution de ses contrôles à |effet| ≥ 2 u, hachée dans
   l'acte de scellement (règle 1.2).
9. **Diagnostic de direction publié.** Tout verdict publie, pour chaque
   contrôle : effet signé, puissance |effet|, direction (conforme/inverse/
   faible).

## 5. Registre des cartes candidates v2 (jalon 1 à venir — aucune carte rédigée ici)

Matériau déclaré : les dépôts `PORTEMANN/noetic-machine-complete` (archive
canonique P0–P48, registre de frontières REG-FR-1.0) et `PORTEMANN/mvcg`
(contacts ouverts O1–O20 + tiroirs). Les directions suivantes sont des
**propositions de cartes** à rédiger au jalon 1 v2 — aucune n'est écrite ici,
aucun calcul n'a été fait pour elles dans ce chantier :

- **V2-CAND-A — loi harmonique sur le zoo particulaire** (mvcg, tiroir
  LOI-HARMONIQUE : m = m_p·2^{n/12} ; déjà pesée par contact — S+ serrés sur
  leptons et boson Z, P sur quarks moyens/lourds, dettes nommées). Une carte
  MCS la testerait comme correspondance inter-domaines (masses × tempérament
  égal) sous déformations (ancre, sous-ensembles, unités), avec nuls
  structurels — pas comme suite de pesées locales.
- **V2-CAND-B — frontière F17 (agrégation d'essais EEG)** (noetic-machine-
  complete, P44/P47 : illettrisme BCI mesuré, vote réfuté au seuil figé) :
  la frontière est ouverte ; une carte demanderait si l'agrégation dérivée
  survit à ses déformations.
- **V2-CAND-C — loi des bifurcations** (bifurcations/, conjecture catégorie II
  étiquetée) : la dérivabilité décroît avec la complexité pour les
  bifurcations physiques — un objet de carte possible, à frontière mesurée.
- **V2-CAND-D — économie de l'information à la frontière** (M1/M1b :
  l'inversion a survécu à la réplication par proxy de Kolmogorov) : la
  réfutation structurelle est un résultat acquis ; une carte MCS la
  reformulerait comme correspondance (ratio informationnel × distance à la
  frontière) sous déformations.

La ligne KO-6 ↔ E₈ reste **fermée** par MCS-03 (non-testable par l'invariant
C ; aucune refonte sans un invariant nouveau, qui serait une carte nouvelle
avec son propre regard ailleurs).

## 6. Séquence des jalons (v2.0)

- **Jalon 1 v2** : le présent manifeste + rédaction des cartes retenues avec
  leur démonstration de puissance (règle 1.2) — aucun calcul de mesure.
- **Jalon 2 v2** : validation du moteur v2 (fait : `validation/validation_synthetique_v2.py`,
  6/6 conformes, dont la régression du jalon 4 sur chiffres enregistrés).
- **Jalon 3 v2** : gel — SHA-256, chaînage, horodatage.
- **Jalon 4 v2** : ouverture — exécution unique, verdicts publiés quels que
  soient.

## 7. Politique de publication (inchangée)

Carte hashée, code hashé, journal chaîné, distributions nulles, contrôles
(effets signés + puissances + directions), Σ par déformation. Un CS+ publié
sans ses z_g complets est invalide.

## 8. Limites de portée (inchangées, renforcées)

- La MCS ne dit rien sur la conscience, la noétique ou l'ontologie.
- Aucune carte sur des données ayant servi à construire sa correspondance.
- La v2.0 ne rouvre ni MCS-01, ni MCS-02, ni MCS-03 (fermées au jalon 4).
- Elle ne modifie ni mvcg ni la Machine Noétique : opérateur distinct.

## 9. Scellement (à remplir au jalon 3 v2)

```
SHA256_MANIFESTE : a9eb7c44ce7a61063328ba627161161df9d81ee53ce5987c899c188e12098660
SHA256_CODE_V2   : f762bc361fa87ef3115d271cf935101c48c6bf339d68013eccdff39eec338fa6
CHAINE_JOURNAL   : 745d7475bddc0ecbd92cfadd04f4bbaedea74d306911727a3e3dac84ef358c09
HORODATAGE       : 2026-10-10T06:17:08Z
```

---

*Successeur du manifeste v0.1. La v0.1 est close : ses trois cartes ont reçu
leurs verdicts au jalon 4 (CSi, CSi, CS0), publiés.*
