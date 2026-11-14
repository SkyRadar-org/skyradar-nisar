"""SkyRadar NISAR Water Pulse — backend API (read-only, serves the static NISAR data package).

Run:  uvicorn app.main:app --reload        Docs: /docs
"""
import os, unicodedata
from collections import Counter, defaultdict
from typing import Literal, Optional
from fastapi import FastAPI, HTTPException, Query, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.staticfiles import StaticFiles
from .data import DATA_DIR, store
from .frontend import router as frontend_router

app = FastAPI(title="SkyRadar NISAR Water Pulse API", version="0.2.0",
              description="Commune-level flood and recession monitoring for Mekong Delta rice land from NISAR L-band radar. "
                          "Data: NASA/JPL-Caltech & ISRO NISAR (ASF DAAC), OPERA DSWx (PO.DAAC), © OpenStreetMap contributors.")
app.include_router(frontend_router)
app.add_middleware(CORSMiddleware, allow_origins=os.environ.get("CORS_ORIGINS", "*").split(","), allow_methods=["GET"], allow_headers=["*"])
app.add_middleware(GZipMiddleware, minimum_size=1000)
app.mount("/static", StaticFiles(directory=DATA_DIR), name="static")   # /static/water/<date>_<track>.png, /static/summary/*.png


@app.middleware("http")
async def cache_headers(request: Request, call_next):
    resp = await call_next(request)
    if request.method == "GET" and resp.status_code == 200:   # data only changes when the package is re-synced
        resp.headers.setdefault("Cache-Control", "public, max-age=86400" if request.url.path.startswith("/static") else "public, max-age=300")
    return resp


def _fold(s):
    """Lower-case, strip Vietnamese diacritics (đ -> d) for accent-insensitive search."""
    s = unicodedata.normalize("NFD", (s or "").replace("đ", "d").replace("Đ", "D"))
    return "".join(ch for ch in s if unicodedata.category(ch) != "Mn").lower()

TRACKS = Literal["047D", "083A", "148D"]


def _frame(f):
    out = dict(f, png_url=f"/static/{f['png']}")
    if f.get("radar_jpg"):
        out["radar_url"] = f"/static/{f['radar_jpg']}"   # own radar background (GIBS breaks above zoom 10)
    return out


def _404(what):
    raise HTTPException(status_code=404, detail=f"{what} not found")


@app.get("/health")
def health():
    s = store()
    return {"status": "ok", "frames": len(s.manifest["frames"]), "communes": len(s.by_id)}


@app.get("/api/manifest")
def manifest():
    """Dates, tracks, maturity, overlay bounds ([[S, W], [N, E]]), GIBS tile template, water rule, attribution."""
    m = dict(store().manifest)
    m["frames"] = [_frame(f) for f in m["frames"]]
    return m


@app.get("/api/frames")
def frames(track: Optional[TRACKS] = None):
    """NISAR acquisitions (one per date and track) with the URL of the water overlay."""
    fr = store().manifest["frames"]
    return [_frame(f) for f in fr if track is None or f["track"] == track]


@app.get("/api/communes")
def communes():
    """GeoJSON of the communes with per-track timing and flood-release class."""
    return store().communes


@app.get("/api/communes/{osm_id}")
def commune(osm_id: int):
    s = store()
    if osm_id not in s.by_id:
        _404("commune")
    return s.commune_summary(osm_id)


@app.get("/api/communes/{osm_id}/series")
def commune_series(osm_id: int, track: Optional[TRACKS] = None):
    """Water % per acquisition date — one line per track (never average tracks: viewing geometry differs)."""
    s = store()
    if osm_id not in s.by_id:
        _404("commune")
    rows = [r for r in s.series.get(osm_id, []) if track is None or r["track"] == track]
    keep = ("date", "track", "maturity", "valid_km2", "water_km2", "water_pct")
    return [{k: r[k] for k in keep} for r in rows]


@app.get("/api/ranking")
def ranking(metric: Literal["last_pct", "peak_pct"] = "last_pct", track: TRACKS = "047D", limit: int = Query(20, ge=1, le=200),
            province: Optional[str] = None):
    """Communes ranked by water at the last image (default) or at the peak, for one track."""
    rows = [r for r in store().timing if r["track"] == track and (province is None or province.lower() in r["province"].lower())]
    rows.sort(key=lambda r: -(r[metric] or 0))
    return rows[:limit]


@app.get("/api/sowing-check")
def sowing_check(status: Optional[Literal["ready", "draining", "still_wet"]] = None, province: Optional[str] = None):
    """Sowing readiness per commune on the most recent covering image: ready < 10 %, draining 10-30 %, still_wet >= 30 % water."""
    rows = list(store().sowing.values())
    rows = [r for r in rows if (status is None or r["status"] == status) and (province is None or province.lower() in r["province"].lower())]
    rows.sort(key=lambda r: -(r["status_pct"] or 0))
    counts = {k: sum(r["status"] == k for r in store().sowing.values()) for k in ("ready", "draining", "still_wet")}
    return {"reference_date": rows[0]["ref_date"] if rows else None, "counts_all": counts, "communes": rows}


@app.get("/api/flood-release")
def flood_release(cls: Optional[Literal["A", "B", "C"]] = None):
    """Flood-release timing class per commune: A water in early & out while the river is high (controlled release timing),
    B other, C still wet at the last image."""
    rows = [r for r in store().flood_class.values() if cls is None or r["cls"] == cls]
    return sorted(rows, key=lambda r: (r["cls"], r["commune"]))


@app.get("/api/validation")
def validation():
    """Calibration (vs OPERA DSWx-S1 on 2 dates) and validation (vs DSWx-S1 and optical DSWx-HLS)."""
    return store().validation


@app.get("/api/search")
def search(q: str = Query(..., min_length=2), limit: int = Query(10, ge=1, le=50)):
    """Find communes by name, accent-insensitive ("son kien" -> Xã Sơn Kiên)."""
    fq = _fold(q)
    out = []
    for oid, f in store().by_id.items():
        p = f["properties"]
        if fq in _fold(p["name"]) or fq in _fold(p["province"]):
            out.append(dict(osm_id=oid, name=p["name"], province=p["province"], sowing_status=(store().sowing.get(oid) or {}).get("status")))
    out.sort(key=lambda r: (not _fold(r["name"]).endswith(fq), r["name"]))
    return out[:limit]


@app.get("/api/provinces")
def provinces():
    """Per-province overview: communes by sowing status and by flood-release class."""
    s = store()
    agg = defaultdict(lambda: {"communes": 0, "sowing": Counter(), "flood_release": Counter()})
    for oid, f in s.by_id.items():
        prov = f["properties"]["province"]; a = agg[prov]; a["communes"] += 1
        if oid in s.sowing:
            a["sowing"][s.sowing[oid]["status"]] += 1
        if oid in s.flood_class:
            a["flood_release"][s.flood_class[oid]["cls"]] += 1
    return [dict(province=k, communes=v["communes"], sowing=dict(v["sowing"]), flood_release=dict(v["flood_release"]))
            for k, v in sorted(agg.items(), key=lambda kv: -kv[1]["communes"])]
