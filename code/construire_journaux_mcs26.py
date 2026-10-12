"""construire_journaux_mcs26.py — Journal chaine MCS-26 (non scellee).

Empreintes calculees depuis les fichiers (jamais transcrites). Chaine liee :
MCS-26 <- tete JALON-MCS25.
"""
from __future__ import annotations

import json
import os
import sys
import hashlib

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(RACINE, "code"))
import mcs_score_v2 as mcs  # noqa: E402


def sha(rel):
    with open(os.path.join(RACINE, rel), "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()


def tete(rel):
    lignes = open(os.path.join(RACINE, rel), encoding="utf-8").read().strip().splitlines()
    return json.loads(lignes[-1])["record_hash"]


def main():
    t25 = tete("journal/JALON-MCS25.jsonl")
    recs = [
        {"type": "GENESE_MCS26", "chainon_precedent_mcs25": t25[:16],
         "note": "registre — siege du vide x canal neutrinos mesure "
                 "(campagne G : les candidats declares restants de la "
                 "frontiere de MCS-24) ; carte redigee, NON SCELLEE"},
        {"type": "ACQUISITION_MCS26",
         "fichier": "donnees/mcs26/nufit_splittings.json",
         "sha256": sha("donnees/mcs26/nufit_splittings.json"),
         "note": "tables NuFIT epinglees (v5.2 2022, v5.3 03/2024, v6.0 "
                 "09/2024 — nu-fit.org) ; les pdf sources restent chez "
                 "l'autorite, leurs sha256 sont consignes dans le json ; "
                 "variante declaree : without SK-atm, ordre normal",
         "premiere_mesure": "2026-10-12"},
        {"type": "REDACTION_MCS26",
         "fichier": "cartes/v2/MCS-26-siege-vide-canal-neutrinos.md",
         "sha256": sha("cartes/v2/MCS-26-siege-vide-canal-neutrinos.md"),
         "note": "forme declaree par la mesure T13 (un zero protege + "
                 "deux modes massifs — hiérarchie normale minimale)"},
        {"type": "PUISSANCE_MCS26_ECHOUEE",
         "fichier_demo_v1": "validation/demonstration_puissance_mcs26_v1.py",
         "sha256_demo_v1": sha("validation/demonstration_puissance_mcs26_v1.py"),
         "journal_demo_v1": "validation/journal_puissance_mcs26_v1.jsonl",
         "sha256_journal_v1": sha("validation/journal_puissance_mcs26_v1.jsonl"),
         "sigma_demo_v1": 2.05,
         "fichier_demo_v2": "validation/demonstration_puissance_mcs26.py",
         "sha256_demo_v2": sha("validation/demonstration_puissance_mcs26.py"),
         "journal_demo_v2": "validation/journal_puissance_mcs26.jsonl",
         "sha256_journal_v2": sha("validation/journal_puissance_mcs26.jsonl"),
         "sigma_demo_v2": 2.92,
         "puissances_demo_v2": {"c1": 2.641065, "c2": 3.592118},
         "verdict": "NON SCELLABLE — regle 1.2, correction unique "
                    "consommee : v1 (nul spectral complet) sigma = 2,05 ; "
                    "v2 (nul de forme : taille 5, rang 2, distinct — 6528 "
                    "matrices) sigma = 2,92 < 3,0 : les controles "
                    "d'instrument resolvent (c1 = 2,6 u ; c2 = 3,6 u) mais "
                    "le canal a un seul rapport mesure n'a pas la hauteur "
                    "requise — plafond mesure a deux pas",
         "note": "la carte dort sans avoir ete gelee : aucune mesure "
                 "produite. La frontiere de MCS-24 est documentee : le "
                 "canal neutrino (un seul rapport, R_nu ~ 33,9) est "
                 "plafonne a ~2,9 sigma pour cet instrument — la seconde "
                 "ancre mesuree n'est pas accessible ici sans une mesure "
                 "jointe (plusieurs nombres du canal a la fois — declare "
                 "comme frontiere, pas comme iteration)"},
    ]
    path = os.path.join(RACINE, "journal", "JALON-MCS26.jsonl")
    if os.path.exists(path):
        os.remove(path)
    jc = mcs.JournalChaine(path, genesis="GENESIS-MCS-26")
    for r in recs:
        jc.ajouter(r)
    ok, nb = mcs.JournalChaine.verifier(path, genesis="GENESIS-MCS-26")
    print("JALON-MCS26.jsonl :", ok, f"({nb} records)", "tete", jc.prev_hash[:16])


if __name__ == "__main__":
    main()
