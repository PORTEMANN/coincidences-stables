# coincidences-stables

**MCS — Machine à Coïncidences Stables / Machine des Points Fixes inter-domaines.**

Un opérateur de verdict sur des morphismes : une correspondance déclarée
τ : A → B entre deux domaines indépendants survit-elle aux déformations qui
devraient la détruire si elle n'était qu'un artefact de langage ?

Ni une ontologie, ni un instrument de mesure : une grammaire de la preuve
admissible pour correspondances inter-domaines.

## Doctrine

- **fermer, ne pas ajouter** — une carte morte est une frontière mesurée ;
- **un mot = un objet** — chaque terme a une définition opératoire unique, gelée ;
- **échecs publiés** — les verdicts CS− ont la même valeur que CS+ (B3-FAIL) ;
- **contrôles positifs obligatoires** — un sabotage qui ne casse rien rend le
  banc aveugle : verdict **CS0**, quel que soit le score.

## Opérateur

    z_g(τ) = ( m_g(τ) − μ_null,g ) / u_g        pour chaque déformation g ∈ 𝒢
    Σ(τ)   = min_g z_g(τ)                        maillon le plus faible, jamais de moyenne

Verdicts : **CS+** (Σ ≥ seuil gelé) · **CSp** (2 ≤ Σ < seuil) · **CS−** (−2 < Σ < 2)
· **CSi** (Σ ≤ −2) · **CS0** (contrôles muets : test impuissant).

## Statut : JALON 4 ACCOMPLI — les trois cartes ont été exécutées sur données réelles

Verdicts publiés (exécution unique par carte, journal chaîné de 20 records) :

| Carte | Verdict | Σ | Lecture |
|-------|---------|---|---------|
| MCS-01 | **CSi** | −6,93 | k(Z) anti-alignée avec la vallée β dans les 9 configurations ; les données miroir Z↔N l'ajustent à +45,6 u |
| MCS-02 | **CSi** | −25,10 | la structure de phase sépare les domaines plus que le spectre seul (inversion stable, 8 configurations) ; séparation essentiellement spectrale, générique |
| MCS-03 | **CS0** | −1,95 (suspendu) | test impuissant sur l'invariant C ; cécité démontrée locale à cette statistique |

Voir `RAPPORT-JALON-4.md`, le journal chaîné `journal/JALON-4-OUVERTURE.jsonl`
et `resultats/`. Empreinte globale du scellement jalon 3 (2026-10-09) :

```
6f7d03433c055f30088e7863d361fd662c57b41f1aee4b3cd4743a65621168b1
```

Le présent dépôt, publié avant toute ouverture, sert d'horodatage externe :
les cartes, les seuils et le code sont publiquement datés avant le premier
chiffre réel. Voir `scellement/ACTE-DE-SCELLEMENT-J3.md`.

## Moteur v2.0 (successeur, scellé)

Le jalon 4 a appris deux leçons au moteur, publiées dans le journal :

- **règle d'impuissance robuste au signe** : la puissance d'un contrôle est
  |effet| en unités u_null ; la direction (conforme/inverse) est un diagnostic
  publié séparément — la convention signée de la v0.1 déclarait aveugles des
  bancs mesurant ±53 u et ±97 u (MCS-01/MCS-02) ;
- **puissance démontrée avant gel** : toute carte jointe une preuve synthétique
  de résolution de ses contrôles (leçon MCS-03, cécité structurelle).

`manifeste/MANIFESTE-MCS-v2.0.md` · `code/mcs_score_v2.py` · validation
synthétique 6/6 (dont la régression du jalon 4 sur chiffres enregistrés :
le moteur v2 reproduit CSi, CSi, CS0) · `scellement/SCCELLEMENT-V2.json`
(empreinte globale `d23216f5…`, chaîne liée à la tête du journal jalon 4).
La v0.1 reste gelée ; MCS-01/02/03 restent fermées.

## Cartes scellées (v0.1, closes au jalon 4)

| Carte | Objet | Échelle | Attente honnête |
|-------|-------|---------|------------------|
| MCS-01 | k(Z) contre la vallée de stabilité β | micro (nucléaire) | à fermer |
| MCS-02 | invariants spectraux ASH inter-signaux | méso (physiologie/vibration) | à discipliner |
| MCS-03 | KO-6 / triples spectraux ↔ 2I ⊂ E₈ | formelle (hors échelle) | calibration négative |

## Structure

```
manifeste/    MANIFESTE-MCS-v0.1.md (scellé) + MANIFESTE-MCS-v2.0.md (scellé)
cartes/       MCS-01, MCS-02, MCS-03 (scellées)
code/         mcs_score.py (opérateur Σ, verdicts, journal chaîné)
              ash_invariants.py (pipeline ASH gelé)
              prng_chacha.py (ChaCha20-IETF, graine publique jalon 4)
              mcs01_runner.py, mcs02_runner.py, mcs03_runner.py (exécutions uniques)
              jalon4_acquisition_mcs02.py (tirage et acquisition publiés)
              mcs_score_v2.py (moteur v2.0, scellé séparément)
nulls/        surrogates.py (FT, IAAFT, permutation, familles de lois)
              positive_controls.py (sabotages, calibration)
validation/   validation_synthetique.py (5 scénarios à vérité connue)
              validation_synthetique_v2.py (v2 : 6/6, régression jalon 4)
              verifier_scellement.py (revérification indépendante du gel)
              rapport_synthetique.md, journal_synthetique.jsonl
scellement/   geler_jalon3.py, SCCELLEMENT-J3.json, ACTE, journal chaîné
              + geler_v2.py, SCCELLEMENT-V2.json, ACTE-DE-SCELLEMENT-V2.md
journal/      JALON-4-OUVERTURE.jsonl (20 records chaînés)
resultats/    mcs01/mcs02/mcs03_resultats.json (verdicts et mesures complets)
donnees/      manifestes et métadonnées (les brutes ~700 Mo restent chez les
              sources publiques ; leurs empreintes sont au journal)
```

## Revérifier

```bash
python3 validation/verifier_scellement.py     # intégrité du gel
python3 validation/validation_synthetique.py  # le banc sur vérité connue
```

Le jalon 2 est validé si : correspondance plantée → CS+, artefacts → CS−,
banc volontairement aveugle → CS0 (même avec Σ = 5).

## Jalons

1. ✅ manifeste + cartes, sans code — 2. ✅ moteur validé sur synthétique —
3. ✅ gel (ce dépôt) — 4. ✅ ouverture sur données réelles : **CSi, CSi, CS0**
(exécution unique par carte, verdicts et échecs publiés — voir
`RAPPORT-JALON-4.md`).

## Licences

- Code : MIT (`LICENSE-CODE`)
- Textes (manifeste, cartes, actes, rapports) : CC-BY-4.0 (`LICENSE-TEXTES`)
