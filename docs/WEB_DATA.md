# Web data package (`data/web`) — guide for the web app

Everything the web app needs is static (no backend). Regenerate with `python -m skyradar_nisar.export_web`.

| File | Content |
|---|---|
| `manifest.json` | `frames` (one per NISAR acquisition: `date`, `track`, `maturity`, `png`), `bounds` of all PNG overlays, `tracks`, water `rule`, `timing_png`, `gibs_template`, `attribution` |
| `water/<date>_<track>.png` | Transparent PNG, water = blue (RGBA 30,110,230,200), EPSG:4326, covers `manifest.bounds` |
| `radar/<date>_<track>.jpg` | **Radar background** for that date (R = HH, G = HV, B = HH−HV), ~60 m, same `bounds` — use this instead of GIBS when zoomed in |
| `composite/<date>_<track>.webp`, `_simple.webp`, `_radar.webp` | **Playback mosaics** (visual aid, half resolution, same `bounds`, transparent outside Vietnamese land = union of commune polygons). Per pixel: the latest valid observation from any track up to that date, ≤ `composite_rule.max_age_days` (12) old; single-pass flips are cancelled by a temporal median (previous / current / next valid observation). `<key>.webp` = professional view (water faded by age, light grey veil = no recent observation); `_simple.webp` = one colour, no fading or veil, window `simple_max_age_days` (30) so the 25 Jul → 11 Aug gap has no hole; `_radar.webp` = radar mosaic, transparent where unobserved. Listed in `manifest.composites` (`png`, `simple_png`, `radar`, `observed_pct` over Vietnamese land, `sources`). Built by `python -m skyradar_nisar.composite` (also run by `export_web`; needs shapely). Statistics always use the raw frames |
| `gibs_availability.json` | GIBS tiles present per frame (zoom 9 test): 30/33 complete; 13/07, 18/07, 03/11 partial |
| `summary/recession.png` | Recession date colour map (blue = late Sep → red = end Oct; **purple = still wet on the last image**) |
| `summary/first_flood.png` | First flooded date (blue = early Aug → red = late Oct) |
| `communes.geojson` | 140 communes (OSM 2025): `name`, `province`, `osm_id`, `area_km2`, `timing[track]` (`peak_pct`, `peak_date`, `first_date_ge20pct`, `halved_after_peak`, `last_date`, `last_pct`), `flood_class` (A = water in early & out while river high → controlled release timing; B = other; C = still wet at last image) |
| `stats/commune_water_by_date.csv` | One row per commune × date × track: `valid_km2`, `water_km2`, `water_pct` → per-commune chart |
| `stats/commune_flood_timing.csv` | Same as `timing` in the GeoJSON, as a table |
| `stats/commune_flood_class.csv` | Flood-release classification (A/B/C) |
| `stats/sowing_check.csv` | Per commune: latest water % per track; `status` from the most recent image covering ≥ 50 % of the commune (ready < 10 %, draining 10–30 %, still_wet ≥ 30 %); `worst_*` = worst case across tracks; `tracks_agree` |
| `stats/vs_dswx_hls.csv`, `vs_dswx_s1.csv`, `calibration.json` | Validation numbers for the "Does it work?" panel |

## ⚠️ NASA GIBS NISAR layer
Tiles render correctly **only up to zoom 10**; zoom 11–13 tiles are corrupted (checked 2026-11-14). Set `maxzoom: 10` on the
GIBS source (MapLibre over-zooms it) or use `radar/<frame>.jpg` as the radar background. Our water PNG aligns pixel-exact
with `radar/*.jpg` (same bounds).

## Rules for the UI
- **Plot each track as its own line** (047D, 083A, 148D). Do not average tracks: viewing geometry differs.
- Show `maturity` (provisional / validated) on the date slider.
- Show the attribution string from `manifest.json` on the map.
- Label "water on the field", not "flood": the app cannot tell river flood, controlled release or pumping apart.

## MapLibre snippets

```js
const m = await (await fetch('data/web/manifest.json')).json();
const [[S, W], [N, E]] = m.bounds;
const corners = [[W, N], [E, N], [E, S], [W, S]];            // MapLibre image source order: TL, TR, BR, BL

// 1) NISAR radar background from NASA GIBS for the selected date
function gibsUrl(date) { return m.gibs_template.replace('{date}', date); }
map.addSource('nisar', { type: 'raster', tiles: [gibsUrl(m.frames[0].date)], tileSize: 256, maxzoom: 10,  // >10 is corrupted
                         attribution: 'NASA GIBS / NISAR' });
map.addLayer({ id: 'nisar', type: 'raster', source: 'nisar', paint: { 'raster-opacity': 0.9 } });

// 2) Water layer of the selected frame
map.addSource('water', { type: 'image', url: 'data/web/' + m.frames[0].png, coordinates: corners });
map.addLayer({ id: 'water', type: 'raster', source: 'water' });

function showFrame(i) {                                       // call from the time slider
  const f = m.frames[i];
  map.getSource('water').updateImage({ url: 'data/web/' + f.png, coordinates: corners });
  map.getSource('nisar').setTiles([gibsUrl(f.date)]);
}

// 3) Communes coloured by flood class, click -> commune panel
map.addSource('communes', { type: 'geojson', data: 'data/web/communes.geojson' });
map.addLayer({ id: 'communes', type: 'line', source: 'communes', paint: { 'line-color': '#ffffff', 'line-width': 0.8 } });
map.addLayer({ id: 'communes-fill', type: 'fill', source: 'communes', paint: {
  'fill-color': ['match', ['get', 'flood_class'], 'A', '#2f9e44', 'C', '#ae3ec9', 'B', '#f59f00', 'rgba(0,0,0,0)'],
  'fill-opacity': 0.25 } });
map.on('click', 'communes-fill', e => openCommunePanel(e.features[0].properties));
```

Note: `properties.timing` comes back from MapLibre as a JSON string; use `JSON.parse(props.timing)`.

## Coverage-aware assessment (14 November 2026)

`sowing_check.csv` now adds `area_km2` and `observed_pct` (0–100, full OSM commune denominator), and `partial` status.
Only the newest acquisition with ≥50% commune coverage and ≥5 km² can supply an assessment. Counts: 43 low,
39 moderate, 33 high water share; 16 `partial` CSV records. Water percentages retain the observed-area denominator.
The frontend adapter exposes these fields for all 140 communes, including unassessed communes (`observed_pct=null`
when there is no observation); `coverage_sufficient=false` always has `status=uncertain`.
