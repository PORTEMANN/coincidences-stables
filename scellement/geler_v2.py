"""geler_v2.py — Scellement du moteur MCS v2.0 (jalon 3 v2).

Convention identique au jalon 3 (geler_jalon3.py) : empreinte SHA-256 sur le
contenu PRE-GEL (bloc de scellement a null), bloc nul conserve dans l'acte,
journal chaine SHA-256. Le premier record du journal v2 lie la tete du
journal JALON-4 (9171759e...) — la v2.0 succede a une campagne close.

Scelle : manifeste v2.0, code v2 (moteur + validation synthetique + son
journal). Aucune carte n'est scellee ici : les cartes v2 seront redigees au
jalon 1 v2 avec leur demonstration de puissance (regle 1.2 du manifeste).
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
import mcs_score as mcs  # noqa: E402  (JournalChaine — inchange en v2)

GENESE = "GENESIS-MCS-V2-SCELLEMENT"
TETE_J4 = "9171759e5a344576179b2b7dac8772837ec5a9a8611344a88749a9836918ffcd"
MANIFESTE = "manifeste/MANIFESTE-MCS-v2.0.md"
CODE = ["code/mcs_score_v2.py",
        "validation/validation_synthetique_v2.py",
        "validation/journal_synthetique_v2.jsonl"]
JSON_ACTE = os.path.join(RACINE, "scellement", "SCCELLEMENT-V2.json")
MD_ACTE = os.path.join(RACINE, "scellement", "ACTE-DE-SCELLEMENT-V2.md")
JOURNAL = os.path.join(RACINE, "scellement", "journal_scellement_v2.jsonl")

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
        print("REFUS : un acte de scellement v2 existe deja.")
        return 1

    # 1. Empreintes pre-gel
    pre = {}
    blocs_nuls = {}
    chemin = os.path.join(RACINE, MANIFESTE)
    with open(chemin, encoding="utf-8") as f:
        contenu = f.read()
    bloc = dernier_bloc(contenu)
    blocs_nuls[MANIFESTE] = bloc.group(0)
    pre[MANIFESTE] = hashlib.sha256(contenu.encode("utf-8")).hexdigest()
    for rel in CODE:
        pre[rel] = sha256_fichier(os.path.join(RACINE, rel))
    paquet_code = hashlib.sha256(json.dumps(
        {rel: pre[rel] for rel in CODE},
        sort_keys=True, separators=(",", ":")).encode("utf-8")).hexdigest()

    # 2. Journal chaine du scellement v2 (lie a la tete J4)
    if os.path.exists(JOURNAL):
        os.remove(JOURNAL)
    journal = mcs.JournalChaine(JOURNAL, genesis=GENESE)
    journal.ajouter({"type": "genese_v2", "horodatage": ts,
                     "chainon_precedent_jalon4": TETE_J4,
                     "note": "le moteur v2.0 succede a la campagne v0.1 close au jalon 4"})
    journal.ajouter({"type": "scellement_code_v2", "fichiers": CODE,
                     "sha256_paquet": paquet_code, "horodatage": ts})
    journal.ajouter({"type": "scellement_manifeste_v2", "fichier": MANIFESTE,
                     "sha256_pre_gel": pre[MANIFESTE], "horodatage": ts})
    tete = journal.prev_hash

    empreinte_globale = hashlib.sha256(json.dumps({
        "manifeste_v2": pre[MANIFESTE],
        "code_v2_paquet": paquet_code,
        "chaine_journal": tete,
        "chainon_jalon4": TETE_J4,
        "horodatage": ts,
    }, sort_keys=True, separators=(",", ":")).encode("utf-8")).hexdigest()

    # 3. Bloc de scellement du manifeste
    nouveau_m = remplir_bloc(blocs_nuls[MANIFESTE], {
        "SHA256_MANIFESTE": pre[MANIFESTE],
        "SHA256_CODE_V2": paquet_code,
        "CHAINE_JOURNAL": tete,
        "HORODATAGE": ts,
    })
    with open(chemin, "w", encoding="utf-8") as f:
        f.write(contenu[:bloc.start()] + nouveau_m + contenu[bloc.end():])

    # 4. Actes
    acte = {
        "acte": "SCCELLEMENT MCS — moteur v2.0 (jalon 3 v2)",
        "horodatage_utc": ts,
        "convention": "sha256 calculee sur le contenu PRE-GEL (bloc a null) ; "
                      "le bloc nul original est conserve ici pour verification "
                      "octet par octet (meme convention que le jalon 3)",
        "genese_journal": GENESE,
        "chainon_precedent_jalon4": TETE_J4,
        "fichiers": {MANIFESTE: {"sha256_pre_gel": pre[MANIFESTE],
                                 "bloc_nul_original": blocs_nuls[MANIFESTE]}},
        "code": {rel: pre[rel] for rel in CODE},
        "sha256_paquet_code": paquet_code,
        "chaine_journal_tete": tete,
        "empreinte_globale": empreinte_globale,
        "statut": "GELE — moteur v2.0 ; aucune carte v2 n'existe encore",
    }
    with open(JSON_ACTE, "w", encoding="utf-8") as f:
        json.dump(acte, f, ensure_ascii=False, indent=2)

    lignes = [
        "# ACTE DE SCELLEMENT — MCS moteur v2.0", "",
        f"Horodatage UTC : `{ts}`", "",
        "**Statut : GELÉ. Moteur v2.0 ; aucune carte v2 n'existe encore.**", "",
        f"Chaînon précédent (tête du journal jalon 4) : `{TETE_J4}`", "",
        "## Empreintes SHA-256 (pré-gel)", "",
        "| Fichier | Empreinte |", "|---------|-----------|",
    ]
    for rel in [MANIFESTE] + CODE:
        lignes.append(f"| `{rel}` | `{pre[rel]}` |")
    lignes += ["",
               f"Paquet code : `{paquet_code}`",
               f"Tête du journal de scellement : `{tete}`",
               f"Empreinte globale v2 : `{empreinte_globale}`", ""]
    with open(MD_ACTE, "w", encoding="utf-8") as f:
        f.write("\n".join(lignes))

    print("Empreinte globale v2 :", empreinte_globale)
    print("Actes :", JSON_ACTE, MD_ACTE)
    return 0


if __name__ == "__main__":
    sys.exit(main())
