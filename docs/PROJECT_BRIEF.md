# PROJECT_BRIEF — Project description for the slides and the video / Mô tả dự án để làm slide và video

> **EN:** Bilingual brief. **Slides, video and the submission page must be in English**: use the EN text on them; the VI
> text is for the team. Every number comes from `data/web/stats/*.csv` on `main` of `SkyRadar-org/skyradar-nisar`
> (14 Nov 2026, ~21:00). If the pipeline is re-run (e.g. new NISAR images on 15 Nov), update section 13 first.
>
> **VI:** Tài liệu song ngữ. **Slide, video và trang nộp bài bắt buộc tiếng Anh**: dùng phần EN để đưa lên; phần VI để cả
> đội đọc. Mọi con số lấy từ `data/web/stats/*.csv` trên `main` của `SkyRadar-org/skyradar-nisar` (14/11/2026, khoảng
> 21:00). Nếu chạy lại pipeline (ví dụ có ảnh NISAR mới sáng 15/11), cập nhật mục 13 trước.

---

## 0. Instructions for the slide/video maker / Dặn người làm slide và video

### Deliverables / Sản phẩm cần làm

| EN | VI |
|---|---|
| A slide deck in English, 7 slides recommended (section 11). Export a PDF and keep an editable source. | Bộ slide tiếng Anh, khuyến nghị 7 slide (mục 11). Xuất PDF và giữ bản gốc sửa được. |
| A demo video in English, 30 seconds recommended (section 12), plus an optional 60-second cut. | Video demo tiếng Anh, khuyến nghị 30 giây (mục 12), thêm bản 60 giây tuỳ chọn. |
| Host both online and **link** them from the submission page: Space Apps does not accept uploads of video or slides. | Đăng cả hai lên mạng rồi **dán link** vào trang nộp bài: Space Apps không cho tải video hay slide lên. |

### Hard rules / Quy tắc bắt buộc

| EN | VI |
|---|---|
| **English only** on slides, video and voice-over. | Slide, video, lời đọc **chỉ dùng tiếng Anh**. |
| **No people under 18** in any image, video or audio. Use screen recordings, maps and charts. | **Không có người dưới 18 tuổi** trong ảnh, video, âm thanh. Dùng quay màn hình, bản đồ, biểu đồ. |
| **Use only the numbers in this file** (sources in section 13). Do not round differently, add numbers or invent comparisons. Flag a number that looks wrong instead of changing it. | **Chỉ dùng số trong file này** (nguồn ở mục 13). Không làm tròn khác, không thêm số, không bịa phép so sánh. Số nào nghi sai thì báo lại, không tự sửa. |
| Do not make the claims listed in section 10. | Không tuyên bố các điều trong mục 10. |
| Credit all data sources and the basemap (section 14) on the last slide and at the end of the video. | Ghi nguồn dữ liệu và bản đồ nền (mục 14) ở slide cuối và cuối video. |
| Check slide/video limits in the official guides before finalising (this brief could not confirm them): [Project Submission Guide](https://www.spaceappschallenge.org/resources/project-submission-guide/), [Judging & Awards Guide](https://www.spaceappschallenge.org/resources/judging-awards-guide). 2025 criteria: **Impact, Creativity, Validity, Relevance, Presentation**. | Kiểm giới hạn số slide và độ dài video trong hướng dẫn chính thức trước khi chốt (file này chưa xác nhận được). Tiêu chí chấm 2025: **Impact, Creativity, Validity, Relevance, Presentation**. |
| Deadline: submission closes **15 November 2026, 23:59** (Hanoi time). | Hạn: cổng nộp đóng **23:59 ngày 15/11/2026** (giờ Hà Nội). |

### Assets / Tài liệu dùng được

| Asset | EN | VI |
|---|---|---|
| Live app | **https://nisar-flood.skyradar.vn** — record the screen here (demo path in section 9) | Web thật, quay màn hình ở đây (kịch bản thao tác ở mục 9) |
| Code (public) | **https://github.com/SkyRadar-org/skyradar-nisar** | Repo công khai: pipeline, dữ liệu, backend, tài liệu |
| `docs/figures/fig1_water_timeseries.png` | Water share over the season, per track, NISAR vs Sentinel-1 | Tỉ lệ nước theo mùa, từng track, NISAR so với Sentinel-1 |
| `docs/figures/fig2_validation_optical.png` | F1 against optical maps, NISAR vs Sentinel-1, 16 dates | F1 so với ảnh quang học, 16 ngày |
| `docs/figures/fig3_commune_examples.png` | Commune timelines: Vĩnh Hưng, Phương Thịnh vs Tây Phú, Vĩnh Hanh | Diễn biến nước của 4 xã ví dụ |
| `docs/figures/fig4_flood_release.png` | Controlled flood-release timing signature | Dấu hiệu xả lũ có điều tiết |
| `docs/figures/fig5_sowing_check.png` | Latest water share per commune on a map | Bản đồ tỉ lệ nước gần nhất theo xã |
| Colours | Header navy `#0f2a4a`, brand blue `#1d4ed8`; tracks 047D `#2563eb`, 083A `#ea580c`, 148D `#7c3aed`; font Inter / system sans-serif | Màu và phông chữ của app, dùng cho slide để đồng bộ |

---

## 1. Identity / Thông tin chung

| | EN | VI |
|---|---|---|
| Name / Tên | **SkyRadar NISAR Water Pulse** | (giữ tên tiếng Anh) |
| Team / Đội | **SkyRadar** (Hanoi, Vietnam) — Duy Chí (lead; data and backend), Thành Đông (frontend), Trịnh Đạt (data validation, testing and review) | **SkyRadar** (Hà Nội) — Duy Chí (trưởng nhóm; dữ liệu và backend), Thành Đông (frontend), Trịnh Đạt (kiểm chứng dữ liệu, kiểm thử, rà soát) |
| Event / Cuộc thi | NASA International Space Apps Challenge 2026, Hanoi, 14–15 Nov 2026 | NASA Space Apps Challenge 2026, điểm cầu Hà Nội, 14–15/11/2026 |
| Challenge / Đề | **"Dancing with the SARs"** (challenge 5): build something useful with NASA–ISRO NISAR radar data. Check the exact wording: https://www.spaceappschallenge.org/2026/challenges/dancing-with-the-sars/ | Đề 5 **"Dancing with the SARs"**: làm sản phẩm hữu ích từ dữ liệu radar NISAR. Đối chiếu câu chữ chính thức ở link bên |
| One-liner (≤ 200 chars) / Câu tóm tắt | Commune-by-commune flood and drainage tracking for Mekong Delta rice land, from NASA–ISRO NISAR L-band radar that sees through clouds. | Theo dõi ngập và rút nước trên ruộng lúa ĐBSCL theo từng xã, bằng radar băng L NISAR của NASA–ISRO nhìn xuyên mây. |
| Taglines / Khẩu hiệu | "Is the field dry yet? Ask the radar." · "Seeing flooded rice fields through the clouds, commune by commune." | "Ruộng đã rút nước chưa? Hỏi radar." · "Nhìn xuyên mây thấy ruộng lúa còn ngập, theo từng xã." |

---

## 2. The problem / Vấn đề

**EN**
- The **Mekong Delta** in southern Vietnam grows more than half of the country's rice. Every year the Mekong floods the
  upper delta (Long Xuyên Quadrangle and Plain of Reeds) from August to November. Dykes divide the land into
  compartments; many are flooded on purpose to take in silt, then closed and pumped dry.
- After the flood, the **winter–spring rice crop**, the largest of the year, must be sown on time. In 2026–2027 the
  regional plan has an early batch 10–30 October, a main batch in November, and all sowing done before 10 January 2027.
  Provinces and communes set their own batches (An Giang: 1–30 Nov and 1–31 Dec; Tân Hồng commune: first batch 5–11 Nov).
- An **El Niño** year is forecast: drought and saltwater intrusion may arrive from late December, so sowing late is risky.
- Provincial agriculture departments need to know, **commune by commune, whether water is still on the fields and
  whether it is going down**. Field checks are slow, optical satellites are blind under rainy-season clouds, and existing
  radar flood maps (Sentinel-1, C-band) miss part of the shallow water in rice fields.
- **Users:** provincial Departments of Agriculture and Environment, their irrigation and disaster-prevention offices, and
  agricultural cooperatives.

**VI**
- **ĐBSCL** làm ra hơn một nửa sản lượng lúa cả nước. Hằng năm lũ sông Mê Kông tràn vào vùng đầu nguồn (Tứ giác Long
  Xuyên, Đồng Tháp Mười) từ tháng 8 đến tháng 11. Đê bao chia đồng ruộng thành từng ô; nhiều ô được chủ động xả lũ vào để
  lấy phù sa, sau đó đóng cống và bơm rút nước.
- Sau lũ, **vụ Đông Xuân**, vụ lớn nhất trong năm, phải xuống giống đúng lịch. Vụ 2026–2027 có trà sớm 10–30/10, trà chính
  trong tháng 11, và phải xong trước 10/1/2027. Mỗi tỉnh, mỗi xã có lịch riêng (An Giang: 1–30/11 và 1–31/12; xã Tân Hồng:
  đợt 1 từ 5–11/11).
- Năm nay dự báo có **El Niño**: hạn và xâm nhập mặn có thể đến từ cuối tháng 12, nên xuống giống trễ là rủi ro.
- Sở Nông nghiệp cần biết **theo từng xã: ruộng còn nước không, nước có đang rút không**. Đi kiểm tra thực địa thì chậm,
  vệ tinh quang học bị mây che, còn bản đồ ngập từ radar hiện có (Sentinel-1, băng C) bỏ sót một phần nước nông trên ruộng.
- **Người dùng:** Sở Nông nghiệp và Môi trường các tỉnh, Chi cục Thuỷ lợi / Phòng chống thiên tai, hợp tác xã nông nghiệp.

---

## 3. Why NISAR / Vì sao dùng NISAR

| EN | VI |
|---|---|
| **NISAR** (NASA–ISRO, launched 2025) carries an **L-band** radar (24 cm wavelength). Radar works day and night and **through clouds**. | **NISAR** (NASA–ISRO, phóng năm 2025) mang radar **băng L** (bước sóng 24 cm). Radar hoạt động ngày đêm và **xuyên mây**. |
| Calm open water reflects the pulse away from the satellite, so flooded fields look **dark** in HH and HV; dry fields and rice plants scatter energy back and look brighter. | Mặt nước phẳng phản xạ sóng đi chỗ khác, nên ruộng ngập hiện **tối** ở cả HH và HV; ruộng khô và cây lúa tán xạ ngược nên sáng hơn. |
| We use the **L2 GCOV** product: terrain-corrected backscatter (γ⁰) in HH and HV, already on a map grid. | Dùng sản phẩm **L2 GCOV**: tán xạ ngược đã hiệu chỉnh địa hình (γ⁰), phân cực HH và HV, đã nằm trên lưới bản đồ. |
| Three tracks cover the area (047D, 083A, 148D), each repeating every **12 days**; together about one image of a place every **5–7 days**. | Ba quỹ đạo phủ vùng (047D, 083A, 148D), mỗi quỹ đạo lặp lại **12 ngày**; gộp lại khoảng **5–7 ngày** có một ảnh. |
| **Measured advantage:** against independent optical water maps, NISAR finds more of the real water than Sentinel-1 on **14 of 16** flood-season dates (section 6). | **Ưu thế đã đo:** so với ảnh quang học độc lập, NISAR phát hiện nước tốt hơn Sentinel-1 ở **14/16** ngày mùa lũ (mục 6). |

---

## 4. Data / Dữ liệu

| Dataset / Bộ dữ liệu | Provider / Nguồn | EN role | Vai trò |
|---|---|---|---|
| **NISAR L2 GCOV** (HH, HV): **33 acquisitions**, tracks 047D/083A/148D, **17 Jun – 3 Nov 2026**; 29 provisional, 4 validated | NASA/JPL-Caltech & ISRO, **ASF DAAC** (Earthdata Cloud) | Main input | Đầu vào chính |
| OPERA **DSWx-S1** (water from Sentinel-1) | NASA JPL OPERA, **PO.DAAC** | Calibration (2 dates), validation (25 dates) | Hiệu chỉnh (2 ngày), kiểm chứng (25 ngày) |
| OPERA **DSWx-HLS** (optical water, Landsat/Sentinel-2) | NASA JPL OPERA, **PO.DAAC** | Independent validation, 16 clear-sky flood-season dates | Kiểm chứng độc lập, 16 ngày trời quang mùa lũ |
| **SWOT** L2 HR Raster 100 m (Ka-band radar) | NASA/CNES, **PO.DAAC** | Third independent radar, 13 dates | Radar độc lập thứ ba, 13 ngày |
| NASA **CMR** | NASA Earthdata | Data discovery | Tìm dữ liệu |
| Commune boundaries (after the 2025 reform), **140 communes** | © OpenStreetMap contributors (ODbL) | Statistics per commune | Thống kê theo xã |

**EN:** Study area 104.95–106.0° E, 10.25–11.0° N (Long Xuyên Quadrangle and Plain of Reeds; parts of An Giang, Đồng Tháp,
Tây Ninh, Cần Thơ, Vĩnh Long).
**VI:** Vùng nghiên cứu 104,95–106,0° Đ, 10,25–11,0° B (Tứ giác Long Xuyên và Đồng Tháp Mười; một phần An Giang, Đồng
Tháp, Tây Ninh, Cần Thơ, Vĩnh Long).

---

## 5. Method / Phương pháp

| # | EN | VI |
|---|---|---|
| 1 | **Find** every NISAR GCOV acquisition over the area with NASA CMR (newest product version). | **Tìm** mọi ảnh NISAR GCOV phủ vùng qua NASA CMR (lấy phiên bản mới nhất). |
| 2 | **Read only what is needed** from each multi-gigabyte HDF5 file on Earthdata Cloud: read the chunk index once, download only the compressed chunks inside the area, in parallel (0.5–3 min per acquisition instead of the whole file). Bit-identical to the standard reader. | **Chỉ đọc phần cần** trong mỗi file HDF5 nhiều GB trên Earthdata Cloud: đọc bảng chỉ mục một lần, tải song song đúng các khối nằm trong vùng (0,5–3 phút mỗi ảnh thay vì tải cả file). Kết quả trùng từng bit với cách đọc chuẩn. |
| 3 | **Grid:** average HH and HV to a common **20 m** grid (UTM 48N) in linear power; drop invalid pixels. | **Lưới:** đưa HH, HV về lưới chung **20 m** (UTM 48N), lấy trung bình trên công suất tuyến tính; bỏ điểm ảnh không hợp lệ. |
| 4 | **Water rule:** water when **HH < −14 dB and HV < −22 dB**; drop patches < **3 ha**; remove permanent water (rivers, canals). Thresholds tuned against OPERA DSWx-S1 on **only two dates** (17 Jun, 21 Sep); all other dates are independent checks. | **Quy tắc nước:** là nước khi **HH < −14 dB và HV < −22 dB**; bỏ mảng < **3 ha**; loại nước thường xuyên (sông, kênh). Ngưỡng chọn bằng cách so với DSWx-S1 trên **đúng 2 ngày** (17/6, 21/9); các ngày khác là kiểm chứng độc lập. |
| 5 | **Per commune and date:** observed area, water area, water share. **Tracks are never merged** (median difference between tracks 3.4 points). | **Theo xã và theo ngày:** diện tích quan sát, diện tích nước, tỉ lệ nước. **Không bao giờ gộp các quỹ đạo** (chênh lệch trung vị giữa quỹ đạo 3,4 điểm %). |
| 6 | **Latest assessment:** the newest image that observes **≥ 50 % of the commune's full area**; below that the commune is "insufficient observation", never "dry". | **Đánh giá gần nhất:** ảnh mới nhất quan sát được **≥ 50% diện tích xã**; dưới mức đó là "chưa đủ quan sát", không bao giờ coi là "khô". |
| 7 | **Trend (measured, not forecast):** latest image vs the previous image of the **same track** (≤ 24 days, same footprint), in points per 12 days: **falling ≤ −5, steady, rising ≥ +5**. | **Xu hướng (số đo, không dự báo):** ảnh gần nhất so với ảnh trước đó của **cùng quỹ đạo** (cách ≤ 24 ngày, cùng vùng phủ), tính theo điểm % mỗi 12 ngày: **giảm ≤ −5, đứng yên, tăng ≥ +5**. |
| 8 | **Season timing:** first flooded date, peak, date water halved, controlled flood-release signature. | **Thời gian trong mùa:** ngày bắt đầu ngập, đỉnh, ngày nước giảm còn một nửa, dấu hiệu xả lũ có điều tiết. |
| 9 | **Publish:** static data package (PNG, GeoJSON, CSV) behind a read-only API; web app on Cloudflare Pages. | **Xuất bản:** gói dữ liệu tĩnh (PNG, GeoJSON, CSV) qua API chỉ đọc; web chạy trên Cloudflare Pages. |

**EN — Reproducibility:** a teammate re-ran the whole pipeline from a fresh clone on Windows; every table matched (about 20
of 6 million water pixels differ because of library versions).
**VI — Tái lập:** một thành viên chạy lại toàn bộ pipeline từ bản clone mới trên Windows; mọi bảng số trùng khớp (khoảng 20
trên 6 triệu điểm ảnh nước khác nhau do khác phiên bản thư viện).

---

## 6. Validation / Kiểm chứng

| Check / Phép kiểm | EN result | Kết quả (VI) |
|---|---|---|
| **vs optical OPERA DSWx-HLS** (independent; clear-sky pixels; ±2 days; flood season Aug–Nov; 16 dates, 3 tracks) | **NISAR better than Sentinel-1 on 14 of 16 dates.** F1 **0.57–0.86** vs **0.50–0.78** (the 2 exceptions within 0.02). NISAR finds **47–82 %** of the optical water area, Sentinel-1 **35–64 %**. Of the area only NISAR maps as water, **53–98 %** is also water optically. | **NISAR tốt hơn Sentinel-1 ở 14/16 ngày.** F1 **0,57–0,86** so với **0,50–0,78** (2 ngày còn lại chênh ≤ 0,02). NISAR thấy **47–82%** diện tích nước của ảnh quang học, Sentinel-1 **35–64%**. Phần chỉ NISAR thấy nước thì **53–98%** cũng là nước trên ảnh quang học. |
| **vs SWOT** (NASA/CNES Ka-band; 13 dates ≤ 2 days from a NISAR image) | NISAR agrees with SWOT better than Sentinel-1 on **11 of 12** dates (exception: 10 Sep, a SWOT anomaly). | NISAR khớp SWOT tốt hơn Sentinel-1 ở **11/12** ngày (ngoại lệ 10/9 là ảnh SWOT bất thường). |
| **vs OPERA DSWx-S1** (25 independent dates) | Median F1 **0.63**. | F1 trung vị **0,63**. |
| **Reported events** | Communes named in 2026 flood-release news (Bình Mỹ, Thạnh Mỹ Tây, Bình Thạnh Đông) show the expected release curve; early-November press (Đồng Tháp Mười pumping, Tân Hồng sowing 5–11 Nov) matches the maps (section 7). | Các xã có tên trong tin xả lũ 2026 (Bình Mỹ, Thạnh Mỹ Tây, Bình Thạnh Đông) có đúng đường cong xả lũ; tin đầu tháng 11 (Đồng Tháp Mười bơm rút, Tân Hồng xuống giống 5–11/11) khớp bản đồ (mục 7). |
| **Tested and rejected** | "Flooded vegetation" layer from HH brightening (F1 ≈ 0.02): growing rice also brightens HH. | Lớp "ngập dưới tán" từ HH sáng lên (F1 ≈ 0,02): lúa lớn cũng làm HH sáng lên. Đã loại khỏi sản phẩm. |

**EN:** F1 = how well two maps agree (1 = perfect).  **VI:** F1 = mức độ hai bản đồ khớp nhau (1 = khớp hoàn toàn).

---

## 7. Results 2026 / Kết quả mùa 2026

| EN | VI |
|---|---|
| **2026 was a low-flood year.** Water share of observed commune land rose from about 1–6 % in July to a peak of about **35 %** in mid-September to early October (083A 35.1 % on 11 Sep; 047D 33.8 % on 3 Oct), then declined. | **2026 là năm lũ thấp.** Tỉ lệ nước trên đất quan sát tăng từ khoảng 1–6% tháng 7 lên đỉnh khoảng **35%** từ giữa tháng 9 đến đầu tháng 10 (083A 35,1% ngày 11/9; 047D 33,8% ngày 3/10), sau đó giảm. |
| **Latest assessment (27 Oct – 3 Nov), 115 communes with ≥ 50 % of their area observed:** **33 high (≥ 30 %)**, **39 moderate (10–<30 %)**, **43 low (< 10 %)**. 25 communes lack sufficient observation (16 partial, 9 without an image) and are **not** counted as dry. | **Đánh giá gần nhất (27/10–3/11), 115 xã được quan sát ≥ 50% diện tích:** **33 nhiều nước (≥ 30%)**, **39 vừa (10–<30%)**, **43 ít (< 10%)**. 25 xã chưa đủ quan sát (16 xã một phần, 9 xã không có ảnh) và **không** bị tính là khô. |
| **Trend, same 115 communes:** **24 falling, 79 steady, 12 rising.** Level and trend differ: a commune can hold a lot of water and already be falling, or little water and rising (silt intake). | **Xu hướng, cùng 115 xã:** **24 đang giảm, 79 đứng yên, 12 đang tăng.** Mức nước và xu hướng là hai chuyện khác: xã nhiều nước vẫn có thể đang giảm, xã ít nước có thể đang tăng (lấy phù sa). |
| **Vĩnh Hưng** (Tây Ninh): 61.3 % on 27 Oct, steady (64.3 % on 15 Oct). | **Vĩnh Hưng** (Tây Ninh): 61,3% ngày 27/10, đứng yên (64,3% ngày 15/10). |
| **Phương Thịnh** (Đồng Tháp): 59.8 % on 27 Oct, rising. | **Phương Thịnh** (Đồng Tháp): 59,8% ngày 27/10, đang tăng. |
| **Tân Hồng** (Đồng Tháp): 43.7 % on 29 Oct and **falling** (50.0 % on 17 Oct), one week before its first sowing batch (5–11 Nov); matches reports of fields being pumped dry. | **Tân Hồng** (Đồng Tháp): 43,7% ngày 29/10 và **đang giảm** (50,0% ngày 17/10), một tuần trước đợt 1 xuống giống (5–11/11); khớp tin ruộng đang được bơm rút. |
| **Lấp Vò** (Đồng Tháp): **rising** from 12.1 % to 20.1 % in late October; matches reports of cooperatives letting floodwater in for silt before pumping; first sowing batch later (24 Nov – 1 Dec). | **Lấp Vò** (Đồng Tháp): **đang tăng** từ 12,1% lên 20,1% cuối tháng 10; khớp tin HTX xả lũ lấy phù sa trước khi bơm; đợt 1 xuống giống muộn hơn (24/11–1/12). |
| **Tây Phú** (An Giang): 0 % on 3 Nov, drained. | **Tây Phú** (An Giang): 0% ngày 3/11, đã rút hết. |
| **Controlled flood release is visible:** 10 communes show the release signature (water arrives mid-August while the river is still low, sharp drop late September); 15 other patterns; 55 kept water late. | **Thấy được xả lũ có điều tiết:** 10 xã có dấu hiệu xả lũ (nước vào giữa tháng 8 khi sông còn thấp, rút mạnh cuối tháng 9); 15 xã kiểu khác; 55 xã giữ nước muộn. |

All examples are observed over ~100 % of their area. / Các xã ví dụ đều được quan sát gần 100% diện tích.

---

## 8. The app / Ứng dụng web (https://nisar-flood.skyradar.vn)

**EN:** Vietnamese / English (switch in the header), works on phones.  **VI:** Song ngữ Việt / Anh (nút ở thanh trên), dùng được trên điện thoại.

| Tab (EN / VI) | EN | VI |
|---|---|---|
| **Overview / Tổng quan** | Season story of the Mekong Delta; commune counts by latest water share (high / moderate / low / insufficient); priority list sorted by water, each with a trend tag (↓ falling, → steady, ↑ rising), date, coverage and "View map". | Câu chuyện mùa lũ ĐBSCL; số xã theo mức nước gần nhất (nhiều / vừa / ít / chưa đủ quan sát); danh sách xã ưu tiên theo mức nước, mỗi xã có nhãn xu hướng (↓ giảm, → đứng yên, ↑ tăng), ngày, độ phủ và nút "Xem bản đồ". |
| **Map / Bản đồ** | Communes coloured by latest water share; or "One satellite image" mode with the NISAR water layer and radar image for any of 33 acquisitions; time slider with only real dates, one lane per track, **Play**; simple / professional view. Commune panel: latest water share and date, coverage, **measured trend** (previous → latest image, same track), recommended action, evidence image, season chart per track. | Xã tô màu theo mức nước gần nhất; hoặc chế độ "Xem một lần chụp" với lớp nước NISAR và ảnh radar cho từng ảnh trong 33 ảnh; thanh thời gian chỉ có ngày chụp thật, mỗi quỹ đạo một làn, nút **Play**; chế độ đơn giản / chuyên nghiệp. Bảng chi tiết xã: mức nước và ngày gần nhất, độ phủ, **xu hướng đo được** (ảnh trước → ảnh gần nhất, cùng quỹ đạo), khuyến nghị, nút xem ảnh bằng chứng, biểu đồ cả mùa theo quỹ đạo. |
| **Reports / Báo cáo** | Season trend chart (rising / near peak / going down), flood calendar by month, flood duration, province comparison, commune table; CSV export. | Biểu đồ xu hướng cả mùa (lên / gần đỉnh / xuống), lịch ngập theo tháng, thời gian ngập, so sánh tỉnh, bảng xã; xuất CSV. |
| **Validation / Độ tin cậy** | Plain summary and limits; charts and tables vs optical maps and vs SWOT; agreement with DSWx-S1; method; what was dropped; sources. | Tóm tắt dễ hiểu và giới hạn; biểu đồ, bảng so với ảnh quang học và SWOT; mức khớp với DSWx-S1; phương pháp; những gì đã bỏ; nguồn. |
| **About / Giới thiệu** | Project intro, how to read the map, limits, sources, team. | Giới thiệu dự án, cách đọc bản đồ, giới hạn, nguồn, đội. |

---

## 9. Demo path for the video / Kịch bản thao tác khi quay

| # | EN | VI |
|---|---|---|
| 1 | Open https://nisar-flood.skyradar.vn/?lang=en (Overview). Hold 2 s on the season story and commune counts. | Mở web ở tiếng Anh (tab Overview). Dừng 2 giây ở phần câu chuyện mùa lũ và số xã. |
| 2 | Click **Map**. Switch to **One satellite image**, choose **Simple** view. | Bấm **Map**. Chuyển sang **One satellite image**, chọn **Simple**. |
| 3 | Click the first dot (17 Jun), then **Play** ▶: water spreads in Aug–Sep and shrinks in October. Run ~6 s, pause around **3 Oct**. | Bấm chấm đầu tiên (17/6) rồi **Play** ▶: nước lan rộng tháng 8–9 và co lại tháng 10. Chạy khoảng 6 giây, dừng quanh **3/10**. |
| 4 | Switch back to **Latest per commune**. Type **"Tan Hong"** in "Find a commune", Enter. Show the panel: 43.7 % on 29 Oct, **↓ Water falling** (50.0 % → 43.7 %, same orbit). | Về **Latest per commune**. Gõ **"Tan Hong"** vào ô tìm xã, Enter. Cho thấy bảng chi tiết: 43,7% ngày 29/10, **↓ Water falling** (50,0% → 43,7%, cùng quỹ đạo). |
| 5 | Optional: **"Lap Vo"** → **↑ Water rising** (silt intake before pumping). | Tuỳ chọn: **"Lap Vo"** → **↑ Water rising** (lấy phù sa trước khi bơm). |
| 6 | Click **Validation**: show the optical comparison (NISAR better than Sentinel-1 on 14 of 16 dates) and its chart. | Bấm **Validation**: cho thấy phần so với ảnh quang học (NISAR tốt hơn Sentinel-1 ở 14/16 ngày) và biểu đồ. |

**EN:** Record at 1920×1080 (or 1440×900), zoom 100 %, English UI; hide bookmarks and personal tabs.
**VI:** Quay ở 1920×1080 (hoặc 1440×900), zoom 100%, giao diện tiếng Anh; ẩn thanh dấu trang và các tab cá nhân.

---

## 10. Limits, and claims to avoid / Giới hạn và những điều không được tuyên bố

### Say clearly / Nói rõ

| EN | VI |
|---|---|
| Most NISAR products used are **provisional** (29 of 33). | Phần lớn ảnh NISAR là bản **tạm thời** (29/33). |
| Radar sees **water on the field**, not its cause (river flood, controlled release or pumping). | Radar thấy **nước trên ruộng**, không biết nguồn gốc (lũ sông, xả lũ có điều tiết hay bơm). |
| **Not early warning:** data arrive 2–3 days after each pass; one image per place every ~5–7 days. | **Không phải cảnh báo sớm:** dữ liệu có sau 2–3 ngày; mỗi nơi khoảng 5–7 ngày mới có một ảnh. |
| **Early season (Jun–Jul) is weak:** the fixed rule over-reports water on smooth dry fields (F1 vs DSWx-S1 0.07–0.19). The tool targets the flood and drainage period (Aug–Nov). | **Đầu mùa (tháng 6–7) yếu:** quy tắc cố định báo thừa nước trên ruộng khô phẳng (F1 so với DSWx-S1 0,07–0,19). Công cụ dành cho mùa lũ và nước rút (tháng 8–11). |
| Water share refers to the **observed** part of a commune; communes observed below 50 % are not assessed. | Tỉ lệ nước tính trên phần xã **được quan sát**; xã quan sát dưới 50% không được đánh giá. |
| Validation references (OPERA DSWx, SWOT) are other satellite products, not field surveys. | Dữ liệu dùng để kiểm chứng (OPERA DSWx, SWOT) là sản phẩm vệ tinh khác, không phải khảo sát thực địa. |

### Must NOT claim / Không được tuyên bố

| EN | VI |
|---|---|
| That the app says **when to sow** or that a field is "ready to sow". It shows one condition (water on the field and its trend). Sowing also depends on the local calendar, synchronised sowing against brown planthoppers, the gap after the previous harvest, and secure irrigation water. | App cho biết **khi nào xuống giống** hay ruộng "sẵn sàng xuống giống". App chỉ cho thấy một điều kiện (nước trên ruộng và xu hướng). Xuống giống còn phụ thuộc lịch thời vụ địa phương, gieo đồng loạt né rầy nâu, thời gian cách ly sau thu hoạch vụ trước, và chủ động nước tưới. |
| Any **forecast** of when water will be gone (not made on purpose: 2–3 images, levels set by sluices and pumping). | Bất kỳ **dự báo** ngày nước rút hết (cố ý không làm: chỉ 2–3 ảnh, mực nước do cống và bơm quyết định). |
| That NISAR "sees water under the rice canopy" as a validated product (that layer was rejected). | NISAR "thấy nước dưới tán lúa" như một sản phẩm đã kiểm chứng (lớp đó đã bị loại). |
| That results cover the whole Mekong Delta (study area: 140 communes in the upper delta). | Kết quả phủ toàn ĐBSCL (vùng nghiên cứu chỉ 140 xã vùng đầu nguồn). |
| Real-time status ("today"): every figure belongs to an acquisition date. | Tình trạng "hôm nay": mọi con số gắn với một ngày chụp. |
| Field validation (none was done). | Đã kiểm chứng thực địa (chưa làm). |

---

## 11. Slide outline (7 slides) / Dàn ý 7 slide

Slide text must be the EN column; the VI column explains it for the team. / Chữ trên slide dùng cột EN; cột VI để đội hiểu.

| # | Title (EN) | Message (EN) | On the slide (EN) | Visual | VI: ý chính của slide |
|---|---|---|---|---|---|
| 1 | **Is the field dry yet?** | After the Mekong flood, provinces must decide commune by commune whether rice can be sown, but clouds hide the fields. | Mekong Delta; flood Aug–Nov; winter–spring crop; El Niño risk, sowing must not be late; users: provincial agriculture departments | Map tab, latest per commune | Vấn đề: sau lũ phải quyết định xuống giống theo từng xã nhưng mây che ruộng. |
| 2 | **Why NISAR L-band** | L-band radar sees through clouds and finds more of the water in rice fields than C-band. | 24 cm wavelength; calm water = dark in HH and HV; 3 tracks × 12-day repeat, an image every ~5–7 days; 33 acquisitions, 17 Jun – 3 Nov 2026 | Radar image + water layer (Map, one satellite image) | Vì sao NISAR: radar băng L xuyên mây, thấy nhiều nước trên ruộng hơn băng C. |
| 3 | **From NISAR files to commune answers** | We stream only the area we need and turn radar into water maps and commune statistics. | CMR → partial read on Earthdata Cloud (minutes, not GB) → 20 m grid → HH < −14 dB & HV < −22 dB, ≥ 3 ha → per commune, per track → latest assessment + measured trend | 5-box pipeline diagram | Phương pháp: chỉ đọc phần cần, ra bản đồ nước rồi thống kê theo xã. |
| 4 | **Demo** | One page answers: where is water now, since when, and is it going down? | Overview counts; Map with Play; commune panel (Tân Hồng ↓ falling) | 2–3 app screenshots | Demo: một trang trả lời nước ở đâu, từ khi nào, có đang rút không. |
| 5 | **Does it work?** | Against independent optical maps, NISAR beats Sentinel-1 on 14 of 16 dates. | F1 0.57–0.86 vs 0.50–0.78; finds 47–82 % vs 35–64 % of optical water; vs SWOT 11 of 12 dates; calibrated on 2 dates only; flooded-vegetation layer rejected | `fig2_validation_optical.png` | Độ tin cậy: thắng Sentinel-1 ở 14/16 ngày so với ảnh quang học, 11/12 ngày so với SWOT. |
| 6 | **What it shows in 2026** | A low-flood year, and drainage is visible commune by commune. | 115 communes assessed: 33 high / 39 moderate / 43 low; trend 24 falling / 79 steady / 12 rising; Tân Hồng falling a week before sowing; Lấp Vò rising (silt intake); flood release visible in 10 communes | `fig3_commune_examples.png` or `fig5_sowing_check.png`; small `fig4_flood_release.png` | Kết quả 2026: năm lũ thấp, thấy rõ nước rút theo từng xã. |
| 7 | **Limits, next steps, team** | Honest about what radar can and cannot say; next, put it next to the sowing calendar. | Limits (max 4 bullets from section 10). Next: commune sowing calendars next to water level and trend; planthopper light-trap and salinity data; detect the previous harvest with NISAR; whole delta; updates after each pass. Team. Credits. App + repo links | Team line, QR code to the app | Giới hạn, hướng phát triển (đặt cạnh lịch thời vụ, số liệu rầy, mặn, phát hiện thu hoạch), đội, nguồn. |

**EN — speaker notes:** one idea per slide; numbers exactly as above; explain any term in plain words ("F1 = how well two
maps agree, 1 = perfect").
**VI — ghi chú thuyết trình:** mỗi slide một ý; số giữ đúng như trên; thuật ngữ nào cũng giải thích bằng lời thường.

---

## 12. Video script / Kịch bản video

### 30 seconds (recommended) / 30 giây (khuyến nghị)

| Time | Picture (EN) | Voice-over / on-screen text (EN, use this) | VI (để đội hiểu) |
|---|---|---|---|
| 0:00–0:05 | Overview tab, Mekong Delta map | "Mekong Delta, autumn 2026. The flood is going down. Is this commune's rice land dry enough to sow?" | "ĐBSCL, mùa thu 2026. Lũ đang rút. Ruộng lúa của xã này đã đủ khô để xuống giống chưa?" |
| 0:05–0:15 | Map, one satellite image, Play from June to October | "NASA–ISRO NISAR's L-band radar sees water on the fields through the clouds — 33 images from three orbits." | "Radar băng L của NISAR thấy nước trên ruộng xuyên qua mây — 33 ảnh từ ba quỹ đạo." |
| 0:15–0:22 | Click Tân Hồng → 43.7 % and "↓ Water falling" | "For each of 140 communes: how much water is left, and whether it is going down." | "Với từng xã trong 140 xã: còn bao nhiêu nước, và nước có đang giảm không." |
| 0:22–0:27 | Validation tab chart | "Checked against independent optical maps, NISAR finds more of the water than Sentinel-1 on 14 of 16 dates." | "So với ảnh quang học độc lập, NISAR phát hiện nước tốt hơn Sentinel-1 ở 14/16 ngày." |
| 0:27–0:30 | Title card: app URL, team, "NASA Space Apps 2026 · Hanoi" | "SkyRadar NISAR Water Pulse." | Màn hình cuối: link app, tên đội. |

### 60 seconds (optional) / 60 giây (tuỳ chọn)

| EN | VI |
|---|---|
| After 0:15 add: Lấp Vò rising (silt intake); Reports tab season chart (peak about 35 % in mid-September); one limit sentence: "Radar shows water on the field, not when to sow; that stays with the local sowing calendar." | Sau giây 15 thêm: Lấp Vò đang tăng (lấy phù sa); biểu đồ cả mùa ở tab Reports (đỉnh khoảng 35% giữa tháng 9); một câu giới hạn: "Radar cho thấy nước trên ruộng, không quyết định ngày xuống giống; việc đó theo lịch thời vụ địa phương." |

### Production notes / Ghi chú sản xuất

| EN | VI |
|---|---|
| English captions burned in; no music with vocals; no people. | Phụ đề tiếng Anh gắn cứng vào video; nhạc không lời; không có người. |
| End card credits: "NISAR data: NASA/JPL-Caltech & ISRO (ASF DAAC). OPERA DSWx and SWOT: NASA JPL / CNES (PO.DAAC). Basemap © Esri; boundaries © OpenStreetMap contributors." | Màn hình cuối ghi nguồn đúng như câu tiếng Anh bên trái. |

---

## 13. Numbers and sources / Con số và nguồn

Files in `data/web/stats/` of `SkyRadar-org/skyradar-nisar` (`main`). / Các file nằm trong `data/web/stats/`.

| Number (EN) / Con số (VI) | Value / Giá trị | Source / Nguồn |
|---|---|---|
| NISAR acquisitions, tracks, period / Số ảnh, quỹ đạo, thời gian | 33; 047D, 083A, 148D; 17 Jun – 3 Nov 2026 | `data/web/manifest.json` |
| Provisional / validated / Tạm thời / đã kiểm định | 29 / 4 | `manifest.json` (`maturity`) |
| Communes in study area / Số xã | 140 | `data/boundaries/communes_aoi.geojson` |
| Water rule / Quy tắc nước | HH < −14 dB, HV < −22 dB, ≥ 3 ha | `calibration.json`, `src/skyradar_nisar/config.py` |
| NISAR vs Sentinel-1 against optical / So với ảnh quang học | 14 of 16; F1 0.57–0.86 vs 0.50–0.78; recall 47–82 % vs 35–64 %; NISAR-only water confirmed 53–98 % | `vs_dswx_hls.csv` |
| vs SWOT / So với SWOT | 11 of 12 dates | `vs_swot.csv` |
| vs DSWx-S1 | median F1 0.63, 25 dates | `vs_dswx_s1.csv` (`role = validation`) |
| Early-season F1 / F1 đầu mùa | 0.07–0.19 (Jun–Jul) | `vs_dswx_s1.csv` |
| Latest assessment / Đánh giá gần nhất | 115 communes: 33 / 39 / 43; 16 partial | `sowing_check.csv` (`status`: still_wet / draining / ready / partial) |
| Trend / Xu hướng | 24 falling / 79 steady / 12 rising | `sowing_check.csv` (`trend`) |
| Season peak / Đỉnh mùa | 35.1 % (083A, 11 Sep); 33.8 % (047D, 3 Oct) | `commune_water_by_date.csv` (water km² / observed km² per image) |
| Examples / Xã ví dụ | Vĩnh Hưng 61.3 % (27 Oct, steady); Phương Thịnh 59.8 % (27 Oct, rising); Tân Hồng 43.7 % (29 Oct, falling from 50.0 %); Lấp Vò 20.1 % (29 Oct, rising from 12.1 %); Tây Phú 0 % (3 Nov) | `sowing_check.csv` |
| Flood-release classes / Lớp xả lũ | A 10 / B 15 / C 55 | `commune_flood_class.csv` |
| Sowing calendars / Lịch xuống giống | Regional: 3 batches, done before 10 Jan 2027; An Giang 1–30 Nov & 1–31 Dec; Tân Hồng 5–11 Nov; Lấp Vò 24 Nov – 1 Dec | Press reports, see `docs/SOWING_CONDITIONS.md` (not checked against official documents / chưa đối chiếu văn bản gốc) |

---

## 14. Credits, licences, tools / Nguồn, giấy phép, công cụ

| EN | VI |
|---|---|
| NISAR L2 GCOV — NASA/JPL-Caltech and ISRO, distributed by the Alaska Satellite Facility DAAC. | Dữ liệu NISAR của NASA/JPL-Caltech và ISRO, phân phối qua ASF DAAC. |
| OPERA DSWx-S1 and DSWx-HLS — NASA JPL OPERA, distributed by PO.DAAC (contains modified Copernicus Sentinel data). | OPERA DSWx của NASA JPL, phân phối qua PO.DAAC (có dữ liệu Copernicus Sentinel đã xử lý). |
| SWOT L2 KaRIn High Rate Raster — NASA/CNES, distributed by PO.DAAC. | SWOT của NASA/CNES, phân phối qua PO.DAAC. |
| NASA CMR, NASA Earthdata Cloud. | Công cụ tìm và lưu trữ dữ liệu của NASA. |
| Boundaries and basemap data © OpenStreetMap contributors (ODbL); basemap © Esri. | Ranh giới xã và dữ liệu bản đồ nền © OpenStreetMap (ODbL); bản đồ nền © Esri. |
| Code licence: Apache-2.0. | Giấy phép mã nguồn: Apache-2.0. |
| Tools: Python (h5py, rasterio, numpy), FastAPI, TypeScript, Vite, MapLibre GL, Chart.js, Cloudflare Pages. | Công cụ lập trình như bên trái. |
| AI assistance: parts of the code and documentation were drafted with AI assistants (Claude, Codex, Gemini) and reviewed by the team. | Có dùng AI (Claude, Codex, Gemini) để soạn một phần code và tài liệu; đội đã rà soát. |

---

## 15. Related documents / Tài liệu liên quan

| File | EN | VI |
|---|---|---|
| `README.md` | How to run, method, validation, limits | Cách chạy, phương pháp, kiểm chứng, giới hạn |
| `docs/METHOD.md` | Full method and validation (English) | Phương pháp và kiểm chứng đầy đủ (tiếng Anh) |
| `docs/SUBMISSION.md` | Earlier drafts; use this brief where they differ | Bản nháp cũ; chỗ nào khác thì theo file này |
| `docs/SOWING_CONDITIONS.md` | Sowing conditions research (Vietnamese) | Tìm hiểu điều kiện xuống giống |
| `docs/HANDOFF.md`, `docs/UX_PLAN.md` | Team handoff and UI notes (Vietnamese) | Bàn giao và ghi chú giao diện |
