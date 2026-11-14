"""Check NASA GIBS NISAR tile availability for every frame date, and the alignment of our water overlay with GIBS.

    python -m skyradar_nisar.check_gibs
Writes data/web/gibs_availability.json ({date: {"tiles_ok": n, "tiles_tested": m}}) and docs/figures/check_gibs_overlay.png.
"""
import io, json, math, urllib.request
import numpy as np
from PIL import Image
from . import config as C

Z = 9


def tile_xy(lat, lon, z=Z):
    n = 2 ** z
    return (lon + 180) / 360 * n, (1 - math.asinh(math.tan(math.radians(lat))) / math.pi) / 2 * n


def get_tile(tpl, date, x, y, z=Z):
    try:
        d = urllib.request.urlopen(tpl.format(date=date, z=z, x=x, y=y), timeout=60).read()
        return d if len(d) > 500 else None   # GIBS returns a ~288-byte empty PNG where there is no data
    except Exception:
        return None


def main():
    m = json.loads((C.WEB / "manifest.json").read_text(encoding="utf-8"))
    tpl = m["gibs_template"]
    (S, W), (N, E) = m["bounds"]
    x0, y0 = tile_xy(N, W); x1, y1 = tile_xy(S, E)
    tiles = [(x, y) for x in range(int(x0), int(x1) + 1) for y in range(int(y0), int(y1) + 1)]
    avail = {}
    for f in m["frames"]:
        ok = sum(get_tile(tpl, f["date"], x, y) is not None for x, y in tiles)
        avail[f["key"]] = dict(date=f["date"], track=f["track"], tiles_ok=ok, tiles_tested=len(tiles))
        print(f["key"], ok, "/", len(tiles), flush=True)
    (C.WEB / "gibs_availability.json").write_text(json.dumps(avail, indent=1))

    # alignment check on one flood date: GIBS mosaic + our water overlay edges
    f = next(fr for fr in m["frames"] if fr["key"] == "2026-10-03_047D")
    tx0, ty0, tx1, ty1 = int(x0), int(y0), int(x1), int(y1)
    mos = Image.new("RGB", ((tx1 - tx0 + 1) * 256, (ty1 - ty0 + 1) * 256))
    for x, y in tiles:
        d = get_tile(tpl, f["date"], x, y)
        if d:
            mos.paste(Image.open(io.BytesIO(d)).convert("RGB"), ((x - tx0) * 256, (y - ty0) * 256))
    # paste the EPSG:4326 water PNG into Web Mercator pixel space row by row (latitude-dependent scale)
    wat = np.array(Image.open(C.WEB / f["png"]).convert("RGBA"))
    H, Wd = wat.shape[:2]
    out = np.array(mos)
    for r in range(0, H, 1):
        lat = N - (r + 0.5) / H * (N - S)
        py = int((tile_xy(lat, W)[1] - ty0) * 256)
        if not 0 <= py < out.shape[0]:
            continue
        cols = np.arange(Wd)
        lon = W + (cols + 0.5) / Wd * (E - W)
        px = ((tile_xy(lat, 0)[0] * 0 + (lon + 180) / 360 * 2 ** Z) - tx0) * 256
        px = px.astype(int); ok = (px >= 0) & (px < out.shape[1]) & (wat[r, :, 3] > 0)
        edge = ok & (np.roll(wat[r, :, 3] > 0, 1) != (wat[r, :, 3] > 0))   # outline of water patches only
        out[py, px[edge]] = (255, 255, 0)
    a = (tile_xy(N, W)[0] - tx0) * 256, (tile_xy(N, W)[1] - ty0) * 256
    b = (tile_xy(S, E)[0] - tx0) * 256, (tile_xy(S, E)[1] - ty0) * 256
    crop = Image.fromarray(out).crop((int(a[0]), int(a[1]), int(b[0]), int(b[1])))
    (C.ROOT / "docs" / "figures").mkdir(parents=True, exist_ok=True)
    crop.save(C.ROOT / "docs" / "figures" / "check_gibs_overlay.png")
    print("overlay check saved")


if __name__ == "__main__":
    main()
