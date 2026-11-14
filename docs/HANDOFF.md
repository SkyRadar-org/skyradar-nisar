# HANDOFF — tài liệu bàn giao cho AI trợ lý mới (GPT / Codex / Copilot…)

Cập nhật: **14/11/2026 ~14:30 (giờ VN)**. Người viết: Claude (trợ lý của Chí). Đọc hết file này trước khi đụng vào code.
**Việc UI/UX còn lại và kế hoạch 4 gói việc: xem `docs/UX_PLAN.md`.**
**Triển khai đã kiểm, người dùng đã duyệt merge main; trạng thái phát hành xem checkpoint của nhánh `codex/ux-implementation-20261114`: [checkpoint](verification/ux-implementation-20261114/checkpoint.md). Chưa phát hành production.**
**Phản biện kế hoạch ngày 14/11/2026 (Codex + Gemini, hai vòng): xem [báo cáo và bằng chứng](verification/ux-plan-review-20261114/README.md). Bản đánh giá ban đầu; trạng thái triển khai xem checkpoint mới ở trên. Đính chính: mục hướng dẫn đã có wrapper `<details>` tại chỗ `root.replaceChildren`; nhận xét bác Gemini về điểm này trong bản đánh giá là sai.**
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
| **[SkyRadar-org/skyradar-nisar](https://github.com/SkyRadar-org/skyradar-nisar)** | **public** | **`main`** (nhánh chính, gộp nhánh Claude, Codex, Đạt) | Pipeline Python (`src/skyradar_nisar`), gói dữ liệu web (`data/web`, 32 MB), **backend `water-pulse-be/`**, tài liệu (`docs/`) | Repo nộp bài. Có thêm `scripts/export_pages.py` (xuất API cho Cloudflare) |
| **[SkyRadar-org/water-pulse-fe](https://github.com/SkyRadar-org/water-pulse-fe)** | private | `main`; nhánh `codex/local-cloudflare-20261114` = **đúng bản đang chạy** (Đông merge vào `main`) | Frontend: Vite + TypeScript (không dùng framework), MapLibre GL 6, Chart.js, song ngữ VI/EN | Của Đông. Deploy tại **https://nisar-flood.skyradar.vn** (Cloudflare Pages + Worker, dữ liệu thật) |
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
        └──────────────────────────────►  water-pulse-fe (Vite)  ◄───────────────────┘   (Cloudflare: bản chụp JSON của /api/frontend/*)
```

## 3. Trạng thái hiện tại

### Đã xong
- **Pipeline đầy đủ:**
  - tìm ảnh qua CMR, rồi đọc nhanh GCOV (đọc song song các chunk HDF5 qua HTTP Range, khoảng 40 giây mỗi ngày chụp, cho kết quả trùng từng bit với h5py);
  - đưa về lưới 20 m (EPSG:32648), tách nước, hiệu chỉnh và kiểm chứng với OPERA DSWx;
  - tính thời gian ngập theo xã, dấu hiệu xả lũ, kiểm tra xuống giống;
  - xuất dữ liệu web và vẽ hình.
- **Backend FastAPI** (`water-pulse-be/`):
  - 14 endpoint gốc cộng adapter `/api/frontend/*` đúng định dạng frontend (Codex); 11 test đều qua;
  - không cần chạy server: `scripts/export_pages.py` xuất toàn bộ câu trả lời thành JSON cho Cloudflare;
  - vẫn có Dockerfile và cấu hình Vercel nếu cần server thật.
- **Frontend** (Đông):
  - đã nối dữ liệu thật và **deploy tại https://nisar-flood.skyradar.vn** (Codex, 14/11); có tab Tổng quan, lớp ảnh radar riêng;
  - build: `npm run build:cloudflare` (cần repo `skyradar-nisar` đặt cạnh), rồi `npm run test:cloudflare`;
  - **bản cũ dữ liệu giả vẫn còn ở water-pulse.pages.dev**, cần tắt hoặc chuyển hướng.
- **Tài liệu:** `docs/METHOD.md` (Method & Validation), `docs/SUBMISSION.md` (bản nháp bài nộp: tóm tắt, mô tả, dàn ý slide, kịch bản video), `docs/WEB_DATA.md`, `docs/BACKEND_API.md`, `docs/figures/fig1–fig5`.

### Số liệu chuẩn (lấy từ file, KHÔNG lấy từ trí nhớ)

| Nội dung | Giá trị | Nguồn |
|---|---|---|
| Quy tắc tách nước | HH < −14 dB **và** HV < −22 dB; mảng ≥ 3 ha; bỏ nước thường xuyên | `src/skyradar_nisar/config.py`, `data/web/stats/calibration.json` |
| So với DSWx-S1 (25 ngày độc lập) | F1 trung vị 0,63; mùa lũ 0,57–0,76; recall 0,87 | `data/web/stats/vs_dswx_s1.csv` |
| **So với ảnh quang học DSWx-HLS (16 ngày, chỉ mùa lũ tháng 8–11)** | **NISAR tốt hơn Sentinel-1 ở 14/16 ngày.** F1 0,57–0,86 so với 0,50–0,78. **Recall 0,47–0,82 so với 0,35–0,64.** 53–98% diện tích chỉ NISAR thấy nước thì ảnh quang học cũng thấy nước | `data/web/stats/vs_dswx_hls.csv` |
| Kiểm tra xuống giống (ảnh gần nhất phủ xã) | 115 xã đủ phủ: 43 ít nước, 39 một phần nước, **33 nhiều nước**; 25/140 xã chưa đủ đánh giá | `data/web/stats/sowing_check.csv` |
| Theo tỉnh (sẵn sàng / đang rút / còn ngập) | Ít / trung bình / nhiều: An Giang 24/22/3; Đồng Tháp 16/11/21; Tây Ninh 0/5/8; Cần Thơ 0/1/1; Vĩnh Long 3/0/0 | như trên |
| Dấu hiệu xả lũ | Lớp A 10 xã, B 15, C 55. Ba xã có tên trong tin xả lũ (Bình Mỹ, Thạnh Mỹ Tây, Bình Thạnh Đông) đều thuộc lớp A | `data/web/stats/commune_flood_class.csv` |
| Ví dụ xã còn ngập | Vĩnh Hưng (Tây Ninh, ID 15012314): 61,3% phần quan trắc có nước ngày 27/10, phủ gần 100% xã; Sơn Kiên chỉ phủ 19,68%, không được đánh giá | `commune_water_by_date.csv` |
| Đầu mùa (tháng 6–7) | Yếu: F1 so với DSWx-S1 chỉ 0,07–0,19 (báo thừa nước trên ruộng khô). Sản phẩm dành cho mùa lũ và nước rút (tháng 8–11) | `vs_dswx_s1.csv` |
| Diện tích NISAR so với DSWx-S1 (mùa lũ, cùng pixel) | 1,0–2,1 lần, trung vị 1,65 lần | `vs_dswx_s1.csv` (recall / precision) |
| Đã thử nhưng loại | Lớp "ngập dưới tán" (HH sáng lên): F1 khoảng 0,02 | `docs/METHOD.md` |

**Năm 2026 là năm lũ thấp.** Diện tích nước đạt đỉnh khoảng 36% vào cuối tháng 9 đến đầu tháng 10, khớp với mực nước trạm Tân Châu. Tin báo đầu tháng 11 cũng khớp: Đồng Tháp Mười đang bơm rút nước; Tân Hồng xuống giống đợt 1 từ 5/11.

## 4. Cách chạy

```bash
# Pipeline (cần token Earthdata; KHÔNG commit token)
git clone https://github.com/SkyRadar-org/skyradar-nisar.git
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

## 5. Frontend và backend: đã nối (14/11)

- Định dạng dữ liệu của frontend nằm ở `water-pulse-fe/src/data/types.ts`. Backend phục vụ đúng định dạng đó qua `water-pulse-be/app/frontend.py` (`/api/frontend/scenes|communes|communes/{id}/series|choropleth|area|summary|validation`).
- **Trạng thái xã:** `ready`→`receded`, `draining`→`uncertain`, `still_wet`→`not_receded`. Thêm `no_flood` khi đỉnh < 5%. Xã không đủ ảnh phủ thì `uncertain` kèm `coverage_sufficient=false`.
- **Số liệu thống kê dùng một track tham chiếu**, là track của ảnh gần nhất phủ ít nhất nửa xã (`reference_track`). Chuỗi thời gian giữ riêng từng track.
- **Cố ý để trống:**
  - `dswx_km2` là `null`, vì chưa có tổng DSWx trên cùng vùng;
  - `summary` là `[]`, vì ảnh tổng kết hiện gộp các track. Đạt đang xuất bản theo từng track.
- **Khi `data/web` thay đổi:** chạy `npm run build:cloudflare`, `npm run test:cloudflare`, rồi deploy lại.

## 6. Việc còn mở (theo thứ tự ưu tiên)

Lịch chi tiết từng người: trang "Giao việc chiều 14/11: Đông & Đạt" trên web research.

1. Đông đưa `main` của `water-pulse-fe` về đúng nhánh `codex/local-cloudflare-20261114`; tắt bản dữ liệu giả ở water-pulse.pages.dev.
2. Sửa chữ trên web: ghi "mùa lũ (tháng 8–11)" cạnh số kiểm chứng với ảnh quang học, thêm giới hạn đầu mùa (mục 3).
3. Tự host font bản đồ, vì `demotiles.maplibre.org` chỉ là máy chủ demo.
4. Chốt `docs/SUBMISSION.md`: tóm tắt, mô tả, slide, video, link demo, link repo.
5. Đọc Judging Guide: https://www.spaceappschallenge.org/resources/judging-awards-guide/ (mỗi tiêu chí chấm 1–5 điểm).
6. Sáng 15/11 truy vấn lại CMR để lấy ảnh NISAR mới (nếu có), rồi chạy lại pipeline và `export_web`. Nếu số liệu đổi, cập nhật luôn các số kiểm tra trong `water-pulse-be/tests`.
7. Tuỳ chọn: lớp tổng kết mùa theo từng track (Đạt); văn bản gốc Kế hoạch 457/KH-UBND.
8. Người Việt đọc lại bản dịch `water-pulse-fe/src/locales/vi.ts`.

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
  - ngưỡng tỷ lệ nước trên phần quan trắc: <10% ít nước, 10–<30% một phần nước, ≥30% nhiều nước; không tự suy ra sẵn sàng xuống giống hoặc xu thế nước rút.
  - chọn ảnh mới nhất đạt ≥50% diện tích toàn xã OSM và ≥5 km² trước làm tròn; ảnh mới phủ ít không thay thế ảnh cũ đủ điều kiện.
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
