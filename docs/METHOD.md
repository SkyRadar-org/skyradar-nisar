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
F1 0.57–0.76, recall 0.87. NISAR maps more water than DSWx-S1 (≈ 1.4–1.5× in the flood season).

**b) Is the extra water real? Independent optical check (DSWx-HLS, clear-sky pixels, ±2 days, 16 dates, 3 tracks):**

- NISAR F1 **0.57–0.86** vs Sentinel-1 **0.50–0.78** — **NISAR is better on 14 of 16 dates**; the two exceptions
  (track 148D, 28 Sep and 10 Oct) differ by ≤ 0.02.
- NISAR detects **47–82 %** of the optical water area, Sentinel-1 **35–64 %**; NISAR precision stays high.
- **53–98 %** of the area that only NISAR maps as water is also water in the optical product.

→ L-band sees flooded rice fields that C-band misses.

**c) Against reported events:** sluice gates Tha La/Tra Su (closed 14 Aug, opened 25 Sep) — the commune where they stand
(Thoi Son) is ~50 % under water from September to late October; no commune-scale signal of the 25 Sep opening was
detected. Small reported events (1 ha flooded in Hoi An commune, 19 Sep) are below commune-scale detectability.

**d) Tested and rejected:** an "inundated vegetation" layer from HH brightening vs a dry reference (F1 ≈ 0.02 vs DSWx-S1
inundated vegetation): rice growth brightens HH as well, so this layer is not part of the product.

## 5. Results (demo area, 2026)

- About **5 300 km²** were flooded at least once between August and early November; **~3 000 km²** were still under water
  on the 27–29 Oct images.
- Two contrasting groups of communes:
  - **Early flood, early recession** — Tây Phú, Vĩnh Hanh (An Giang): 73–79 % under water at the end of August, almost dry by early October.
  - **Late flood, not receded** — Sơn Kiên, Hòn Đất, Mỹ Thuận (An Giang): peak 70–90 % in October and still **58–78 %
    under water on 3 November**, after the sowing window opened.
- Of 80 communes that were ever > 30 % flooded, 50 had not halved their water area by 29 October.

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
- Prototype: grouping pixels that flood and dry on the *same dates* finds 45 field blocks ≥ 50 ha (≈ 3 000 ha) flooded on
  16–18 Aug and drained before the last image, many bounded by straight canals — candidate dyke compartments.

## 6. Limitations

- Most NISAR products used are **PROVISIONAL**; one frame over Da Nang (126A/f010, 8 Oct) was flagged invalid.
- **What we measure is water on the field, not its cause:** river flood, controlled flood release into dyke compartments
  (An Giang plan: 46 324 ha) or pumping for land preparation all look the same.
- Revisit: 12 days per track, ≈ 5–7 days combining 2–3 tracks; latency ≈ 2–3 days → **not an early-warning tool**, and flash
  floods (e.g. Da Nang, 8–9 Oct) are only partly captured (≈ 15–30 km² of short-lived new water at Nui Thanh–Tam Ky).
- References (DSWx) are products, not field surveys; optical validation covers clear-sky areas only.

## 7. Impact

A provincial agriculture officer can open a commune, see its 2026 water timeline from three independent NISAR tracks and
know whether its fields are likely to be drained before the sowing window — without downloading or processing radar data.
The pipeline is region-agnostic: changing the bounding box and track list in `config.py` reruns it for any delta.
