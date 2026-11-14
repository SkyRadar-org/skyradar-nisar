"""Fast area-of-interest reader for NISAR L2 GCOV HDF5 files on NASA Earthdata Cloud.

Why: a GCOV frame is ~6 GB. Reading a sub-window with h5py over HTTPS is slow (many tiny requests, each
redirected 303 -> CloudFront, and h5py serialises all reads). Instead we:
  1. resolve the signed CloudFront URL once (ASF redirects authenticated requests),
  2. read the HDF5 metadata once to get the byte offset/size of every 512x512 chunk in the window,
  3. download those compressed chunks in parallel with HTTP Range requests,
  4. decompress (shuffle + gzip) and assemble them ourselves.
Output is bit-identical to h5py reads (checked on 2026-06-17, track 047D).

Auth: set EARTHDATA_TOKEN (Earthdata Login bearer token, https://urs.earthdata.nasa.gov/profile -> Generate Token).
"""
import os, time, zlib, urllib.request
from concurrent.futures import ThreadPoolExecutor
import fsspec, h5py, numpy as np
from pyproj import Transformer

GRID = "/science/LSAR/GCOV/grids/frequencyA"


class _NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, *a, **k):
        return None


def _auth_headers():
    tok = os.environ.get("EARTHDATA_TOKEN")
    return {"Authorization": f"Bearer {tok}"} if tok else {}


def presigned(url):
    """Return the signed CloudFront URL ASF redirects to (valid for a limited time)."""
    op = urllib.request.build_opener(_NoRedirect)
    req = urllib.request.Request(url, headers={"Range": "bytes=0-0", **_auth_headers()})
    try:
        op.open(req, timeout=60)
    except urllib.error.HTTPError as e:
        if e.code in (301, 302, 303, 307):
            loc = e.headers["Location"]
            if "urs.earthdata.nasa.gov" in loc:
                raise PermissionError("Earthdata login required: set EARTHDATA_TOKEN") from None
            return loc
        raise
    return url


def _unshuffle(buf, itemsize):
    return np.frombuffer(buf, dtype=np.uint8).reshape(itemsize, -1).T.copy().tobytes()


def read_window(url, layers, bbox_lonlat, workers=24):
    """Read `layers` (e.g. ["HHHH", "HVHV", "mask"]) of a GCOV file inside a lon/lat bbox (W, S, E, N).

    Returns (arrays, info). info["x0"], info["y0"] are the projected coordinates of the CENTRE of the first pixel;
    info["epsg"] is the grid CRS; info["spacing"] the pixel size (m).
    """
    cf = presigned(url)
    fs = fsspec.filesystem("http", client_kwargs={"trust_env": True})
    f = fs.open(cf, "rb", block_size=2 << 20, cache_type="blockcache")
    h = h5py.File(f, "r")
    g = h[GRID]
    epsg = int(g["projection"][()])
    x = g["xCoordinates"][:]; y = g["yCoordinates"][:]
    tr = Transformer.from_crs(4326, epsg, always_xy=True)
    W, S, E, N = bbox_lonlat
    xs, ys = tr.transform([W, E, W, E], [S, S, N, N])
    c0, c1 = np.searchsorted(x, [min(xs), max(xs)])
    r0, r1 = np.searchsorted(-y, [-max(ys), -min(ys)])
    jobs = {}
    for k in layers:
        d = g[k]; ch = d.chunks
        cr = range(r0 // ch[0], (r1 - 1) // ch[0] + 1); cc = range(c0 // ch[1], (c1 - 1) // ch[1] + 1)
        lst = []
        for i in cr:
            for j in cc:
                ci = d.id.get_chunk_info_by_coord((i * ch[0], j * ch[1]))
                lst.append((i, j, ci.byte_offset, ci.size))
        jobs[k] = (d.dtype, ch, list(d._filters.keys()), cr, cc, lst)
    spacing = float(g["xCoordinateSpacing"][()])
    h.close(); f.close()

    def fetch(item):
        i, j, off, size = item
        req = urllib.request.Request(cf, headers={"Range": f"bytes={off}-{off + size - 1}"})
        for attempt in range(4):
            try:
                return item, urllib.request.urlopen(req, timeout=120).read()
            except Exception:
                time.sleep(2 * (attempt + 1))
        raise RuntimeError(f"chunk fetch failed at offset {off}")

    out, info = {}, {"bytes": {}}
    for k, (dtype, ch, filters, cr, cc, lst) in jobs.items():
        arr = np.full((len(cr) * ch[0], len(cc) * ch[1]), np.nan if dtype.kind == "f" else 255, dtype=dtype)
        nbytes = 0
        with ThreadPoolExecutor(workers) as ex:
            for (i, j, off, size), raw in ex.map(fetch, lst):
                nbytes += len(raw)
                buf = zlib.decompress(raw) if "gzip" in filters else raw
                if "shuffle" in filters:
                    buf = _unshuffle(buf, dtype.itemsize)
                arr[(i - cr.start) * ch[0]:(i - cr.start + 1) * ch[0], (j - cc.start) * ch[1]:(j - cc.start + 1) * ch[1]] = \
                    np.frombuffer(buf, dtype=dtype).reshape(ch)
        rr0, cc0 = r0 - cr.start * ch[0], c0 - cc.start * ch[1]
        out[k] = arr[rr0:rr0 + (r1 - r0), cc0:cc0 + (c1 - c0)]
        info["bytes"][k] = nbytes
    info.update(x0=float(x[c0]), y0=float(y[r0]), epsg=epsg, spacing=spacing)
    return out, info
