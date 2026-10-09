# ACTE DE SCELLEMENT — MCS, jalon 3

Horodatage UTC : `2026-10-09T13:31:46Z`

**Statut : GELÉ. Aucune donnée réelle n'a été exécutée.**

Convention : chaque empreinte est calculée sur le contenu pré-gel
(bloc de scellement à null) ; le bloc nul original est conservé dans
`SCCELLEMENT-J3.json`, ce qui permet de revérifier chaque empreinte
à l'octet près (`validation/verifier_scellement.py`).

## Empreintes SHA-256 (pré-gel)

| Fichier | Empreinte |
|---------|-----------|
| `cartes/MCS-01-kZ-AME.md` | `45185f63459fcf9e580a0a86725110a9bdf462aa1754b56321259a73ca34c0e1` |
| `cartes/MCS-02-ASH-signaux.md` | `0aa840f23ca4516ae5f76342be950694d0dcd4c204e02ea7ad0c8b1f08fa167a` |
| `cartes/MCS-03-KO6-E8.md` | `e5b082c87c996842c707e06a66d98008c62c9dfc114ee33a35ff5da7dc0a1f70` |
| `manifeste/MANIFESTE-MCS-v0.1.md` | `3c5d50bec884571fb41b6c4a5fb3739b8b70fb7458f3651e3297a3ae3e1fce78` |
| `code/mcs_score.py` | `aa8e1b87fc9cfa5159672b8117a5f1cc5384f5a50f75657869374956f0bf6d08` |
| `code/ash_invariants.py` | `0098dd431534fbaee4725d6dbc791fd8d87f951398a2c41b24be43551b42811c` |
| `nulls/surrogates.py` | `86d588064e0d5f5a62b160f3ccf1fbf235e85c77d7a1a3550e92ce1e2781bb42` |
| `nulls/positive_controls.py` | `6f14e2b09f5a3e2cd4325047e0acbb07eef190081c5d5c2dfc977c576310f41a` |
| `validation/validation_synthetique.py` | `149f840d0e1593ee005207e82ab2ebbee4203f00873c03c3e294f42432a41133` |

| **Paquet code** | `892cd28ee5aad1f31dae866abed9d61dee06c4dc2737e8c813acf426f96db0a9` |
| **Tête du journal chaîné** | `e611625fafa6e760358371d4c33f6021f0dd42bec5d15a28a64a490f10b9d22f` |
| **EMPREINTE GLOBALE** | `6f7d03433c055f30088e7863d361fd662c57b41f1aee4b3cd4743a65621168b1` |

## Horodatage externe (à faire)

L'acte est scellé en interne (chaîne SHA-256). Pour un tiers de
confiance, horodater l'empreinte globale :

```bash
pip install opentimestamps-client
echo 6f7d03433c055f30088e7863d361fd662c57b41f1aee4b3cd4743a65621168b1 > empreinte_globale.txt
ots stamp empreinte_globale.txt
```

## Règle de suite

Toute modification d'un fichier scellé = nouvelle version
(v0.2), nouveau scellement, nouveau regard ailleurs déclaré.
Le jalon 4 (ouverture sur données réelles) ne peut commencer
qu'avec `verifier_scellement.py` au vert.
