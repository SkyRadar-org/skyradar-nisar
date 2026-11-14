# Backend API (repo `water-pulse-be`) — contract between backend and web

> **Implemented** (FastAPI) in `water-pulse-be`: all endpoints below plus `/api/flood-release`, `/api/search?q=`
> (accent-insensitive) and `/api/provinces`; `/api/sowing-check` takes `status` and `province` filters (the reference date
> is fixed by the pipeline run, 2026-11-01). Interactive docs at `/docs`.

Source of truth: the static package produced by this repository in `data/web` (see `WEB_DATA.md`).
The backend can be as simple as a static file server plus a few JSON endpoints; everything below is read-only.

| Method & path | Returns | Built from |
|---|---|---|
| `GET /api/manifest` | Dates, tracks, maturity, overlay bounds, GIBS template, attribution | `manifest.json` |
| `GET /api/frames?track=047D` | Frames of one track (date, maturity, overlay URL) | `manifest.json` → `frames` |
| `GET /static/water/{date}_{track}.png` | Water overlay PNG (EPSG:4326, `manifest.bounds`) | `water/` |
| `GET /static/summary/{recession,first_flood}.png` | Timing maps | `summary/` |
| `GET /api/frontend/scenes` | Adds `composite` per scene (`png`, `simplePng`, `radar`, `maxAgeDays`, `observedPct`, `sources`) when the playback mosaics exist | `manifest.json` → `composites` |
| `GET /api/frontend/choropleth/composite?date=&track=` | `{osm_id: {pct, age, date, track}}`: each commune's latest observation on or before the scene, covering ≥ 50 % of its best pass and ≤ 12 days old (companion of the mosaic; the exact-scene `/choropleth` is unchanged) | `stats/commune_water_by_date.csv` |
| `GET /api/communes` | GeoJSON: 140 communes with `timing` per track and `flood_class` | `communes.geojson` |
| `GET /api/communes/{osm_id}` | One commune: properties + timing + class | `communes.geojson`, `stats/commune_flood_timing.csv`, `stats/commune_flood_class.csv` |
| `GET /api/communes/{osm_id}/series` | `[{date, track, maturity, valid_km2, water_km2, water_pct}]` sorted by date — **one line per track** | `stats/commune_water_by_date.csv` |
| `GET /api/ranking?metric=last_pct&track=047D&limit=20` | Communes ranked (e.g. most water at the last image, latest recession) | `stats/commune_flood_timing.csv` |
| `GET /api/validation` | `{calibration, vs_dswx_s1:[...], vs_dswx_hls:[...]}` | `stats/calibration.json`, `stats/vs_dswx_*.csv` |
| `GET /api/sowing-check?date=2026-11-01` | For each commune: water % at the last image before/after `date`, flag `still_wet` if ≥ 30 % | `stats/commune_water_by_date.csv` |

Response rules
- Always include `track` and `maturity` per data point; never average tracks.
- Include the `attribution` string from `manifest.json` in `/api/manifest` (NASA/JPL/ISRO NISAR via ASF DAAC, OPERA DSWx via PO.DAAC, © OpenStreetMap contributors).
- Commune ids are OpenStreetMap relation ids (`osm_id`).
- CORS: allow the web app origin.

Example `/api/communes/15416586/series` (Xã Sơn Kiên):

```json
[{"date": "2026-10-27", "track": "047D", "maturity": "validated", "valid_km2": 32.1, "water_km2": 25.1, "water_pct": 78.2},
 {"date": "2026-10-29", "track": "083A", "maturity": "validated", "valid_km2": 32.1, "water_km2": 27.8, "water_pct": 86.6},
 {"date": "2026-11-03", "track": "148D", "maturity": "validated", "valid_km2": 32.1, "water_km2": 25.1, "water_pct": 78.2}]
```
(values illustrative of the format; take real numbers from the CSV)
