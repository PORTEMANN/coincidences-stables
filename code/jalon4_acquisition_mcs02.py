"""jalon4_acquisition_mcs02.py — Acquisition des donnees MCS-02 (jalon 4).

Ce script N'EST PAS le runner : il telecharge les donnees et fixe le tirage
des fenetres. Le runner (execution unique, hache separement) ne fait que
calculer sur les fichiers locaux. Tout est deterministe et publie :

  cle_selection = SHA-256("MCS-J4-SEL|" + empreinte_carte + "|" + empreinte_meta)
  empreinte_meta = SHA-256(canon des 4 fichiers de metadonnees :
    participants.tsv (EEG ds004584), allen_cells_humaines.json,
    cwru_fichiers.json, nsrdb_headers.json)

  Ordre des tirages (ChaCha20-IETF, nonce nulle) :
    1. EEG : permutation des 49 sujets Control -> 20 ; par sujet (dans l'ordre
       tire), permutation des fenetres disjointes de 10 s -> 3 ;
    2. ECG : permutation des 18 records ; 60 tirages (record cyclique, offset
       uniforme dans [0, duree-10]) ;
    3. Allen : permutation des 413 cellules -> 10 ; (apres telechargement)
       pool (cellule, sweep >= 12 s) -> permutation -> 60 fenetres (offset
       uniforme dans [0, duree_sweep-10]) ;
    4. CWRU 1 HP : permutation des 12 fichiers ; 60 tirages (fichier cyclique,
       offset uniforme) ; idem 3 HP (11 fichiers).

Deviations declarees (carte MCS-02 section 4, clause "ou equivalent") :
  - EEG : ds003778 remplace par ds004584 ("EEG Rest eyes open", OpenNeuro,
    49 controles sains, 63 canaux dont Cz et O1, 500 Hz, CC0) — ds003778 est
    un protocole de memoire, pas un repos yeux ouverts ;
  - ECG : derivation ECG1 (= lead II de la documentation nsrdb) ;
  - CWRU : 216.mat (B021 3 HP) et 3009-3012.mat inexistants (HTTP 404) ;
  - fenetres a offsets uniformes : chevauchement possible pour ECG, Allen et
    CWRU (declare ; les fenetres EEG sont disjointes par construction).
"""
from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys

import numpy as np
import scipy.io

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(RACINE, "code"))
from prng_chacha import PRNGChaCha  # noqa: E402

EMPREINTE_CARTE = "0aa840f23ca4516ae5f76342be950694d0dcd4c204e02ea7ad0c8b1f08fa167a"
D = os.path.join(RACINE, "donnees")
S3 = "https://s3.amazonaws.com/openneuro.org/ds004584"
CWRU_URL = "https://engineering.case.edu/sites/default/files/{}.mat"


def sha256_fichier(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()


def telecharge(url, dest, taille_min=1000, essais=3):
    for _ in range(essais):
        r = subprocess.run(["curl", "-sS", "-L", "-C", "-", "--max-time", "570",
                            "-o", dest, url], capture_output=True, text=True)
        if os.path.exists(dest) and os.path.getsize(dest) >= taille_min:
            return True
    return os.path.exists(dest) and os.path.getsize(dest) >= taille_min


def get_json_url(url):
    import urllib.request
    return json.load(urllib.request.urlopen(url, timeout=60))


def main():
    manifeste = {"carte": "MCS-02", "empreinte_carte": EMPREINTE_CARTE}

    # --- 0. metadonnees ------------------------------------------------------
    metas = ["eeg/participants.tsv", "allen_cells_humaines.json",
             "cwru_fichiers.json", "nsrdb_headers.json"]
    emp_meta = hashlib.sha256("\n".join(
        f"{m}:{sha256_fichier(os.path.join(D, m))}" for m in sorted(metas)
    ).encode()).hexdigest()
    cle_sel = hashlib.sha256(f"MCS-J4-SEL|{EMPREINTE_CARTE}|{emp_meta}".encode("ascii")).digest()
    rng = PRNGChaCha(cle_sel)
    manifeste["empreinte_meta"] = emp_meta
    manifeste["cle_selection_hex"] = cle_sel.hex()

    # --- 1. EEG : 20 sujets Control, 3 fenetres disjointes de 10 s -----------
    os.makedirs(f"{D}/eeg", exist_ok=True)
    lignes = open(f"{D}/eeg/participants.tsv").read().splitlines()
    controles = sorted(l.split("\t")[0] for l in lignes[1:] if l.split("\t")[1] == "Control")
    assert len(controles) == 49
    sujets = list(rng.permutation(np.array(controles)))[:20]
    manifeste["eeg_sujets"] = list(sujets)
    manifeste["eeg_fenetres"] = {}
    for sub in sorted(sujets):
        base = f"{S3}/{sub}/eeg/{sub}_task-Rest"
        ej = get_json_url(f"{base}_eeg.json")
        ch = get_json_url(f"{base}_channels.tsv") if False else None
        dur = float(ej["RecordingDuration"]); fs = float(ej["SamplingFrequency"])
        n_ch = int(ej["EEGChannelCount"])
        fdt = f"{D}/eeg/{sub}.fdt"
        ok = telecharge(f"{base}_eeg.fdt", fdt, taille_min=int(n_ch * fs * dur * 4 * 0.99))
        assert ok, f"echec fdt {sub}"
        # canaux (petit fichier)
        ch_tsv = subprocess.run(["curl", "-sS", "-L", "--max-time", "60", f"{base}_channels.tsv"],
                                capture_output=True, text=True).stdout
        canaux = [l.split("\t")[0] for l in ch_tsv.splitlines()[1:] if l.strip()]
        idx = {c: canaux.index(c) for c in ("Cz", "O1")}
        # verification du format multiplexe float32
        n_samples = os.path.getsize(fdt) // (4 * n_ch)
        assert os.path.getsize(fdt) == n_ch * n_samples * 4
        n_win = int(dur // 10)
        wins = list(rng.permutation(np.arange(n_win)))[:3]
        manifeste["eeg_fenetres"][sub] = {"fs": fs, "n_ch": n_ch, "n_samples": n_samples,
                                          "idx": idx, "fenetres": [int(w) for w in wins]}
        print(f"EEG {sub}: dur={dur:.1f}s {n_ch}ch fenetres={sorted(wins)}")

    # --- 2. ECG : 60 segments (record, offset) --------------------------------
    os.makedirs(f"{D}/ecg", exist_ok=True)
    headers = json.load(open(f"{D}/nsrdb_headers.json"))
    recs = sorted(headers)
    assert len(recs) == 18
    rec_perm = list(rng.permutation(np.array(recs)))
    import wfdb
    manifeste["ecg_fenetres"] = []
    for i in range(60):
        rec = rec_perm[i % 18]
        dur = headers[rec]["sig_len"] / headers[rec]["fs"]
        off = rng.uniform(0.0, dur - 10.0)
        s0 = int(off * 128)
        sig = wfdb.rdrecord(rec, pn_dir="nsrdb", sampfrom=s0, sampto=s0 + 1280, channels=[0])
        np.save(f"{D}/ecg/{rec}_{s0}.npy", sig.p_signal[:, 0].astype(np.float64))
        manifeste["ecg_fenetres"].append({"record": rec, "offset_ech": s0, "fs": 128,
                                          "fichier": f"ecg/{rec}_{s0}.npy"})
    print(f"ECG: 60 fenetres sur {len(set(f['record'] for f in manifeste['ecg_fenetres']))} records")

    # --- 3. Allen : 10 cellules, 60 fenetres ----------------------------------
    os.makedirs(f"{D}/allen", exist_ok=True)
    cells = json.load(open(f"{D}/allen_cells_humaines.json"))
    assert len(cells) == 413
    sel = list(rng.permutation(np.arange(len(cells))))[:10]
    cellules = [cells[i] for i in sel]
    manifeste["allen_cellules"] = [c["specimen_id"] for c in cellules]
    import h5py

    def plage_utile(arr):
        """Plus longue plage contigue non nulle : (debut, longueur) ou None.
        Les sweeps Allen sont zero-paddes (queue, parfois tete et trous)."""
        nz = np.nonzero(arr)[0]
        if nz.size == 0:
            return None
        gaps = np.where(np.diff(nz) > 1)[0]
        starts = np.r_[0, gaps + 1]
        ends = np.r_[gaps, nz.size - 1]
        i_best = int(np.argmax(ends - starts + 1))
        run = nz[starts[i_best]:ends[i_best] + 1]
        return int(run[0]), int(run.size)

    pool = []
    for c in cellules:
        sid = c["specimen_id"]; wkf = c["erwkf_id"]
        nwb = f"{D}/allen/cell_{sid}.nwb"
        ok = telecharge(f"https://celltypes.brain-map.org/api/v2/well_known_file_download/{wkf}",
                        nwb, taille_min=1000000)
        assert ok, f"echec nwb {sid}"
        with h5py.File(nwb, "r") as f:
            for k in f["acquisition"]["timeseries"].keys():
                ts = f["acquisition"]["timeseries"][k]
                rate = float(ts["starting_time"].attrs.get("rate"))
                pu = plage_utile(ts["data"][()])
                if pu is None:
                    continue
                s_run, n_run = pu
                if n_run / rate >= 12.0:
                    pool.append({"cellule": sid, "sweep": k, "n": n_run,
                                 "rate": rate, "debut": s_run})
    print(f"Allen: {len(cellules)} cellules, {len(pool)} sweeps >= 12 s")
    pool_perm = list(rng.permutation(np.arange(len(pool))))
    manifeste["allen_fenetres"] = []
    for i in range(60):
        p = pool[pool_perm[i % len(pool)]]
        off = rng.uniform(0.0, p["n"] / p["rate"] - 10.0)
        s0 = p["debut"] + int(off * p["rate"])
        with h5py.File(f"{D}/allen/cell_{p['cellule']}.nwb", "r") as f:
            x = f["acquisition"]["timeseries"][p["sweep"]]["data"][s0:s0 + int(10 * p["rate"])]
        x = np.asarray(x, dtype=np.float64)
        assert x.size == int(10 * p["rate"]) and np.all(np.isfinite(x)) and x.std() > 0, \
            f"fenetre Allen invalide ({p['cellule']}/{p['sweep']}@{s0})"
        np.save(f"{D}/allen/{p['cellule']}_{p['sweep']}_{s0}.npy", x)
        manifeste["allen_fenetres"].append({"cellule": p["cellule"], "sweep": p["sweep"],
                                            "offset_ech": s0, "fs": p["rate"],
                                            "fichier": f"allen/{p['cellule']}_{p['sweep']}_{s0}.npy"})

    # --- 4. CWRU 1 HP et 3 HP -------------------------------------------------
    os.makedirs(f"{D}/cwru", exist_ok=True)
    cwru = json.load(open(f"{D}/cwru_fichiers.json"))
    for hp, ids in (("1HP", cwru["1HP"]), ("3HP", cwru["3HP"])):
        fichiers = {}
        for i in ids:
            dest = f"{D}/cwru/{i}.mat"
            ok = telecharge(CWRU_URL.format(i), dest, taille_min=100000)
            assert ok, f"echec {i}.mat"
            mat = scipy.io.loadmat(dest)
            de = [k for k in mat if "DE_time" in k][0]
            x = mat[de].ravel()
            fs = 12000  # convention CWRU DE ; 48000 si le fichier est 4x plus long
            fichiers[i] = {"n": len(x), "cle": de}
        perm = list(rng.permutation(np.array(ids)))
        manifeste[f"cwru_{hp}"] = {"fichiers": fichiers, "fenetres": []}
        for i in range(60):
            fid = perm[i % len(perm)]
            n = fichiers[fid]["n"]
            # offsets a la resolution echantillon (fichiers ~12 s : les offsets
            # entiers en secondes produiraient des doublons massifs — declare)
            s0 = int(rng.uniform(0.0, (n - 120000) / 12000.0) * 12000.0)
            mat = scipy.io.loadmat(f"{D}/cwru/{fid}.mat")
            x = mat[fichiers[fid]["cle"]].ravel()[s0:s0 + 120000]
            x = np.asarray(x, dtype=np.float64)
            assert x.size == 120000 and x.std() > 0, f"fenetre CWRU invalide ({fid}@{s0})"
            np.save(f"{D}/cwru/{fid}_{s0}.npy", x)
            manifeste[f"cwru_{hp}"]["fenetres"].append(
                {"fichier_mat": fid, "offset_ech": s0, "fs": 12000,
                 "fichier": f"cwru/{fid}_{s0}.npy"})
        print(f"CWRU {hp}: 60 fenetres, fichiers {sorted(fichiers)}")

    # --- 5. empreintes ---------------------------------------------------------
    empreintes = {}
    for sous in ("eeg", "ecg", "allen", "cwru"):
        rep = os.path.join(D, sous)
        for nom in sorted(os.listdir(rep)):
            p = os.path.join(rep, nom)
            if os.path.isfile(p) and not nom.endswith((".tsv",)):
                empreintes[f"{sous}/{nom}"] = sha256_fichier(p)
    for extra in ("allen_cells_humaines.json", "cwru_fichiers.json", "nsrdb_headers.json"):
        empreintes[extra] = sha256_fichier(os.path.join(D, extra))
    canon = "\n".join(f"{k}:{empreintes[k]}" for k in sorted(empreintes))
    manifeste["empreintes_fichiers"] = empreintes
    manifeste["empreinte_donnees"] = hashlib.sha256(canon.encode()).hexdigest()
    with open(f"{D}/MANIFESTE-ACQUISITION-MCS02.json", "w", encoding="utf-8") as f:
        json.dump(manifeste, f, ensure_ascii=False, indent=1,
                  default=lambda o: int(o) if isinstance(o, np.integer)
                  else float(o) if isinstance(o, np.floating) else str(o))
    print("EMPREINTE_META    =", emp_meta)
    print("EMPREINTE_DONNEES =", manifeste["empreinte_donnees"])


if __name__ == "__main__":
    main()
