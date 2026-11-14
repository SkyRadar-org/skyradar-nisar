"""Calibrate the water thresholds against DSWx-S1 and validate (DSWx-S1 on other dates; DSWx-HLS optical, clear pixels).

    python -m skyradar_nisar.calibrate
Outputs data/processed/validation/*.csv and calibration.json.
"""
import json, csv
import numpy as np, rasterio
from . import config as C
from .grid import read_db
from .water import water_map, permanent_water

CAL_DATES = ["2026-06-17_047D", "2026-09-21_047D"]


def _rd(p):
    with rasterio.open(p) as s:
        return s.read(1)


def scores(pred, ref):
    tp = int(np.sum(pred & ref)); fp = int(np.sum(pred & ~ref)); fn = int(np.sum(~pred & ref))
    p = tp / max(tp + fp, 1); r = tp / max(tp + fn, 1)
    return dict(precision=round(p, 3), recall=round(r, 3), f1=round(2 * p * r / max(p + r, 1e-9), 3), iou=round(tp / max(tp + fp + fn, 1), 3))


def main():
    P = C.PROCESSED; out = P / "validation"; out.mkdir(parents=True, exist_ok=True)
    qa = json.loads((P / "qa.json").read_text())
    keys = [k for k in sorted(qa) if (P / f"dswx_s1/{k}_WTR.tif").exists()]
    load = lambda k: (read_db(P / f"gcov/{k}_HH.tif"), read_db(P / f"gcov/{k}_HV.tif"), _rd(P / f"dswx_s1/{k}_WTR.tif"))

    # 1) grid search on the calibration dates (pooled F1 vs DSWx-S1 open water), no MMU during search
    data = [load(k) for k in CAL_DATES]
    best = None
    for th in np.arange(-22, -11.9, 0.5):
        for tv in np.arange(-30, -18.9, 0.5):
            tp = fp = fn = 0
            for hh, hv, w in data:
                ok = np.isfinite(hh) & np.isfinite(hv) & np.isin(w, [0, 1, 3])
                pr = (hh < th) & (hv < tv) & ok; rf = (w == 1) & ok
                tp += np.sum(pr & rf); fp += np.sum(pr & ~rf); fn += np.sum(~pr & rf)
            f1 = 2 * tp / max(2 * tp + fp + fn, 1)
            if best is None or f1 > best[0]:
                best = (float(f1), float(th), float(tv))
    print("calibrated:", best)

    # 2) validation vs DSWx-S1 on land (permanent water removed)
    perm = permanent_water([_rd(P / f"dswx_s1/{k}_WTR.tif") for k in keys])
    rows = []
    for k in keys:
        hh, hv, w = load(k)
        pred, valid = water_map(hh, hv, best[1], best[2])
        ok = valid & np.isin(w, [0, 1, 3]) & ~perm
        rows.append(dict(key=k, role="calibration" if k in CAL_DATES else "validation", **scores(pred & ok, (w == 1) & ok)))
    _write(out / "vs_dswx_s1.csv", rows)

    # 3) independent check vs optical DSWx-HLS (clear pixels only), NISAR vs Sentinel-1
    hrows = []
    for k in keys:
        f = P / f"dswx_hls/{k}_WTR.tif"
        if not f.exists():
            continue
        h = _rd(f)
        hh, hv, w = load(k)
        pred, valid = water_map(hh, hv, best[1], best[2])
        ok = valid & np.isin(w, [0, 1, 3]) & np.isin(h, [0, 1, 2]) & ~perm
        if ok.mean() < 0.05:
            continue
        ref = np.isin(h, [1, 2]) & ok; s1 = (w == 1) & ok; n = pred & ok
        only = n & ~s1
        hrows.append(dict(key=k, clear_km2=round(ok.sum() * C.RES ** 2 / 1e6), nisar=scores(n, ref)["f1"], s1=scores(s1, ref)["f1"],
                          nisar_recall=scores(n, ref)["recall"], s1_recall=scores(s1, ref)["recall"],
                          nisar_only_is_optical_water_pct=round(float(ref[only].mean() * 100), 1) if only.any() else None))
    if hrows:
        _write(out / "vs_dswx_hls.csv", hrows)
    (out / "calibration.json").write_text(json.dumps(dict(th_hh_db=best[1], th_hv_db=best[2], pooled_f1=round(best[0], 3),
                                                          calibration_dates=CAL_DATES), indent=1))


def _write(path, rows):
    with open(path, "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
    print("wrote", path)


if __name__ == "__main__":
    main()
