"""geler_cartes_v2.py — Gel des quatre cartes v2 (jalon 3 v2, phase cartes).

Convention identique a geler_v2.py : empreinte SHA-256 sur le contenu PRE-GEL
(bloc de scellement a null), bloc nul conserve dans l'acte, journal chaine
SHA-256 dont le premier record lie la tete du journal de scellement du moteur
v2.0 (745d7475...). La demonstration de puissance (regle 1.2 du manifeste
v2.0) est hachee dans l'acte : script + journal de demonstration.

Scelle : cartes/v2/MCS-04, MCS-05, MCS-06, MCS-07.
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

GENESE = "GENESIS-MCS-V2-GEL-CARTES"
TETE_SCELLEMENT_V2 = "745d7475bddc0ecbd92cfadd04f4bbaedea74d306911727a3e3dac84ef358c09"
CARTES = ["cartes/v2/MCS-04-loi-harmonique.md",
          "cartes/v2/MCS-05-agregation-EEG-F17.md",
          "cartes/v2/MCS-06-loi-bifurcations.md",
          "cartes/v2/MCS-07-economie-information.md"]
DEMO = ["validation/demonstrations_puissance_v2.py",
        "validation/journal_puissance_v2.jsonl"]
JSON_ACTE = os.path.join(RACINE, "scellement", "GEL-CARTES-V2.json")
MD_ACTE = os.path.join(RACINE, "scellement", "ACTE-DE-GEL-CARTES-V2.md")
JOURNAL = os.path.join(RACINE, "scellement", "journal_gel_cartes_v2.jsonl")

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
        print("REFUS : un acte de gel des cartes v2 existe deja.")
        return 1

    # 1. Empreintes pre-gel (contenu avec bloc a null)
    pre, blocs_nuls = {}, {}
    for rel in CARTES:
        chemin = os.path.join(RACINE, rel)
        with open(chemin, encoding="utf-8") as f:
            contenu = f.read()
        blocs_nuls[rel] = dernier_bloc(contenu).group(0)
        pre[rel] = hashlib.sha256(contenu.encode("utf-8")).hexdigest()

    # 2. Demonstration de puissance (regle 1.2) : hachee dans l'acte
    demo = {rel: sha256_fichier(os.path.join(RACINE, rel)) for rel in DEMO}

    # 3. Journal chaine du gel (lie a la tete du scellement moteur v2)
    if os.path.exists(JOURNAL):
        os.remove(JOURNAL)
    jc = mcs.JournalChaine(JOURNAL, GENESE)
    jc.ajouter({"type": "LIEN_SCELLEMENT_V2", "chainon_precedent": TETE_SCELLEMENT_V2})
    jc.ajouter({"type": "GEL_CARTES_V2", "empreintes_pre_gel": pre,
                    "demonstration_puissance": demo,
                    "horodatage_utc": ts})
    tete = jc.prev_hash

    # 4. Acte JSON (blocs nuls conserves pour verification octet par octet)
    acte = {
        "acte": "GEL DES CARTES MCS v2 (jalon 3 v2, phase cartes)",
        "horodatage_utc": ts,
        "convention": "sha256 calculee sur le contenu PRE-GEL (bloc a null) ; "
                      "le bloc nul original est conserve ici pour verification "
                      "octet par octet (meme convention que le jalon 3)",
        "genese_journal": GENESE,
        "chainon_precedent_scellement_v2": TETE_SCELLEMENT_V2,
        "cartes": {rel: {"sha256_pre_gel": pre[rel],
                         "bloc_nul_original": blocs_nuls[rel]}
                   for rel in CARTES},
        "demonstration_puissance": demo,
        "tete_journal": tete,
    }
    with open(JSON_ACTE, "w", encoding="utf-8") as f:
        json.dump(acte, f, ensure_ascii=False, indent=2)

    # 5. Remplissage des blocs de scellement dans chaque carte (post-gel)
    for rel in CARTES:
        chemin = os.path.join(RACINE, rel)
        with open(chemin, encoding="utf-8") as f:
            contenu = f.read()
        bloc_rempli = remplir_bloc(blocs_nuls[rel], {
            "SHA256_CARTE": pre[rel],
            "HORODATAGE": ts,
        })
        contenu = contenu.replace(blocs_nuls[rel], bloc_rempli, 1)
        with open(chemin, "w", encoding="utf-8") as f:
            f.write(contenu)

    # 6. Acte lisible
    lignes = ["# ACTE DE GEL — Cartes MCS v2 (jalon 3 v2, phase cartes)", "",
              f"Horodatage UTC : {ts}", "",
              "Convention : empreinte SHA-256 calculee sur le contenu PRE-GEL",
              "(bloc de scellement a null) ; le bloc nul original est conserve",
              "dans l'acte JSON pour verification octet par octet.", "",
              f"Chainon precedent (scellement moteur v2.0) : {TETE_SCELLEMENT_V2}",
              f"Tete du journal de gel : {tete}", "", "## Cartes gelees", ""]
    for rel in CARTES:
        lignes.append(f"- `{rel}` — sha256 pre-gel : `{pre[rel]}`")
    lignes += ["", "## Demonstration de puissance (regle 1.2)", ""]
    for rel in DEMO:
        lignes.append(f"- `{rel}` — sha256 : `{demo[rel]}`")
    lignes.append("")
    with open(MD_ACTE, "w", encoding="utf-8") as f:
        f.write("\n".join(lignes))

    print("GEL CARTES V2 effectue :", ts)
    for rel in CARTES:
        print(" ", rel, pre[rel][:16])
    print("tete journal :", tete[:16])
    return 0


if __name__ == "__main__":
    sys.exit(main())
