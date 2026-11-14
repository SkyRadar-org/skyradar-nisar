# PROJECT_BRIEF — full project description for making the slides and the video

> **Ghi chú cho đội:** file này viết bằng tiếng Anh vì slide, video và trang nộp bài bắt buộc tiếng Anh. Đưa nguyên file
> cho Codex (hoặc AI khác) làm slide và video. Mọi con số ở đây lấy từ `data/web/stats/*.csv` trên `main` lúc
> **14/11/2026 ~21:00** (commit `55afa1c`). Nếu chạy lại pipeline (ví dụ có ảnh NISAR mới sáng 15/11), cập nhật mục 13.

---

## 0. Instructions for the AI making the slides and video

**Deliverables**
1. A slide deck (English), 7 slides recommended (outline in section 11). Export to PDF and keep an editable source.
2. A demo video (English), 30 seconds recommended (script in section 12), plus an optional 60-second cut.
3. Both must be hosted online and **linked** from the submission page: Space Apps does not accept uploads of video or slides.

**Hard rules**
- **English only** on slides, video and voice-over.
- **No people under 18** in any image, video or audio. Use screen recordings, maps and charts, not photos of people.
- **Use only the numbers in this file.** Each number has its source in section 13. Do not round differently, do not add
  numbers, do not invent comparisons. If a number seems wrong, flag it instead of changing it.
- **Do not claim** the things listed in section 10 ("What we must not claim").
- Credit every data source and the basemap (section 14) on the last slide and at the end of the video.
- Before finalising, open the official guides and check slide/video limits, which this brief could not confirm:
  [Project Submission Guide](https://www.spaceappschallenge.org/resources/project-submission-guide/),
  [Judging & Awards Guide](https://www.spaceappschallenge.org/resources/judging-awards-guide).
  The 2025 judging criteria were **Impact, Creativity, Validity, Relevance, Presentation**; assume the same unless the
  2026 guide says otherwise.
- Deadline: submission closes **15 November 2026, 23:59** (local time, Hanoi).

**Assets you can use**
- Live app: **https://nisar-flood.skyradar.vn** (record the screen from here; section 9 has a click-by-click demo path).
- Code (public): **https://github.com/SkyRadar-org/skyradar-nisar** (pipeline, data, backend, docs).
- Figures (PNG, 150 dpi) in `docs/figures/` of that repo:
  - `fig1_water_timeseries.png` — water share over the season, per track, NISAR vs Sentinel-1.
  - `fig2_validation_optical.png` — F1 against optical maps, NISAR vs Sentinel-1, 16 dates.
  - `fig3_commune_examples.png` — commune water timelines (Vĩnh Hưng, Phương Thịnh vs Tây Phú, Vĩnh Hanh).
  - `fig4_flood_release.png` — controlled flood-release timing signature.
  - `fig5_sowing_check.png` — latest water share per commune on a map.
- App colours: header navy `#0f2a4a`, brand blue `#1d4ed8`, water blue; tracks 047D blue `#2563eb`, 083A orange
  `#ea580c`, 148D violet `#7c3aed`. Font in the app: Inter / system sans-serif.

---

## 1. Identity

| | |
|---|---|
| Project name | **SkyRadar NISAR Water Pulse** |
| Team | **SkyRadar** (Hanoi, Vietnam) — Duy Chí (lead; data and backend), Thành Đông (frontend), Trịnh Đạt (data validation, testing and review) |
| Event | NASA International Space Apps Challenge 2026, Hanoi local event, 14–15 November 2026 |
| Challenge | **"Dancing with the SARs"** (challenge 5): build something useful with NASA–ISRO NISAR synthetic aperture radar data. Check the official challenge page for its exact wording: https://www.spaceappschallenge.org/2026/challenges/dancing-with-the-sars/ |
| One-line summary (≤ 200 characters) | Commune-by-commune flood and drainage tracking for Mekong Delta rice land, from NASA–ISRO NISAR L-band radar that sees through clouds. |
| Tagline options | "Is the field dry yet? Ask the radar." · "Seeing flooded rice fields through the clouds, commune by commune." |

---

## 2. The problem

- The **Mekong Delta** in southern Vietnam grows more than half of the country's rice. Every year the Mekong floods the
  upper delta (Long Xuyên Quadrangle and Plain of Reeds / Đồng Tháp Mười) from August to November. Dykes divide the land
  into compartments; many are flooded on purpose to take in silt, then closed and pumped dry.
- After the flood, the **winter–spring rice crop** (Đông Xuân, the largest crop of the year) must be sown on time. In
  2026–2027 the regional plan has an early batch 10–30 October, a main batch in November, and all sowing done before
  10 January 2027. Each province and commune sets its own sowing batches (for example An Giang: 1–30 November and
  1–31 December; Tân Hồng commune: first batch 5–11 November).
- An El Niño year is forecast: drought and saltwater intrusion may arrive from late December, so **sowing late is risky**.
- Provincial agriculture departments need to know, **commune by commune: is water still on the fields, and is it going
  down?** Field checks are slow. Optical satellites are blind under rainy-season clouds. Existing radar flood maps
  (Sentinel-1, C-band) miss part of the shallow water in rice fields.

**Users:** provincial Departments of Agriculture and Environment and their irrigation / disaster-prevention offices
(Chi cục Thuỷ lợi, Phòng chống thiên tai) in the Mekong Delta, plus agricultural cooperatives.

---

## 3. Why NISAR

- **NISAR** (NASA–ISRO, launched 2025) carries an **L-band** radar (24 cm wavelength). Radar works day and night and
  **through clouds**.
- Calm open water reflects the radar pulse away from the satellite (specular reflection), so flooded fields look **dark**
  in both HH and HV polarisations; dry fields and rice plants scatter energy back and look brighter.
- We use the **L2 GCOV** product: terrain-corrected backscatter (γ⁰) in HH and HV, already on a map grid.
- Three NISAR tracks cover the area (047D, 083A, 148D), each repeating every **12 days**; together they give an image of a
  given place about every **5–7 days**.
- **Measured advantage:** against independent optical water maps, NISAR finds more of the real water than Sentinel-1 on
  **14 of 16** flood-season dates (section 6).

---

## 4. Data used

| Dataset | Provider | Role |
|---|---|---|
| **NISAR L2 GCOV** (HH, HV), **33 acquisitions**, tracks 047D/083A/148D, **17 Jun – 3 Nov 2026** (29 provisional, 4 validated products) | NASA/JPL-Caltech & ISRO, via **ASF DAAC** (NASA Earthdata Cloud) | Main input |
| OPERA **DSWx-S1** (water maps from Sentinel-1) | NASA JPL OPERA, **PO.DAAC** | Calibration (2 dates) and validation (25 dates) |
| OPERA **DSWx-HLS** (water maps from Landsat/Sentinel-2, optical) | NASA JPL OPERA, **PO.DAAC** | Independent validation (16 clear-sky flood-season dates) |
| **SWOT** L2 HR Raster 100 m (Ka-band interferometric radar) | NASA/CNES, **PO.DAAC** | Third independent radar for comparison (13 dates) |
| NASA **CMR** search | NASA Earthdata | Data discovery |
| Commune boundaries (2025 administrative reform), **140 communes** in the study area | © OpenStreetMap contributors (ODbL) | Statistics per commune |

Study area: 104.95–106.0° E, 10.25–11.0° N (Long Xuyên Quadrangle and Plain of Reeds; parts of An Giang, Đồng Tháp,
Tây Ninh, Cần Thơ, Vĩnh Long provinces).

---

## 5. Method (pipeline)

1. **Find** every NISAR GCOV acquisition over the area with NASA CMR (newest product version per acquisition).
2. **Read only what is needed** from each multi-gigabyte HDF5 file on NASA Earthdata Cloud: the file's chunk index is
   read once, then only the compressed 512×512 chunks inside the area are downloaded in parallel (about 0.5–3 minutes per
   acquisition, depending on bandwidth, instead of downloading the whole file). Result is bit-identical to the standard
   HDF5 reader.
3. **Grid:** average HH and HV to a common **20 m** grid (UTM 48N), in linear power; discard invalid pixels.
4. **Water rule:** a pixel is water when **HH < −14 dB and HV < −22 dB**; patches smaller than **3 ha** are dropped;
   permanent water (rivers, canals) is removed. The two thresholds were chosen by maximising agreement with OPERA DSWx-S1
   on **only two dates** (17 Jun dry, 21 Sep near peak); all other dates are independent checks.
5. **Per commune and per date:** observed area, water area, water share. **Tracks are never merged** (different viewing
   geometry; median difference between tracks 3.4 percentage points).
6. **Latest assessment per commune:** the newest acquisition that observes **at least 50 % of the commune's full area**.
   Communes below that are "insufficient observation" and are never shown as dry.
7. **Trend per commune (measured, not forecast):** latest image vs the previous image of the **same track** (≤ 24 days
   earlier, same footprint), in percentage points per 12 days: **falling ≤ −5, steady, rising ≥ +5**.
8. **Season timing:** first flooded date, peak, date water halved after the peak, and a controlled flood-release
   signature per commune.
9. **Publish:** a static data package (PNG overlays, GeoJSON, CSV) served by a read-only API; the web app is hosted on
   Cloudflare Pages.

**Reproducibility:** a teammate re-ran the whole pipeline from a fresh clone on Windows; every published table matched
(about 20 of 6 million water pixels differ because of library versions).

---

## 6. Does it work? (validation)

| Check | Result |
|---|---|
| **vs optical OPERA DSWx-HLS** (independent of calibration; clear-sky pixels only; ±2 days; flood season Aug–Nov; 16 dates, 3 tracks) | **NISAR better than Sentinel-1 on 14 of 16 dates.** F1: NISAR **0.57–0.86**, Sentinel-1 **0.50–0.78** (the 2 exceptions are within 0.02). NISAR finds **47–82 %** of the optical water area, Sentinel-1 **35–64 %**. Of the area only NISAR maps as water, **53–98 %** is also water in the optical map. |
| **vs SWOT** (NASA/CNES Ka-band, a third independent radar; 13 dates ≤ 2 days from a NISAR image) | NISAR agrees with SWOT better than Sentinel-1 does on **11 of 12** dates. (The exception, 10 Sep, is a SWOT anomaly.) |
| **vs OPERA DSWx-S1** (25 independent dates) | Median F1 **0.63**. |
| **Against reported events** | Communes named in 2026 flood-release news (Bình Mỹ, Thạnh Mỹ Tây, Bình Thạnh Đông) show the expected controlled-release curve. Early-November press: Đồng Tháp Mười fields being pumped dry; Tân Hồng first sowing batch 5–11 Nov — consistent with the maps (section 7). |
| **Tested and rejected** | A "flooded vegetation" layer from HH brightening (F1 ≈ 0.02): growing rice also brightens HH. Not part of the product. |

---

## 7. What the data show (2026 season)

- **2026 was a low-flood year.** Water share of observed commune land rose from about 1–6 % in July to a peak of about
  **35 % in mid-September to early October** (track 083A 35.1 % on 11 Sep; track 047D 33.8 % on 3 Oct), then declined.
- **Latest assessment (27 Oct – 3 Nov 2026), 115 communes with at least half their area observed:**
  **33 high water (≥ 30 %)**, **39 moderate (10–<30 %)**, **43 low (< 10 %)**. 25 communes lack sufficient observation
  (16 partially observed, the rest without an image) and are **not** counted as dry.
- **Trend on the same 115 communes:** **24 falling, 79 steady, 12 rising.** Level and trend differ: a commune can hold
  a lot of water and already be falling, or little water and rising (silt intake).
- **Examples (all observed over ~100 % of their area):**
  - **Vĩnh Hưng** (Tây Ninh): 61.3 % water on 27 Oct, steady (64.3 % on 15 Oct).
  - **Phương Thịnh** (Đồng Tháp): 59.8 % water on 27 Oct, rising.
  - **Tân Hồng** (Đồng Tháp): 43.7 % on 29 Oct and **falling** (50.0 % on 17 Oct), one week before its first sowing batch
    (5–11 Nov) — matches press reports of fields being pumped dry.
  - **Lấp Vò** (Đồng Tháp): water **rising** from 12.1 % to 20.1 % in late October — matches reports that cooperatives
    there let floodwater in for silt before pumping; its first sowing batch is later (24 Nov – 1 Dec).
  - **Tây Phú** (An Giang): 0 % on 3 Nov — drained.
- **Controlled flood release is visible:** 10 communes show the release signature (water arrives in mid-August while the
  river is still low, then drops sharply at the end of September); 15 show other patterns; 55 kept water late.

---

## 8. The app (https://nisar-flood.skyradar.vn)

Bilingual (Vietnamese / English, switch in the header), works on phones. Tabs:

| Tab | What it shows |
|---|---|
| **Overview** | Season story of the Mekong Delta; counts of communes by latest water share (high / moderate / low / insufficient); priority list of communes sorted by water, each with its trend tag (↓ falling, → steady, ↑ rising), date and coverage, with a "View map" button. |
| **Map** | Communes coloured by latest water share; or "One satellite image" mode with the NISAR water layer and radar image for any of the 33 acquisitions; **time slider** with only real acquisition dates, one lane per track, **Play** to animate the season; simple / professional view. Click a commune: panel with latest water share and date, coverage, **measured trend** (previous image → latest image, same track), a recommended action, a button to open the evidence image, and the season chart (one line per track). |
| **Reports** | Season trend chart (rising / near peak / going down), flood calendar by month, flood duration, province comparison, commune table; export to CSV. |
| **Validation** | Plain-language summary and limits, then charts and tables: NISAR vs Sentinel-1 against optical maps, NISAR vs Sentinel-1 against SWOT, agreement with DSWx-S1, method, what was dropped, sources. |
| **About** | Project intro, how to read the map, limits, sources, team. |

---

## 9. Demo path for the video (click by click, about 25 s of screen time)

1. Open https://nisar-flood.skyradar.vn/?lang=en (Overview). Hold 2 s on the season story and the commune counts.
2. Click **Map**. Switch to **One satellite image**, choose **Simple** view.
3. Click the first dot on the time slider (17 Jun), then **Play** ▶: water spreads in August–September and shrinks in
   October. Let it run about 6 s. Pause around **3 Oct**.
4. Switch back to **Latest per commune**. Type **"Tan Hong"** in "Find a commune", press Enter. Show the panel:
   43.7 % on 29 Oct, **↓ Water falling** (50.0 % → 43.7 %, same orbit).
5. Optional: type **"Lap Vo"** → **↑ Water rising** (silt intake before pumping).
6. Click **Validation**: show the optical comparison (NISAR better than Sentinel-1 on 14 of 16 dates) and its chart.

Record at 1920×1080 (or 1440×900), browser zoom 100 %, English UI. Hide bookmarks and personal tabs.

---

## 10. Limits — and what we must not claim

**Say clearly (judges reward honesty):**
- Most NISAR products used are **provisional** (29 of 33).
- Radar sees **water on the field**, not its cause (river flood, controlled release, or pumping).
- **Not an early-warning system:** data arrive 2–3 days after each pass; one image per place every ~5–7 days.
- **Early season (June–July) is weak:** with little water, the fixed rule over-reports water on smooth dry fields
  (F1 vs DSWx-S1 0.07–0.19). The tool targets the flood and drainage period (Aug–Nov).
- Water share refers to the **observed** part of a commune; communes observed below 50 % are not assessed.
- Validation references (OPERA DSWx, SWOT) are other satellite products, not field surveys.

**Must NOT claim:**
- That the app says **when to sow** or that a field is "ready to sow". It shows one condition (water on the field and its
  trend). Sowing also depends on the local sowing calendar, synchronised sowing against brown planthoppers, the gap after
  the previous harvest, and secure irrigation water.
- Any **forecast** of when water will be gone (deliberately not made: 2–3 images, levels set by sluices and pumping).
- That NISAR "sees water under the rice canopy" as a validated product (the flooded-vegetation layer was rejected).
- That results cover the whole Mekong Delta (the study area is 140 communes in the upper delta).
- Real-time status ("today"): every figure belongs to an acquisition date.
- Field validation (none was done).

---

## 11. Slide outline (7 slides)

| # | Title | Message (one sentence) | On the slide | Visual |
|---|---|---|---|---|
| 1 | **Is the field dry yet?** | After the Mekong flood, provinces must decide commune by commune whether rice can be sown, but clouds hide the fields. | Mekong Delta; flood Aug–Nov; winter–spring crop; El Niño risk → sowing must not be late; users = provincial agriculture departments | Map of the study area (screenshot of the Map tab, latest per commune) |
| 2 | **Why NISAR L-band** | L-band radar sees through clouds and finds more of the water in rice fields than C-band. | 24 cm wavelength; calm water = dark in HH and HV; 3 tracks × 12-day repeat → image every ~5–7 days; 33 acquisitions, 17 Jun – 3 Nov 2026 | Radar image + water layer for one date (Map, one satellite image) |
| 3 | **From NISAR files to commune answers** | We stream only the area we need and turn radar into water maps and commune statistics. | Pipeline: CMR → partial read on Earthdata Cloud (minutes, not GB) → 20 m grid → HH < −14 dB & HV < −22 dB, ≥ 3 ha → per commune, per track → latest assessment + measured trend | Simple pipeline diagram (5 boxes) |
| 4 | **Demo** | One page answers: where is water now, since when, and is it going down? | Overview counts; Map with Play; commune panel (Tân Hồng ↓ falling) | 2–3 app screenshots |
| 5 | **Does it work?** | Against independent optical maps, NISAR beats Sentinel-1 on 14 of 16 dates. | F1 0.57–0.86 vs 0.50–0.78; finds 47–82 % vs 35–64 % of optical water; vs SWOT: 11 of 12 dates; calibrated on 2 dates only; flooded-vegetation layer rejected | `fig2_validation_optical.png` |
| 6 | **What it shows in 2026** | A low-flood year, and the drainage is visible commune by commune. | 115 communes assessed: 33 high / 39 moderate / 43 low; trend 24 falling / 79 steady / 12 rising; Tân Hồng falling a week before sowing; Lấp Vò rising (silt intake); flood release visible in 10 communes | `fig3_commune_examples.png` or `fig5_sowing_check.png`, `fig4_flood_release.png` small |
| 7 | **Limits, next steps, team** | Honest about what radar can and cannot say; next is to put it next to the sowing calendar. | Limits (section 10, 4 bullets max). Next: commune sowing calendars next to water level and trend; planthopper light-trap and salinity data; detect previous harvest with NISAR; whole delta; operational updates after each pass. Team names. Data credits. Live app + repo links | Team line, QR code to the app |

**Speaker-note style:** one idea per slide, numbers exactly as above, no jargon without a plain explanation ("F1 = how well
two maps agree, 1 = perfect").

---

## 12. Video script

**30-second version (recommended)**

| Time | Picture | Voice-over / on-screen text |
|---|---|---|
| 0:00–0:05 | Overview tab of the app, Mekong Delta map | "Mekong Delta, autumn 2026. The flood is going down. Is this commune's rice land dry enough to sow?" |
| 0:05–0:15 | Map, one satellite image, Play from June to October | "NASA–ISRO NISAR's L-band radar sees water on the fields through the clouds — 33 images from three orbits." |
| 0:15–0:22 | Click Tân Hồng → panel with 43.7 % and "↓ Water falling" | "For each of 140 communes: how much water is left, and whether it is going down." |
| 0:22–0:27 | Validation tab chart | "Checked against independent optical maps, NISAR finds more of the water than Sentinel-1 on 14 of 16 dates." |
| 0:27–0:30 | Title card: app URL, team, "NASA Space Apps 2026 · Hanoi" | "SkyRadar NISAR Water Pulse." |

**60-second version (optional):** add after 0:15 — Lấp Vò rising (silt intake), Reports tab season chart (peak about 35 %
in mid-September), and one sentence on limits ("radar shows water on the field, not when to sow; that stays with the
local sowing calendar").

**Production notes:** English captions burned in; no music with vocals; no people; end card with credits: "NISAR data:
NASA/JPL-Caltech & ISRO (ASF DAAC). OPERA DSWx and SWOT: NASA JPL / CNES (PO.DAAC). Basemap © Esri; boundaries ©
OpenStreetMap contributors."

---

## 13. Numbers and where they come from

All files are in `data/web/stats/` of `SkyRadar-org/skyradar-nisar` (`main`).

| Number | Value | Source |
|---|---|---|
| NISAR acquisitions, tracks, period | 33; 047D, 083A, 148D; 17 Jun – 3 Nov 2026 | `data/web/manifest.json` |
| Provisional / validated products | 29 / 4 | `manifest.json` (`maturity`) |
| Communes in the study area | 140 | `data/boundaries/communes_aoi.geojson` |
| Water rule | HH < −14 dB, HV < −22 dB, ≥ 3 ha | `calibration.json`, `src/skyradar_nisar/config.py` |
| NISAR vs Sentinel-1 against optical | 14 of 16; F1 0.57–0.86 vs 0.50–0.78; recall 47–82 % vs 35–64 %; NISAR-only water confirmed 53–98 % | `vs_dswx_hls.csv` |
| vs SWOT | 11 of 12 dates | `vs_swot.csv` |
| vs DSWx-S1 | median F1 0.63, 25 dates | `vs_dswx_s1.csv` (`role = validation`) |
| Early-season F1 | 0.07–0.19 (Jun–Jul) | `vs_dswx_s1.csv` |
| Latest assessment | 115 communes: 33 / 39 / 43; 16 partial | `sowing_check.csv` (`status`: still_wet / draining / ready / partial) |
| Trend | 24 falling / 79 steady / 12 rising | `sowing_check.csv` (`trend`) |
| Season peak | 35.1 % (083A, 11 Sep); 33.8 % (047D, 3 Oct) | `commune_water_by_date.csv` (sum of water km² / observed km² per image) |
| Examples | Vĩnh Hưng 61.3 % (27 Oct, steady); Phương Thịnh 59.8 % (27 Oct, rising); Tân Hồng 43.7 % (29 Oct, falling from 50.0 %); Lấp Vò 20.1 % (29 Oct, rising from 12.1 %); Tây Phú 0 % (3 Nov) | `sowing_check.csv` |
| Flood-release classes | A 10 / B 15 / C 55 | `commune_flood_class.csv` |
| Sowing calendars | regional 3 batches, done before 10 Jan 2027; An Giang 1–30 Nov & 1–31 Dec; Tân Hồng 5–11 Nov; Lấp Vò 24 Nov – 1 Dec | press reports, see `docs/SOWING_CONDITIONS.md` (not checked against official documents) |

---

## 14. Credits, licences, tools

- NISAR L2 GCOV — NASA/JPL-Caltech and ISRO, distributed by the Alaska Satellite Facility DAAC.
- OPERA DSWx-S1 and DSWx-HLS — NASA JPL OPERA project, distributed by PO.DAAC (contains modified Copernicus Sentinel data).
- SWOT L2 KaRIn High Rate Raster — NASA/CNES, distributed by PO.DAAC.
- NASA CMR (data search), NASA Earthdata Cloud.
- Commune boundaries and basemap data © OpenStreetMap contributors (ODbL); basemap © Esri.
- Code licence: Apache-2.0 (repository `LICENSE`).
- Tools: Python (h5py, rasterio, numpy), FastAPI, TypeScript, Vite, MapLibre GL, Chart.js, Cloudflare Pages.
- AI assistance: parts of the code and documentation were drafted with AI assistants (Claude, Codex, Gemini) and reviewed
  by the team.

---

## 15. Related documents in the repo

- `README.md` — how to run, method summary, validation, limits.
- `docs/METHOD.md` — full method and validation write-up (English).
- `docs/SUBMISSION.md` — earlier submission drafts (use this brief where they differ).
- `docs/SOWING_CONDITIONS.md` — sowing conditions research (Vietnamese) and what NISAR can answer.
- `docs/HANDOFF.md`, `docs/UX_PLAN.md` — team handoff and UI notes (Vietnamese).
