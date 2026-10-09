"""geler_jalon3.py — Jalon 3 : le gel.

Convention de scellement (gelee ici, non amendable sans version majeure) :

  L'empreinte SHA-256 d'un document scelle est calculee sur son contenu
  PRE-GEL, c'est-a-dire avec son bloc de scellement a null. Le bloc est
  ensuite rempli ; le JSON d'acte conserve le bloc nul original, ce qui
  permet a verifier_scellement.py de reconstruire le contenu pre-gel a
  l'octet pres et de reverifier chaque empreinte.

Ordre des operations :
  1. empreintes pre-gel des cartes, du code, du manifeste ;
  2. journal chaine dedie au scellement (genese GENESIS-MCS-J3-SCELLEMENT) ;
  3. ecriture des blocs de scellement (cartes puis manifeste) ;
  4. acte de scellement (JSON + Markdown) ;
  5. aucune donnee reelle n'a ete executee — c'est le sens du gel.

L'horodatage cryptographique externe (OpenTimestamps) reste a faire hors
bac a sable : l'empreinte globale est ecrite dans l'acte pour cela.
"""
from __future__ import annotations

import hashlib
import json
import os
import re
import sys
from datetime import datetime, timezone

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(RACINE, "code"))
import mcs_score as mcs

GENESE = "GENESIS-MCS-J3-SCELLEMENT"
CARTES = ["cartes/MCS-01-kZ-AME.md",
          "cartes/MCS-02-ASH-signaux.md",
          "cartes/MCS-03-KO6-E8.md"]
CODE = ["code/mcs_score.py",
        "code/ash_invariants.py",
        "nulls/surrogates.py",
        "nulls/positive_controls.py",
        "validation/validation_synthetique.py"]
MANIFESTE = "manifeste/MANIFESTE-MCS-v0.1.md"
JSON_ACTE = os.path.join(RACINE, "scellement", "SCCELLEMENT-J3.json")
MD_ACTE = os.path.join(RACINE, "scellement", "ACTE-DE-SCELLEMENT-J3.md")
JOURNAL = os.path.join(RACINE, "scellement", "journal_scellement.jsonl")

BLOC_RE = re.compile(r"```\n.*?```", re.DOTALL)


def sha256_fichier(chemin: str) -> str:
    with open(chemin, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()


def dernier_bloc(contenu: str):
    blocs = list(BLOC_RE.finditer(contenu))
    if not blocs:
        raise ValueError("aucun bloc de scellement (fenced) trouve")
    return blocs[-1]


def remplir_bloc(bloc_nul: str, valeurs: dict) -> str:
    lignes = bloc_nul.split("\n")
    out = []
    for ln in lignes:
        m = re.match(r"^([A-Z0-9_\-]+)(\s*:\s*)(.*)$", ln)
        if m and m.group(1) in valeurs:
            out.append(m.group(1) + m.group(2) + valeurs[m.group(1)])
        else:
            out.append(ln)
    return "\n".join(out)


def main() -> int:
    ts = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    if os.path.exists(JSON_ACTE):
        print("REFUS : un acte de scellement existe deja. "
              "Toute modification = nouvelle version (fermer, ne pas ajouter).")
        return 1

    # 1. Empreintes pre-gel ------------------------------------------------
    pre = {}
    blocs_nuls = {}
    for rel in CARTES + [MANIFESTE]:
        chemin = os.path.join(RACINE, rel)
        with open(chemin, encoding="utf-8") as f:
            contenu = f.read()
        bloc = dernier_bloc(contenu)
        blocs_nuls[rel] = bloc.group(0)
        pre[rel] = hashlib.sha256(contenu.encode("utf-8")).hexdigest()
    for rel in CODE:
        pre[rel] = sha256_fichier(os.path.join(RACINE, rel))
    paquet_code = hashlib.sha256(json.dumps(
        {rel: pre[rel] for rel in CODE},
        sort_keys=True, separators=(",", ":")).encode("utf-8")).hexdigest()

    # 2. Journal chaine du scellement --------------------------------------
    if os.path.exists(JOURNAL):
        os.remove(JOURNAL)
    journal = mcs.JournalChaine(JOURNAL, genesis=GENESE)
    for rel in CARTES:
        journal.ajouter({"type": "scellement_carte", "fichier": rel,
                         "sha256_pre_gel": pre[rel], "horodatage": ts})
    journal.ajouter({"type": "scellement_code", "fichiers": CODE,
                     "sha256_paquet": paquet_code, "horodatage": ts})
    journal.ajouter({"type": "scellement_manifeste", "fichier": MANIFESTE,
                     "sha256_pre_gel": pre[MANIFESTE], "horodatage": ts})
    tete = journal.prev_hash

    empreinte_globale = hashlib.sha256(json.dumps({
        "cartes": {rel: pre[rel] for rel in CARTES},
        "code_paquet": paquet_code,
        "manifeste": pre[MANIFESTE],
        "chaine_journal": tete,
        "horodatage": ts,
    }, sort_keys=True, separators=(",", ":")).encode("utf-8")).hexdigest()

    # 3. Ecriture des blocs -------------------------------------------------
    for rel in CARTES:
        chemin = os.path.join(RACINE, rel)
        with open(chemin, encoding="utf-8") as f:
            contenu = f.read()
        bloc = dernier_bloc(contenu)
        nouveau = remplir_bloc(blocs_nuls[rel], {
            "SHA256_CARTE": pre[rel], "HORODATAGE": ts})
        with open(chemin, "w", encoding="utf-8") as f:
            f.write(contenu[:bloc.start()] + nouveau + contenu[bloc.end():])

    chemin_m = os.path.join(RACINE, MANIFESTE)
    with open(chemin_m, encoding="utf-8") as f:
        contenu_m = f.read()
    bloc_m = dernier_bloc(contenu_m)
    nouveau_m = remplir_bloc(blocs_nuls[MANIFESTE], {
        "SHA256_MANIFESTE": pre[MANIFESTE],
        "SHA256_MCS-01": pre[CARTES[0]],
        "SHA256_MCS-02": pre[CARTES[1]],
        "SHA256_MCS-03": pre[CARTES[2]],
        "SHA256_CODE": paquet_code,
        "CHAINE_JOURNAL": tete,
        "HORODATAGE": ts,
    })
    with open(chemin_m, "w", encoding="utf-8") as f:
        f.write(contenu_m[:bloc_m.start()] + nouveau_m + contenu_m[bloc_m.end():])

    # 4. Actes --------------------------------------------------------------
    acte = {
        "acte": "SCCELLEMENT MCS — JALON 3",
        "horodatage_utc": ts,
        "convention": "sha256 calculee sur le contenu PRE-GEL (bloc a null) ; "
                      "le bloc nul original est conserve ici pour verification "
                      "octet par octet",
        "genese_journal": GENESE,
        "fichiers": {rel: {"sha256_pre_gel": pre[rel],
                           "bloc_nul_original": blocs_nuls.get(rel)}
                     for rel in CARTES + [MANIFESTE]},
        "code": {rel: pre[rel] for rel in CODE},
        "sha256_paquet_code": paquet_code,
        "chaine_journal_tete": tete,
        "empreinte_globale": empreinte_globale,
        "horodatage_externe": "A FAIRE : opentimestamps sur empreinte_globale "
                              "(ots stamp) — hors bac a sable",
        "statut": "GELE — aucune donnee reelle executee",
    }
    with open(JSON_ACTE, "w", encoding="utf-8") as f:
        json.dump(acte, f, ensure_ascii=False, indent=2)

    lignes = [
        "# ACTE DE SCELLEMENT — MCS, jalon 3", "",
        f"Horodatage UTC : `{ts}`", "",
        "**Statut : GELÉ. Aucune donnée réelle n'a été exécutée.**", "",
        "Convention : chaque empreinte est calculée sur le contenu pré-gel",
        "(bloc de scellement à null) ; le bloc nul original est conservé dans",
        "`SCCELLEMENT-J3.json`, ce qui permet de revérifier chaque empreinte",
        "à l'octet près (`validation/verifier_scellement.py`).", "",
        "## Empreintes SHA-256 (pré-gel)", "",
        "| Fichier | Empreinte |", "|---------|-----------|",
    ]
    for rel in CARTES + [MANIFESTE] + CODE:
        lignes.append(f"| `{rel}` | `{pre[rel]}` |")
    lignes += ["",
               f"| **Paquet code** | `{paquet_code}` |",
               f"| **Tête du journal chaîné** | `{tete}` |",
               f"| **EMPREINTE GLOBALE** | `{empreinte_globale}` |", "",
               "## Horodatage externe (à faire)", "",
               "L'acte est scellé en interne (chaîne SHA-256). Pour un tiers de",
               "confiance, horodater l'empreinte globale :", "",
               "```bash",
               "pip install opentimestamps-client",
               f"echo {empreinte_globale} > empreinte_globale.txt",
               "ots stamp empreinte_globale.txt", "```", "",
               "## Règle de suite", "",
               "Toute modification d'un fichier scellé = nouvelle version",
               "(v0.2), nouveau scellement, nouveau regard ailleurs déclaré.",
               "Le jalon 4 (ouverture sur données réelles) ne peut commencer",
               "qu'avec `verifier_scellement.py` au vert.", ""]
    with open(MD_ACTE, "w", encoding="utf-8") as f:
        f.write("\n".join(lignes))

    print(f"gel effectue — {ts}")
    print(f"empreinte globale : {empreinte_globale}")
    print(f"tete du journal   : {tete}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
