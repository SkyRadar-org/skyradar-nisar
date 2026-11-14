# SkyRadar NISAR Water Pulse — Method & Validation (draft)

## 1. Problem and users

Every flood season, provincial **Departments of Agriculture and Environment** in the Mekong Delta must decide when and
where rice can be sown again (the 2026–2027 winter–spring crop window in An Giang opens on **1 November**). They need to
know, **commune by commune**, when water arrived on the fields, when it peaked and whether it has receded. In the rainy
season optical satellites are mostly blind (clouds), and existing radar flood maps (C-band Sentinel-1) miss shallow water
in rice fields. Vietnam's national remote-sensing services run rapid flood mapping *per event*; nobody provides a
continuous, season-long, commune-level view.

**Our tool** turns NASA–ISRO NISAR L-band radar into commune-level flood and recession timelines that an agriculture
officer can read without SAR expertise.

## 2. Data

| Dataset | Use |
|---|---|
| **NISAR L2 GCOV** (HH, HV, γ⁰ power, radiometric terrain correction, 10 m) — tracks 047D/f083, 083A/f007, 148D/f083, 33 acquisitions, 17 Jun – 3 Nov 2026 (mostly PROVISIONAL; 27/29 Oct and 3 Nov VALIDATED) | Main input |
| **OPERA DSWx-S1** (Sentinel-1 C-band surface water, 30 m) | Calibration (2 dates) and comparison |
| **OPERA DSWx-HLS** (Landsat/Sentinel-2 optical surface water, 30 m) | Independent validation on clear-sky pixels |
| **OpenStreetMap** 2025 commune boundaries (admin_level 6) | Commune statistics (140 communes) |
| NASA **GIBS** NISAR GCOV visualisation layer | Radar background in the web app |

Demo area: Long Xuyen Quadrangle and Dong Thap Muoi (104.95–106.00 E, 10.25–11.00 N, ≈ 8 700 km²).

## 3. Processing

1. **Search** acquisitions in NASA CMR; keep the newest product version (validated > provisional, highest CRID).
2. **Read only the area of interest** from each ~6 GB HDF5 file on Earthdata Cloud: we index the HDF5 chunk table once
   and download the needed compressed 512×512 chunks in parallel (≈ 465 MB and 30–40 s per acquisition instead of
   6 GB; output identical to a full read).
3. Discard pixels with `mask` = 0 (invalid) or 255 (outside swath); average 2×2 **in power** to a common 20 m UTM-48N
   grid; convert to dB.
4. **Water rule:** HH < −14 dB **and** HV < −22 dB, connected patches ≥ 3 ha; permanent water (rivers, canals) removed.
   Thresholds were chosen by maximising F1 against DSWx-S1 on **two dates only** (17 Jun dry, 21 Sep near peak).
5. **Flood timing** per pixel and per commune: first flooded date, peak, date when water halved after the peak,
   water still present at the last image. Statistics are kept **separately per track** because viewing geometry
   changes backscatter (median inter-track difference 3.4 percentage points; a few communes differ by up to 44).

## 4. Validation

**a) Against Sentinel-1 DSWx (25 independent dates, land only):** median F1 0.63; in the flood season (from 25 Aug)
F1 0.57–0.76, recall 0.87. NISAR maps more water than DSWx-S1 on the same pixels (flood season, 18 dates: 1.0–2.1×, median 1.65×).
Early season (June–July) is weak: F1 0.07–0.19, because the fixed rule over-reports water on smooth dry fields when
there is little water (see Limitations).

**b) Is the extra water real? Independent optical check, flood season Aug–Nov (DSWx-HLS, clear-sky pixels, ±2 days,
16 dates, 3 tracks; June–July optical scenes are almost all cloudy and were not used):**

- NISAR F1 **0.57–0.86** vs Sentinel-1 **0.50–0.78** — **NISAR is better on 14 of 16 dates**; the two exceptions
  (track 148D, 28 Sep and 10 Oct) differ by ≤ 0.02.
- NISAR detects **47–82 %** of the optical water area, Sentinel-1 **35–64 %**; NISAR precision stays high.
- **53–98 %** of the area that only NISAR maps as water is also water in the optical product.

→ L-band sees flooded rice fields that C-band misses.

**c) Third independent radar — SWOT (NASA/CNES, Ka-band interferometry, L2 HR Raster 100 m, version D).**
Two SWOT passes cover 86 % and 77 % of the area (14 dates, ~every 10 days). Raster cells exist only where water or
near-water was sampled, so we rebuild the swath (10–60 km cross-track) and treat empty cells inside it as dry when
a SWOT sample lies within 1.5 km (larger voids are data gaps, e.g. whole communes without samples on pass 577);
water = water fraction ≥ 0.5, quality good/suspect. Each SWOT date is paired with the nearest NISAR acquisition
(≤ 2 days; three same-day pairs: 19 Jun, 15 Oct, 22 Oct) and scored on the same pixels (permanent water excluded):

- NISAR agrees with SWOT better than Sentinel-1 DSWx on **11 of 12** dates (flood season F1 0.38–0.68 vs 0.28–0.62).
  The exception, 10 Sep, is a SWOT anomaly (11 % water at the flood peak, NISAR 33 %, DSWx-S1 similar to NISAR).
- SWOT maps more water than both radars (Aug–Nov 35–68 % of land); against optical DSWx-HLS (8 dates) SWOT F1
  0.55–0.88 vs NISAR 0.59–0.88 (NISAR ≥ SWOT on 6 of 8). In June–July SWOT shows 14–28 % water where NISAR shows
  3–7 % and DSWx-S1 ~1 %, probably shallow water in summer–autumn paddies; without clear optical scenes this is not verified.
- SWOT is a comparison source, not ground truth; its revisit (~10 days, 2 passes) is sparser than NISAR's 3 tracks.

**d) Against reported events:** sluice gates Tha La/Tra Su (closed 14 Aug, opened 25 Sep) — the commune where they stand
(Thoi Son) is ~50 % under water from September to late October; no commune-scale signal of the 25 Sep opening was
detected. Small reported events (1 ha flooded in Hoi An commune, 19 Sep) are below commune-scale detectability.

**e) Tested and rejected:** an "inundated vegetation" layer from HH brightening vs a dry reference (F1 ≈ 0.02 vs DSWx-S1
inundated vegetation): rice growth brightens HH as well, so this layer is not part of the product.

## 5. Results (demo area, 2026)

- About **5 300 km²** were flooded at least once between August and early November; **~3 000 km²** were still under water
  on the 27–29 Oct images.
- Two contrasting groups of communes:
  - **Early flood, early recession** — Tây Phú, Vĩnh Hanh (An Giang): 73–79 % under water at the end of August, almost dry by early October.
  - **Substantial water at the latest observation** — Vĩnh Hưng, Tây Ninh (`15012314`), 61.3%, and Phương Thịnh,
    Đồng Tháp (`15586694`), 59.8%, on 27 October; both images cover approximately the full commune.
    These percentages refer to observed area and do not establish sowing readiness.
- Of 80 communes that were ever > 30 % flooded, 50 had not halved their water area by 29 October.
- **Latest eligible water-share assessment**: **115 communes**, with **33 high (≥30%)**, **39 moderate (10–<30%)**,
  and **43 low (<10%)** observed water share. An acquisition must cover ≥50% of the full OSM commune and ≥5 km²,
  evaluated before rounding. The newest eligible acquisition is selected across all dates/tracks; a more recent
  partial pass remains evidence, not a replacement assessment. Six communes have no observations and 19 have only
  insufficient observations under this rule (including 16 `partial` records in `sowing_check.csv`). The legacy CSV
  codes `ready`, `draining`, `still_wet` label these bins; they are not agronomic recommendations or proof of a trend.
- **Trend (measured, not forecast):** for the 115 assessed communes, the selected image against the previous image of
  the same track (≤ 24 days earlier, same footprint), in percentage points per 12 days: **24 falling (≤ −5), 79 steady,
  12 rising (≥ +5)**. Level and trend are independent: of the 39 moderate communes only 12 are falling and 4 are rising;
  5 of the 33 high communes are rising. We deliberately give **no drain-date projection**: with 2–3 points 12 days
  apart and water levels set by sluices and pumping, an extrapolated date is not defensible.
- **Coverage denominator:** `observed_pct = valid_km2 / area_km2 × 100`; `water_pct = water_km2 / valid_km2 × 100`.
  Communes at the AOI/swath edge may only be partially observed. The 50% gate is a product screening rule, not a
  validated guarantee that the observed part represents the whole commune.

### Controlled flood release (xả lũ) is visible in the timing

An Giang's plan 457/KH-UBND (12 Aug 2026) opens dyke-protected three-crop sub-regions to the flood (46 324 ha in 2026)
to bring sediment and break pest cycles, then the fields are drained for the next crop. NISAR shows this **timing
signature**: water enters in mid-August while the Tien river at Tan Chau is still below alarm level 1 (2.8 m on 17 Aug)
and leaves in late September – early October **while the river peaks (3.45 m)** — i.e. fields pumped dry, not natural
recession.

- The three communes named in 2026 flood-release news (Bình Mỹ, Thạnh Mỹ Tây, Bình Thạnh Đông) all follow this curve on
  all three tracks (≈ 0–5 % water in July → 45–64 % in September → sharp drop 21 Sep – 5 Oct). Example Bình Mỹ (047D):
  52 % → 27 %.
- 10 of the 80 communes that were > 30 % flooded have this "early-in / out-while-river-high" signature (Châu Thành,
  Thoại Sơn, Châu Phú area of An Giang); 55 were still wet at the last image.
- Caveat: the flooded area in these communes is 2–17× the reported release areas, so natural flooding is mixed in; the
  release area itself cannot be isolated without the dyke sub-region boundaries (held by the province).
- Prototype: grouping pixels that flood and dry on the *same dates* finds 31 field blocks ≥ 50 ha (≈ 2 300 ha) flooded on
  16–18 Aug and drained before the last image, many bounded by straight canals — candidate dyke compartments (exact-date
  matching is strict, so this is a lower bound).

## 6. Limitations

- Most NISAR products used are **PROVISIONAL**; one frame over Da Nang (126A/f010, 8 Oct) was flagged invalid.
- **What we measure is water on the field, not its cause:** river flood, controlled flood release into dyke compartments
  (An Giang plan: 46 324 ha) or pumping for land preparation all look the same.
- Revisit: 12 days per track, ≈ 5–7 days combining 2–3 tracks; latency ≈ 2–3 days → **not an early-warning tool**, and flash
  floods (e.g. Da Nang, 8–9 Oct) are only partly captured (≈ 15–30 km² of short-lived new water at Nui Thanh–Tam Ky).
- References (DSWx) are products, not field surveys; optical validation covers clear-sky areas of the flood season (Aug–Nov) only.
- **Early season is weak:** in June–July, with little water on the fields, the fixed HH/HV rule over-reports water on
  smooth dry fields (F1 vs DSWx-S1 0.07–0.19). The tool is meant for the flood and recession period (Aug–Nov).

## 7. Impact

A provincial agriculture officer can open a commune, see its 2026 water timeline from three independent NISAR tracks and
know whether its fields are likely to be drained before the sowing window — without downloading or processing radar data.
The pipeline is region-agnostic: changing the bounding box and track list in `config.py` reruns it for any delta.
