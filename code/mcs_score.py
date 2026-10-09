"""mcs_score.py — Operateur MCS (jalon 2).

Sigma = min_g z_g : la stabilite est le maillon le plus faible.
Aucune moyenne de preuves n'est autorisee (manifeste MCS v0.1, section 2).

Verdicts : CS+, CSp, CS-, CSi, CS0 (test impuissant).
Double contrainte pour les cartes spectrales (MCS-02, section 9) :
la coincidence doit vivre sur les donnees ET mourir sous surrogates.

Aucune donnee reelle ici : ce module est valide sur synthetique (jalon 2).
Les seuils sont geles conformement aux cartes v0.1.
"""
from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass

# --- Seuils geles (cartes v0.1) ---------------------------------------------
SEUILS_GELES = {
    "MCS-01": 3.0,   # carte MCS-01, section 8
    "MCS-02": 3.3,   # carte MCS-02, section 8 (regard ailleurs : 11 invariants)
    "MCS-03": 3.4,   # carte MCS-03, section 8 (2 correspondances deja enterrees)
    "DEFAULT": 3.0,
}
SEUIL_CSI = -2.0          # inversion stable
SEUIL_CSP = 2.0           # borne basse de la stabilite locale
SEUIL_CONTROLE = 2.0      # un controle positif doit produire un effet >= 2 u_null
SEUIL_EFFONDREMENT = -2.0 # double contrainte : mort sous surrogates


def z_score(m: float, mu_null: float, u_null: float) -> float:
    """Marge normalisee d'une mesure contre son modele nul."""
    if u_null <= 0:
        raise ValueError("u_null nul : modele nul degenere, verdict impossible")
    return (m - mu_null) / u_null


def sigma(z_par_g: dict, exclure: tuple = ()) -> float:
    """Sigma = minimum des z sur les deformations retenues (maillon le plus faible)."""
    vals = [z for g, z in z_par_g.items() if g not in exclure]
    if not vals:
        raise ValueError("aucune deformation retenue pour Sigma")
    return min(vals)


def controles_ok(controles: dict) -> tuple:
    """controles : {nom: effet_en_unites_u_null}. Un controle est muet si son
    effet < SEUIL_CONTROLE : le banc est aveugle sur cet axe."""
    muets = [nom for nom, effet in controles.items() if effet < SEUIL_CONTROLE]
    return (len(muets) == 0, muets)


@dataclass
class Verdict:
    verdict: str
    sigma: float
    seuil: float
    motif: str
    z_par_g: dict
    controles: dict

    def to_dict(self) -> dict:
        return {
            "verdict": self.verdict,
            "sigma": round(self.sigma, 6),
            "seuil": self.seuil,
            "motif": self.motif,
            "z_par_g": {g: round(z, 6) for g, z in self.z_par_g.items()},
            "controles": {c: round(e, 6) for c, e in self.controles.items()},
        }


def _verdict_simple(sigma_val: float, seuil: float) -> tuple:
    if sigma_val <= SEUIL_CSI:
        return "CSi", "inversion stable (Sigma <= -2), publication prioritaire"
    if sigma_val >= seuil:
        return "CS+", "coincidence stable : survit a toutes les deformations"
    if sigma_val >= SEUIL_CSP:
        return "CSp", "stabilite locale ; hors-echantillon non demontre"
    return "CS-", "artefact probable ; publication B3-FAIL"


def evaluer(carte_id: str, z_par_g: dict, controles: dict,
            exclure: tuple = ()) -> Verdict:
    """Verdict standard (cartes MCS-01, MCS-03)."""
    seuil = SEUILS_GELES.get(carte_id, SEUILS_GELES["DEFAULT"])
    ok, muets = controles_ok(controles)
    s = sigma(z_par_g, exclure=exclure)
    if not ok:
        return Verdict("CS0", s, seuil,
                       f"controles positifs muets : {muets} ; test impuissant",
                       z_par_g, controles)
    v, motif = _verdict_simple(s, seuil)
    return Verdict(v, s, seuil, motif, z_par_g, controles)


def evaluer_double(carte_id: str, z_par_g: dict, z_effondrement: float,
                   controles: dict, g_surrogate: str = "g1_iaaft") -> Verdict:
    """Verdict a double contrainte (carte MCS-02, section 9).

    (a) Sigma >= seuil sur les donnees reelles ;
    (b) z_effondrement <= -2 : la mesure s'effondre sous surrogates IAAFT.
    (a) sans (b) => CS- deguise : la coincidence etait spectrale, generique.
    """
    seuil = SEUILS_GELES.get(carte_id, SEUILS_GELES["DEFAULT"])
    ok, muets = controles_ok(controles)
    s = sigma(z_par_g, exclure=(g_surrogate,))
    if not ok:
        return Verdict("CS0", s, seuil,
                       f"controles positifs muets : {muets} ; test impuissant",
                       z_par_g, controles)
    a = s >= seuil
    b = z_effondrement <= SEUIL_EFFONDREMENT
    if s <= SEUIL_CSI:
        return Verdict("CSi", s, seuil,
                       "inversion stable sur donnees reelles", z_par_g, controles)
    if a and b:
        return Verdict("CS+", s, seuil,
                       "structure de phase inter-domaines stable "
                       "(vit sur donnees, meurt sous IAAFT)", z_par_g, controles)
    if a and not b:
        return Verdict("CS-", s, seuil,
                       "CS- deguise : survit aux surrogates ; la coincidence "
                       "etait spectrale, donc generique", z_par_g, controles)
    if b and not a:
        return Verdict("CSp", s, seuil,
                       "meurt sous IAAFT mais Sigma insuffisant sur donnees",
                       z_par_g, controles)
    return Verdict("CS-", s, seuil, "ni (a) ni (b) : artefact probable",
                   z_par_g, controles)


# --- Journal chaine SHA-256 (meme doctrine que acq_v1/analyse_v1) -----------
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
        """Le hachage porte sur l'enregistrement COMPLET incluant prev_hash
        (comme a l'ecriture) ; seul record_hash est exclu."""
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
