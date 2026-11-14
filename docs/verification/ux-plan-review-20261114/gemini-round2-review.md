**Thời gian báo cáo:** `18:33 ngày 14/11/2026 (GMT+7)`
**Trạng thái kiểm chứng (UAM-V3):** Phân tích tĩnh vòng 2 trên mã nguồn `origin/main` (`4f59e90`) của `water-pulse-fe`, mã nguồn `skyradar-nisar` và kết quả đối chiếu CSV độc lập do Codex cung cấp. Không gọi tool, không chạy lệnh, không sửa file.

---

## 1. Các kết luận Vòng 1 rút lại sau khi đối chiếu Remote `4f59e90`

Do `local main` (`6a13caa`) chỉ là ancestor chậm 5 commit so với `origin/main` (`4f59e90`) và không có phân kỳ, các phát hiện sau ở Vòng 1 **được rút lại**:
1. **Rút lại lỗi thiếu `viewMode`, `Scene.composite` và `Validation.vsSwot` trong TypeScript:** Bản `4f59e90` tại [state.ts](file:///Users/Chris/nisar/water-pulse-fe/src/state.ts#L5-L38), [types.ts](file:///Users/Chris/nisar/water-pulse-fe/src/data/types.ts#L12-L97) và [validation.ts](file:///Users/Chris/nisar/water-pulse-fe/src/ui/validation.ts#L42-L56) đã khai báo đầy đủ các kiểu này và đã có bảng `swotTable()`. Chỉ cần `git pull --ff-only` trên `water-pulse-fe` trước khi tách nhánh.
2. **Rút lại nghi ngờ trùng ngày trong `vs_dswx_hls.csv`:** Dữ liệu thực tế có đúng 16 hàng ứng với 16 ngày riêng biệt (NISAR thắng 14/16).
3. **Rút lại yêu cầu gập phần giải thích ở tab Tổng quan (G4):** Tại `4f59e90`, [overview.ts](file:///Users/Chris/nisar/water-pulse-fe/src/ui/overview.ts#L399) đã đặt sẵn `guideAndCaveatsSection` trong thẻ `<details class="ov-explanation">`.

*(Lưu ý: Phát hiện về `heroBlock()` nằm ở [about.ts](file:///Users/Chris/nisar/water-pulse-fe/src/ui/about.ts#L4) thay vì `hero.ts` vẫn giữ nguyên).*

---

## 2. Kết luận đánh giá sau hiệu chỉnh: **CẦN CHỈNH TRƯỚC KHI TRIỂN KHAI**

Kế hoạch [UX_PLAN.md](file:///Users/Chris/Downloads/UX_PLAN.md) **cần chỉnh các lỗi kỹ thuật và ngữ nghĩa dưới đây** trước khi thực thi G1–G4.

### 🔴 Các lỗi P0 (Chặn triển khai: gây crash, sai số liệu hoặc liệt tính năng)

1. **G1 — Crash `StopIteration` khi vẽ `fig5` và sót nhãn xã `partial` ([sowing.py](file:///Users/Chris/nisar/skyradar-nisar/src/skyradar_nisar/sowing.py#L61-L68)):**
   - Khi gán `r["status"] = "partial"`, dòng 61 `next(c for n, *_, c in LEVELS if r and n == r["status"])` sẽ ném `StopIteration` vì `"partial"` không thuộc `LEVELS`.
   - Dòng 65 `for r in table[:6]:` lấy 6 xã có `status_pct` cao nhất sẽ tiếp tục vẽ nhãn Sơn Kiên (78,2%) lên bản đồ `fig5` nếu không lọc `r["status"] != "partial"`.
2. **G1 — Ghi đè nhầm `status = "no_flood"` lên xã `partial` ([frontend.py](file:///Users/Chris/nisar/skyradar-nisar/water-pulse-be/app/frontend.py#L51-L55)):**
   - Khi xã `partial` vẫn nằm trong `sowing_check.csv`, biến `sowing` là `dict` (truthy). Dòng 53 `if sowing and peak_pct is not None and peak_pct < 5: status = "no_flood"` sẽ biến xã thiếu độ phủ (`partial`) có đỉnh ngập `< 5%` thành `no_flood` thay vì giữ `uncertain`.
   - **Cách sửa:** Đặt `coverage_sufficient = bool(sowing and sowing.get("status") != "partial")` và đổi điều kiện dòng 53 thành `if coverage_sufficient and peak_pct is not None and peak_pct < 5:`.
3. **G1 — Lỗi logic chọn ảnh ≥ 50% và làm tròn ngưỡng (`sowing.py` dòng 39–41, `frontend.py` dòng 104):**
   - `sowing.py` đang chọn ảnh mới nhất trong các track đạt `v[2] >= 0.5 * cover` (so với track phủ lớn nhất của xã đó), dẫn tới việc **Thoại Sơn** có track phủ `28,9 / 68,9 km² (42%)` nhưng ảnh được chọn (03/11, `148D`) chỉ phủ `14,89 / 68,89 km² (21,61%)`. Dù trên tập CSV hiện tại cả hai cách (lọc `valid_km2 >= 0.5 * area_km2` trước hay kiểm tra sau) đều cho `115` xã (`43/39/33`) và `16 partial`, nhưng về thuật toán **bắt buộc phải ưu tiên chọn ảnh mới nhất trong các track thỏa `v[2] >= 0.5 * area_km2`** (chỉ fallback về `0.5 * cover` khi không có track nào đạt 50% diện tích thật) để không đánh tụt oan xã có track khác phủ đủ.
   - Phải so sánh `< 50.0` trên giá trị thực trước khi làm tròn (trường hợp **Tịnh Biên** `36,73 / 73,93 = 49,6821%` vẫn là `partial`, không được làm tròn lên `50%` trước khi xét ngưỡng). Đồng thời chuẩn hóa `observed_pct` theo thang **`0–100`** (khớp với `water_pct` và `composite.observedPct`).
   - Cập nhật cả `choropleth_composite` ([frontend.py](file:///Users/Chris/nisar/skyradar-nisar/water-pulse-be/app/frontend.py#L103-L104)) đang dùng `0.5 * best_valid`.
4. **G1 — Thiếu `data/processed` khi chạy local và sót chỗ gõ cứng Sơn Kiên / số 9 trên Frontend (`4f59e90`):**
   - `data/processed` không tồn tại trên máy nên `sowing.py` cần đọc/ghi fallback sang `data/web/stats/` và không thể chạy `export_web` đầy đủ (do thiếu raster). `area_km2` trong `frontend.py` cần lấy được cho cả 9 xã không nằm trong `sowing_check.csv` (từ `communes_aoi.geojson` / `communes.geojson`).
   - **Phát hiện mới trên `4f59e90`:** [overview.ts](file:///Users/Chris/nisar/water-pulse-fe/src/ui/overview.ts#L322-L324) đang tìm cứng `c.osm_id === '15416586'` (**Sơn Kiên**) mà không kiểm tra `isEvaluated(c)`, nên sau G1 vẫn lấy Sơn Kiên làm ví dụ! Đồng thời [locales/overview.ts](file:///Users/Chris/nisar/water-pulse-fe/src/locales/overview.ts#L50) (dòng 50, 129, 198, 273) vẫn gõ cứng tên `Sơn Kiên` và câu *"9 xã chưa đủ độ phủ"* (sau G1 là **25 xã** = 9 không quan trắc + 16 partial).
5. **G2 — Bấm CTA không chạy timer Play và thiếu reset trạng thái ([timeline.ts](file:///Users/Chris/nisar/water-pulse-fe/src/ui/timeline.ts#L63-L75), dòng 240–244):**
   - Trên `4f59e90`, `play()` và chuỗi `setTimeout` (`tick()`) vẫn đóng kín trong `mountTimeline()`. Listener `subscribe` dòng 240 chỉ gọi `stop()` khi `!s.playing`, **không khởi động `tick()` khi `set({ playing: true })` được gọi từ `overview.ts`**.
   - **Cách sửa:** Trong `timeline.ts`, khi `s.playing && !prev.playing && timer === undefined` thì gọi `play()`. Nút CTA ở G2 phải đồng thời đặt `location.hash = 'map'`, `activeSummary: null`, `selectedCommune: null`, `trackFilter: 'all'`, bật `layers.water = true`. Ngoài ra, vì đầu mùa (tháng 6–7) F1 rất thấp (`0,07–0,19`), CTA *"Xem mùa lũ 2026"* nên bắt đầu phát từ đầu mùa lũ (`>= 2026-08-01`) thay vì ngày `17/06`.

---

### 🟡 Các lỗi P1 (Sai lệch KPI, ngữ nghĩa khoa học và hồi quy tiếp cận)

1. **G2 — Không được tính KPI số xã từ trường `status` của `/api/frontend/communes`:**
   - Xác nhận phát hiện của Codex: API `/api/frontend/communes` hiện tách 21 xã có `peak_pct < 5` sang `no_flood` và gộp `draining` vào `uncertain` (`21 no_flood / 32 receded / 38 not_receded / 49 uncertain`). Để hiển thị đúng bộ số (`33 còn ngập / 115 xã đủ độ phủ` sau G1), G2 **phải lọc `coverage_sufficient === true && last_pct !== null` và phân nhóm theo `last_pct` (`>= 30`, `10–<30`, `< 10`)** giống hệt `classifyCommune()` trong [overview.ts](file:///Users/Chris/nisar/water-pulse-fe/src/ui/overview.ts#L24-L29).
2. **G1/G2 — Ngữ nghĩa `water_pct` và diễn giải nông học ([locales/overview.ts](file:///Users/Chris/nisar/water-pulse-fe/src/locales/overview.ts#L179-L187)):**
   - `water_pct = ww / v * 100` là tỷ lệ nước **trên phần diện tích xã được quan sát (`valid_km2`)**, không phải trên diện tích toàn xã (`area_km2`). Bản tiếng Việt ở `locales/overview.ts` dòng 179 & 187 đang ghi *"Từ 30% diện tích có nước"* / *"Dưới 10% diện tích có nước"* — cần ghi rõ là trên phần diện tích quan trắc được.
   - Giữ đúng cách tiếp cận của `overview.ts`: chỉ mô tả mức nước mặt quan trắc được (*Còn nhiều nước / Còn một phần nước / Ít nước trên ảnh*), không khẳng định kết luận nông học (*sẵn sàng xuống giống*) từ tỷ lệ nước đơn thời điểm.
3. **G3 — Công thức SWOT cùng pixel (`same_px`):**
   - Trong 13 hàng của `vs_swot.csv`, chỉ có 12 hàng có dữ liệu Sentinel-1 (`f1_s1 !== null`). Khi tính số lần NISAR thắng S-1 (`11/12`), code phải lọc `r.f1_s1 !== null && r.f1_nisar_same_px !== null` và so sánh **`r.f1_nisar_same_px > r.f1_s1`** (như cách `swotTable` ở [validation.ts](file:///Users/Chris/nisar/water-pulse-fe/src/ui/validation.ts#L49) đang lấy `r.f1_nisar_same_px ?? r.f1_nisar`).
4. **G4 — Đổi mặc định `viewMode: 'simple'` làm mất phân biệt `Provisional / Validated` trên các chấm timeline và trên mobile ([timeline.ts](file:///Users/Chris/nisar/water-pulse-fe/src/ui/timeline.ts#L177-L181)):**
   - Dòng 177–181 gán mọi chấm ở chế độ `simple` thành class `'validated'` và bỏ `maturity` + `track` khỏi `aria-label`/`title`. Dù trên desktop vẫn còn nhãn `.maturity` ở header của timeline cho ảnh đang chọn, nhưng trên mobile nhãn này bị CSS ẩn và toàn bộ các chấm trên thanh trượt mất dấu hiệu `Provisional` (trước 22/10/2026). Nếu đặt `simple` làm mặc định, phải giữ kiểu chấm `s.maturity` (hoặc giữ nhãn `maturity` hiển thị trên cả mobile) và ghi rõ trên `mapContext` rằng chế độ `simple` đang hiển thị ảnh ghép nhiều ngày (`composite`, tối đa 12 ngày), không phải một lần chụp đơn lẻ.
5. **G1 — Phụ thuộc kiểm thử và CI/CD:**
   - Cần cập nhật thêm endpoint gốc `/api/sowing-check` (nếu có kiểm tra enum `status`) và test frontend `tests/observations.test.mjs`.
   - Vì `.github/workflows/deploy.yml` của `water-pulse-fe` luôn checkout `skyradar-nisar` tại nhánh `main`, **G1 bắt buộc phải được merge vào `main` của `skyradar-nisar` (kèm `data/web/stats/sowing_check.csv` mới)** trước khi merge G2–G4 lên `water-pulse-fe`.

---

## 3. Giới hạn kiểm chứng tĩnh

- Chưa có nội dung file `water-pulse-fe/tests/observations.test.mjs`, `scripts/export_pages.py`, `src/skyradar_nisar/figures.py` và các file CSS (`styles/timeline.css`, `styles/overview.css`) trong gói văn bản để đối chiếu từng dòng selector của `npm run test:ux`.
- Trước khi sửa code, cần chạy `git pull --ff-only` trên `water-pulse-fe` để đưa workspace từ `6a13caa` lên đúng `4f59e90`.
