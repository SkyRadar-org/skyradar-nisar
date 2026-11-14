**Thời gian báo cáo:** 19:03 GMT+7 (14/11/2026)
**Kết quả thẩm định (Verdict):** `PASS`

---

### 1. Đánh giá chi tiết các hạng mục trọng tâm (G2 / G3 / G4)

1. **Quản lý bộ đếm thời gian duy nhất (Timer 1 Owner) & Vòng đời phát (`timeline.ts`, `season.ts`, `main.ts`):**
   - **Một chủ sở hữu duy nhất:** Chỉ `mountTimeline` trong `src/ui/timeline.ts` nắm biến `let timer: number | undefined`. Không có module nào khác tự tạo `setTimeout` / `setInterval` cho tiến trình phát.
   - **Mount bất đồng bộ (Async mount):** Trong `src/main.ts`, `buildMapView` chờ `Promise.all([getScenes(), getSummaryLayers()])` rồi mới gọi `mountTimeline`. Nếu người dùng bấm CTA từ trang Tổng quan/Giới thiệu trước khi `mountTimeline` khởi tạo xong, `state` đã được `exploreSeason` cập nhật sẵn (`playing: true`, `selectedDate: '2026-08-11'`); khi `mountTimeline` chạy tới cuối hàm, lệnh `syncPlayback()` sẽ tự động kích hoạt `tick()` từ đúng ảnh đầu mùa lũ mà không bị rơi nhịp.
   - **Bấm đúp CTA (Double CTA):** `exploreSeason()` (`src/ui/season.ts`) gọi `set({ playing: false })` tách biệt ngay trước khi `set({ ..., playing: true })`. Nhờ `set()` phát thông báo đồng bộ cho các subscriber, lần gọi đầu kích hoạt `syncPlayback()` -> `stop()` để hủy `clearTimeout(timer)` cũ trước khi lần gọi thứ hai khởi tạo `tick()` mới từ đầu mùa. Bên trong `tick()`, điều kiện `if (timer === undefined && state.playing) tick()` ngăn việc tạo chồng timer khi `step(1)` đã kích hoạt `syncPlayback()` qua subscriber.
   - **Đổi tab / Tạm dừng (Tab change / Pause):** `syncPlayback()` kiểm tra chặt điều kiện `!state.playing || state.mapMode !== 'scene' || state.tab !== 'map' || state.activeSummary`. Khi chuyển sang tab khác, bật lớp tổng hợp mùa lũ, đổi về chế độ `latest`, bấm nút Pause (`playBtn`), kéo thanh thời gian (scrub) hoặc nhấn phím mũi tên, `stop()` đều xóa `timer` và đưa `playing` về `false`.

2. **Tính toán KPI từ độ phủ và tỷ lệ nước (`observations.ts`, `about.ts`, `overview.ts`, `mapContext.ts`):**
   - Hàm `hasAssessment()` (`src/data/observations.ts`) và `isEvaluated()` (`src/ui/overview.ts`) thống nhất điều kiện `coverage_sufficient === true && last_pct !== null && last_date !== null`.
   - Khối Hero (`src/ui/about.ts`) tính tỷ lệ xã ngập cao bằng `assessed.filter(f => f.properties.last_pct! >= 30).length / assessed.length`, khớp chặt với phân nhóm `highList.length / evaluatedCount` (`33/115`) tại `src/ui/overview.ts` và thông báo độ phủ tại `src/ui/mapContext.ts`. Các xã thiếu quan sát hoặc chỉ phủ một phần được tách riêng vào `insufficient`, không bị gộp nhầm thành ngập thấp.

3. **Đối sánh SWOT cùng điểm ảnh (Same-pixel SWOT) & Cặp dữ liệu hữu hạn (`validationStats.ts`, `validation.ts`):**
   - Hàm `score()` kiểm tra `typeof x === 'number' && Number.isFinite(x) && x >= 0 && x <= 1`, loại bỏ hoàn toàn `null`, `undefined`, `NaN`, `Infinity` khỏi mẫu số.
   - `hlsPairs()` lọc đúng khung thời gian mùa lũ (`r.date >= '2026-08-01' && r.date < '2026-12-01'`) và dùng chung cho cả KPI, biểu đồ `createOpticalChart` lẫn bảng `hlsTable`.
   - `swotPairs()` và `swotTable()` đều sử dụng `f1_nisar_same_px` đối chiếu với `f1_s1`. Số lần thắng dùng phép so sánh nghiêm ngặt `>` (trường hợp hòa không tính là thắng), khớp với kiểm thử đơn vị tại `tests/validationStats.test.mjs`.

4. **Khả năng tiếp cận nhãn độ trưởng thành dữ liệu (Accessible Maturity) cho ảnh ghép (`timeline.ts`, `story.css`):**
   - Trong `src/ui/timeline.ts`, biến `allValidated` kiểm tra toàn bộ `scene.composite.sources` xem mọi ảnh thành phần đã đạt `'validated'` hay chưa để hiển thị nhãn `T.story.mosaicValidated` hoặc `T.story.mosaicProvisional` trên `maturityEl`.
   - Trong `src/styles/story.css`, `.timeline.simple .tl-meta { display: flex; }`, `.timeline.simple .tl-legend > span:not(.tl-legend-note) { display: inline-flex; }` và `.tl-meta .maturity` đảm bảo trạng thái dữ liệu của ảnh ghép luôn hiển thị rõ trên cả màn hình lớn và thiết bị di động.

5. **Tương thích Schema Optional cho chế độ Mock (`overview.ts`, `timeline.ts`, `map.ts`, `validation.ts`):**
   - Các trường mở rộng đều có nhánh dự phòng an toàn: `c.observed_pct != null` (rơi về `coverageSufficient` / `partial` khi chạy mock không có `observed_pct`), `scene.composite` (chuyển về chế độ `'pro'` và `getChoropleth` thường khi không có ảnh ghép), và `v.vsSwot ?? []` / `v.vsSwot?.length`.

---

### 2. Lỗi có bằng chứng

- **Không phát hiện lỗi (0 lỗi).**

---

### 3. Giới hạn kiểm tra (Review Limitations)

- Đây là bước thẩm định tĩnh độc lập trên các tệp mã nguồn được cung cấp; không bao gồm toàn bộ tệp định nghĩa kiểu (`src/data/types.ts`) và từ điển đa ngôn ngữ (`src/i18n.ts`), nhưng đã dựa trên kết quả `tsc` và bộ test (17 backend, 10 UX, 4 Worker) đã vượt qua từ phía triển khai.
- Không tự thực thi mã nguồn, không chạy trình duyệt hay kiểm tra trực quan bố cục khung nhìn (1440×900, 390×844) mà ghi nhận kết quả kiểm chứng thực tế đã được xác nhận trước đó.
