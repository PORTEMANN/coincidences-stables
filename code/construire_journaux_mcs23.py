"""construire_journaux_mcs23.py — Journal chaine MCS-23 (non scellee).

Empreintes calculees depuis les fichiers (jamais transcrites). Chaine liee :
MCS-23 <- tete JALON-MCS22.
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
    t22 = tete("journal/JALON-MCS22.jsonl")
    recs = [
        {"type": "GENESE_MCS23", "chainon_precedent_mcs22": t22[:16],
         "note": "registre — tarif de Bekenstein-Hawking x contenu spectral "
                 "declare du corpus (programme 'qui encaisse') ; carte "
                 "redigee, NON SCELLEE"},
        {"type": "REDACTION_MCS23",
         "fichier": "cartes/v2/MCS-23-tarif-bh-contenu-spectral.md",
         "sha256": sha("cartes/v2/MCS-23-tarif-bh-contenu-spectral.md"),
         "note": "nul combinatoire exact : enumeration de la fenetre "
                 "Krajewski datee (CONVENTIONS.md du depot, C-BORNES) — "
                 "erratum 2026-09-06 du depot lu et declare (compte 63160 "
                 "refute, dimension 7 convention-dependante, triplet C4 "
                 "verifie)"},
        {"type": "PUISSANCE_MCS23_ECHOUEE",
         "fichier_demo": "validation/demonstration_puissance_mcs23.py",
         "sha256_demo": sha("validation/demonstration_puissance_mcs23.py"),
         "journal_demo": "validation/journal_puissance_mcs23.jsonl",
         "sha256_journal": sha("validation/journal_puissance_mcs23.jsonl"),
         "sigma_demo": 2.71,
         "puissances_demo": {"c1": 6.686567, "c2": 2.542308},
         "verdict": "NON SCELLABLE — regle 1.2 : les controles resolvent "
                    "(c1 = 6,7 u ; c2 = 2,5 u) mais la verite plantee au "
                    "tarif n'atteint que sigma = 2,71 < 3,0 : la fenetre "
                    "auditee contient par chance combinatoire des contenus "
                    "quasi au tarif (p = 1,6 % au mieux) — la question "
                    "'qui encaisse a quel taux' n'a pas la hauteur requise "
                    "sur un seul nombre",
         "note": "la carte dort sans avoir ete gelee : aucune mesure "
                 "produite. Le programme : pour gagner la hauteur, il faut "
                 "soit une mesure jointe (plusieurs relations gelees du "
                 "corpus), soit le nul resolu par les vrais (D, J, gamma) — "
                 "la question ouverte de l'erratum du depot — declares "
                 "comme nouvelle carte avec son regard ailleurs, pas une "
                 "iteration"},
    ]
    path = os.path.join(RACINE, "journal", "JALON-MCS23.jsonl")
    if os.path.exists(path):
        os.remove(path)
    jc = mcs.JournalChaine(path, genesis="GENESIS-MCS-23")
    for r in recs:
        jc.ajouter(r)
    ok, nb = mcs.JournalChaine.verifier(path, genesis="GENESIS-MCS-23")
    print("JALON-MCS23.jsonl :", ok, f"({nb} records)", "tete", jc.prev_hash[:16])


if __name__ == "__main__":
    main()
