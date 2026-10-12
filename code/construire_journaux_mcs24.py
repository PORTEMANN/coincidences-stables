"""construire_journaux_mcs24.py — Journal chaine MCS-24 (scellee, executee).

Empreintes calculees depuis les fichiers (jamais transcrites). Chaine liee :
MCS-24 <- tete JALON-MCS23.
"""
from __future__ import annotations

import hashlib
import json
import os
import sys

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
    t23 = tete("journal/JALON-MCS23.jsonl")
    acte = json.load(open(os.path.join(RACINE, "scellement", "GEL-MCS24.json"),
                          encoding="utf-8"))
    res = json.load(open(os.path.join(RACINE, "resultats", "mcs24_resultats.json"),
                         encoding="utf-8"))
    recs = [
        {"type": "GENESE_MCS24", "chainon_precedent_mcs23": t23[:16],
         "gel_acte": "scellement/GEL-MCS24.json",
         "tete_gel": acte["tete_journal"][:16],
         "note": "registre — tarif BH x porteur repare (nul reel) ; "
                 "execution unique"},
        {"type": "ACQUISITION_MCS24",
         "mode": "constantes gelees dans le runner (CODATA deja acquise, "
                 "MCS-08/16) ; contenu du porteur mesure aux verdicts "
                 "T5/T6/T7 du corpus (declare) ; le nul reel calcule par "
                 "la machine des orbites (filiation T1/T5) a l'execution — "
                 "jamais avant le gel",
         "empreinte_donnees": res["empreinte_donnees"],
         "premiere_mesure": "2026-10-12"},
        {"type": "CODE_MCS24", "fichier": "code/mcs24_runner.py",
         "sha256": sha("code/mcs24_runner.py")},
        {"type": "RESULTAT_MCS24", "fichier": "resultats/mcs24_resultats.json",
         "sha256": sha("resultats/mcs24_resultats.json"),
         "sigma": res["verdict_moteur_seuil_3.0"]["sigma"],
         "verdict_carte": res["verdict_carte_seuil_3.0"]},
        {"type": "LECTURE_MCS24",
         "lecture": "CSi (Sigma = -10,71). La proximite du porteur repare au "
                   "tarif des horizons est reelle au cadran de Planck NON "
                   "reduit (z = 10,9 ; rang p = 1,6 pour mille dans le nul "
                   "reel ; les deux contenus reels du corpus, porteur N=5 et "
                   "C4 N=4, sont les plus proches de la fenetre) ; mais elle "
                   "s'inverse sous le cadran reduit (z = -10,7) : la "
                   "coincidence mesure la convention de coupure, pas le "
                   "contenu. Controles puissants (c1 = 68 u ; c2 = 11 u). "
                   "Verdict mesure : sans loi sans cadran, le tarif n'est "
                   "pas une propriete stable — la question est close "
                   "(anti-stable) ; la frontiere du programme est publiee : "
                   "il faudrait une loi qui fixe le cadran, ou une seconde "
                   "ancre mesuree independante de Lambda."},
    ]
    path = os.path.join(RACINE, "journal", "JALON-MCS24.jsonl")
    if os.path.exists(path):
        os.remove(path)
    jc = mcs.JournalChaine(path, genesis="GENESIS-MCS-24")
    for r in recs:
        jc.ajouter(r)
    ok, nb = mcs.JournalChaine.verifier(path, genesis="GENESIS-MCS-24")
    print("JALON-MCS24.jsonl :", ok, f"({nb} records)", "tete", jc.prev_hash[:16])


if __name__ == "__main__":
    main()
