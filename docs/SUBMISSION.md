# Submission drafts (EN) — to be checked against the official Judging & Submission guide

## Project name
**SkyRadar NISAR Water Pulse**

## One-line summary (≤ 200 characters)
Commune-level flood and recession timelines for Mekong Delta rice land from NASA–ISRO NISAR L-band radar — seeing through
clouds and into flooded fields that C-band misses.

## Project description (≈ 250 words)
Every flood season, agriculture departments in Vietnam's Mekong Delta must decide when rice can be sown again. The
2026–2027 winter–spring window in An Giang opens on 1 November, but nobody can easily tell, commune by commune, whether
the fields have drained: clouds blind optical satellites in the rainy season, and existing radar flood maps (Sentinel-1,
C-band) miss shallow water in rice fields.

SkyRadar NISAR Water Pulse turns NISAR L-band GCOV radar into a simple question-and-answer tool for provincial officers:
*Where is water now? When did it arrive? Has it receded before sowing?* We stream only the area of interest from NISAR
files on NASA Earthdata Cloud (≈ 40 s per acquisition instead of 6 GB), classify water with an HH/HV rule calibrated on two
dates against OPERA DSWx-S1, and summarise 33 acquisitions from three tracks (June–November 2026) for 140 communes.

Validated independently against optical OPERA DSWx-HLS, NISAR detects more of the real water than Sentinel-1 on 14 of
16 comparison dates (F1 0.57–0.86 vs 0.50–0.78). The tool shows, for example, that Sơn Kiên and Hòn Đất communes were
still 58–78 % under water on 3 November, after the sowing window opened, while Tây Phú had drained by early October.

We are explicit about limits: provisional data, 5–7-day effective revisit, and that radar sees water on the field, not
whether it came from the river, a controlled flood release or pumping.

## How we used NASA data
- NISAR L2 GCOV (HH, HV), ASF DAAC — main input, 33 acquisitions, 3 tracks.
- OPERA DSWx-S1 and DSWx-HLS (JPL, PO.DAAC) — calibration and independent validation.
- NASA GIBS NISAR GCOV layer — radar background in the web map.
- NASA CMR — data discovery; NISAR Data User Guide and ASF NISAR Cookbook — file format and access.

## Slides (7)

| # | Title | Content | Visual |
|---|---|---|---|
| 1 | **Is the field dry yet?** | Mekong Delta flood season; 1 Nov sowing window; officers need commune-level answers; clouds + C-band blind spots | Photo/map of the delta, sowing calendar |
| 2 | **Why NISAR L-band** | L-band (24 cm) penetrates rice canopy, sees water under young rice; dual-pol HH/HV; 12-day repeat, 3 tracks → 5–7 days | Side-by-side NISAR vs Sentinel-1 water map (fig: disagreement map) |
| 3 | **Data & method** | Stream AOI from Earthdata Cloud → 20 m grid → HH/HV water rule (calibrated on 2 dates) → per-commune timing | Pipeline diagram |
| 4 | **Demo** | Time slider over 33 NISAR dates, commune table (first flood, peak, recession), per-track charts | Screenshot of the web app |
| 5 | **Does it work?** | vs optical DSWx-HLS: NISAR better on 14/16 dates (2 ties within 0.02); 53–98 % of NISAR-only water confirmed optically; rejected method (inundated vegetation) | fig2_validation_optical |
| 6 | **What it tells farmers' managers** | Sơn Kiên/Hòn Đất still wet on 3 Nov vs Tây Phú drained in Oct; controlled flood release visible in Bình Mỹ, Thạnh Mỹ Tây, Bình Thạnh Đông | fig3_commune_examples + fig4_flood_release |
| 7 | **Limits & next steps / Team** | Provisional data; cause of water unknown; not early warning. Next: whole delta, sowing-date alerts, field (dyke compartment) level | Team |

## 30-second video script
- 0–5 s: "Mekong Delta, October 2026. Clouds everywhere. Is this rice field ready to sow?"
- 5–20 s: screen recording — slide through NISAR dates, click Sơn Kiên → timeline still high after 1 Nov; click Tây Phú → drained.
- 20–27 s: "NISAR L-band finds up to 82 % of the water seen by optical satellites; Sentinel-1 finds up to 64 %."
- 27–30 s: "SkyRadar NISAR Water Pulse — NASA Space Apps 2026." + link.
