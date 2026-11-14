# UX_PLAN — đánh giá UI/UX và kế hoạch sửa (để làm tiếp trên máy local)

Cập nhật: **14/11/2026 ~19:00 (giờ VN)**. Người viết: Claude (phiên cloud của Chí).
Đọc kèm `docs/HANDOFF.md` (bối cảnh dự án, repo, quy tắc commit). File này chỉ nói về **UI/UX và 4 gói việc còn lại**.

- Web thật: https://nisar-flood.skyradar.vn (tự deploy khi push vào `main` của `water-pulse-fe`, qua GitHub Actions).
- Trạng thái code lúc viết: `skyradar-nisar` `main` = `79ec208`; `water-pulse-fe` `main` = `4f59e90`.
- Hạn: đóng băng tính năng **11:00 ngày 15/11**, nộp bài **23:59 ngày 15/11**.
- Tiêu chí chấm Space Apps (bản 2025; **cần mở bản 2026 để xác nhận**): Impact, Creativity, Validity, Relevance, Presentation.

---

## 1. Kết luận đánh giá

Web nhiều chức năng và trung thực về dữ liệu, nhưng **giống bảng điều khiển nội bộ hơn là sản phẩm dự thi**. Trong 10 giây đầu, người chấm không thấy câu chuyện, không thấy bản đồ, không thấy ảnh NISAR.

Cách đánh giá: mở web thật, chụp 5 tab ở 1440×900 và 390×844, cả VI và EN; đo số chữ, cỡ chữ, số nút; đối chiếu số liệu với `data/web/stats/*.csv`.

| # | Phát hiện | Mức | Thuộc gói |
|---|---|---|---|
| 1 | Nhãn "đủ độ phủ ≥ 50%" sai nghĩa: tính so với phần xã nằm trong khung dữ liệu, không so với diện tích thật. 16/131 xã được xếp loại trên < 50% diện tích thật, gồm các xã đội lấy làm ví dụ (Sơn Kiên 20%, Hòn Đất 24%, Mỹ Thuận 4%) | 🔴 | G1 |
| 2 | Trang mở đầu (tab Tổng quan) là bảng số liệu ~600 chữ, không có câu chuyện. Khối giới thiệu hay nhất nằm ở tab cuối (Giới thiệu) | 🔴 | G2 |
| 3 | Ảnh NISAR bị giấu: bản đồ mặc định chỉ tô màu xã; lớp nước và radar chỉ hiện sau khi bấm "Xem một lần chụp" | 🔴 | G2 |
| 4 | Màn bản đồ có 51 nút và 3 cặp chế độ ("Ảnh gần nhất / Một lần chụp", "Chuyên nghiệp / Đơn giản", "Tất cả quỹ đạo / 3 track") | 🟡 | G4 |
| 5 | Tab Độ tin cậy: biểu đồ và bảng bằng chứng (ảnh quang học, SWOT) nằm trong mục "Technical details" đóng sẵn | 🟡 | G3 |
| 6 | Bản đồ chỉ chiếm ~55% chiều cao màn hình (thanh trên + khối tiêu đề + thanh thời gian + chân trang) | 🟡 | G4 |
| 7 | Chữ nhỏ (Tổng quan: 77 đoạn chữ cỡ 11–12 px), nhiều thuật ngữ ("water fraction", "standing water", "coverage"), tiêu đề lúc Title Case lúc viết thường | 🟡 | G4 |
| 8 | Màu đỏ/cam/xanh lá: người mù màu đỏ–lục khó phân biệt; đỏ gợi "nguy hiểm" dù ngập mùa lũ có thể bình thường | 🟢 | tuỳ chọn |
| 9 | Điện thoại: thanh trên khác nhau giữa các tab; bản đồ mở quá gần | 🟢 | tuỳ chọn |

**Điểm làm tốt, giữ nguyên:** thanh thời gian chỉ có ngày chụp thật và 3 track tách riêng; nhãn Tạm thời / Đã kiểm định; câu "không phải tình trạng trực tiếp hôm nay"; bảng xã có câu khuyến nghị và nút xem ảnh làm bằng chứng; song ngữ; xuất báo cáo; Play.

---

## 2. Số liệu của phát hiện 1 (độ phủ theo diện tích thật)

Nguyên nhân trong code: `src/skyradar_nisar/sowing.py` dòng 42–44 chọn ảnh "phủ ≥ 50% **của track phủ tốt nhất**", không so với `area_km2` của xã (thuộc tính có sẵn trong `data/boundaries/communes_aoi.geojson`). Backend (`water-pulse-be/app/frontend.py`) đặt `coverage_sufficient = bool(sowing)`.

16 xã đang được xếp loại dù quan sát được < 50% diện tích thật:

| Xã | Diện tích (km²) | Quan sát được (km²) | % | Đang xếp loại |
|---|---|---|---|---|
| Mỹ Thuận | 210,0 | 8,5 | 4% | còn ngập |
| Ba Chúc | 70,4 | 5,0 | 7% | sẵn sàng |
| Thạnh Quới | 103,9 | 8,8 | 8% | sẵn sàng |
| Tân Nhuận Đông | 92,0 | 11,9 | 13% | sẵn sàng |
| **Sơn Kiên** | 163,0 | 32,1 | **20%** | còn ngập |
| Hội Cư | 48,8 | 11,1 | 23% | sẵn sàng |
| Trung Nhứt | 30,9 | 7,4 | 24% | còn ngập |
| **Hòn Đất** | 278,8 | 67,7 | **24%** | còn ngập |
| Bình Hòa | 116,1 | 29,6 | 25% | đang rút |
| Tân Phú Trung | 82,6 | 23,6 | 29% | sẵn sàng |
| Mộc Hóa | 135,6 | 47,9 | 35% | còn ngập |
| Thoại Sơn | 68,9 | 28,9 | 42% | sẵn sàng |
| Cái Bè | 40,8 | 19,1 | 47% | sẵn sàng |
| Ô Lâm | 99,6 | 47,1 | 47% | sẵn sàng |
| Tân Lộc | 33,5 | 16,1 | 48% | sẵn sàng |
| Tịnh Biên | 73,9 | 36,7 | 50% | sẵn sàng |

- **Ước tính sau khi sửa** (ngưỡng 50% diện tích thật, tính theo diện tích quan sát lớn nhất của mỗi xã): 115 xã được xếp loại = 43 sẵn sàng / 39 đang rút / 33 còn ngập. **Số chính thức phải lấy từ code sau khi sửa**, có thể lệch 1–2 xã vì quy tắc chọn ảnh.
- Hiện tại: 131 xã = 53 / 40 / 38. 108/131 xã có ≥ 80% diện tích được quan sát.
- **Xã ví dụ thay thế** (phủ 100%, còn ngập): Vĩnh Hưng 61,3% và Vĩnh Thạnh 60,9% (Tây Ninh, ảnh 27/10); Phương Thịnh 59,8% (Đồng Tháp, 27/10); An Hòa 59,8% và Phú Thọ 57,8% (Đồng Tháp, 29/10); Trường Xuân 58,3% (Đồng Tháp, 27/10).
- Các chỗ đang nhắc Sơn Kiên / Hòn Đất / Mỹ Thuận: `README.md`, `docs/METHOD.md`, `docs/SUBMISSION.md`, `docs/HANDOFF.md`, hình `fig3` (`figures.py`, tham số `names`), test backend (`tests/test_frontend.py` kiểm Sơn Kiên 78,2% và số 53/40/38), chữ trên web (`water-pulse-fe/src/locales/*.ts`), slide.

---

## 3. Bốn gói việc

Thứ tự ưu tiên: G1 → G2 → G3 → G4. Mỗi gói một nhánh riêng, tạo từ `main` mới nhất.

### G1. Độ phủ theo diện tích thật (repo `skyradar-nisar`)

- **Nhánh:** `gemini/coverage-true-area` (hoặc tên AI khác).
- **Sửa:**
  - `src/skyradar_nisar/sowing.py`: thêm cột `area_km2`, `observed_pct` (= `valid_km2` của ảnh được chọn / `area_km2`). Xã có `observed_pct` < 50 thì `status = "partial"`, không tính vào 3 nhóm. Giữ nguyên quy tắc chọn ảnh gần nhất.
  - `water-pulse-be/app/frontend.py`: `coverage_sufficient` = false cho xã `partial`; trả thêm `area_km2`, `observed_pct`. Trạng thái giữ `uncertain` như các xã thiếu ảnh.
  - `water-pulse-be/tests/test_frontend.py` và `tests/test_api.py`: cập nhật số mới; thêm kiểm Sơn Kiên có `coverage_sufficient == false`.
  - `src/skyradar_nisar/figures.py` (`fig3`): đổi xã ví dụ sang xã phủ đủ. `fig5` (`sowing.py`) vẽ lại.
  - Tài liệu: `README.md`, `docs/METHOD.md`, `docs/SUBMISSION.md`, `docs/HANDOFF.md` đổi số 38/40/53 và các xã ví dụ. Thêm một dòng giới hạn: xã nằm ở rìa khung dữ liệu chỉ được quan sát một phần.
- **Cần `data/processed`** để chạy lại `sowing`, `export_web`, `figures`. Thư mục này không có trên GitHub: phải chạy lại pipeline trên máy local (xem `README.md`, cần `EARTHDATA_TOKEN`), hoặc chỉ sửa bước `sowing` (bước này chỉ đọc `data/processed/stats/commune_water_by_date.csv`, file đó có bản sao ở `data/web/stats/`).
- **Nghiệm thu:**
  - Sơn Kiên, Hòn Đất, Mỹ Thuận không còn được xếp loại.
  - Ba con số mới lấy từ `sowing_check.csv`, khớp nhau ở API, test, tài liệu.
  - `cd water-pulse-be && pytest -q` qua.
  - `grep -rn "38 \|53 \|Sơn Kiên" README.md docs/` không còn chỗ dùng số hoặc ví dụ cũ sai ngữ cảnh.

### G2. Trang đầu kể câu chuyện (repo `water-pulse-fe`)

- **Nhánh:** `gemini/ux-hero`. Làm **sau G1** (cần số mới).
- **Sửa:**
  - `src/ui/overview.ts`, `src/styles/overview.css`: đặt khối giới thiệu lên đầu tab Tổng quan. Dùng lại `heroBlock()` trong `src/ui/hero.ts` (đang dùng ở tab Giới thiệu).
  - Nội dung: 1 câu ("Radar băng L của NISAR nhìn xuyên mây, thấy ruộng lúa còn ngập theo từng xã"), 3 con số, 1 nút chính "Xem mùa lũ 2026".
  - **3 con số lấy từ API, không gõ cứng:** số xã còn ngập / số xã được xếp loại (`/api/frontend/communes`); "NISAR tốt hơn Sentinel-1 ở X/Y ngày" (`/api/frontend/validation`, `vsHls`); số lần chụp (`/api/frontend/scenes`).
  - Nút chính: `set({ tab: 'map', mapMode: 'scene', viewMode: 'simple' })`, chọn ảnh đầu tiên rồi chạy Play (logic Play ở `src/ui/timeline.ts`).
  - `src/locales/en.ts`, `vi.ts`, `overview.ts`: thêm chữ; cập nhật chữ "đủ độ phủ" theo G1 ("≥ 50% diện tích xã").
- **Nghiệm thu:**
  - Ở 1440×900 và 390×844, không cần cuộn, thấy: câu giới thiệu có chữ NISAR, 3 con số, nút chính.
  - Bấm nút: bản đồ hiện lớp nước và Play chạy.
  - Đúng ở cả `?lang=vi` và `?lang=en`.
  - `npm run build`, `npm run build:cloudflare`, `npm run test:cloudflare`, `npm run test:ux` đều qua.

### G3. Bằng chứng lên đầu tab Độ tin cậy (repo `water-pulse-fe`)

- **Nhánh:** `gemini/ux-validation`.
- **Sửa:** `src/ui/validation.ts`, `src/charts/` (thêm biểu đồ cột), `src/locales/*.ts`.
  - Trên cùng: một con số lớn ("NISAR tốt hơn Sentinel-1 ở 14/16 ngày, so với ảnh quang học, mùa lũ tháng 8–11") và một biểu đồ cột F1 theo ngày (NISAR và Sentinel-1), không gập.
  - Một dòng SWOT: "So với radar độc lập SWOT (NASA/CNES): NISAR khớp hơn Sentinel-1 ở 11/12 ngày."
  - Bảng chi tiết vẫn để trong mục gập.
- **Nghiệm thu:** thấy con số và biểu đồ mà không cần bấm; số tính từ `vsHls` và `vsSwot` của API, khớp `data/web/stats/vs_dswx_hls.csv` và `vs_swot.csv`; có `aria-label` cho biểu đồ.

### G4. Gọn giao diện (repo `water-pulse-fe`)

- **Nhánh:** `gemini/ux-trim`.
- **Sửa:**
  - Cỡ chữ tối thiểu 13 px (`src/styles/tokens.css` và các file CSS dùng 10–12 px).
  - Tiêu đề thống nhất viết thường kiểu câu (ví dụ "Commune breakdown by latest water share"), bỏ Title Case.
  - Tab Tổng quan: hai khối giải thích dài ("Why Coverage Varies…", "3-Step Operational Guide") thành mục gập `<details>`.
  - Bản đồ: mặc định `viewMode: 'simple'` (`src/state.ts`); gom chọn track và lớp vào một nút "Nâng cao".
  - Thanh thời gian (`src/ui/timeline.ts`, `src/styles/timeline.css`): bỏ 2 dòng chú thích, chuyển thành tooltip.
- **Nghiệm thu:** tab Tổng quan < 350 chữ (đo bằng `innerText`); bản đồ ≥ 60% chiều cao ở 1440×900; Play, phím ←/→ và các test hiện có vẫn qua.
- **Đừng phá các thứ đã sửa hôm nay:** thanh thời gian luôn hiện; Play dừng thật khi đổi chế độ (commit `e7dfb5f`); SWOT chỉ ở tab Độ tin cậy, không đưa lên bản đồ (`4f59e90`).

---

## 4. Quy trình "AI làm, AI khác phản biện"

1. **Người ra đề** (Claude hoặc Chí) đưa đúng một gói ở mục 3 cho AI làm (Gemini, Codex…), kèm `docs/HANDOFF.md`.
2. **AI làm** trên nhánh riêng, commit theo quy tắc (`[Gemini] fe: …`), **không push vào `main`**.
3. **AI kiểm** (Claude) làm đủ các bước:
   - đọc diff, tìm chỗ sửa ngoài phạm vi gói;
   - chạy các lệnh nghiệm thu của gói;
   - build bản Cloudflare và mở bằng trình duyệt, chụp 1440×900 và 390×844, VI và EN;
   - đối chiếu mọi con số trên màn hình với CSV;
   - viết phản biện: lỗi chặn merge, lỗi nên sửa, ý kiến.
4. **AI làm sửa theo phản biện**, tối đa 2 vòng. AI làm được phản biện lại; chỗ hai bên không thống nhất ghi vào `docs/verification/` để Chí quyết.
5. **Merge:** rebase lên `main` mới nhất, chạy lại test, rồi merge. Với `water-pulse-fe`, merge là lên web thật ngay; kiểm lại trên https://nisar-flood.skyradar.vn sau khi deploy.

**Rủi ro xung đột:** Đông push liên tục vào `main` của frontend (chiều 14/11 có các commit về Play mượt, ảnh ghép nhiều track, tooltip). Trước khi sửa file nào, `git pull`; khi gỡ hoặc khôi phục code, sửa đúng dòng, **không** `git checkout <commit cũ> -- <file>` (cách đó ghi đè mất commit mới của người khác).

---

## 5. Lệnh hay dùng trên máy local

Thư mục: `~/nisar/` chứa `skyradar-nisar/`, `water-pulse-fe/`, `.venv/`.

```bash
cd ~/nisar/skyradar-nisar && git pull && cd ../water-pulse-fe && git pull
```

```bash
cd ~/nisar/skyradar-nisar/water-pulse-be && ~/nisar/.venv/bin/python -m pytest -q
```

```bash
cd ~/nisar/water-pulse-fe && PYTHON=~/nisar/.venv/bin/python npm run build:cloudflare && npm run test:cloudflare && npm run test:ux
```

```bash
cd ~/nisar/water-pulse-fe && npm run dev:cloudflare
```

Lệnh cuối chạy bản giống hệt Cloudflare tại http://localhost:8788. Để sửa giao diện có tự tải lại: chạy backend (`uvicorn app.main:app --port 8000` trong `water-pulse-be/`) và `npm run dev` (http://localhost:5173).

Gemini CLI (nếu dùng trên máy local): `npm i -g @google/gemini-cli`, đặt `GEMINI_API_KEY`, chạy trong thư mục repo: `gemini -p "<đề bài của gói>" --approval-mode auto_edit`.

---

## 6. Việc khác còn mở (ngoài UI/UX)

- Đặt `main` làm nhánh mặc định của `skyradar-nisar` (Settings của repo).
- Xoá ID tài khoản Cloudflare ở dòng 6 file `water-pulse-fe/docs/LOCAL_DEPLOYMENT.md`.
- Tắt hoặc chuyển hướng bản dữ liệu giả ở `water-pulse.pages.dev`.
- Sáng 15/11: truy vấn CMR tìm ảnh NISAR mới; nếu có thì chạy lại pipeline và cập nhật số trong test.
- Tuỳ chọn: mực nước sông từ SWOT RiverSP (thay số liệu trạm MRC), chỉ dùng làm số liệu đối chiếu.
- Chốt `docs/SUBMISSION.md`, slide, video; mở Judging Guide 2026 để xác nhận tiêu chí.
