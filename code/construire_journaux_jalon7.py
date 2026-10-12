"""construire_journaux_jalon7.py — Journaux chaines MCS-20/21/22.

Empreintes calculees depuis les fichiers (jamais transcrites). Chaines
liees : MCS-20 <- tete JALON-MCS19 ; MCS-21 <- tete MCS-20 ; MCS-22 <-
tete MCS-21.
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


def journal(nom, genesis, records):
    path = os.path.join(RACINE, "journal", nom)
    if os.path.exists(path):
        os.remove(path)
    jc = mcs.JournalChaine(path, genesis=genesis)
    for r in records:
        jc.ajouter(r)
    ok, nb = mcs.JournalChaine.verifier(path, genesis=genesis)
    print(nom, ":", ok, f"({nb} records)", "tete", jc.prev_hash[:16])
    return jc.prev_hash


def main():
    t19 = tete("journal/JALON-MCS19.jsonl")

    # ---------------- MCS-20 (NON SCELLEE, deux demos echouees) ----------
    rec20 = [
        {"type": "GENESE_MCS20", "chainon_precedent_mcs19": t19[:16],
         "note": "registre — constance de l'energie noire (w = -1) x residus "
                 "Pantheon+ ; carte redigee, NON SCELLEE"},
        {"type": "REDACTION_MCS20",
         "fichier": "cartes/v2/MCS-20-constance-w-pantheon.md",
         "sha256": sha("cartes/v2/MCS-20-constance-w-pantheon.md"),
         "note": "mesure finale m = -Delta_chi2 ; la version initiale "
                 "(pente OLS) a ete corrigee UNE fois avant gel apres echec "
                 "de la demo v1 — correction declaree dans la carte"},
        {"type": "PUISSANCE_MCS20_V1_ECHOUEE",
         "fichier_demo": "validation/demonstration_puissance_mcs20_v1.py",
         "sha256_demo": sha("validation/demonstration_puissance_mcs20_v1.py"),
         "journal_demo": "validation/journal_puissance_mcs20_v1.jsonl",
         "sha256_journal": sha("validation/journal_puissance_mcs20_v1.jsonl"),
         "sigma_demo": 1.66,
         "puissances_demo": {"c1": 1.261158, "c2": 1.193053},
         "verdict": "NON SCELLABLE — la pente OLS a ordonnee libre dilue "
                    "l'effet de w (le niveau absorbe la derive)"},
        {"type": "CORRECTION_PRE_GEL_MCS20",
         "objet": "mesure corrigee une fois avant gel vers la statistique "
                  "suffisante standard (Delta-chi2, bruit diagonal declare) — "
                  "precedent MCS-05b ; la demo v1 est conservee et publiee"},
        {"type": "PUISSANCE_MCS20_V2_ECHOUEE",
         "fichier_demo": "validation/demonstration_puissance_mcs20.py",
         "sha256_demo": sha("validation/demonstration_puissance_mcs20.py"),
         "journal_demo": "validation/journal_puissance_mcs20.jsonl",
         "sha256_journal": sha("validation/journal_puissance_mcs20.jsonl"),
         "sigma_demo": 1.09,
         "puissances_demo": {"c1": 0.444185, "c2": 0.573377},
         "verdict": "NON SCELLABLE — regle 1.2 : le nul a etendue honnete "
                    "[-1,4 ; -0,6] inclut des univers arbitrairement proches "
                    "de w = -1 ; sa dispersion (u = 163) egale sa moyenne "
                    "(Delta = 178) : aucun z ne peut decoller. La question "
                    "'exactement -1' n'est pas tranchable par Pantheon+ a "
                    "cette etendue",
         "note": "la carte dort sans avoir ete gelee. Une carte future "
                 "exigerait un nul a marge declaree (|w+1| >= epsilon gele) "
                 "ou une mesure d'intervalle — nouvelle carte avec son "
                 "regard ailleurs, pas une iteration"},
    ]
    t20 = journal("JALON-MCS20.jsonl", "GENESIS-MCS-20", rec20)

    # ---------------- MCS-21 (SCELLEE, executee : CSp) -------------------
    acte = json.load(open(os.path.join(RACINE, "scellement", "GEL-MCS21.json"),
                          encoding="utf-8"))
    res = json.load(open(os.path.join(RACINE, "resultats", "mcs21_resultats.json"),
                         encoding="utf-8"))
    rec21 = [
        {"type": "GENESE_MCS21", "chainon_precedent_mcs20": t20[:16],
         "gel_acte": "scellement/GEL-MCS21.json",
         "tete_gel": acte["tete_journal"][:16],
         "note": "registre — tension S8 x familles CMB/lentilles ; execution "
                 "unique"},
        {"type": "ACQUISITION_MCS21",
         "mode": "valeurs gelees dans le runner avec sources publiques "
                 "citees (convention MCS-16) — Planck 2018, ACT DR6, "
                 "KiDS-1000, DES-Y3, HSC-Y3 ; editions Combined CMB 2026 et "
                 "KiDS-Legacy ; aucune acquisition de fichiers",
         "empreinte_donnees": res["empreinte_donnees"],
         "premiere_mesure": "2026-10-12 — aucune tension calculee avant le "
                            "gel de la carte"},
        {"type": "CODE_MCS21", "fichier": "code/mcs21_runner.py",
         "sha256": sha("code/mcs21_runner.py")},
        {"type": "RESULTAT_MCS21", "fichier": "resultats/mcs21_resultats.json",
         "sha256": sha("resultats/mcs21_resultats.json"),
         "sigma": res["verdict_moteur_seuil_3.0"]["sigma"],
         "verdict_carte": res["verdict_carte_seuil_3.1"]},
        {"type": "LECTURE_MCS21",
         "lecture": "CSp (Sigma = 2,62, seuil 3,1). La tension S8 est forte "
                    "avec les editions historiques (canonique z = 4,80 ; "
                    "Combined CMB 2026 : 5,11 ; bornes hautes/basses : 4,70/"
                    "4,96 ; sans HSC : 4,59 ; retrait ACT : 4,24) mais "
                    "s'effondre sous l'edition KiDS-Legacy (z = 2,62) : la "
                    "tension depend de l'edition KiDS — la machine mesure "
                    "exactement la geographie 2026 (KiDS converge vers le "
                    "CMB, DES reste bas). Controles puissants (c1 = c2 = "
                    "6,08 u — symetriques par construction, declare). La "
                    "carte dort : la tension S8 est reelle dans les editions "
                    "historiques, non stable a travers les editions. La "
                    "question physique (systematiques des lentilles ou "
                    "nouvelle physique) reste hors de portee — la machine "
                    "mesure la stabilite, pas son explication."},
    ]
    t21 = journal("JALON-MCS21.jsonl", "GENESIS-MCS-21", rec21)

    # ---------------- MCS-22 (NON SCELLEE) -------------------------------
    rec22 = [
        {"type": "GENESE_MCS22", "chainon_precedent_mcs21": t21[:16],
         "note": "registre — quasi-unification des couplages SM x running "
                 "gele ; carte redigee, NON SCELLEE"},
        {"type": "REDACTION_MCS22",
         "fichier": "cartes/v2/MCS-22-quasi-unification-couplages.md",
         "sha256": sha("cartes/v2/MCS-22-quasi-unification-couplages.md"),
         "note": "mesure continue (gap au croisement t12, running 1-loop "
                 "gele, normalisation SU(5)) — concue pour eviter "
                 "l'impuissance des mesures a trois nombres (MCS-18/19)"},
        {"type": "PUISSANCE_MCS22_ECHOUEE",
         "fichier_demo": "validation/demonstration_puissance_mcs22.py",
         "sha256_demo": sha("validation/demonstration_puissance_mcs22.py"),
         "journal_demo": "validation/journal_puissance_mcs22.jsonl",
         "sha256_journal": sha("validation/journal_puissance_mcs22.jsonl"),
         "sigma_demo": 1.48,
         "puissances_demo": {"c1": 0.393149, "c2": 0.825194},
         "verdict": "NON SCELLABLE — regle 1.2 : aux etendues honnetes "
                    "declarees, des couplages libres atteignent souvent des "
                    "gaps aussi petits que le SM (mu_gap = 6,92 ; u = 4,67) ; "
                    "meme une verite plantee exacte ne depasse pas 1,5 sigma "
                    "et les sabotages restent sous 2 u",
         "note": "troisieme refus de la machine sur les questions "
                 "d'unification (MCS-18 CKM, MCS-19 KSS, MCS-22 couplages) : "
                 "trois mesures, trois impuissances — la quasi-unification "
                 "n'est pas tranchable par trois couplages a ces etendues ; "
                 "une carte future exigerait une mesure enrichie (contenu de "
                 "representations complet, seuils) avec son regard ailleurs"},
    ]
    journal("JALON-MCS22.jsonl", "GENESIS-MCS-22", rec22)


if __name__ == "__main__":
    main()
