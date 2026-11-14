# water-pulse-be — SkyRadar NISAR Water Pulse API

Read-only API for the web app. It serves the static NISAR data package produced by the pipeline in this repository
(`../data/web`) — no database. Data folder lookup: `$WATER_PULSE_DATA`, else `./data` (bundled copy for deployment),
else `../data/web`.

## Run locally

```bash
pip install -r requirements.txt
uvicorn app.main:app --reload          # http://127.0.0.1:8000/docs
pytest -q
```

Run from this folder (`cd water-pulse-be`). For Docker/Vercel builds, bundle the data first: `scripts/sync_data.sh ..`
(copies `../data/web` into `./data`, which is git-ignored).
`WATER_PULSE_DATA` overrides the data folder; `CORS_ORIGINS` (comma-separated) restricts CORS (default `*`).

## Endpoints

| Path | Returns |
|---|---|
| `GET /health` | status, number of frames and communes |
| `GET /api/manifest` | dates, tracks, maturity, overlay `bounds` `[[S,W],[N,E]]`, `gibs_template`, water rule, `attribution`; each frame has `png_url` |
| `GET /api/frames?track=047D` | acquisitions of one track with `png_url` |
| `GET /static/water/{date}_{track}.png` | water overlay (EPSG:4326, `manifest.bounds`) |
| `GET /static/summary/{recession,first_flood}.png` | timing maps |
| `GET /api/communes` | GeoJSON of communes (`timing` per track, `flood_class`) |
| `GET /api/communes/{osm_id}` | one commune + flood-release class + sowing status |
| `GET /api/communes/{osm_id}/series?track=` | water % per date, **one line per track** |
| `GET /api/ranking?metric=last_pct\|peak_pct&track=047D&limit=20&province=` | communes ranked |
| `GET /api/sowing-check?status=ready\|draining\|still_wet&province=` | sowing readiness on the most recent covering image + counts |
| `GET /api/flood-release?cls=A\|B\|C` | flood-release timing class per commune |
| `GET /api/validation` | calibration + validation vs DSWx-S1 and optical DSWx-HLS |
| `GET /api/search?q=son kien` | accent-insensitive commune search |
| `GET /api/provinces` | per-province counts by sowing status and flood-release class |

Interactive documentation: `/docs` (Swagger) and `/redoc`; static copy of the schema in `docs/openapi.json`. Responses are gzip-compressed; JSON is cacheable for 5 min,
static overlays for 1 day.

## Deploy

- **Vercel:** `vercel deploy` (uses `api/index.py` + `vercel.json`, all routes go to the FastAPI app).
- **Docker / Render / Railway:** `docker build -t water-pulse-be . && docker run -p 8000:8000 water-pulse-be`.

## Data credits

NISAR GCOV — NASA/JPL-Caltech and ISRO, distributed by ASF DAAC; OPERA DSWx-S1/DSWx-HLS — NASA JPL OPERA, PO.DAAC;
commune boundaries © OpenStreetMap contributors (ODbL). Show the `attribution` string from `/api/manifest` in the UI.
