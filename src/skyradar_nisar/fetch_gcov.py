"""Fetch NISAR GCOV (HH, HV, mask) for the AOI, all dates of the configured tracks, onto the 20 m grid.

    python -m skyradar_nisar.fetch_gcov            # all tracks in config
    python -m skyradar_nisar.fetch_gcov 047D 083A  # selected tracks
Re-running skips acquisitions already processed (qa.json).
"""
import json, sys, time
import numpy as np
from . import config as C
from .cmr import gcov_acquisitions
from .fastread import read_window
from .grid import Grid, write_db


def main(tracks=None):
    tracks = {k: v for k, v in C.TRACKS.items() if not tracks or k in tracks}
    out = C.PROCESSED / "gcov"; out.mkdir(parents=True, exist_ok=True)
    qa_path = C.PROCESSED / "qa.json"
    qa = json.loads(qa_path.read_text()) if qa_path.exists() else {}
    grid = Grid()
    jobs = gcov_acquisitions(C.AOI, C.START, C.END, tracks)
    print(f"{len(jobs)} acquisitions", flush=True)
    for j in jobs:
        k = f"{j['date']}_{j['track']}"
        if k in qa and qa[k].get("crid") == j["crid"] and (out / f"{k}_HV.tif").exists():
            continue
        t0 = time.time()
        arr, info = read_window(j["url"], ["HHHH", "HVHV", "mask"], C.AOI)
        valid = (arr["mask"] > 0) & (arr["mask"] < 255)   # mask: 1..n = valid subswath, 0 = invalid, 255 = outside
        for pol, lay in [("HH", "HHHH"), ("HV", "HVHV")]:
            p = np.where(valid & (arr[lay] > 0), arr[lay], np.nan)
            with np.errstate(all="ignore"):
                db = 10 * np.log10(grid.from_native(p, info["x0"], info["y0"], info["spacing"]))
            write_db(out / f"{k}_{pol}.tif", db, grid)
        qa[k] = {kk: v for kk, v in j.items() if kk != "rank"}
        qa[k].update(seconds=round(time.time() - t0, 1), MB=round(sum(info["bytes"].values()) / 1e6),
                     valid_pct=round(float(np.isfinite(db).mean() * 100), 1))
        qa_path.write_text(json.dumps(qa, indent=1))
        print("ok", k, qa[k]["seconds"], "s", qa[k]["MB"], "MB, valid", qa[k]["valid_pct"], "%", flush=True)


if __name__ == "__main__":
    main(sys.argv[1:] or None)
