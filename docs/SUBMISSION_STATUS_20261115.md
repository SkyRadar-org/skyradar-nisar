# Trạng thái nộp bài SkyRadar — 15/11/2026

## VERIFIED

- Trang đã hiển thị **Project Submitted for Judging**.
- Last Saved và Last Submitted hiển thị **15 November 2026 01:13** (GMT+7).
- Trang đội: https://www.spaceappschallenge.org/2026/find-a-team/skyradar/?tab=project
- Chủ đội đã xác nhận rõ việc đồng ý điều khoản NASA và cam kết quyền sử dụng tài liệu tại bước nộp.
- Trạng thái đã nộp đã xuất hiện ở lần kiểm tra trước thao tác cuối; không bấm nộp lặp lại. Không suy đoán ai đã thực hiện thao tác trên giao diện dùng chung.
- Bằng chứng ảnh và bản đọc trường biểu mẫu được lưu riêng trên máy; không đưa thông tin phiên đăng nhập lên repo.
- Xác minh trạng thái trong giao diện đã đăng nhập; chưa kiểm tra lại bản hiển thị của khách chưa đăng nhập sau nộp.

## Nội dung đọc lại từ biểu mẫu đã nộp

### Project name

SkyRadar NISAR Water Pulse

### Summary

Which communes need drainage checks before the next rice crop? SkyRadar NISAR Water Pulse helps agriculture officers, irrigation teams and cooperatives in Vietnam’s upper Mekong Delta prioritize field inspections and follow drainage progress. We turn NASA–ISRO NISAR L-band radar observations into dated commune water maps, same-track trends, imagery and CSV reports, working through rainy-season clouds. Users identify high-water communes, check coverage and change, then consult local sowing calendars and field conditions. A partial-HDF5 reader fetches only the required image chunks, making large satellite files practical to process into local evidence. Our prototype uses 33 acquisitions for 140 communes; 115 have sufficient observations. Independent optical comparisons show higher F1 than Sentinel-1 on 14 of 16 flood-season dates. The intended benefit is more focused checking and better-informed crop preparation; field outcomes remain untested. The app supports local decisions without prescribing sowing dates or pump operations.

### Project Demonstration

https://github.com/SkyRadar-org/skyradar-nisar/blob/1776e8a8b237cfdb3cd7755bae7edf5a8fe1b010/docs/demo/vi-en/SkyRadar_Demo_VI_EN.mp4

### Project

https://nisar-flood.skyradar.vn

### Project Details

THE DECISION: WHICH COMMUNES NEED CHECKING FIRST?




Before the next rice crop, agriculture officers, irrigation teams and cooperatives need to know where standing water remains and whether drainage is progressing. In the upper Mekong Delta, water may also be deliberately admitted into dyke compartments for silt. The same water-covered area can therefore call for different local checks. Rainy-season clouds limit optical observations; a map alone is not enough without its date, coverage and trend.




SkyRadar NISAR Water Pulse addresses Dancing with the SARs by turning NASA–ISRO NISAR observations of surface change into an interactive, commune-level evidence tool. Its strongest practical use is to focus field checks and follow drainage progress while local teams prepare the next rice crop.




HOW IT FITS THE FARMING WORKFLOW




Local water plan → satellite observation → prioritize communes → inspect gates, pumps and fields → consult the sowing calendar.




The current app supports observation and commune prioritization. An officer can filter by province or water-share class, select a high-water commune, check acquisition date and coverage, inspect the measured same-track trend, and open imagery and seasonal history. Reports provide commune statistics and CSV export. The bilingual Vietnamese/English interface works on phones.




Three examples show why the follow-up matters:

• Vĩnh Hưng: 61.3% observed water on 27 October 2026, steady. Prioritize verification of drainage progress against the local water plan.

• Tân Hồng: 50.0% on 17 October → 43.7% on 29 October, falling. Track recession while consulting the local sowing calendar.

• Lấp Vò: 12.1% on 17 October → 20.1% on 29 October, rising. Check planned water intake with local teams before proposing drainage.




These are operational questions, not pump commands or a diagnosis of why water changed. The intended benefit is to concentrate inspection effort and make crop preparation better informed. We have not yet measured time, cost, water savings or yield effects in an operational field trial.




MAKING NISAR PRACTICAL TO PROCESS




We use 33 NISAR L2 GCOV acquisitions from 17 June to 3 November 2026 across tracks 047D, 083A and 148D, covering a study area of 140 communes in the Long Xuyên Quadrangle and Plain of Reeds. NISAR L-band radar supplies observations through clouds; NASA data are the core input, not a decorative background.




NASA CMR discovers acquisitions. Our partial-HDF5 reader reads the chunk index once and downloads only the required compressed chunks within the area of interest, in parallel, rather than whole multi-gigabyte files. The project brief reports 0.5–3 minutes per acquisition; this is a documented benchmark, not a new timing experiment. Read values match the standard reader bit for bit. The rerunnable pipeline supports new processing runs when data arrive; we do not claim an automatic acquisition/publication schedule.




HH and HV are averaged in linear power onto a common 20 m grid. Water is classified using HH < −14 dB and HV < −22 dB; patches below 3 ha and permanent water are removed. Thresholds were calibrated against OPERA DSWx-S1 on two dates. Statistics remain separate by track. The latest assessment requires observation of at least 50% of the full commune area and at least 5 km²; newer partial coverage does not replace an eligible observation. Water share uses the observed part of the commune as its denominator. Trends compare observations from the same track, at most 24 days apart, normalized to 12 days. Outputs become maps, trends, API data and CSV reports.




EVIDENCE AND UNCERTAINTY




Against independent OPERA DSWx-HLS clear-sky pixels within ±2 days, NISAR has higher F1 than Sentinel-1 on 14 of 16 August–November comparison dates: F1 0.57–0.86 versus 0.50–0.78. F1 measures agreement between maps. Same-pixel comparisons against SWOT favor NISAR on 11 of 12 paired dates. These references are satellite products, not field surveys.




The latest eligible assessment includes 115 of 140 communes: 33 high, 39 moderate and 43 low observed water share; measured trends are 24 falling, 79 steady and 12 rising. The other 25 lack sufficient observations and are never counted as dry. Most inputs, 29 of 33, are provisional. The fixed rule is weak in June–July and over-reports water on smooth dry fields; the intended use period is flood and drainage monitoring in August–November.




Every result belongs to an acquisition date; this is not a live or early-warning service. There is no rice-field mask, depth estimate, forecast of when water will disappear, or certification that a field is ready to sow. The radar does not determine whether water came from river flooding, managed intake or pumping. Calendars, salinity, pest risk, the previous harvest and irrigation security still need local checks. Future work is to integrate those factors alongside water evidence and evaluate usefulness with local partners.




IMPLEMENTATION, ORIGINALITY AND TEAM




The implementation uses Python with h5py, rasterio and NumPy, FastAPI, TypeScript, Vite, MapLibre GL, Chart.js and Cloudflare Pages. Public code, data snapshots, methods and validation: https://github.com/SkyRadar-org/skyradar-nisar




Our contribution combines efficient access to large NISAR files with an inspection workflow: dated observations, explicit coverage, same-track trends and evidence at the administrative scale used by local officers. Team SkyRadar: Duy Chí, Thành Đông and Trịnh Đạt.




DEMO AND AI DISCLOSURE




The demonstration is a public 29.8-second MP4 on GitHub; click “View raw” or “Download raw file” to open/download it without an account. It uses actual app screen recordings and actual processed NISAR imagery, Vietnamese synthetic narration and simultaneous Vietnamese/English subtitles. Supporting bilingual slides, script and verification are in the repository’s docs/demo/vi-en folder on commit 1776e8a8b237cfdb3cd7755bae7edf5a8fe1b010.




Claude, Codex and Gemini assisted ideation, research, code/debugging, analysis, writing/translation, visual layout and presentation editing. Synthetic Vietnamese narration was generated locally with VieNeu-TTS 3.8.3, Hải Đăng voice; Whisper assisted automated transcript checks. The video visibly discloses AI-assisted editing and synthetic narration, also recorded in MP4/WAV metadata. AI assisted code and analysis; water masks and statistics are computed from the cited satellite inputs, not invented or AI-generated observations. No NASA logos were generated or modified.




DATA CREDITS




NISAR: NASA/JPL-Caltech & ISRO, ASF DAAC. OPERA DSWx: NASA JPL, PO.DAAC, containing modified Copernicus Sentinel data. SWOT: NASA/CNES, PO.DAAC. NASA CMR and Earthdata Cloud. Commune boundaries © OpenStreetMap contributors (ODbL); basemap © Esri. External data, software and contextual references are listed below.

### NASA Data

- [NISAR L2 GCOV HH/HV — NASA/JPL-Caltech & ISRO; ASF DAAC](https://nisar-docs.asf.alaska.edu/gcov/)
- [OPERA DSWx-S1 calibration and DSWx-HLS independent optical comparison — NASA JPL/PO.DAAC](https://www.jpl.nasa.gov/go/opera/products/dswx-product-suite/)
- [NASA/CNES SWOT L2 HR Raster (100 m) — independent radar comparison, PO.DAAC](https://podaac.jpl.nasa.gov/swot)
- [NASA Common Metadata Repository — acquisition discovery API](https://cmr.earthdata.nasa.gov/search/site/docs/search/api.html)
- [NASA Earthdata Cloud — NISAR cloud access documentation](https://nisar-docs.asf.alaska.edu/aws-s3-access/)
- [ASF NISAR Cookbook — data-access reference](https://asfopensarlab.github.io/NISAR_Cookbook/nisar-data-access/)

### Space Agency Partner & Other Data

- [OpenStreetMap contributors — commune boundaries, ODbL attribution](https://www.openstreetmap.org/copyright)
- [Esri World Light Gray Base — basemap used in the app and screen recordings](https://server.arcgisonline.com/ArcGIS/rest/services/Canvas/World_Light_Gray_Base/MapServer)
- [Python processing dependencies: NumPy, SciPy, h5py, fsspec, aiohttp, rasterio, pyproj, Shapely, Pillow, matplotlib](https://github.com/SkyRadar-org/skyradar-nisar/blob/1776e8a8b237cfdb3cd7755bae7edf5a8fe1b010/requirements.txt)
- [FastAPI — backend framework](https://fastapi.tiangolo.com/)
- [TypeScript — frontend language](https://www.typescriptlang.org/)
- [Vite — frontend build tool](https://vite.dev/)
- [MapLibre GL JS — interactive maps](https://maplibre.org/maplibre-gl-js/docs/)
- [Chart.js — interactive charts](https://www.chartjs.org/)
- [Cloudflare Pages — app hosting](https://developers.cloudflare.com/pages/)
- [Claude — AI assistance for code and documentation](https://www.anthropic.com/claude)
- [Codex — AI assistance for code, writing, visual layout and video editing](https://openai.com/codex/)
- [Gemini — AI assistance for research and independent text review](https://gemini.google.com/)
- [Viet Nam Ministry of Agriculture and Environment — crop-planning context (Vietnamese)](https://mae.gov.vn/dbscl-chu-dong-ne-han-man-bao-dam-san-xuat-vu-dong-xuan-20262027-23153.htm)
- [Báo Đồng Tháp — Tân Hồng winter–spring crop context (Vietnamese)](https://baodongthap.vn/xa-tan-hong-tap-trung-san-xuat-ben-vung-vu-dong-xuan-a247109.html)

