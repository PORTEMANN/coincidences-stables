"""mcs_score_v2.py — Operateur MCS v2.0 (successeur de mcs_score.py v0.1).

Succession : mcs_score.py (v0.1) reste gele et ferme avec les cartes
MCS-01/02/03 (jalon 4, journal JALON-4-OUVERTURE.jsonl). La v2.0 ne rouvre
aucune carte fermee.

Changements motives par les records publies du jalon 4 :

1. REGLE D'IMPUISSANCE ROBUSTE AU SIGNE (records LECTURE_MCS01,
   LECTURE_MCS02) : en v0.1, controles_ok exigeait effet >= +2 u signe.
   Quand la candidate est INVERSEE (CSi), un sabotage peut produire un effet
   massif dans la direction opposee a l'attente de la carte (MCS-01 : c1 =
   -52,6 u car les donnees miroir ajustent mieux ; MCS-02 : c1 = -96,9 u car
   l'effondrement vers N3 part d'une mesure deja tres negative). Ces bancs
   etaient puissants ; la convention signee les appelait aveugles.
   En v2.0 : la PUISSANCE d'un controle est |effet| en unites u_null ;
   un controle est muet ssi |effet| < SEUIL_CONTROLE. La direction
   (conforme ou inverse a l'attente declaree dans la carte) est un
   diagnostic publie separement dans le verdict — elle n'est jamais
   confondue avec la puissance.

2. PUISSANCE DEMONTREE AVANT GEL (record LECTURE_MCS03) : la cecite de
   MCS-03 etait structurelle (correlation de rangs sur 15 points
   insensible aux sabotages point-par-point). En v2.0, toute carte doit
   joindre une demonstration de puissance sur synthetique (la statistique
   resout ses controles a |effet| >= 2 u) hachee dans l'acte de
   scellement. C'est une regle de redaction (jalon 1), pas du code.

3. Le reste est inchange : Sigma = min z_g (maillon le plus faible,
   moyenne interdite), seuils par carte, CS0/CSi/CS-/CSp/CS+, double
   contrainte pour les cartes spectrales, journal chaine SHA-256.
"""
from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass, field

# --- Seuils (inchangés) ------------------------------------------------------
SEUILS_GELES = {
    "MCS-01": 3.0,
    "MCS-02": 3.3,
    "MCS-03": 3.4,
    "DEFAULT": 3.0,
}
SEUIL_CSI = -2.0
SEUIL_CSP = 2.0
SEUIL_CONTROLE = 2.0       # puissance minimale : |effet| >= 2 u_null
SEUIL_EFFONDREMENT = -2.0


def z_score(m: float, mu_null: float, u_null: float) -> float:
    """Marge normalisée d'une mesure contre son modèle nul."""
    if u_null <= 0:
        raise ValueError("u_null nul : modele nul degenere, verdict impossible")
    return (m - mu_null) / u_null


def sigma(z_par_g: dict, exclure: tuple = ()) -> float:
    """Sigma = minimum des z sur les déformations retenues (maillon le plus faible)."""
    vals = [z for g, z in z_par_g.items() if g not in exclure]
    if not vals:
        raise ValueError("aucune deformation retenue pour Sigma")
    return min(vals)


def controles_ok_v2(controles: dict) -> tuple:
    """v2.0 : controles = {nom: effet_en_unites_u_null (signe)}.
    Un controle est MUET ssi |effet| < SEUIL_CONTROLE (vraiment aveugle).
    Retourne (ok, muets, puissances) — puissances = {nom: |effet|}."""
    puissances = {nom: abs(e) for nom, e in controles.items()}
    muets = [nom for nom, p in puissances.items() if p < SEUIL_CONTROLE]
    return (len(muets) == 0, muets, puissances)


@dataclass
class VerdictV2:
    """Verdict v2.0 : ajoute la direction des controles (conforme/inverse a
    l'attente de la carte) et leurs puissances, publies separement."""
    verdict: str
    sigma: float
    seuil: float
    motif: str
    z_par_g: dict
    controles: dict
    puissances_controles: dict = field(default_factory=dict)
    directions_controles: dict = field(default_factory=dict)

    def to_dict(self) -> dict:
        return {
            "verdict": self.verdict,
            "sigma": round(self.sigma, 6),
            "seuil": self.seuil,
            "motif": self.motif,
            "z_par_g": {g: round(z, 6) for g, z in self.z_par_g.items()},
            "controles": {c: round(e, 6) for c, e in self.controles.items()},
            "puissances_controles": {c: round(p, 6) for c, p in self.puissances_controles.items()},
            "directions_controles": self.directions_controles,
        }


def _verdict_simple(sigma_val: float, seuil: float) -> tuple:
    if sigma_val <= SEUIL_CSI:
        return "CSi", "inversion stable (Sigma <= -2), publication prioritaire"
    if sigma_val >= seuil:
        return "CS+", "coincidence stable : survit a toutes les deformations"
    if sigma_val >= SEUIL_CSP:
        return "CSp", "stabilite locale ; hors-echantillon non demontre"
    return "CS-", "artefact probable ; publication B3-FAIL"


def _directions(controles: dict, attentes: dict) -> dict:
    """attentes = {nom: +1 (effet positif attendu) / -1 (negatif attendu)}.
    Direction : 'conforme', 'inverse' ou 'faible' (|effet| < seuil)."""
    out = {}
    for nom, effet in controles.items():
        att = attentes.get(nom, 1)
        if abs(effet) < SEUIL_CONTROLE:
            out[nom] = "faible"
        elif (effet > 0) == (att > 0):
            out[nom] = "conforme"
        else:
            out[nom] = "inverse"
    return out


def evaluer_v2(carte_id: str, z_par_g: dict, controles: dict,
               attentes: dict | None = None, exclure: tuple = ()) -> VerdictV2:
    """Verdict standard v2.0 (cartes simples)."""
    seuil = SEUILS_GELES.get(carte_id, SEUILS_GELES["DEFAULT"])
    ok, muets, puissances = controles_ok_v2(controles)
    s = sigma(z_par_g, exclure=exclure)
    directions = _directions(controles, attentes or {})
    if not ok:
        return VerdictV2("CS0", s, seuil,
                         f"controles positifs muets (|effet| < 2 u) : {muets} ; "
                         f"test impuissant", z_par_g, controles,
                         puissances, directions)
    v, motif = _verdict_simple(s, seuil)
    if any(d == "inverse" for d in directions.values()):
        motif += " ; note : controle(s) inverse(s) " + \
                 str([c for c, d in directions.items() if d == "inverse"]) + \
                 " (puissant mais de direction opposee a l'attente — publie)"
    return VerdictV2(v, s, seuil, motif, z_par_g, controles, puissances, directions)


def evaluer_double_v2(carte_id: str, z_par_g: dict, z_effondrement: float,
                      controles: dict, attentes: dict | None = None,
                      g_surrogate: str = "g1_iaaft") -> VerdictV2:
    """Verdict a double contrainte v2.0 (cartes spectrales).

    (a) Sigma >= seuil sur les donnees reelles ;
    (b) z_effondrement <= -2 : la mesure s'effondre sous surrogates IAAFT.
    (a) sans (b) => CS- deguise : la coincidence etait spectrale, generique.
    """
    seuil = SEUILS_GELES.get(carte_id, SEUILS_GELES["DEFAULT"])
    ok, muets, puissances = controles_ok_v2(controles)
    s = sigma(z_par_g, exclure=(g_surrogate,))
    directions = _directions(controles, attentes or {})
    if not ok:
        return VerdictV2("CS0", s, seuil,
                         f"controles positifs muets (|effet| < 2 u) : {muets} ; "
                         f"test impuissant", z_par_g, controles,
                         puissances, directions)
    a = s >= seuil
    b = z_effondrement <= SEUIL_EFFONDREMENT
    base_motif = ""
    if any(d == "inverse" for d in directions.values()):
        base_motif = " ; controle(s) inverse(s) publie(s)"
    if s <= SEUIL_CSI:
        return VerdictV2("CSi", s, seuil,
                         "inversion stable sur donnees reelles" + base_motif,
                         z_par_g, controles, puissances, directions)
    if a and b:
        return VerdictV2("CS+", s, seuil,
                         "structure de phase inter-domaines stable "
                         "(vit sur donnees, meurt sous IAAFT)" + base_motif,
                         z_par_g, controles, puissances, directions)
    if a and not b:
        return VerdictV2("CS-", s, seuil,
                         "CS- deguise : survit aux surrogates ; la coincidence "
                         "etait spectrale, donc generique" + base_motif,
                         z_par_g, controles, puissances, directions)
    if b and not a:
        return VerdictV2("CSp", s, seuil,
                         "meurt sous IAAFT mais Sigma insuffisant sur donnees" + base_motif,
                         z_par_g, controles, puissances, directions)
    return VerdictV2("CS-", s, seuil, "ni (a) ni (b) : artefact probable" + base_motif,
                     z_par_g, controles, puissances, directions)


# --- Journal chaine SHA-256 (inchange) ----------------------------------------

class JournalChaine:
    """Journal append-only JSONL, chainage SHA-256. Aucune suppression possible
    sans casser la chaine : c'est la memoire du banc."""

    def __init__(self, chemin: str, genesis: str = "GENESIS-MCS-J2"):
        self.chemin = chemin
        self.genesis = genesis
        self.prev_hash = genesis

    @staticmethod
    def _canon(rec: dict) -> bytes:
        return json.dumps(rec, sort_keys=True, separators=(",", ":"),
                          ensure_ascii=False).encode("utf-8")

    def ajouter(self, rec: dict) -> str:
        rec = dict(rec)
        rec["prev_hash"] = self.prev_hash
        h = hashlib.sha256(self._canon(rec)).hexdigest()
        rec["record_hash"] = h
        with open(self.chemin, "a", encoding="utf-8") as f:
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")
        self.prev_hash = h
        return h

    @staticmethod
    def verifier(chemin: str, genesis: str = "GENESIS-MCS-J2") -> tuple:
        prev = genesis
        n = 0
        with open(chemin, encoding="utf-8") as f:
            for ligne in f:
                rec = json.loads(ligne)
                h = rec.pop("record_hash")
                if rec.get("prev_hash") != prev:
                    return False, n
                if hashlib.sha256(JournalChaine._canon(rec)).hexdigest() != h:
                    return False, n
                prev = h
                n += 1
        return True, n
