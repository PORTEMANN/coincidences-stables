"""construire_journaux_mcs27.py — Journal chaine MCS-27 (scellee, executee).

Empreintes calculees depuis les fichiers (jamais transcrites). Chaine liee :
MCS-27 <- tete JALON-MCS26.
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
    t26 = tete("journal/JALON-MCS26.jsonl")
    acte = json.load(open(os.path.join(RACINE, "scellement", "GEL-MCS27.json"),
                          encoding="utf-8"))
    res = json.load(open(os.path.join(RACINE, "resultats", "mcs27_resultats.json"),
                         encoding="utf-8"))
    recs = [
        {"type": "GENESE_MCS27", "chainon_precedent_mcs26": t26[:16],
         "gel_acte": "scellement/GEL-MCS27.json",
         "tete_gel": acte["tete_journal"][:16],
         "note": "registre — la mesure jointe : vecteur de forme "
                 "(Koide, rapport) x le porteur a son vide (nul conjoint "
                 "de forme) ; execution unique"},
        {"type": "ACQUISITION_MCS27",
         "mode": "tables PDG deja acquises (MCS-04/16/25 — empreintes "
                 "reconsignees ; parseur MCS-16, filiation declaree) ; "
                 "contenu : formes closes du spectre mesure T7 (T13 pour "
                 "le zero protege) ; le nul conjoint enumere par la "
                 "machine hachee au gel de MCS-25 a l'execution — jamais "
                 "avant le gel",
         "empreinte_donnees": res["empreinte_donnees"],
         "premiere_mesure": "2026-10-12"},
        {"type": "CODE_MCS27", "fichier": "code/mcs27_runner.py",
         "sha256": sha("code/mcs27_runner.py")},
        {"type": "RESULTAT_MCS27", "fichier": "resultats/mcs27_resultats.json",
         "sha256": sha("resultats/mcs27_resultats.json"),
         "sigma": res["verdict_moteur_seuil_3.0"]["sigma"],
         "verdict_carte": res["verdict_carte_seuil_3.0"]},
        {"type": "LECTURE_MCS27",
         "lecture": "CS- (Sigma = +1,00). La forme du porteur a son vide "
                   "(K = 5-2sqrt5 = 0,5279 ; R = phi^2 = 2,618 — formes "
                   "closes du spectre mesure T7) n'est pas celle du canal "
                   "leptonique (K = 0,6666645 ; R = 16,82) : ecart "
                   "blanchi 6,27, ordinaire dans le nul conjoint de forme "
                   "(z canonique = +1,10 ; le minimum est l'espace "
                   "lineaire a +1,00 ; le vide deplace a Lambda = 2,5 "
                   "approche a +3,26 sans franchir). Controles "
                   "d'instrument puissants (c1 = 3,2 u ; c2 = 5,5 u). La "
                   "mesure jointe demandee par la frontiere de MCS-26 est "
                   "faite avec la puissance requise : la forme du porteur "
                   "n'est pas celle des leptons. Defaut de la demo "
                   "publie : le nul de l'ampute ne porte que 2 vecteurs "
                   "distincts (covariance de rang 1) — la metrique de "
                   "blanchiment est la covariance du nul canonique "
                   "(fixe, declaree)."},
    ]
    path = os.path.join(RACINE, "journal", "JALON-MCS27.jsonl")
    if os.path.exists(path):
        os.remove(path)
    jc = mcs.JournalChaine(path, genesis="GENESIS-MCS-27")
    for r in recs:
        jc.ajouter(r)
    ok, nb = mcs.JournalChaine.verifier(path, genesis="GENESIS-MCS-27")
    print("JALON-MCS27.jsonl :", ok, f"({nb} records)", "tete", jc.prev_hash[:16])


if __name__ == "__main__":
    main()
