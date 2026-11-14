# Đánh giá UX_PLAN — Codex và Gemini

Chốt đánh giá: 18:38 ngày 14/11/2026 (GMT+7). Phạm vi: phản biện kế hoạch, chưa thực hiện G1–G4.

## Kết luận

**Cần chỉnh trước khi triển khai.** Giữ hướng sửa độ phủ, đưa câu chuyện và bằng chứng lên đầu. G1 là việc bắt buộc; giảm phạm vi G4 để dành thời gian kiểm dữ liệu, bản trình diễn và bài nộp. Các phát hiện dưới đây là thiếu sót của kế hoạch triển khai, không có nghĩa mọi lỗi dự kiến đã xảy ra trên sản phẩm hiện tại.

## Nguồn và phạm vi đã xác minh

- Bản `/Users/Chris/Downloads/UX_PLAN.md` giống `docs/UX_PLAN.md` tại backend `f937b04`. Đã đọc skill UAM và `docs/HANDOFF.md`; không tìm thấy kho memory canonical trong workspace, không tạo kho mới.
- Backend local và remote `main`: `f937b04421f51e3de9b3004ced81b7d59e2603ed`. Frontend local `6a13caa` chậm năm commit so với remote `4f59e90f907c84b006d3ecb7a34097fea5ad003f`; đã fetch, không thay checkout frontend. `viewMode`, composite và `vsSwot` đều có trong remote. Nhận xét thiếu những trường này từ bản local cũ không còn áp dụng.
- Codex đối chiếu mã, CSV và chạy kiểm tra. Gemini được gọi thật qua Antigravity CLI, yêu cầu model `gemini-4-argon-high`, chỉ phân tích tĩnh gói nguồn. Vòng hai nhận nguồn frontend remote và các đính chính. Không coi Gemini là người đã tự chạy test hoặc kiểm trình duyệt.
- Chưa tái đo các con số 51 nút, 55% chiều cao, 600 chữ hoặc chụp lại ma trận desktop/mobile, VI/EN của Claude. Đây vẫn là nhận định trong tài liệu nguồn.

## Số liệu: phần cốt lõi của plan đúng

Đã tính độc lập trên 2.959 hàng quan trắc, 140 ranh giới xã và 131 bản ghi `sowing_check.csv`. Xem [coverage-audit.json](coverage-audit.json); có thể tái lập bằng [audit_coverage.py](audit_coverage.py).

| Nội dung | Kết quả kiểm tra |
|---|---|
| Ba nhóm hiện tại, thứ tự thấp / trung bình / cao | 53 / 40 / 38 |
| Ảnh tham chiếu hiện chọn quan sát dưới 50% diện tích xã | 16 xã |
| Mô phỏng sau khi loại 16 xã đó | 115 xã: 43 / 39 / 33 |
| Đối chiếu HLS | F1 NISAR cao hơn 14/16 cặp; hiện có 16 ngày khác nhau |
| Đối chiếu SWOT | 13 hàng tổng cộng, 12 hàng có cặp so sánh, NISAR F1 cùng pixel cao hơn 11/12 |

**115 và 43/39/33 là kết quả mô phỏng trên snapshot hiện có, chưa phải dữ liệu mới đã xuất bản.** Với ba cách chọn ảnh được thử, tổng nhóm trùng nhau ở dữ liệu này; điều đó không chứng minh các cách chọn tương đương cho ảnh tương lai.

Hai chi tiết cần sửa trong bảng nguồn: Thoại Sơn có ảnh đang chọn phủ **14,89/68,89 km² = 21,61%**; số 28,9 km², 42% trong plan là track phủ tốt nhất. Tịnh Biên là **49,6821%**, hiển thị làm tròn 50% nhưng vẫn dưới ngưỡng. Ngưỡng phải xét trước khi làm tròn.

## Những chỉnh sửa bắt buộc

### 1. Chốt đúng mẫu số và ngữ nghĩa sản phẩm

`src/skyradar_nisar/timing.py:56–57` tính `water_pct = water_km2 / valid_km2 × 100`. Vì vậy, ghi “tỷ lệ nước trên phần diện tích quan trắc”, không suy thành tỷ lệ ngập trên toàn xã. Tách rõ `observed_pct = valid_km2 / area_km2 × 100`, thang 0–100. Ngưỡng 50% là quy tắc sàng lọc của sản phẩm, chưa được kiểm chứng là bảo đảm suy rộng cho toàn xã.

Giữ cách gọi hiện tại của giao diện: ít nước / một phần nước / nhiều nước. Một tỷ lệ tại một thời điểm không chứng minh nước đang rút hoặc đất đã sẵn sàng gieo sạ. Mã `ready/draining/still_wet` có thể giữ để tương thích, kèm giải thích. Pipeline đang xét nước mặt và ranh giới xã; các tệp đã xem chưa có mặt nạ đất lúa. Câu hero phù hợp hơn: **“NISAR theo dõi nước mặt qua mùa lũ, tổng hợp theo từng xã.”**

### 2. G1 phải bao trọn đường đi của dữ liệu

- Chốt rõ lựa chọn ảnh: chọn ảnh mới nhất trong các ảnh đạt ít nhất 50% diện tích thật; nếu không có, chỉ giữ ảnh làm bằng chứng một phần. Quy định cách xử lý khi ảnh mới phủ ít hơn ảnh cũ, các track cùng ngày, thiếu diện tích và tập ứng viên rỗng. Nếu chỉ giữ quy tắc cũ rồi gắn cờ, cần công bố đúng hạn chế đó thay vì gọi là “ảnh mới nhất đủ phủ”. Giữ ngưỡng 5 km² hiện tại trừ khi có quyết định riêng.
- `sowing.py:65` tra màu bằng `next()` chỉ có ba nhóm. Thêm `partial` mà không sửa ánh xạ sẽ gây `StopIteration` khi vẽ fig5. Sửa màu, chú giải, nhãn ví dụ và chỉ chọn ví dụ đủ phủ.
- `water-pulse-be/app/frontend.py:58` có nhánh `no_flood` độc lập. Phải khóa nhánh này bằng điều kiện đủ phủ. Năm xã trong 16 xã bị loại đang có đỉnh dưới 5%: Tân Lộc, Ba Chúc, Tân Phú Trung, Cái Bè, Hội Cư; nếu chỉ sửa cờ phủ thì trạng thái của chúng vẫn có thể bị ghi đè thành `no_flood`.
- Bổ sung `area_km2`, `observed_pct` vào hợp đồng TypeScript và giao diện; lấy diện tích từ ranh giới cho cả xã không có bản ghi sowing. Cập nhật API gốc `/api/sowing-check`, API adapter, test backend và `water-pulse-fe/tests/observations.test.mjs`. Test frontend hiện khóa 131 và 53/40/38 nên chỉ sửa test backend là chưa đủ.
- Sửa câu gõ cứng “9 xã” trong `src/locales/overview.ts` thành số động; chọn lại ví dụ Sơn Kiên trong `src/ui/overview.ts:368–370` bằng điều kiện đủ đánh giá. Đừng xóa mọi lần xuất hiện của tên xã: vẫn có thể dùng Sơn Kiên làm ví dụ thiếu phủ nếu nói đúng ngữ cảnh.
- Máy này thiếu `data/processed`. Chọn đường chạy chỉ dùng CSV để tái tính và xuất `data/web/stats/sowing_check.csv`; vẽ riêng fig3/fig5. Không yêu cầu chạy lại toàn bộ `export_web` hay `figures.main()` khi thiếu raster/qa đầu vào. CSV backend đọc và CSV được commit phải là cùng bản đã kiểm.
- Phân biệt bản đồ đánh giá mới nhất với lớp cảnh ghép làm bằng chứng. `choropleth_composite()` vẫn dùng ngưỡng theo best pass; phải ghi đúng nghĩa phần quan trắc, tránh gắn nhãn “đủ 50% toàn xã” cho lớp này. Không tự mở rộng G1 thành viết lại toàn bộ thuật toán cảnh ghép trước hạn.

### 3. G2 cần nối đúng CTA, Play và số liệu động

- `heroBlock()` nằm trong `src/ui/about.ts`, được `hero.ts` nhập lại; hiện đọc các số tĩnh từ bản dịch. Truyền dữ liệu động vào thành phần dùng chung và kiểm cả tab Giới thiệu lẫn overlay để tránh ba bộ số khác nhau.
- `mountTimeline()` giữ `play()` và bộ đếm bên trong. `set({ playing: true })` từ hero chỉ đổi state; listener hiện không tạo bộ đếm. Cần một lối khởi động Play dùng chung, xử lý cả lúc timeline chưa mount, API chậm, dữ liệu rỗng và nhấn CTA nhiều lần.
- Không áp dụng nguyên xi gợi ý gọi lại `play()` trong listener: `play()` đang tự gọi `set({ playing: true })` rồi tạo bộ đếm, nên cần thiết kế một nơi duy nhất sở hữu bộ đếm để tránh khởi động hai lần.
- Đồng bộ `location.hash = 'map'`; đặt lại `activeSummary`, lựa chọn xã, bộ lọc track và lớp nước để trạng thái cũ không che bản trình diễn. Kiểm quay lại Tổng quan, Back/Forward và Pause.
- Nếu mục tiêu là trình diễn mùa lũ, bắt đầu từ tháng 8; tháng 6–7 có chất lượng yếu đã được nêu trong phương pháp. Có thể giữ toàn bộ 33 ảnh ở chế độ khám phá, nhưng cần chốt rõ ý đồ của CTA.
- API `status` không trùng ba nhóm tỷ lệ nước: hiện có `no_flood=21`, `receded=32`, `not_receded=38`, `uncertain=49`. Tính KPI theo cùng hàm đủ phủ và ngưỡng `last_pct` mà Tổng quan sử dụng, không đếm trực tiếp nhãn `status` để mong ra 53/40/38 hoặc 43/39/33.

### 4. G3 cần diễn đạt phép đối chiếu, tránh khái quát hóa

Ghi rõ **“F1 cao hơn trong 14/16 cặp đối chiếu với ảnh quang học, mùa lũ tháng 8–11”**. Với SWOT, chỉ đếm cặp có cả `f1_nisar_same_px` và `f1_s1` là số hữu hạn; không dùng 13 hàng làm mẫu số, không thay `f1_nisar_same_px` bằng `f1_nisar`. Đây là mức phù hợp với nguồn đối chiếu, chưa phải chứng minh đúng ở mọi địa điểm/thời điểm.

Biểu đồ và bảng phải dùng cùng hàm tính, phân biệt ngày–track, xử lý thiếu dữ liệu và hòa điểm. Có bảng/tóm tắt chữ đọc được bên cạnh canvas; chỉ thêm `aria-label` chưa giúp người đọc tiếp cận từng giá trị.

### 5. G4 nên thu hẹp và giữ tín hiệu trung thực

Ưu tiên gập hai khối dài, tăng cỡ chữ ở thành phần chính, gom điều khiển nâng cao. Hai khối hiện vẫn là `section` và `div` trong `overview.ts:399–455`; nhận xét vòng hai của Gemini rằng đã có `<details class="ov-explanation">` là sai. Không thay cỡ chữ toàn bộ CSS hoặc đặt một ngưỡng “350 chữ” khi chưa xác định phạm vi đếm, số hàng bảng và trạng thái mục gập. Đo phần nhìn thấy ở màn hình đầu; kiểm tiếng Việt riêng.

Không đưa ngày dữ liệu, tình trạng tạm thời và tuổi của cảnh ghép chỉ vào tooltip. Ở `4f59e90`, timeline simple đang gán lớp `validated` cho mọi chấm, bỏ maturity khỏi aria/title; CSS mobile còn ẩn badge maturity. Bật simple mặc định phải sửa thiếu sót này trong cùng gói. Màu sắc và ngày nguồn cần có chữ hoặc ký hiệu phân biệt; không để người xem tưởng cảnh ghép là ảnh đồng thời hoặc dữ liệu trực tiếp hôm nay.

### 6. Chốt ranh giới phát hành và lịch

Workflow frontend hiện checkout backend `main`. Bản xem trước của G2/G3 phải chỉ rõ snapshot dữ liệu G1; build đạt với backend trên nhánh khác không chứng minh production sẽ lấy cùng dữ liệu. Trước khi phát hành, kiểm đúng cặp commit backend/frontend và artifact. Mọi bước đổi `main` có thể đưa lên production cần chủ dự án duyệt theo yêu cầu hiện hành.

`HANDOFF.md` ghi đóng băng 09:30, `UX_PLAN.md` ghi 11:00 ngày 15/11; chưa có bằng chứng chốt lại giờ nào. Dùng 09:30 làm mốc dự trù thận trọng cho đến khi được chốt. Hướng dẫn cũ cấm GitHub Actions đã mâu thuẫn với workflow thực tế; cần sửa tài liệu sau khi chủ dự án xác nhận quy trình.

## Lịch triển khai đề nghị để duyệt

1. **G1:** sửa độ phủ, hợp đồng API, CSV, test liên quan và hình; thống nhất số liệu và ví dụ bằng `osm_id`, không chỉ bằng tên. Có hai xã Vĩnh Thạnh: Tây Ninh đủ phủ gần 100%, Cần Thơ chỉ khoảng 7,4% ở ảnh tham khảo hiện tại.
2. **G3 bản nhỏ:** đưa số đối chiếu và biểu đồ HLS lên đầu; làm độc lập được với G1 vì dùng tập kiểm chứng riêng.
3. **G2:** hero nhận API, CTA Play hoạt động và trạng thái dữ liệu rõ ràng. Bản bố cục có thể chuẩn bị sớm; số cuối lấy từ dữ liệu G1.
4. **G4 bản nhỏ:** mục gập, bố cục mobile, chữ chính; sửa maturity nếu bật simple mặc định. Dừng các chỉnh sửa mỹ thuật diện rộng để kiểm bài nộp và video.

Đây là đề xuất phân công, chưa giao quyền sửa sản phẩm hoặc phát hành cho Gemini.

## Nghiệm thu cần thêm vào plan

- Dữ liệu: dùng ảnh đúng diện tích, biên 49,999%/50%, ảnh mới thiếu phủ nhưng ảnh cũ đủ phủ, không có ảnh, thiếu mẫu số, track cùng ngày; `partial` có đỉnh dưới 5% vẫn không thành `no_flood`.
- Tổng số: trên snapshot hiện tại kỳ vọng 115 đủ đánh giá, 25 chưa đủ; giữ phân biệt 6 xã không có quan trắc và 19 xã có quan trắc nhưng không đạt quy tắc đánh giá hiện hành. Không biến thiếu dữ liệu thành 0%.
- G1 phải chạy xong CSV và fig5; API, Tổng quan, bản xuất, tài liệu và hình dùng cùng snapshot. Ví dụ đủ phủ được xác định bằng ID và có ngày chụp.
- CTA: từ phiên mới, đã chọn xã, đã bật lớp tổng kết, API chậm, nhấn hai lần; ảnh thực sự tiến ít nhất hai bước, Pause/đổi chế độ dừng bộ đếm; Back/Forward hoạt động.
- Ma trận UI: 1440×900 và 390×844, VI/EN, chuột/bàn phím/cảm ứng; mở đầu thấy câu chuyện, số liệu, CTA; không tràn ngang khi tăng cỡ chữ. Giữ thông tin ngày, maturity và cảnh ghép.
- HLS/SWOT: kiểm mẫu số, cặp thiếu dữ liệu, hòa điểm và số không hữu hạn; tiêu đề, biểu đồ và bảng tính từ cùng nguồn.
- Kiểm bản production chỉ sau khi được duyệt phát hành; xác minh hai commit và số liệu thật, không suy từ bản local.

## Kiểm tra đã chạy và giới hạn

| Phạm vi | Kết quả |
|---|---|
| Backend `f937b04`, `python -m pytest -q` | 13/13 qua; một cảnh báo thư viện, không phải lỗi test |
| Frontend remote `4f59e90`, `build:cloudflare` | Qua TypeScript/Vite; xuất 212 API response, 33 cảnh, 140 xã |
| Frontend remote `4f59e90`, `test:cloudflare` | 4/4 qua |
| Frontend remote `4f59e90`, `test:ux` | 8/8 qua |

Xem [backend-checks.log](backend-checks.log), [remote-frontend-checks.log](remote-frontend-checks.log). Frontend remote được xuất bằng `git archive` vào thư mục tạm, dùng thư viện local sẵn có và chỉ rõ `NISAR_REPO`; không đổi checkout hay lockfile. Đây là kiểm bản nền, chưa xác nhận các thay đổi G1–G4. Chưa kiểm lại trình duyệt hoặc kiểm định khoa học SAR độc lập.

Nguồn chính thức xác nhận hạn nộp 23:59 giờ địa phương ngày 15/11/2026: [Space Apps 2026](https://www.spaceappschallenge.org/2026/). Trang [Judging & Awards Guide](https://www.spaceappschallenge.org/resources/judging-awards-guide/) trả 502 khi thử đọc; tìm kiếm chỉ trả tài liệu 2025. Vì vậy tiêu chí bản 2026 vẫn **chưa được xác minh**, không dùng bản cũ như bằng chứng đã chốt.

## Dấu vết phối hợp và bàn giao

- [Phản biện Gemini vòng 1](gemini-review.md): dùng frontend local cũ; các kết luận thiếu `viewMode`, composite, `vsSwot` và lỗi biên dịch do thiếu các trường đó đã bị bác bỏ khi đọc remote. Không dùng vòng 1 độc lập làm danh sách lỗi hiện hành. Codex cũng không giữ mức khẩn cấp P0, tỷ lệ độ dài tiếng Việt không có chứng cứ hoặc dự đoán test bắt được hành vi chưa được test kiểm.
- [Phản biện Gemini vòng 2](gemini-round2-review.md): đã rút nhận xét thiếu kiểu trên remote, xác nhận các điểm về `partial`, Play, KPI, SWOT và maturity. Codex kiểm lại từng điểm quan trọng; bác nhận xét đã có `ov-explanation`, sửa cách tách 25 xã thành 6 không quan trắc và 19 có quan trắc nhưng chưa đủ đánh giá. Không coi các mức P0 trong phản hồi nguyên văn là mức khẩn cấp sự cố sản phẩm; đây là yêu cầu chỉnh kế hoạch trước triển khai.
- Gói nguồn, phản hồi JSON gốc và đính chính được giữ trong thư mục này. Trường thời gian trong phản hồi Gemini là lời mô hình, không dùng làm chứng cứ thời điểm chạy; kết quả test có log riêng. CLI báo `--mode plan` không có hiệu lực khi tắt mở rộng slash command; việc giới hạn đánh giá tĩnh được nêu trong đề bài, không được xem là bảo đảm sandbox.
- Codex không chấp nhận yêu cầu mở rộng G1 để đổi toàn bộ ngưỡng của cảnh ghép nếu chưa chốt phạm vi. Giữ việc trình bày bằng chứng riêng với việc đánh giá đủ phủ và ghi đúng nghĩa của lớp hiển thị.
- VERIFIED: số liệu và bản nền như trên. PENDING: sửa plan sau duyệt chủ trương; triển khai G1–G4; kiểm trình duyệt; xác nhận Judging Guide 2026 và giờ đóng băng.
- Không tạo kho memory song song. Checkpoint của việc này nằm tại [checkpoint.md](checkpoint.md); chưa sửa mã sản phẩm, dữ liệu hoặc thực hiện merge/deploy.
