"""Per-date water maps, flood-timing rasters and commune statistics.

    python -m skyradar_nisar.timing
Outputs (data/processed):
  water/<date>_<track>_water.tif        uint8 0 dry, 1 water, 255 no data (permanent water excluded)
  summary/{flood_count,first_flood_day,recession_day}.tif   days since 2026-06-01; 9999 = still wet at last image
  stats/commune_water_by_date.csv       one row per commune x date x track (keep tracks separate!)
  stats/commune_flood_timing.csv        per commune: peak, first/last date >= 20 %, halved-after-peak date
"""
import csv, json, datetime as dt
import numpy as np, rasterio
from rasterio.features import rasterize
from shapely.geometry import shape
from shapely.ops import transform as stransform
from pyproj import Transformer
from . import config as C
from .grid import Grid, read_db
from .water import water_map, permanent_water

D0 = dt.date(2026, 6, 1)


def _rd(p):
    with rasterio.open(p) as s:
        return s.read(1)


def commune_zones(grid):
    fc = json.loads((C.DATA / "boundaries" / "communes_aoi.geojson").read_text(encoding="utf-8"))
    to = Transformer.from_crs(4326, grid.epsg, always_xy=True).transform
    zone = rasterize([(stransform(to, shape(f["geometry"])), i + 1) for i, f in enumerate(fc["features"])],
                     out_shape=grid.shape, transform=grid.transform, fill=0, dtype="int32")
    return zone, [f["properties"] for f in fc["features"]]


def main():
    P = C.PROCESSED; grid = Grid()
    for d in ["water", "summary", "stats"]:
        (P / d).mkdir(parents=True, exist_ok=True)
    qa = json.loads((P / "qa.json").read_text(encoding="utf-8")); keys = sorted(qa)
    s1 = [P / f"dswx_s1/{k}_WTR.tif" for k in keys if (P / f"dswx_s1/{k}_WTR.tif").exists()]
    perm = permanent_water([_rd(p) for p in s1]) if s1 else np.zeros(grid.shape, bool)
    zone, props = commune_zones(grid); nz = len(props) + 1
    maps, rows = {}, []
    for k in keys:
        w, valid = water_map(read_db(P / f"gcov/{k}_HH.tif"), read_db(P / f"gcov/{k}_HV.tif"))
        w &= ~perm
        m = np.where(valid, w.astype(np.uint8), 255).astype(np.uint8)
        with rasterio.open(P / f"water/{k}_water.tif", "w", **grid.profile("uint8", 255)) as dst:
            dst.write(m, 1)
        maps[k] = m
        v = np.bincount(zone[m != 255], minlength=nz); ww = np.bincount(zone[m == 1], minlength=nz)
        for z, pr in enumerate(props, start=1):
            if v[z] * C.RES ** 2 / 1e6 >= 3:
                rows.append(dict(date=k[:10], track=k[11:], maturity=qa[k]["maturity"], osm_id=pr["osm_id"], commune=pr["name"],
                                 province=pr["province"], valid_km2=round(v[z] * 4e-4, 2), water_km2=round(ww[z] * 4e-4, 2),
                                 water_pct=round(ww[z] / v[z] * 100, 1)))
    _write(P / "stats/commune_water_by_date.csv", rows)

    # flood timing over the season, all tracks merged by date (a water/dry map is geometry-independent)
    season = [k for k in keys if k[:10] >= C.FLOOD_SEASON_START]
    days = np.array([(dt.date.fromisoformat(k[:10]) - D0).days for k in season], np.int16)[:, None, None]
    st = np.stack([maps[k] for k in season]); obs = st != 255; wet = st == 1
    ever = wet.any(0); BIG = 32767
    first = np.where(wet, days, BIG).min(0); last = np.where(wet, days, -1).max(0)
    reces = np.where(obs & ~wet & (days > last[None]), days, BIG).min(0)
    for name, arr in [("flood_count", np.where(obs.any(0), wet.sum(0), 255)), ("first_flood_day", np.where(ever, first, -1)),
                      ("recession_day", np.where(ever, np.where(reces < BIG, reces, 9999), -1))]:
        dtype, nod = ("uint8", 255) if name == "flood_count" else ("int16", -1)
        with rasterio.open(P / f"summary/{name}.tif", "w", **grid.profile(dtype, nod)) as dst:
            dst.write(arr.astype(dtype), 1)

    # per-commune timing table (per track to avoid mixing viewing geometries; 047D first if present)
    tab = []
    by = {}
    for r in rows:
        by.setdefault((r["osm_id"], r["track"]), []).append(r)
    for (oid, trk), rs in by.items():
        rs.sort(key=lambda r: r["date"])
        seas = [r for r in rs if r["date"] >= C.FLOOD_SEASON_START and r["valid_km2"] >= 5]
        if not seas:
            continue
        pk = max(seas, key=lambda r: r["water_pct"])
        above = [r for r in seas if r["water_pct"] >= 20]
        halved = next((r["date"] for r in seas if r["date"] > pk["date"] and r["water_pct"] < pk["water_pct"] / 2), None)
        tab.append(dict(osm_id=oid, commune=rs[0]["commune"], province=rs[0]["province"], track=trk,
                        peak_pct=pk["water_pct"], peak_date=pk["date"], first_date_ge20pct=above[0]["date"] if above else None,
                        last_date_ge20pct=above[-1]["date"] if above else None, halved_after_peak=halved,
                        last_date=seas[-1]["date"], last_pct=seas[-1]["water_pct"]))
    _write(P / "stats/commune_flood_timing.csv", tab)


def _write(path, rows):
    with open(path, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
    print("wrote", path, len(rows), "rows")


if __name__ == "__main__":
    main()
