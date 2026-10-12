"""construire_journaux_mcs25.py — Journal chaine MCS-25 (scellee, executee).

Empreintes calculees depuis les fichiers (jamais transcrites). Chaine liee :
MCS-25 <- tete JALON-MCS24.
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
    t24 = tete("journal/JALON-MCS24.jsonl")
    acte = json.load(open(os.path.join(RACINE, "scellement", "GEL-MCS25.json"),
                          encoding="utf-8"))
    res = json.load(open(os.path.join(RACINE, "resultats", "mcs25_resultats.json"),
                         encoding="utf-8"))
    recs = [
        {"type": "GENESE_MCS25", "chainon_precedent_mcs24": t24[:16],
         "gel_acte": "scellement/GEL-MCS25.json",
         "tete_gel": acte["tete_journal"][:16],
         "note": "registre — siege du vide x canal leptonique (nul reel "
                 "spectral) ; execution unique ; correction pre-gel "
                 "declaree unique (demo v1 impuissante publiee)"},
        {"type": "ACQUISITION_MCS25",
         "mode": "tables PDG deja acquises (MCS-04/16 — empreintes "
                 "reconsignees) ; contenu du porteur mesure a T7 "
                 "(declare) ; le nul reel spectral enumere par la machine "
                 "des orbites (filiation T1, reimplementation declaree) a "
                 "l execution — jamais avant le gel",
         "empreinte_donnees": res["empreinte_donnees"],
         "premiere_mesure": "2026-10-12"},
        {"type": "CODE_MCS25", "fichier": "code/mcs25_runner.py",
         "sha256": sha("code/mcs25_runner.py"),
         "enum": "code/spectres_triplets.py",
         "sha256_enum": sha("code/spectres_triplets.py")},
        {"type": "RESULTAT_MCS25", "fichier": "resultats/mcs25_resultats.json",
         "sha256": sha("resultats/mcs25_resultats.json"),
         "sigma": res["verdict_moteur_seuil_3.0"]["sigma"],
         "verdict_carte": res["verdict_carte_seuil_3.0"]},
        {"type": "LECTURE_MCS25",
         "lecture": "CS- (Sigma = -0,26). Le vide du porteur (r = phi^2 = "
                   "2,618 — forme close du spectre mesure T7) ne siege pas "
                   "dans le canal leptonique au-dela du nul reel spectral : "
                   "son meilleur siege est mu/e a 0,81 dex, ordinaire parmi "
                   "les triplets nus verifies (z canonique = +0,98 ; le "
                   "point Lambda=6 de la branche fait le minimum a -0,26). "
                   "Controles d'instrument puissants (c1 = 2,9 u ; c2 = 4,4 "
                   "u). La frontiere de MCS-24 recoit sa premiere reponse "
                   "mesuree : la seconde ancre n'est pas dans le canal des "
                   "leptons charges. Diagnostic publie : dans la table "
                   "complete des fermions, le meilleur siege du porteur "
                   "est b/tau (2,354 — 0,046 dex) — mais la demo v1 a "
                   "mesure que cette question est plafonnee a 1,46 sigma "
                   "(table trop dense) — impuissance publiee. Defaut de "
                   "redaction publie : l enonce (section 1 de la carte "
                   "scellee) porte la formulation d avant correction "
                   "(table des fermions) — modification perdue par "
                   "ecriture parallele lors de la correction, attrapee a "
                   "la relecture post-gel ; le lexique gele et "
                   "l execution portent le canal leptonique (la mesure "
                   "est celle du lexique)."},
    ]
    path = os.path.join(RACINE, "journal", "JALON-MCS25.jsonl")
    if os.path.exists(path):
        os.remove(path)
    jc = mcs.JournalChaine(path, genesis="GENESIS-MCS-25")
    for r in recs:
        jc.ajouter(r)
    ok, nb = mcs.JournalChaine.verifier(path, genesis="GENESIS-MCS-25")
    print("JALON-MCS25.jsonl :", ok, f"({nb} records)", "tete", jc.prev_hash[:16])


if __name__ == "__main__":
    main()
