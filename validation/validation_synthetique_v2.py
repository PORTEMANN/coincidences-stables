"""validation_synthetique_v2.py — Validation du moteur MCS v2.0.

Succession : mcs_score.py v0.1 reste gele (jalon 4 ferme). Ce module valide
la v2.0 sur verite connue ET re-evalue les chiffres ENREGISTRES du jalon 4
(aucune nouvelle mesure : on relit les z et controles publies).

Scenarios :

  V2-A  correspondance plantee (PAC partage, meurt sous IAAFT)   -> CS+
  V2-B  artefact spectral (vit sous IAAFT)                       -> CS- deguise
  V2-C  REGRESSION JALON 4 : candidate inversee, controles a effet
        negatif massif (chiffres enregistres de MCS-01/MCS-02)    -> CSi, pas CS0
  V2-D  banc aveugle (controle vraiment muet, |effet| < 2 u)      -> CS0
  V2-E  MCS-03 re-enregistree : controles reellement muets        -> CS0 conserve

Regle d'honnetete : V2-A/B exercice la machinerie complete sur synthetique
(pipeline gele + surrogates) ; V2-C/E re-evaluent des chiffres enregistres
(consistence, pas re-execution) ; V2-D est un scenario z-niveau.

Graine maitresse : 20261010 (consignee). PRNG numpy (synthetique).
"""
from __future__ import annotations

import json
import os
import sys

import numpy as np

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(RACINE, "code"))
sys.path.insert(0, os.path.join(RACINE, "nulls"))

import mcs_score_v2 as mcs  # noqa: E402
import surrogates as nul  # noqa: E402
import positive_controls as pc  # noqa: E402
import ash_invariants as ash  # noqa: E402

FS = 1000.0
DUREE = 10.0
GRAINE = 20261010
JOURNAL = os.path.join(RACINE, "validation", "journal_synthetique_v2.jsonl")
RAPPORT = os.path.join(RACINE, "validation", "rapport_synthetique_v2.md")


def pac_partage(rng, profondeur=0.8):
    """Domaine synthetique a couplage phase-amplitude partage."""
    return pc.injecter_pac(FS, DUREE, profondeur, rng)


def bruit_colore(n, pente, rng):
    X = np.fft.rfft(rng.normal(0, 1, n))
    f = np.fft.rfftfreq(n, d=1.0 / FS)
    f[0] = f[1]
    X = X * f ** (pente / 2.0)
    return np.fft.irfft(X, n=n)


def scenario_spectral(kind, rng):
    """Pipeline complet : mesure = I4 moyen ; z sur N1 (IAAFT) ; double
    contrainte evaluee par le moteur v2."""
    n = int(FS * DUREE)
    N_F, N_S = 12, 20
    fenetres = []
    for i in range(N_F):
        if kind == "plantee":
            x = pac_partage(rng)
        else:
            x = bruit_colore(n, -1.5, rng) + 0.3 * rng.normal(0, 1, n)
        fenetres.append(x)
    m_reel = float(np.mean([ash.I4_pac(x, FS) for x in fenetres]))
    ms = []
    for s in range(N_S):
        surr = [nul.iaaft(x, rng, n_iter=5) for x in fenetres]
        ms.append(float(np.mean([ash.I4_pac(x, FS) for x in surr])))
    mu, u = float(np.mean(ms)), float(np.std(ms))
    z_g1 = mcs.z_score(m_reel, mu, u)
    z_par_g = {"g1_iaaft": z_g1, "g2_renversement": z_g1}
    # controles : c1 (permutation -> mesure ruinee), c2 (PAC injecte -> monte)
    perm = [nul.permutation(x, rng) for x in fenetres]
    m_perm = float(np.mean([ash.I4_pac(x, FS) for x in perm]))
    effet_c1 = (m_reel - m_perm) / u
    x_inj = fenetres[0] + 5.0 * pc.injecter_pac(FS, DUREE, 1.0, rng)
    effet_c2 = (float(ash.I4_pac(x_inj, FS)) - m_reel) / max(u, 1e-12)
    z_eff = (mu - m_reel) / u  # < 0 attendu si la coincidence meurt sous IAAFT
    attentes = {"c1": 1, "c2": 1}
    v = mcs.evaluer_double_v2("MCS-02", z_par_g, z_eff,
                              {"c1": effet_c1, "c2": effet_c2}, attentes)
    return v.to_dict(), {"m_reel": m_reel, "mu": mu, "u": u,
                         "z_g1": z_g1, "effet_c1": effet_c1, "effet_c2": effet_c2}


def main():
    rng = np.random.default_rng(GRAINE)
    jc = mcs.JournalChaine(JOURNAL, genesis="GENESIS-MCS-VALID-V2")
    resultats = []

    def consigner(scenario, attendu, res, detail):
        obtenu = res["verdict"]
        conforme = (obtenu == attendu)
        h = jc.ajouter({"type": "scenario_synthetique_v2", "scenario": scenario,
                        "attendu": attendu, "obtenu": obtenu, "conforme": conforme,
                        "detail": detail, "verdict_complet": res})
        resultats.append((scenario, attendu, obtenu, conforme))
        return h

    # --- V2-A : correspondance plantee ---------------------------------------
    res, det = scenario_spectral("plantee", rng)
    consigner("V2-A correspondance plantee", "CS+", res, det)

    # --- V2-B : artefact spectral ---------------------------------------------
    res, det = scenario_spectral("spectral", rng)
    att_b = "CS-"
    consigner("V2-B artefact spectral (vit sous IAAFT)", att_b, res, det)

    # --- V2-C : regression jalon 4 sur chiffres enregistres -------------------
    r1 = json.load(open(os.path.join(RACINE, "resultats", "mcs01_resultats.json"),
                        encoding="utf-8"))
    v1 = mcs.evaluer_v2("MCS-01", r1["configurations"] and
                        {k: v["z"] for k, v in r1["configurations"].items()},
                        {"c1": r1["controles"]["c1"]["effet_u"],
                         "c2": r1["controles"]["c2"]["effet_u"]},
                        attentes={"c1": 1, "c2": 1})
    assert v1.verdict == "CSi", f"V2-C1 : {v1.verdict} au lieu de CSi"
    consigner("V2-C1 MCS-01 re-enregistree (c1 = -52,6 u)", "CSi",
              v1.to_dict(), {"note": "v0.1 rendait CS0 (convention signee) ; v2.0 rend CSi"})

    r2 = json.load(open(os.path.join(RACINE, "resultats", "mcs02_resultats.json"),
                        encoding="utf-8"))
    z2 = {k: v["z"] for k, v in r2["configurations"].items()}
    v2 = mcs.evaluer_double_v2("MCS-02", z2, r2["z_effondrement"],
                               {"c1": r2["controles"]["c1"]["effet_u"],
                                "c2": r2["controles"]["c2"]["effet_u"]},
                               attentes={"c1": 1, "c2": 1})
    assert v2.verdict == "CSi", f"V2-C2 : {v2.verdict} au lieu de CSi"
    consigner("V2-C2 MCS-02 re-enregistree (c1 = -96,9 u)", "CSi",
              v2.to_dict(), {"note": "v0.1 rendait CS0 ; v2.0 rend CSi, c1 direction 'inverse' publiee"})

    # --- V2-D : banc aveugle ---------------------------------------------------
    v3 = mcs.evaluer_v2("DEFAULT", {"g1": 5.0, "g2": 5.5},
                        {"c1": 0.3, "c2": 0.1})
    assert v3.verdict == "CS0", f"V2-D : {v3.verdict} au lieu de CS0"
    consigner("V2-D banc aveugle (|effets| < 2 u, Sigma = 5)", "CS0",
              v3.to_dict(), {"note": "un banc vraiment aveugle reste CS0 en v2.0"})

    # --- V2-E : MCS-03 re-enregistree ------------------------------------------
    r3 = json.load(open(os.path.join(RACINE, "resultats", "mcs03_resultats.json"),
                        encoding="utf-8"))
    v4 = mcs.evaluer_v2("MCS-03", {k: v["z"] for k, v in r3["configurations"].items()},
                        {"c1": r3["controles"]["c1_2I_vers_I"]["effet_u"],
                         "c2": r3["controles"]["c2_maxima_invertes"]["effet_u"],
                         "c3": r3["controles"]["c3_sans_ordre1"]["effet_u"]})
    assert v4.verdict == "CS0", f"V2-E : {v4.verdict} au lieu de CS0"
    consigner("V2-E MCS-03 re-enregistree (controles muets)", "CS0",
              v4.to_dict(), {"note": "cécite materielle conservee en v2.0 : CS0 correct"})

    # --- bilan -------------------------------------------------------------------
    n_ok = sum(1 for _, _, _, c in resultats if c)
    print(f"\n{'scenario':<46s} {'attendu':<6s} {'obtenu':<6s} conforme")
    for s, a, o, c in resultats:
        print(f"{s:<46s} {a:<6s} {o:<6s} {'OK' if c else '*** ECHEC ***'}")
    print(f"\nBilan : {n_ok}/{len(resultats)} conformes")
    print("journal :", JOURNAL)
    ok, n = mcs.JournalChaine.verifier(JOURNAL, genesis="GENESIS-MCS-VALID-V2")
    print(f"chaine : {ok} ({n} records)")
    return n_ok == len(resultats)


if __name__ == "__main__":
    import sys as _s
    _s.exit(0 if main() else 1)
