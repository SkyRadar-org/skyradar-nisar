"""SWOT (NASA/CNES, Ka-band interferometric radar) water maps as a third, independent comparison source.

    python -m skyradar_nisar.swot            # download SWOT L2 HR Raster 100 m, compare, write tables
Needs the same Earthdata token as the other steps (PO.DAAC host archive.swot.podaac.earthdata.nasa.gov).

SWOT Raster cells exist only where the pixel cloud has water or near-water samples; dry land is *empty*, not 0.
We rebuild the swath footprint from the cross-track distance (10-60 km either side of nadir, the KaRIn swaths)
and treat empty cells inside it as dry when a SWOT sample lies within 1.5 km (larger voids = no data). Water = water_frac >= 0.5 with water_area_qual <= 1 (good/suspect).

Outputs (data/processed):
  swot/<date>_swot.tif                 uint8 0 dry, 1 water, 255 no data, on the common 20 m grid
  validation/vs_swot.csv               per SWOT date: nearest NISAR acquisition (<= 2 days), P/R/F1 of NISAR and of
                                       Sentinel-1 DSWx against SWOT on the same pixels, and SWOT against optical DSWx-HLS
  stats/commune_swot_by_date.csv       % water per commune on each SWOT date (communes with >= 5 km2 observed)
"""
import csv, datetime as dt, json, sys, time, urllib.request
import numpy as np, rasterio
from rasterio.transform import from_origin
from rasterio.warp import reproject, Resampling
from . import config as C
from .cmr import granules
from .fastread import _auth_headers
from .grid import Grid
from .timing import commune_zones
from .water import permanent_water

SHORT = "SWOT_L2_HR_Raster_D"
MAIN_TILES = {("577", "087F"), ("396", "068F")}   # the two pass/tiles that cover most of the AOI (86 % and 77 %)
MAX_DAYS = 2
NEAR_M = 1500   # an empty cell is 'dry' only within this distance of a SWOT sample


def _rd(p):
    with rasterio.open(p) as s:
        return s.read(1)


def _granules():
    """{(date, pass, tile): https url} for the main tiles, newest file per acquisition."""
    out = {}
    for g in granules(SHORT, C.AOI, C.START, C.END):
        t = g["title"].split("_")
        if "_100m_UTM48" not in g["title"] or (t[11], t[12]) not in MAIN_TILES:
            continue
        u = next((l["href"] for l in g["links"] if l["href"].startswith("https://archive.swot") and l["href"].endswith(".nc")), None)
        if u:
            k = (g["time_start"][:10], t[11], t[12])
            if k not in out or u > out[k]:
                out[k] = u
    return out


def classify(fn, grid):
    """SWOT Raster file -> 0 dry / 1 water / 255 no data on the common grid."""
    import h5py
    with h5py.File(fn) as f:
        x, y = f["x"][:], f["y"][:]
        wf, q, ct = f["water_frac"][:], f["water_area_qual"][:], f["cross_track"][:]
    valid = wf < 1e30
    X, Y = np.meshgrid(x, y)
    m = valid & (np.abs(ct) < 1e30)
    coef, *_ = np.linalg.lstsq(np.c_[X[m], Y[m], np.ones(m.sum())], ct[m], rcond=None)   # cross-track ~ planar in UTM
    ctp = coef[0] * X + coef[1] * Y + coef[2]
    swath = (np.abs(ctp) > 10e3) & (np.abs(ctp) < 60e3)
    # Empty cells count as dry only near actual SWOT samples: large voids (no sample within NEAR_M) are data gaps,
    # not dry land (e.g. whole communes without a single sample on pass 577).
    from scipy.ndimage import distance_transform_edt
    near = distance_transform_edt(~valid) * float(x[1] - x[0]) <= NEAR_M
    swath &= near
    out = np.full(wf.shape, 255, np.uint8)
    out[swath] = 0
    out[swath & valid & (q <= 1) & (wf >= 0.5)] = 1
    out[swath & valid & (q > 1)] = 255
    if y[0] < y[-1]:
        out, y = out[::-1], y[::-1]
    res = float(x[1] - x[0])
    dst = np.full(grid.shape, 255, np.uint8)
    reproject(out, dst, src_transform=from_origin(x[0] - res / 2, y[0] + res / 2, res, res), src_crs="EPSG:32648",
              dst_transform=grid.transform, dst_crs=f"EPSG:{grid.epsg}", resampling=Resampling.nearest,
              src_nodata=255, dst_nodata=255)
    return dst


def _score(a, b, ok):
    a, b = a[ok], b[ok]
    tp = float(np.sum(a & b)); p = tp / max(float(a.sum()), 1); r = tp / max(float(b.sum()), 1)
    return round(p, 3), round(r, 3), round(2 * p * r / max(p + r, 1e-9), 3)


def main():
    grid = Grid(); P = C.PROCESSED
    raw = C.RAW / "swot"; raw.mkdir(parents=True, exist_ok=True)
    out = P / "swot"; out.mkdir(parents=True, exist_ok=True)
    G = _granules(); failed = []
    by_date = {}
    for (d, ps, tile), u in sorted(G.items()):
        fn = raw / u.rsplit("/", 1)[-1]
        if not fn.exists():
            for a in range(5):
                try:
                    fn.write_bytes(urllib.request.urlopen(urllib.request.Request(u, headers=_auth_headers()), timeout=600).read()); break
                except Exception as e:
                    err = e; time.sleep(5 * (a + 1))
            else:
                failed.append(f"{u} ({err})"); continue
        by_date.setdefault(d, []).append(fn)
    if failed:
        print("ERROR: SWOT download failed (check EARTHDATA_TOKEN / PO.DAAC access):", *failed, sep="\n  ", file=sys.stderr)
        sys.exit(1)
    for d, fns in sorted(by_date.items()):
        m = np.full(grid.shape, 255, np.uint8)
        for fn in fns:
            c = classify(fn, grid); fill = (m == 255) & (c != 255); m[fill] = c[fill]
        with rasterio.open(out / f"{d}_swot.tif", "w", **grid.profile("uint8", 255)) as w:
            w.write(m, 1)
        print(d, "SWOT observed", round(float((m != 255).mean() * 100), 1), "% of grid", flush=True)

    # comparison with the nearest NISAR acquisition (and Sentinel-1 / optical references of that acquisition)
    qa = json.loads((P / "qa.json").read_text(encoding="utf-8"))
    s1keys = [k for k in sorted(qa) if (P / f"dswx_s1/{k}_WTR.tif").exists()]
    perm = permanent_water([_rd(P / f"dswx_s1/{k}_WTR.tif") for k in s1keys])
    rows = []
    for d in sorted(by_date):
        sw = _rd(out / f"{d}_swot.tif"); dd = dt.date.fromisoformat(d)
        cands = []
        for k in qa:
            gap = abs((dt.date.fromisoformat(k[:10]) - dd).days)
            if gap <= MAX_DAYS and (P / f"water/{k}_water.tif").exists():
                n = _rd(P / f"water/{k}_water.tif"); ok = (sw != 255) & (n != 255) & ~perm
                cands.append((gap, -int(ok.sum()), k, n, ok))
        if not cands:
            continue
        gap, _, k, n, ok = min(cands, key=lambda c: c[:2])
        if ok.mean() < 0.05:
            continue
        r = dict(swot_date=d, nisar=k, days_apart=gap, overlap_km2=round(float(ok.sum()) * C.RES ** 2 / 1e6),
                 swot_water_pct=round(float((sw[ok] == 1).mean() * 100), 1), nisar_water_pct=round(float((n[ok] == 1).mean() * 100), 1))
        r["nisar_precision"], r["nisar_recall"], r["nisar_f1"] = _score(n == 1, sw == 1, ok)
        s1p = P / f"dswx_s1/{k}_WTR.tif"
        r.update(s1_overlap_km2=0, s1_f1=None, nisar_f1_same_px=None, s1_precision=None, s1_recall=None)
        if s1p.exists():
            s1 = _rd(s1p); ok2 = ok & np.isin(s1, [0, 1, 3])
            if ok2.mean() >= 0.05:
                r["s1_overlap_km2"] = round(float(ok2.sum()) * C.RES ** 2 / 1e6)
                r["s1_precision"], r["s1_recall"], r["s1_f1"] = _score(s1 == 1, sw == 1, ok2)
                r["nisar_f1_same_px"] = _score(n == 1, sw == 1, ok2)[2]
        r.update(swot_vs_optical_f1=None, nisar_vs_optical_f1=None)
        hp = P / f"dswx_hls/{k}_WTR.tif"
        if hp.exists():
            h = _rd(hp); ok3 = (sw != 255) & (n != 255) & ~perm & np.isin(h, [0, 1, 2])
            if ok3.sum() * C.RES ** 2 / 1e6 >= 50:
                r["swot_vs_optical_f1"] = _score(sw == 1, np.isin(h, [1, 2]), ok3)[2]
                r["nisar_vs_optical_f1"] = _score(n == 1, np.isin(h, [1, 2]), ok3)[2]
        rows.append(r); print(r, flush=True)
    (P / "validation").mkdir(exist_ok=True)
    with open(P / "validation/vs_swot.csv", "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, list(rows[0])); w.writeheader(); w.writerows(rows)

    # per-commune SWOT water % (same commune masks as timing.py)
    ids, props = commune_zones(grid)
    px_km2 = C.RES ** 2 / 1e6; crows = []
    for d in sorted(by_date):
        sw = _rd(out / f"{d}_swot.tif"); obs = (sw != 255) & ~perm
        nv = np.bincount(ids[obs], minlength=len(props) + 1)
        nw = np.bincount(ids[obs & (sw == 1)], minlength=len(props) + 1)
        for i, p in enumerate(props, start=1):
            if nv[i] * px_km2 >= 5:
                crows.append(dict(date=d, osm_id=p["osm_id"], commune=p["name"], province=p["province"],
                                  valid_km2=round(nv[i] * px_km2, 2), water_km2=round(nw[i] * px_km2, 2),
                                  water_pct=round(100 * nw[i] / nv[i], 1)))
    with open(P / "stats/commune_swot_by_date.csv", "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, list(crows[0])); w.writeheader(); w.writerows(crows)
    print(len(rows), "comparison dates,", len(crows), "commune rows")


if __name__ == "__main__":
    main()
