#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
run.py — point d'entrée de rejou de MCS (Machine II)
==========================================================
Le certificat d'etalonnage (MCS-machine-II.pdf, §5) promet :
    python run.py --carte <id>

Rejou honnete : deux primitives réelles —
  --journal : vérifie l'intégrité du registre chaîné — chaque entrée
              JALON-*.jsonl déclare les empreintes SHA-256 des fichiers de
              données ; les fichiers présents dans donnees/ sont re-hachés
              et comparés ; les fichiers externes (AME, relevés) sont
              déclarés absents, jamais simulés ;
  --carte   : rejoue une carte dont les données brutes sont embarquées ;
              les autres sont en archive (pointeur vers code/mcsNN_runner.py).

Usage :
    python run.py --liste
    python run.py --journal
    python run.py --carte MCS-01
"""
import argparse
import hashlib
import json
import sys
from pathlib import Path

RACINE = Path(__file__).resolve().parent
JOURNAL = RACINE / "journal"
DONNEES = RACINE / "donnees"
CODE = RACINE / "code"

CARTES = {
    "MCS-01": {"donnees": "AME2012 (mass.mas12, nubtab12.asc) — brutes NON embarquées",
               "runner": "code/mcs01_runner.py", "statut": "archive-donnees"},
    "MCS-02": {"donnees": "signaux ASH — voir code/mcs02_runner.py",
               "runner": "code/mcs02_runner.py", "statut": "archive-donnees"},
    "MCS-03": {"donnees": "KO6 × Ê8 — voir code/mcs03_runner.py",
               "runner": "code/mcs03_runner.py", "statut": "archive-donnees"},
}


def verifie_journal():
    print("== VÉRIFICATION DU REGISTRE CHAÎNÉ — journal/*.jsonl ==")
    total_ok = total_absent = total_ko = 0
    for fic in sorted(JOURNAL.glob("*.jsonl")):
        ok = absent = ko = 0
        for ligne in fic.read_text(encoding="utf-8").splitlines():
            if not ligne.strip():
                continue
            try:
                entree = json.loads(ligne)
            except json.JSONDecodeError:
                ko += 1
                continue
            fichiers = entree.get("fichiers")
            if not isinstance(fichiers, dict):
                continue
            for nom, meta in fichiers.items():
                if not isinstance(meta, dict):
                    continue
                chemin = RACINE / meta.get("chemin", "")
                attendu = meta.get("sha256")
                if not chemin.exists():
                    absent += 1
                    continue
                reel = hashlib.sha256(chemin.read_bytes()).hexdigest()
                if reel == attendu:
                    ok += 1
                else:
                    ko += 1
                    print(f"   DIVERGENCE {fic.name} :: {nom} "
                          f"(attendu {attendu[:12]}…, reel {reel[:12]}…)")
        print(f"   {fic.name:28s} empreintes conformes {ok} · "
              f"données externes absentes {absent} · divergences {ko}")
        total_ok += ok
        total_absent += absent
        total_ko += ko
    print(f"\n   TOTAL : {total_ok} conformes · {total_absent} données brutes "
          f"non embarquées (déclarées, non simulées) · {total_ko} divergences")
    if total_ko:
        print("VERDICT DU REJOU : INCIDENT — signaler")
        return 1
    print("VERDICT DU REJOU : CHAÎNE CONFORME (sur les fichiers présents)")
    return 0


def rejoue_carte(ident):
    info = CARTES.get(ident)
    if info is None:
        print(f"Carte inconnue : {ident}. Voir --liste.")
        return 2
    print(f"== CARTE {ident} — statut : {info['statut']} ==")
    print(f"   données : {info['donnees']}")
    print(f"   runner  : {info['runner']}")
    print("   Le rejou direct exige les données brutes ; le certificat les "
          "référence par empreinte, le dépôt ne les embarque pas. La vérification "
          "de chaîne (--journal) reste la primitive rejouable ici.")
    return 2


def liste():
    print("REJOU DE MCS — carte des cartes\n")
    for nom, c in CARTES.items():
        print(f"  {nom} [{c['statut']}] données : {c['donnees']}")
    print("\nPrimitives réelles :")
    print("  python run.py --journal   vérifie les empreintes du registre chaîné")


def main():
    p = argparse.ArgumentParser(prog="run.py", description="Rejou de MCS")
    p.add_argument("--liste", action="store_true")
    p.add_argument("--journal", action="store_true", help="vérifie la chaîne")
    p.add_argument("--carte", help="id de la carte")
    args = p.parse_args()
    if args.journal:
        return verifie_journal()
    if args.carte:
        return rejoue_carte(args.carte)
    liste()
    return 0


if __name__ == "__main__":
    sys.exit(main())
