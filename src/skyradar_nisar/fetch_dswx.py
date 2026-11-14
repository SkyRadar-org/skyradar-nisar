"""Mosaic OPERA DSWx reference water maps onto the 20 m grid for each NISAR acquisition date.

    python -m skyradar_nisar.fetch_dswx s1    # DSWx-S1 (Sentinel-1, C-band), +-1 day  -> calibration/validation
    python -m skyradar_nisar.fetch_dswx hls   # DSWx-HLS (Landsat/Sentinel-2, optical), +-2 days, clear pixels only
DSWx-S1 WTR: 0 not water, 1 open water, 3 inundated vegetation, 250/251 masked, 255 no data.
DSWx-HLS WTR: 0 not water, 1 open water, 2 partial surface water, 252-254 masked/cloud, 255 no data.
"""
import json, sys, time, datetime as dt, urllib.request
import numpy as np, rasterio
from rasterio.warp import reproject, Resampling
from . import config as C
from .cmr import granules, https_link
from .fastread import _auth_headers
from .grid import Grid

PRODUCTS = {"s1": ("OPERA_L3_DSWX-S1_V1", 1, [0, 1, 3]), "hls": ("OPERA_L3_DSWX-HLS_V1", 2, [0, 1, 2])}


def main(kind="s1"):
    short, window, valid_classes = PRODUCTS[kind]
    grid = Grid()
    qa = json.loads((C.PROCESSED / "qa.json").read_text())
    raw = C.RAW / f"dswx_{kind}"; raw.mkdir(parents=True, exist_ok=True)
    out = C.PROCESSED / f"dswx_{kind}"; out.mkdir(parents=True, exist_ok=True)
    G = granules(short, C.AOI, C.START, C.END)
    for k in sorted(qa):
        if kind == "hls" and k[:10] < C.FLOOD_SEASON_START:
            continue   # optical scenes before August are almost always cloudy; validation uses the flood season
        nd = dt.date.fromisoformat(k[:10])
        near = sorted([g for g in G if abs((dt.date.fromisoformat(g["time_start"][:10]) - nd).days) <= window],
                      key=lambda g: abs((dt.date.fromisoformat(g["time_start"][:10]) - nd).days))
        mosaic = np.full(grid.shape, 255, np.uint8)
        for g in near:
            u = https_link(g, "_B01_WTR.tif")
            if not u:
                continue
            fn = raw / u.rsplit("/", 1)[-1]
            if not fn.exists():
                for a in range(5):
                    try:
                        fn.write_bytes(urllib.request.urlopen(urllib.request.Request(u, headers=_auth_headers()), timeout=180).read()); break
                    except Exception:
                        time.sleep(5 * (a + 1))
                else:
                    continue
            with rasterio.open(fn) as s:
                dst = np.full(grid.shape, 255, np.uint8)
                reproject(s.read(1), dst, src_transform=s.transform, src_crs=s.crs, dst_transform=grid.transform,
                          dst_crs=f"EPSG:{grid.epsg}", resampling=Resampling.nearest, src_nodata=255, dst_nodata=255)
            fill = ~np.isin(mosaic, valid_classes) & np.isin(dst, valid_classes)   # closest date wins
            mosaic[fill] = dst[fill]
        with rasterio.open(out / f"{k}_WTR.tif", "w", **grid.profile("uint8", 255)) as d:
            d.write(mosaic, 1)
        print(k, len(near), "granules, valid", round(float(np.isin(mosaic, valid_classes).mean() * 100), 1), "%", flush=True)


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "s1")
