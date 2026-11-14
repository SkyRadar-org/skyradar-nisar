"""Build the small static data package for the web app (data/web).

    python -m skyradar_nisar.export_web
  manifest.json            dates, tracks, maturity, image bounds (lon/lat), file names, attribution
  water/<date>_<track>.png  transparent PNG, water in blue, EPSG:4326 (use as an image overlay with the bounds)
  summary/recession.png, first_flood.png
  communes.geojson         simplified commune polygons + latest/peak stats per track
  stats/*.csv              copied from data/processed/stats (+ validation)
"""
import json, shutil, csv
import numpy as np, rasterio
from rasterio.warp import calculate_default_transform, reproject, Resampling
from PIL import Image
from shapely.geometry import shape, mapping
from . import config as C

ATTRIBUTION = ("NISAR GCOV: NASA/JPL-Caltech & ISRO, distributed by ASF DAAC. Reference water: OPERA DSWx-S1/DSWx-HLS (JPL, PO.DAAC). "
               "Basemap/boundaries: (c) OpenStreetMap contributors (ODbL). Processing: SkyRadar team.")


def _to_4326(src_path, scale=2):
    with rasterio.open(src_path) as s:
        tf, w, h = calculate_default_transform(s.crs, "EPSG:4326", s.width // scale, s.height // scale, *s.bounds)
        dst = np.full((h, w), s.nodata if s.nodata is not None else 0, s.dtypes[0])
        reproject(rasterio.band(s, 1), dst, dst_transform=tf, dst_crs="EPSG:4326", resampling=Resampling.nearest)
    W, N = tf.c, tf.f; E = W + tf.a * w; S = N + tf.e * h
    return dst, [[float(S), float(W)], [float(N), float(E)]]   # Leaflet-style [[south, west], [north, east]]


def main():
    P, OUT = C.PROCESSED, C.WEB
    for d in ["water", "summary", "stats"]:
        (OUT / d).mkdir(parents=True, exist_ok=True)
    qa = json.loads((P / "qa.json").read_text())
    frames, bounds = [], None
    for k in sorted(qa):
        f = P / f"water/{k}_water.tif"
        if not f.exists():
            continue
        a, bounds = _to_4326(f)
        rgba = np.zeros(a.shape + (4,), np.uint8); rgba[a == 1] = (30, 110, 230, 200)
        Image.fromarray(rgba).save(OUT / f"water/{k}.png", optimize=True)
        frames.append(dict(key=k, date=k[:10], track=k[11:], maturity=qa[k]["maturity"], png=f"water/{k}.png",
                           gibs_date=k[:10]))
    # timing maps: colour by date (blue early -> red late); purple = still wet on last image
    for name, lo, hi in [("recession_day", 115, 160), ("first_flood_day", 60, 150)]:
        a, _ = _to_4326(P / f"summary/{name}.tif")
        rgba = np.zeros(a.shape + (4,), np.uint8)
        m = (a >= lo) & (a <= hi); t = (a[m] - lo) / (hi - lo)
        rgba[m] = np.stack([255 * t, 80 + 100 * (1 - t), 255 * (1 - t), np.full_like(t, 210)], -1).astype(np.uint8)
        rgba[a == 9999] = (130, 0, 140, 210)
        Image.fromarray(rgba).save(OUT / f"summary/{name.replace('_day', '')}.png", optimize=True)
    # communes with stats
    fc = json.loads((C.DATA / "boundaries" / "communes_aoi.geojson").read_text())
    timing = list(csv.DictReader(open(P / "stats/commune_flood_timing.csv")))
    by = {}
    for r in timing:
        by.setdefault(int(r["osm_id"]), {})[r["track"]] = {k: r[k] for k in ("peak_pct", "peak_date", "first_date_ge20pct",
                                                                            "halved_after_peak", "last_date", "last_pct")}
    cls_path = P / "stats/commune_flood_class.csv"
    cls = {int(r["osm_id"]): r["cls"] for r in csv.DictReader(open(cls_path))} if cls_path.exists() else {}
    feats = []
    for f in fc["features"]:
        g = shape(f["geometry"]).simplify(0.0004, preserve_topology=True)
        oid = f["properties"]["osm_id"]
        feats.append({"type": "Feature", "properties": {**f["properties"], "timing": by.get(oid, {}),
                                                       "flood_class": cls.get(oid)},   # A early-in/early-out, B other, C still wet
                      "geometry": mapping(g)})
    (OUT / "communes.geojson").write_text(json.dumps({"type": "FeatureCollection", "features": feats}, ensure_ascii=False))
    for src in list((P / "stats").glob("*.csv")) + list((P / "validation").glob("*.csv")) + list((P / "validation").glob("*.json")):
        shutil.copy(src, OUT / "stats" / src.name)
    (OUT / "manifest.json").write_text(json.dumps(dict(
        aoi=C.AOI, bounds=bounds, frames=frames, tracks=sorted({f["track"] for f in frames}),
        rule=dict(th_hh_db=C.TH_HH_DB, th_hv_db=C.TH_HV_DB, mmu_ha=C.MMU_PX * C.RES ** 2 / 1e4),
        timing_png=dict(recession="summary/recession.png", first_flood="summary/first_flood.png",
                        day_zero="2026-06-01", legend="blue=early, red=late, purple=still wet at last image"),
        gibs_template="https://gibs.earthdata.nasa.gov/wmts/epsg3857/best/NISAR_L2_Geocoded_Polarimetric_Covariance/default/{date}/GoogleMapsCompatible_Level13/{z}/{y}/{x}.png",
        attribution=ATTRIBUTION), indent=1, ensure_ascii=False))
    print(len(frames), "frames exported to", OUT)


if __name__ == "__main__":
    main()
