"""geler_mcs08.py — Gel de la carte MCS-08 (jalon 3 v2, carte unique).

Convention identique a geler_cartes_v2.py : empreinte SHA-256 sur le contenu
PRE-GEL (bloc a null), bloc nul conserve dans l'acte, journal chaine lie a la
tete du journal de gel des cartes v2 (d53b0c23...). Demonstration de puissance
(regle 1.2) hachee dans l'acte.
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

GENESE = "GENESIS-MCS-V2-GEL-MCS08"
TETE_GEL_CARTES = "d53b0c23e8ee25feb8113fad9b06f6f5eb55512ebd819a6629295b8d0f1e0b68"
CARTE = "cartes/v2/MCS-08-benford-codata.md"
DEMO = ["validation/demonstration_puissance_mcs08.py",
        "validation/journal_puissance_mcs08.jsonl"]
JSON_ACTE = os.path.join(RACINE, "scellement", "GEL-MCS08.json")
MD_ACTE = os.path.join(RACINE, "scellement", "ACTE-DE-GEL-MCS08.md")
JOURNAL = os.path.join(RACINE, "scellement", "journal_gel_mcs08.jsonl")
BLOC_RE = re.compile(r"```\n.*?```", re.DOTALL)


def sha256_fichier(chemin):
    with open(chemin, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()


def main():
    ts = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    if os.path.exists(JSON_ACTE):
        print("REFUS : l'acte existe deja.")
        return 1
    with open(os.path.join(RACINE, CARTE), encoding="utf-8") as f:
        contenu = f.read()
    bloc = list(BLOC_RE.finditer(contenu))[-1].group(0)
    pre = hashlib.sha256(contenu.encode("utf-8")).hexdigest()
    demo = {rel: sha256_fichier(os.path.join(RACINE, rel)) for rel in DEMO}

    if os.path.exists(JOURNAL):
        os.remove(JOURNAL)
    jc = mcs.JournalChaine(JOURNAL, GENESE)
    jc.ajouter({"type": "LIEN_GEL_CARTES", "chainon_precedent": TETE_GEL_CARTES})
    jc.ajouter({"type": "GEL_MCS08", "empreinte_pre_gel": pre,
                "demonstration_puissance": demo, "horodatage_utc": ts})
    tete = jc.prev_hash

    acte = {"acte": "GEL DE LA CARTE MCS-08 (jalon 3 v2)",
            "horodatage_utc": ts,
            "convention": "sha256 sur le contenu PRE-GEL (bloc a null) ; bloc "
                          "nul conserve ici pour verification octet par octet",
            "genese_journal": GENESE,
            "chainon_precedent_gel_cartes": TETE_GEL_CARTES,
            "carte": CARTE, "sha256_pre_gel": pre, "bloc_nul_original": bloc,
            "demonstration_puissance": demo, "tete_journal": tete}
    with open(JSON_ACTE, "w", encoding="utf-8") as f:
        json.dump(acte, f, ensure_ascii=False, indent=2)

    rempli = bloc.replace("SHA256_CARTE : null", "SHA256_CARTE : " + pre)
    rempli = rempli.replace("HORODATAGE   : null", "HORODATAGE   : " + ts)
    with open(os.path.join(RACINE, CARTE), "w", encoding="utf-8") as f:
        f.write(contenu.replace(bloc, rempli, 1))

    with open(MD_ACTE, "w", encoding="utf-8") as f:
        f.write("\n".join([
            "# ACTE DE GEL — Carte MCS-08 (Benford x CODATA)", "",
            f"Horodatage UTC : {ts}", "",
            f"Carte : `{CARTE}` — sha256 pre-gel : `{pre}`",
            f"Chainon precedent (gel cartes v2) : {TETE_GEL_CARTES}",
            f"Tete du journal de gel : {tete}", "",
            "## Demonstration de puissance (regle 1.2)", ""] +
            [f"- `{rel}` — sha256 : `{demo[rel]}`" for rel in DEMO] + [""]))
    print("GEL MCS-08 :", ts, pre[:16], "tete", tete[:16])
    return 0


if __name__ == "__main__":
    sys.exit(main())
