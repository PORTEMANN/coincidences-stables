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

## Statut : GELÉ — jalon 3 accompli, aucune donnée réelle exécutée

Empreinte globale du scellement (2026-10-09) :

```
6f7d03433c055f30088e7863d361fd662c57b41f1aee4b3cd4743a65621168b1
```

Le présent dépôt, publié avant toute ouverture, sert d'horodatage externe :
les cartes, les seuils et le code sont publiquement datés avant le premier
chiffre réel. Voir `scellement/ACTE-DE-SCELLEMENT-J3.md`.

## Cartes scellées

| Carte | Objet | Échelle | Attente honnête |
|-------|-------|---------|------------------|
| MCS-01 | k(Z) contre la vallée de stabilité β | micro (nucléaire) | à fermer |
| MCS-02 | invariants spectraux ASH inter-signaux | méso (physiologie/vibration) | à discipliner |
| MCS-03 | KO-6 / triples spectraux ↔ 2I ⊂ E₈ | formelle (hors échelle) | calibration négative |

## Structure

```
manifeste/    MANIFESTE-MCS-v0.1.md (scellé)
cartes/       MCS-01, MCS-02, MCS-03 (scellées)
code/         mcs_score.py (opérateur Σ, verdicts, journal chaîné)
              ash_invariants.py (pipeline ASH gelé)
nulls/        surrogates.py (FT, IAAFT, permutation, familles de lois)
              positive_controls.py (sabotages, calibration)
validation/   validation_synthetique.py (5 scénarios à vérité connue)
              verifier_scellement.py (revérification indépendante du gel)
              rapport_synthetique.md, journal_synthetique.jsonl
scellement/   geler_jalon3.py, SCCELLEMENT-J3.json, ACTE, journal chaîné
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
3. ✅ gel (ce dépôt) — 4. ⬜ ouverture sur données réelles (exécution unique,
verdicts publiés quels qu'ils soient).

## Licences

- Code : MIT (`LICENSE-CODE`)
- Textes (manifeste, cartes, actes, rapports) : CC-BY-4.0 (`LICENSE-TEXTES`)
