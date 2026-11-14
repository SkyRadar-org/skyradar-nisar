# SkyRadar NISAR Water Pulse

**NASA Space Apps Challenge 2026 — Challenge "Dancing with the SARs" — Team SkyRadar (Hanoi)**

Commune-level monitoring of **flooding and flood recession on Mekong Delta rice land** with **NISAR L-band radar**
(NASA–ISRO), for provincial agriculture departments: *where is water now, when did it arrive, has it receded before the
sowing window?*

> Status: hackathon MVP (14–15 Nov 2026). Most NISAR data used are **PROVISIONAL** products.

## What is in this repository

```text
src/skyradar_nisar/
  config.py       AOI, NISAR tracks, calibrated water rule, paths
  cmr.py          NASA CMR search (GCOV, DSWx), newest product version per acquisition
  fastread.py     fast AOI reader for GCOV HDF5 on Earthdata Cloud (parallel chunk download, ~40 s per date)
  grid.py         common 20 m UTM-48N grid, power-domain 2x2 averaging, dB*100 int16 GeoTIFF I/O
  fetch_gcov.py   download HH/HV for all dates of the configured tracks
  fetch_dswx.py   OPERA DSWx-S1 (radar) and DSWx-HLS (optical) reference water mosaics on the same grid
  water.py        water rule (HH < -14 dB and HV < -22 dB, >= 3 ha) + permanent-water mask
  calibrate.py    threshold search vs DSWx-S1 (2 dates) and validation (other dates; optical DSWx-HLS)
  communes.py     2025 commune boundaries from OpenStreetMap (admin_level=6)
  timing.py       per-date water maps, first-flood / recession rasters, commune tables
  export_web.py   small static package for the web app (data/web)
  release.py      controlled flood-release (xả lũ) timing signature per commune + figure
  figures.py      slide figures (docs/figures)
data/boundaries/communes_aoi.geojson   140 communes in the demo AOI (OSM, ODbL)
data/web/                              PNG overlays + manifest + commune GeoJSON + CSV stats (for the web app)
```

Large rasters (`data/raw`, `data/processed`) are **not** committed; the pipeline regenerates them.

## Run

```bash
pip install -r requirements.txt
export EARTHDATA_TOKEN=...        # Earthdata Login bearer token (never commit it)
export PYTHONPATH=src
python -m skyradar_nisar.fetch_gcov          # NISAR GCOV, all dates/tracks in config (~40 s per date)
python -m skyradar_nisar.fetch_dswx s1       # OPERA DSWx-S1 reference
python -m skyradar_nisar.fetch_dswx hls      # OPERA DSWx-HLS optical reference
python -m skyradar_nisar.communes            # optional: refresh OSM commune boundaries
python -m skyradar_nisar.calibrate           # thresholds + validation tables
python -m skyradar_nisar.timing              # water maps, timing rasters, commune stats
python -m skyradar_nisar.release             # flood-release signature per commune (needs timing)
python -m skyradar_nisar.export_web          # data/web package
python -m skyradar_nisar.figures             # docs/figures
```

Your Earthdata account must authorise the application *"Alaska Satellite Facility Data Access"*.

## Method (short)

1. **Data:** NISAR L2 GCOV (HH, HV; γ⁰ power, terrain-corrected), tracks 047D/f083, 083A/f007 and 148D/f083 (11 dates each,
   33 acquisitions, 17 Jun – 3 Nov 2026); pixels with `mask` 0 or 255 are discarded; averaged to 20 m in power.
2. **Water rule:** HH < −14 dB and HV < −22 dB, patches ≥ 3 ha, permanent water (DSWx-S1 water on ≥ 20 of 22 dates)
   removed. Thresholds chosen by maximising F1 against OPERA DSWx-S1 on **two** dates (17 Jun, 21 Sep, track 047D).
3. **Timing:** per pixel and per commune — first flooded date, peak, date water halved, still-wet at the last image.
   Statistics are kept **per track** (viewing geometry differs; median inter-track difference 3.4 points).

## Validation (summary)

- vs **DSWx-S1** on land, 25 independent dates: F1 median 0.63; flood season 0.57–0.76 (recall 0.87).
- vs **optical DSWx-HLS** (independent of calibration; clear-sky pixels, ±2 days, 16 dates, 3 tracks):
  **NISAR F1 0.57–0.86 vs Sentinel-1 DSWx 0.50–0.78 — NISAR better on 14 of 16 dates** (the 2 exceptions, track 148D,
  differ by ≤ 0.02); NISAR recall 0.47–0.82 vs 0.35–0.64. 53–98 % of the area that only NISAR maps as water is also
  water in the optical product.
- Tested and **rejected**: an "inundated vegetation" rule from HH brightening (F1 ≈ 0.02; rice growth also brightens HH).

## Limitations

- Mostly PROVISIONAL NISAR products; 12-day repeat per track (≈ 5–7 days with 2–3 tracks).
- Detects *water on the field*, not its cause (river flood, controlled flood release into dyke compartments, or
  pumping for land preparation).
- Not an early-warning system (product latency ~2–3 days; sparse revisit for flash floods).
- References (DSWx) are products, not field surveys.

## Data sources and credits

- NISAR L2 GCOV — NASA/JPL-Caltech and ISRO; distributed by the Alaska Satellite Facility DAAC.
- OPERA DSWx-S1 and DSWx-HLS — NASA JPL OPERA project, distributed by PO.DAAC (contains modified Copernicus Sentinel data).
- NASA GIBS / Worldview NISAR GCOV visualisation layer.
- Administrative boundaries — © OpenStreetMap contributors, ODbL 1.0.
- Reading approach adapted from the ASF NISAR Cookbook (BSD-3-Clause).
- AI assistance: parts of the code and documentation were drafted with Claude (Anthropic) and reviewed by the team.

## License

Code: Apache License 2.0 (see `LICENSE`). Data in `data/` keep the licences of their sources (OSM data: ODbL).
