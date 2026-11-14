# HANDOFF — tài liệu bàn giao cho AI trợ lý mới (GPT / Codex / Copilot…)

Cập nhật: **14/11/2026 ~10:45 (giờ VN)**. Người viết: Claude (trợ lý của Chí). Đọc hết file này trước khi đụng vào code.
Ngôn ngữ làm việc của đội: tiếng Việt. Code, commit, tài liệu nộp bài: tiếng Anh.

---

## 0. Dự án trong 6 dòng

- **Cuộc thi:** NASA Space Apps Challenge 2026, Hà Nội, đề 5 **"Dancing with the SARs"** (bắt buộc dùng dữ liệu NASA–ISRO **NISAR**).
- **Đội:** SkyRadar (3 người).
- **Sản phẩm:** **NISAR Water Pulse**, công cụ giúp **Sở Nông nghiệp và Môi trường / Chi cục Thuỷ lợi** các tỉnh ĐBSCL theo dõi **ngập và nước rút trên ruộng lúa theo từng xã**, dùng radar băng L của NISAR (xuyên mây).
- **Ba câu hỏi sản phẩm trả lời:** xã nào đang có nước? Nước về từ khi nào? Đã rút kịp trước lịch xuống giống Đông Xuân (từ 1/11) chưa?
- **Vùng demo:** Tứ giác Long Xuyên và Đồng Tháp Mười, khung 104,95–106,0°E, 10,25–11,0°N, gồm 140 xã (ranh giới xã mới 2025 lấy từ OSM).
- **Dữ liệu:** 33 lần chụp NISAR L2 GCOV trên 3 track (047D, 083A, 148D), từ 17/06 đến 03/11/2026.
- **Hạn nộp: 15/11/2026 23:59.** Frontend đóng băng **09:30 Chủ nhật 15/11**. Đông deploy bản web 1 **trước 18:45 hôm nay (14/11)**.

## 1. Người và vai trò

| Người | Vai trò | Repo chính |
|---|---|---|
| **Chí** | Trưởng nhóm, **backend**, bài nộp, liên lạc với ban tổ chức | `skyradar-nisar` (thư mục `water-pulse-be/`) |
| **Đông** | Frontend (web app) | `water-pulse-fe` |
| **Đạt** | Dữ liệu, thuật toán, kiểm tra số liệu | `skyradar-nisar` (`src/`) |
| Claude | Đã viết pipeline, backend, tài liệu, các trang research | Làm việc trên nhánh `claude/...` |

## 2. Bản đồ repo và kết nối

| Repo | Hiển thị | Nhánh | Nội dung | Ghi chú |
|---|---|---|---|---|
| **[SkyRadar-org/skyradar-nisar](https://github.com/SkyRadar-org/skyradar-nisar)** | **public** | **`claude/compassionate-fermat-nqqh5z`** (nhánh duy nhất, **chưa có `main`**) | Pipeline Python (`src/skyradar_nisar`), gói dữ liệu web (`data/web`, 32 MB), **backend `water-pulse-be/`**, tài liệu (`docs/`) | Repo nộp bài. Commit mới nhất `ce81a1a` |
| **[SkyRadar-org/water-pulse-fe](https://github.com/SkyRadar-org/water-pulse-fe)** | private | `main` (lịch sử gộp thành 1 commit) | Frontend: Vite + TypeScript (không dùng framework), MapLibre GL 6, Chart.js, song ngữ VI/EN | Của Đông. **Đang ở `DATA_MODE = 'mock'`** (xem mục 5) |
| **[SkyRadar-org/skyradar-research](https://github.com/SkyRadar-org/skyradar-research)** | private | `main` | Web ghi chú kiểu Notion của đội (Next.js, Neon Postgres, BlockNote). Deploy tại **https://skyradar-research.vercel.app** | Chỉ là kho ghi chú, xoá sau cuộc thi. Tiến độ frontend ở `docs/PROGRESS_WATER_PULSE_FE.md` |
| duychris/skyradar-web | private | `main` | Dự án SkyRadar cũ (app mây và thời tiết) | Frontend đã chép sẵn file ranh giới tỉnh, biên giới và nhãn Hoàng Sa, Trường Sa vào `public/geo/`. Không cần đụng thêm |
| duychris/skyradar-mobile, duychris/skyradar-memory | private | — | App Flutter cũ; ghi chú nội bộ | **Không dùng** cho cuộc thi |

- **`water-pulse-be`** hiện là **thư mục** trong `skyradar-nisar`, chưa phải repo riêng. Nếu sau này tách repo, `scripts/sync_data.sh` đã sẵn sàng để chép dữ liệu.
- Repo private: muốn đọc, nhờ Chí cấp quyền.

### Luồng dữ liệu

```text
NASA Earthdata (ASF: NISAR GCOV; PO.DAAC: OPERA DSWx-S1 / DSWx-HLS)  ──token──►  src/skyradar_nisar (pipeline)
        │                                                                            │
        │                                                     data/processed (GeoTIFF, KHÔNG commit)
        │                                                                            │ export_web
        ▼                                                                            ▼
NASA GIBS (lớp NISAR, frontend gọi trực tiếp)                     data/web (PNG, JPG, GeoJSON, CSV, manifest.json)
        │                                                                            │
        │                                                water-pulse-be (FastAPI, đọc file, không có database)
        │                                                                            │  /api/*, /static/*
        └──────────────────────────────►  water-pulse-fe (Vite)  ◄───────────────────┘   ← CHƯA nối (mục 5)
```

## 3. Trạng thái hiện tại

### Đã xong
- **Pipeline đầy đủ:**
  - tìm ảnh qua CMR, rồi đọc nhanh GCOV (đọc song song các chunk HDF5 qua HTTP Range, khoảng 40 giây mỗi ngày chụp, cho kết quả trùng từng bit với h5py);
  - đưa về lưới 20 m (EPSG:32648), tách nước, hiệu chỉnh và kiểm chứng với OPERA DSWx;
  - tính thời gian ngập theo xã, dấu hiệu xả lũ, kiểm tra xuống giống;
  - xuất dữ liệu web và vẽ hình.
- **Backend FastAPI** (`water-pulse-be/`):
  - 14 endpoint, 6 test đều qua; có gzip, cache, CORS;
  - đã có Dockerfile và cấu hình Vercel (`api/index.py`, `vercel.json`);
  - **chưa deploy**.
- **Frontend** (Đông):
  - xong các task T0–T6, T8, T9, T11, song ngữ VI/EN;
  - **còn lại:** T7 deploy (Cloudflare Pages), **T10 nối dữ liệu thật**, T12 (tuỳ chọn), T13 đóng băng.
- **Tài liệu:** `docs/METHOD.md` (Method & Validation), `docs/SUBMISSION.md` (bản nháp bài nộp: tóm tắt, mô tả, dàn ý slide, kịch bản video), `docs/WEB_DATA.md`, `docs/BACKEND_API.md`, `docs/figures/fig1–fig5`.

### Số liệu chuẩn (lấy từ file, KHÔNG lấy từ trí nhớ)

| Nội dung | Giá trị | Nguồn |
|---|---|---|
| Quy tắc tách nước | HH < −14 dB **và** HV < −22 dB; mảng ≥ 3 ha; bỏ nước thường xuyên | `src/skyradar_nisar/config.py`, `data/web/stats/calibration.json` |
| So với DSWx-S1 (25 ngày độc lập) | F1 trung vị 0,63; mùa lũ 0,57–0,76; recall 0,87 | `data/web/stats/vs_dswx_s1.csv` |
| **So với ảnh quang học DSWx-HLS (16 ngày)** | **NISAR tốt hơn Sentinel-1 ở 14/16 ngày.** F1 0,57–0,86 so với 0,50–0,78. **Recall 0,47–0,82 so với 0,35–0,64.** 53–98% diện tích chỉ NISAR thấy nước thì ảnh quang học cũng thấy nước | `data/web/stats/vs_dswx_hls.csv` |
| Kiểm tra xuống giống (ảnh gần nhất phủ xã) | 131 xã: 53 sẵn sàng, 40 đang rút, **38 còn ngập** | `data/web/stats/sowing_check.csv` |
| Theo tỉnh (sẵn sàng / đang rút / còn ngập) | An Giang 28/22/6; Đồng Tháp 20/11/21; Tây Ninh 0/6/9; Cần Thơ 2/1/2; Vĩnh Long 3/0/0 | như trên |
| Dấu hiệu xả lũ | Lớp A 10 xã, B 15, C 55. Ba xã có tên trong tin xả lũ (Bình Mỹ, Thạnh Mỹ Tây, Bình Thạnh Đông) đều thuộc lớp A | `data/web/stats/commune_flood_class.csv` |
| Ví dụ xã còn ngập | Sơn Kiên còn khoảng 78–87% nước ngày 03/11 (tuỳ track) | `commune_water_by_date.csv` |
| Đã thử nhưng loại | Lớp "ngập dưới tán" (HH sáng lên): F1 khoảng 0,02 | `docs/METHOD.md` |

**Năm 2026 là năm lũ thấp.** Diện tích nước đạt đỉnh khoảng 36% vào cuối tháng 9 đến đầu tháng 10, khớp với mực nước trạm Tân Châu. Tin báo đầu tháng 11 cũng khớp: Đồng Tháp Mười đang bơm rút nước; Tân Hồng xuống giống đợt 1 từ 5/11.

## 4. Cách chạy

```bash
# Pipeline (cần token Earthdata; KHÔNG commit token)
git clone -b claude/compassionate-fermat-nqqh5z https://github.com/SkyRadar-org/skyradar-nisar.git
cd skyradar-nisar && pip install -r requirements.txt
export EARTHDATA_TOKEN=...   PYTHONPATH=src
python -m skyradar_nisar.fetch_gcov && python -m skyradar_nisar.fetch_dswx s1 && python -m skyradar_nisar.fetch_dswx hls
python -m skyradar_nisar.calibrate && python -m skyradar_nisar.timing && python -m skyradar_nisar.release
python -m skyradar_nisar.sowing 2026-11-01 && python -m skyradar_nisar.export_web && python -m skyradar_nisar.figures

# Backend (KHÔNG cần token, chỉ đọc ../data/web)
cd water-pulse-be && pip install -r requirements.txt -r requirements-dev.txt
uvicorn app.main:app --reload      # http://127.0.0.1:8000/docs
pytest -q

# Frontend
git clone https://github.com/SkyRadar-org/water-pulse-fe.git && cd water-pulse-fe
npm install && npm run dev         # http://localhost:5173 ; npm run mock để sinh lại dữ liệu giả
```

- **Không cần chạy lại pipeline** để làm web: `data/web` đã được commit.
- Tài khoản Earthdata phải cấp quyền cho ứng dụng *"Alaska Satellite Facility Data Access"*.

## 5. ⚠️ Việc gấp nhất: frontend và backend chưa nói cùng một ngôn ngữ

Frontend định nghĩa hợp đồng dữ liệu riêng trong `water-pulse-fe/src/data/types.ts` và `src/data/dataSource.ts` (3 chế độ `mock | static | api`). Backend được viết theo `docs/WEB_DATA.md` và `docs/BACKEND_API.md`. **Hai bên chưa khớp:**

| Frontend cần | Backend / `data/web` hiện có | Cần làm |
|---|---|---|
| `GET /api/scenes`: `Scene{date, track, maturity, bounds:[W,S,E,N], waterPng, gibsDate}` | `/api/manifest`, `/api/frames`: `bounds` dạng **`[[S,W],[N,E]]`** (kiểu Leaflet), `png_url`, `radar_url` | Thêm endpoint thích ứng (adapter) hoặc file tĩnh `scenes.json` |
| `waterPng`: 0 trong suốt, 1 nước (xanh), **3 nước thường xuyên (xám)** | PNG chỉ có nước xanh; nước thường xuyên đã bị bỏ | Chấp nhận như hiện tại, hoặc xuất thêm lớp xám |
| `GET /api/communes`: `CommuneProps{osm_id (string), name, province, valid_km2, first_flood_date, peak_pct, peak_date, half_date, recession_date, last_pct, last_date, max_flooded_km2, status}` | GeoJSON có `timing` lồng theo track và `flood_class` | Làm phẳng thuộc tính; cần chọn quy tắc gộp track |
| `status`: `receded \| not_receded \| uncertain \| no_flood` | Kiểm tra xuống giống: `ready \| draining \| still_wet` (`sowing_check.csv`) | **Chốt một bộ trạng thái.** Đề xuất: `ready`→`receded`, `still_wet`→`not_receded`, `draining`→`uncertain`; `no_flood` khi `peak_pct` < 5 |
| `GET /api/communes/{id}/series`: `[{date, track, water_pct, water_km2, valid_km2}]` | Có, nhưng tên trường khác | Đổi tên trường |
| `GET /api/choropleth?date=&track=`: `{osm_id: water_pct}` | Chưa có (dữ liệu có trong `commune_water_by_date.csv`) | Thêm mới |
| `GET /api/area`: `[{date, track, nisar_km2, dswx_km2}]` | Chưa có. `nisar_km2` lấy tổng `water_km2` từ `commune_water_by_date.csv`; `dswx_km2` suy ra từ `vs_dswx_s1.csv` (trong vùng chồng phủ, diện tích NISAR / DSWx = recall / precision) | Thêm mới |
| `GET /api/summary`: lớp `flood_count`, `first_flood_date`, `recession_date` (png, bounds, legend) | Có `summary/first_flood.png` và `summary/recession.png`; **chưa có `flood_count`** | Thêm mới hoặc bỏ lớp này |
| `GET /api/validation`: `{vsHls:[{f1_nisar, f1_s1, recall_*, precision_*, nisar_only_true_pct}], vsDswxS1:[{date, track, f1}], notes}` | `/api/validation` trả nguyên nội dung CSV | Đổi định dạng |

**Hướng đề xuất (nhanh và ít rủi ro):**
- Viết `export_fe.py`, hoặc thêm các endpoint `/api/scenes|choropleth|area|summary` vào backend, sinh **đúng định dạng frontend** từ `data/web`.
- Frontend chỉ cần chuyển sang `DATA_MODE='static'` (chép vào `public/data/`) hoặc `'api'` (backend đã deploy, CORS cho domain frontend).
- **Chế độ `static` không cần backend deploy** nên an toàn nhất cho hạn chót.
- Khi chuyển sang dữ liệu thật, dùng mock của Đông để đối chiếu: Sơn Kiên, top 10 xã, bảng F1.

**Số liệu sai cần sửa trong frontend** (đang chép từ kế hoạch cũ 22 ngày, chưa đúng với 33 ảnh):
- `src/locales/en.ts` dòng 155, 226 và `vi.ts` dòng 156, 227 ghi "64–77% vs 43–60%". Số đúng là recall **47–82% vs 35–64%**, NISAR tốt hơn ở **14/16 ngày**.
- `en.ts` dòng 225 ghi "50 of 80 communes not drained halfway by 29 Oct": cần tính lại từ dữ liệu thật hoặc thay bằng "38 of 131 communes still wet on the latest image".
- "NISAR area ~1.4–1.5× DSWx-S1": cần kiểm lại (tỉ lệ = recall / precision trong `vs_dswx_s1.csv`).
- Trang About ghi "22 NISAR passes": số đúng là **33 lần chụp trên 3 track**.

## 6. Việc còn mở (theo thứ tự ưu tiên)

1. **Nối frontend với dữ liệu thật** (mục 5): Chí làm, cùng Đông.
2. Đông deploy frontend (Cloudflare Pages: `npm run build` ra thư mục `dist/`). Cần tài khoản của đội.
3. Deploy backend (Vercel hoặc Docker/Render): **chỉ cần nếu dùng chế độ `api`**. Trước khi deploy, chạy `scripts/sync_data.sh ..`.
4. Chốt `docs/SUBMISSION.md`: tóm tắt, mô tả, slide, video, link demo, link repo.
5. Tạo nhánh `main` cho `skyradar-nisar` từ nhánh `claude/...` (repo nộp bài nên có `main`). **Hỏi Chí trước.**
6. Đọc Judging Guide: https://www.spaceappschallenge.org/resources/judging-awards-guide/ (mỗi tiêu chí chấm 1–5 điểm). Môi trường của Claude không mở được trang này.
7. Sáng 15/11 truy vấn lại CMR để lấy ảnh NISAR mới (nếu có), rồi chạy lại pipeline và `export_web`.
8. Chưa tìm được văn bản gốc danh sách xã xả lũ theo Kế hoạch 457/KH-UBND (tuỳ chọn).
9. Người Việt đọc lại bản dịch `water-pulse-fe/src/locales/vi.ts`.

## 7. Quy tắc bắt buộc

- **Không bao giờ commit hoặc in ra bí mật:**
  - token Earthdata, `.netrc`, `.env`, `INGEST_API_KEY`, mật khẩu web research, `DATABASE_URL`;
  - `skyradar-nisar` là repo **public**;
  - cần thông tin đăng nhập thì hỏi Chí.
- **Không dùng GitHub Actions**: đội đã bỏ, đừng thêm lại.
- **Ghi nguồn:** NISAR (NASA/JPL-Caltech & ISRO, ASF DAAC), OPERA DSWx (JPL, PO.DAAC), NASA GIBS, **© OpenStreetMap contributors (ODbL)**. Mẫu có sẵn trong `manifest.json` → `attribution`. **Không** cần ghi "dùng lại từ SkyRadar".
- **Quy tắc hiển thị** (frontend đã tuân theo, giữ nguyên):
  - không nội suy theo thời gian;
  - **không gộp các track** (mỗi track một đường, do góc chụp khác nhau, chênh trung vị 3,4 điểm %);
  - ảnh trước 22/10/2026 gắn nhãn **Provisional**;
  - không dùng màu làm cách duy nhất để truyền thông tin.
- **Bản đồ Việt Nam:** phải có Hoàng Sa và Trường Sa (frontend đã có `public/geo/`). Không dùng nhãn quốc tế sai chủ quyền.
- Commit nhỏ, thông điệp tiếng Anh. Chỉ push lên nhánh được giao; **hỏi Chí trước khi tạo PR, merge hoặc tạo `main`**.
- **Không bịa số liệu.** Mọi con số trên slide hoặc web phải truy được về một file trong `data/web/stats/`.

## 8. Bẫy kỹ thuật đã gặp (đừng lặp lại)

- **NASA GIBS, lớp `NISAR_L2_Geocoded_Polarimetric_Covariance`:**
  - zoom **11–13 trả về tile hỏng**, nên đặt `maxzoom: 10`;
  - ngoài dải quét GIBS trả HTTP 500;
  - có thể thay bằng `data/web/radar/<date>_<track>.jpg` (khoảng 60 m, cùng `bounds` với ảnh lớp nước, khớp từng pixel).
- **MapLibre GL 6:**
  - cần `setWorkerUrl` và `optimizeDeps.exclude` trong Vite, thiếu thì GeoJSON không tải;
  - MapLibre dùng tile 512 nên `zoom` lệch 1 mức so với Leaflet.
- **Nền bản đồ:** CARTO miễn phí giờ đòi API key, frontend đang dùng Esri World Light Gray.
- **GCOV:**
  - giá trị là γ⁰ dạng công suất tuyến tính (đổi sang dB = 10·log10);
  - `mask` 0 hoặc 255 là pixel không hợp lệ;
  - lấy trung bình trong miền công suất, không lấy trung bình trên dB;
  - URL tải là link CloudFront có chữ ký, mỗi link chỉ resolve một lần.
- **Ngưỡng tách nước:**
  - Otsu theo từng ngày cho kết quả sai, nên dùng ngưỡng cố định đã hiệu chỉnh;
  - track 148D không có DSWx-S1 cùng ngày để so;
  - chỉ so với DSWx-HLS trong mùa lũ (từ 01/08), vì ảnh tháng 6–7 nhiều mây và xử lý chậm.
- **Overpass API:** máy chủ chính hay timeout, dùng mirror `overpass.kumi.systems` và Nominatim.
- **Kiểm tra xuống giống:**
  - lấy **ảnh gần nhất phủ ≥ 50% xã** (không lấy trường hợp xấu nhất của mọi track, vì cách đó gây sai, ví dụ ở Tân Hồng);
  - ngưỡng: < 10% là sẵn sàng, 10–30% là đang rút, ≥ 30% là còn ngập.
- **Web research:**
  - API của editor (BlockNote) từ chối text vừa **đậm vừa code**;
  - trạng thái task chỉ nhận `todo | blocked | done`;
  - đăng bài qua `POST /api/ingest` (cần key; hướng dẫn ở `skyradar-research/docs/AI_INGEST_PROMPT.md`).

## 9. Đọc gì tiếp

1. `README.md` (repo này): cấu trúc, cách chạy, phương pháp, giới hạn.
2. `docs/WEB_DATA.md` và `water-pulse-be/README.md`: định dạng dữ liệu và các endpoint.
3. `water-pulse-fe/README.md`, `src/data/types.ts`, `src/data/dataSource.ts`: hợp đồng dữ liệu phía frontend.
4. `skyradar-research/docs/PROGRESS_WATER_PULSE_FE.md`: tiến độ và các quyết định của Đông.
5. `docs/METHOD.md`, `docs/SUBMISSION.md`: nội dung bài nộp.
6. Web research (đăng nhập bằng tài khoản Chí cấp): trang "Báo cáo tiến độ sáng 14/11", "Phân công", "Kết quả … và hiệu chỉnh", "Bản nháp nộp bài (EN)".

## 10. Thuật ngữ

| Tiếng Việt | Tiếng Anh / trong code |
|---|---|
| Xã / tỉnh | commune (`osm_id`) / province |
| Track / quỹ đạo | track `047D`, `083A`, `148D` (D = descending, A = ascending) |
| Nước rút | recession (`recession_date`, `halved_after_peak`) |
| Xả lũ (có điều tiết) vào ô bao | controlled flood release into dyke compartments (`flood_class` A/B/C) |
| Sẵn sàng / đang rút / còn ngập | `ready` / `draining` / `still_wet` |
| Tạm thời / đã kiểm định | Provisional / Validated (`maturity`) |
