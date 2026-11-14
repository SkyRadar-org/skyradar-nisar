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
| `GET /static/summary/{recession,first_flood}_{track}.png` | timing maps per track (merged `{recession,first_flood}.png` kept for compatibility) |
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

- **Cloudflare Pages + Pages Worker:** `scripts/export_pages.py --out <frontend-dist> --worker-template <frontend>/cloudflare/worker.js`
  packages the read-only frontend API as JSON snapshots plus static assets. Normally invoked by the sibling frontend's
  `npm run build:cloudflare`. No Python process runs on Workers. The original API remains in FastAPI; the Worker serves
  `/api/frontend/*` and `/health`. See `water-pulse-fe/docs/CLOUDFLARE.md` for the target `nisar-flood.skyradar.vn`.
- **Vercel:** `vercel deploy` (uses `api/index.py` + `vercel.json`, all routes go to the FastAPI app).
- **Docker / Render / Railway:** `docker build -t water-pulse-be . && docker run -p 8000:8000 water-pulse-be`.

## Data credits

NISAR GCOV — NASA/JPL-Caltech and ISRO, distributed by ASF DAAC; OPERA DSWx-S1/DSWx-HLS — NASA JPL OPERA, PO.DAAC;
commune boundaries © OpenStreetMap contributors (ODbL). Show the `attribution` string from `/api/manifest` in the UI.

## Frontend adapter

`/api/frontend` serves the contract used by `water-pulse-fe` while the original `/api/*` responses remain unchanged:
`/scenes`, `/communes`, `/communes/{osm_id}/series`, `/choropleth?date=&track=`, `/area`, `/summary`, `/validation`.
Scene bounds are `[west,south,east,north]`; water URLs reference `/static`. `/summary` returns one season-summary layer
per track and kind (`id`, `kind` = `first_flood_date`|`recession_date`, `track`, `title`, `png`, `bounds`, `legend`,
`seasonDates`, `lastDate`, `range`) from `manifest.timing_png_by_track`; the merged-track PNGs are never offered. Unknown communes/scenes return 404;
invalid tracks return 422. Run `pytest -q` for both original API and adapter tests.

Commune IDs are strings. Status uses `sowing_check.csv`'s latest >=50%-coverage image and maps ready/draining/still_wet
to receded/uncertain/not_receded; peak below 5% on the reference track maps to no_flood. Without a sowing assessment,
coverage_sufficient is false and status is uncertain. Statistics use one reference_track, not a mix of tracks;
half_date/recession_date retain the separate half-peak metric. Series retain individual acquisitions.

Area totals sum observed commune water_km2 per date and track; dswx_km2 is null because same-area reference totals
are unavailable. HLS precision is null (not present in source CSV); DSWx-S1 calibration rows are excluded.
Summary returns [] because committed timing PNGs merge tracks. No synthetic data or guessed measurements are returned.
