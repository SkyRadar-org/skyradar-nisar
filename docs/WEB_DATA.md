# Web data package (`data/web`) — guide for the web app

Everything the web app needs is static (no backend). Regenerate with `python -m skyradar_nisar.export_web`.

| File | Content |
|---|---|
| `manifest.json` | `frames` (one per NISAR acquisition: `date`, `track`, `maturity`, `png`), `bounds` of all PNG overlays, `tracks`, water `rule`, `timing_png`, `gibs_template`, `attribution` |
| `water/<date>_<track>.png` | Transparent PNG, water = blue (RGBA 30,110,230,200), EPSG:4326, covers `manifest.bounds` |
| `summary/recession.png` | Recession date colour map (blue = late Sep → red = end Oct; **purple = still wet on the last image**) |
| `summary/first_flood.png` | First flooded date (blue = early Aug → red = late Oct) |
| `communes.geojson` | 140 communes (OSM 2025): `name`, `province`, `osm_id`, `area_km2`, `timing[track]` (`peak_pct`, `peak_date`, `first_date_ge20pct`, `halved_after_peak`, `last_date`, `last_pct`), `flood_class` (A = water in early & out while river high → controlled release timing; B = other; C = still wet at last image) |
| `stats/commune_water_by_date.csv` | One row per commune × date × track: `valid_km2`, `water_km2`, `water_pct` → per-commune chart |
| `stats/commune_flood_timing.csv` | Same as `timing` in the GeoJSON, as a table |
| `stats/commune_flood_class.csv` | Flood-release classification (A/B/C) |
| `stats/sowing_check.csv` | Per commune: latest water % per track; `status` from the most recent image covering ≥ 50 % of the commune (ready < 10 %, draining 10–30 %, still_wet ≥ 30 %); `worst_*` = worst case across tracks; `tracks_agree` |
| `stats/vs_dswx_hls.csv`, `vs_dswx_s1.csv`, `calibration.json` | Validation numbers for the "Does it work?" panel |

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
map.addSource('nisar', { type: 'raster', tiles: [gibsUrl(m.frames[0].date)], tileSize: 256, maxzoom: 13,
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
