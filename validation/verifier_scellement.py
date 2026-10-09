"""verifier_scellement.py — Verification independante du gel (jalon 3).

Pour chaque document scelle : reconstruit le contenu pre-gel en remplacant
le bloc de scellement actuel par le bloc nul original conserve dans
SCCELLEMENT-J3.json, recalcule l'empreinte, compare. Verifie aussi :
  - les empreintes du code et du paquet ;
  - l'integrite de la chaine du journal de scellement ;
  - la tete de chaine consignee.

Doit etre au vert avant toute ouverture (jalon 4). Sortie 0 = integre.
"""
from __future__ import annotations

import hashlib
import json
import os
import re
import sys

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(RACINE, "code"))
import mcs_score as mcs

BLOC_RE = re.compile(r"```\n.*?```", re.DOTALL)


def main() -> int:
    chemin_acte = os.path.join(RACINE, "scellement", "SCCELLEMENT-J3.json")
    with open(chemin_acte, encoding="utf-8") as f:
        acte = json.load(f)
    echecs = []

    # Documents avec bloc de scellement
    for rel, info in acte["fichiers"].items():
        chemin = os.path.join(RACINE, rel)
        with open(chemin, encoding="utf-8") as f:
            contenu = f.read()
        blocs = list(BLOC_RE.finditer(contenu))
        if not blocs:
            echecs.append(f"{rel} : bloc de scellement introuvable")
            continue
        bloc = blocs[-1]
        pre_gel = contenu[:bloc.start()] + info["bloc_nul_original"] \
            + contenu[bloc.end():]
        h = hashlib.sha256(pre_gel.encode("utf-8")).hexdigest()
        if h != info["sha256_pre_gel"]:
            echecs.append(f"{rel} : empreinte {h[:12]}… != "
                          f"{info['sha256_pre_gel'][:12]}…")

    # Code
    for rel, h_attendu in acte["code"].items():
        with open(os.path.join(RACINE, rel), "rb") as f:
            h = hashlib.sha256(f.read()).hexdigest()
        if h != h_attendu:
            echecs.append(f"{rel} : code modifie depuis le gel")
    paquet = hashlib.sha256(json.dumps(acte["code"], sort_keys=True,
                                       separators=(",", ":"))
                            .encode("utf-8")).hexdigest()
    if paquet != acte["sha256_paquet_code"]:
        echecs.append("paquet code : incoherence")

    # Chaine du journal
    chemin_journal = os.path.join(RACINE, "scellement",
                                  "journal_scellement.jsonl")
    ok, n = mcs.JournalChaine.verifier(chemin_journal,
                                       genesis=acte["genese_journal"])
    if not ok:
        echecs.append(f"journal de scellement : chaine rompue au record {n}")
    else:
        with open(chemin_journal, encoding="utf-8") as f:
            dernier = None
            for ligne in f:
                dernier = json.loads(ligne)
        if dernier is None or dernier.get("record_hash") != acte["chaine_journal_tete"]:
            echecs.append("tete de chaine differente de l'acte")

    if echecs:
        print("SCELLEMENT ROMPU :")
        for e in echecs:
            print(f"  - {e}")
        return 1
    print(f"scellement integre : {len(acte['fichiers'])} documents, "
          f"{len(acte['code'])} fichiers de code, chaine de {n} records")
    print(f"empreinte globale : {acte['empreinte_globale']}")
    print(f"horodatage acte   : {acte['horodatage_utc']}")
    print("autorisation d'ouverture (jalon 4) : OUI, une fois l'horodatage "
          "externe (ots) effectue")
    return 0


if __name__ == "__main__":
    sys.exit(main())
