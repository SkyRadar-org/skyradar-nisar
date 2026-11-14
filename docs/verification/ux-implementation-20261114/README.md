# Triển khai UX_PLAN — đã merge và phát hành

Cập nhật: 19:17 ngày 14/11/2026 (GMT+7). Người dùng đã duyệt triển khai, merge main và phát hành; xem phần trạng thái production cuối báo cáo.

## Kết quả

- G1: chọn ảnh mới nhất quan trắc ≥50% diện tích toàn xã OSM và ≥5 km², trước làm tròn. Giữ ảnh phần rìa làm bằng chứng; không thay ảnh cũ đủ phủ bằng ảnh mới thiếu phủ. CSV xuất lại khớp từng byte với thuật toán hiện tại.
- 115 xã đủ đánh giá: **43 ít nước / 39 một phần nước / 33 nhiều nước**. Trong 140 xã, 25 chưa đủ đánh giá: **6 không có quan trắc, 19 có quan trắc một phần**. Có 16 bản ghi `partial` mới trong CSV; ba xã còn lại trước đó đã không đạt ngưỡng diện tích tối thiểu.
- API trả `area_km2`, `observed_pct`; thiếu phủ luôn `uncertain`, kể cả đỉnh nước thấp. API gốc hỗ trợ lọc `partial` và tách `partial_count`. Hình 2/3/5 đã tái tạo từ CSV, kiểm trực quan; fig3 dùng Vĩnh Hưng/Phương Thịnh, fig5 phân biệt phần quan trắc thiếu phủ.
- G2: hero dùng chung, lấy **33/115**, **14/16**, **33** từ API. CTA bắt đầu từ ảnh tháng 8, xóa lựa chọn và lớp tổng kết cũ, bật nước và chạy Play. Timer chỉ có một nơi sở hữu; Pause, đổi tab/chế độ và phím mũi tên dừng phát.
- G3: đưa kết quả HLS, biểu đồ cột và SWOT lên đầu, dùng chung hàm tính; **14/16 cặp quang học**, **11/12 cặp SWOT cùng pixel**. Bỏ cặp thiếu/không hữu hạn; hòa không tính là thắng. Có bảng đọc số thay cho canvas.
- G4 bản gọn: simple mặc định, một mục Điều khiển nâng cao chứa lớp, chế độ và bộ lọc quỹ đạo. Giữ nhãn nguồn tạm thời/đã kiểm định cho ảnh ghép trên cả điện thoại và desktop. Chữ chính được tăng; không thay hàng loạt mọi CSS hoặc áp ngưỡng 350 từ không phân biệt ngôn ngữ.
- Giữ mục giải thích đã được gập sẵn. Đính chính phản biện trước: Codex đã nhìn nơi định nghĩa `section` và bỏ sót wrapper `<details>` ở `root.replaceChildren`; Gemini đúng về việc có mục gập. Tài liệu và checkpoint liên quan đã có đính chính.

Tỷ lệ nước mô tả phần diện tích quan trắc, tỷ lệ phủ mô tả toàn xã theo ranh OSM. Nhóm nước thấp không phải khuyến nghị xuống giống; nhóm trung bình không tự chứng minh nước đang rút. Cảnh ghép được ghi rõ dùng nguồn nhiều ngày, không phải ảnh chụp đồng thời hoặc dữ liệu trực tiếp hôm nay.

## Kiểm chứng

| Hạng mục | Kết quả thực chạy |
|---|---|
| Backend, `python -m pytest -q` | 17/17 qua, gồm bốn ca biên thuật toán phủ |
| Frontend, `npm run test:ux` | 10/10 qua, gồm số liệu mới và phép đếm HLS/SWOT |
| Worker, `npm run test:cloudflare` | 4/4 qua |
| `PYTHON=/Users/Chris/nisar/.venv/bin/python npm run build:cloudflare` | Qua TypeScript/Vite; 212 API response, 33 cảnh, 140 xã, 472 file |
| API trên Wrangler/workerd `localhost:8794` | health/scenes/communes/validation trả 200 JSON, API lạ trả 404 JSON; xác nhận115 đánh giá, nhóm 43/39/33 |
| Trình duyệt VI/EN, 1440×900 và 390×844 | Hero và CTA trước cuộn, không tràn ngang; số và biểu đồ đúng |
| Play/Pause và điều hướng | Thực thấy11/8 → 16/8, Pause giữ ảnh ở cả VI/EN; ←/→ 16/8 → 18/8 → 16/8; Back/Forward, track047D và chế độ chuyên nghiệp hoạt động |
| Chiều cao bản đồ khi mở timeline | VI 62,3%, EN 64,5% ở 1440×900 |
| Xã thiếu phủ và CTA | Sơn Kiên: 78,2% nước trên phần quan trắc, phủ 19,6% toàn xã, không đánh giá; CTA xóa panel và khôi phục toàn vùng |

Xem [verification.json](verification.json), [browser-qa.json](browser-qa.json). Console trình duyệt không có cảnh báo/lỗi được ghi nhận trong lượt kiểm cuối. Backend có một cảnh báo thư viện Starlette/httpx; không phải lỗi kiểm thử.

## Phản biện Gemini

Đã gọi thật Antigravity CLI với model yêu cầu `gemini-4-argon-high`, hai lượt độc lập:

- [G1 — PASS kiểm tĩnh](gemini-g1-review.md).
- [Frontend — PASS kiểm tĩnh](gemini-frontend-review.md).

Gói nguồn backend và phản hồi JSON nguyên văn được giữ cạnh báo cáo. Gói nguồn frontend được giữ local vì repo frontend là private; repo public chỉ lưu [manifest và SHA-256](gemini-frontend-input-manifest.json). Gemini không tự chạy test/trình duyệt. Các chỉnh nhỏ sau review gồm chú giải hình, cách hiển thị phần trăm phủ, lời nhắc trong panel và bản dịch; đã build/kiểm thực tế lại. Số liệu chính thức trong báo cáo lấy từ CSV/API, không lấy từ con số diễn giải của mô hình.

## Ảnh kiểm giao diện

| Trang | VI desktop | VI điện thoại | EN desktop | EN điện thoại |
|---|---|---|---|---|
| Tổng quan | [Ảnh](overview-vi-1440.png) | [Ảnh](overview-vi-390.png) | [Ảnh](overview-en-1440.png) | [Ảnh](overview-en-390.png) |
| Bản đồ | [Ảnh](map-vi-1440.png) | [Ảnh](map-vi-390.png) | [Ảnh](map-en-1440.png) | [Ảnh](map-en-390.png) |
| Độ tin cậy | [Ảnh](validation-vi-1440.png) | [Ảnh](validation-vi-390.png) | [Ảnh](validation-en-1440.png) | [Ảnh](validation-en-390.png) |

[Bằng chứng Sơn Kiên](partial-son-kien-vi.png) · [Điều khiển nâng cao](advanced-en-1440.png).

## Bàn giao và phát hành

**ĐÃ PHÁT HÀNH**: cập nhật cuối 19:42 ngày 14/11/2026 (GMT+7). Người dùng đã duyệt merge, cả hai main đã cập nhật; bản sửa Play `5ccc76c` đã lên production. Các đoạn chờ duyệt phía trên là trạng thái lịch sử của lần bàn giao đầu.

- Hai repo dùng nhánh `codex/ux-implementation-20261114`. Mốc đầu: backend `f937b04` cùng commit review `95bdad7`; frontend `4f59e90`. `main` từ xa vẫn đúng hai mốc dữ liệu/mã đầu khi kiểm lại trước chốt.
- Bản chạy thử tại [localhost:8794](http://localhost:8794/?lang=vi). Đây là server local của phiên kiểm; cần server còn chạy để mở được.
- Frontend workflow luôn lấy backend `main`: khi được duyệt production, đưa dữ liệu/backend đúng bản lên trước rồi frontend, build và kiểm số lần cuối trước phát hành. Build với backend cũ sẽ không thỏa test115xã.
- Đã commit/push và kiểm SHA remote: backend `2f451ad`, frontend `8e9daf8`. Xem [bằng chứng bàn giao](delivery.json). Commit tài liệu ghi nhận bàn giao được thêm sau cặp commit mã này. Chưa tạo PR, chưa merge, chưa deploy.
- Không có memory canonical được cấu hình trong workspace; đã cập nhật HANDOFF hiện có và [checkpoint](checkpoint.md), không tạo kho nhớ song song.
- Ngoài phạm vi: tải ảnh Earthdata mới, sửa thuật toán cảnh ghép, thêm lớp SWOT lên bản đồ, biên tập slide/video, các thay đổi tài khoản/hosting. Hướng dẫn chấm2026 và giờ đóng băng 09:30/11:00 vẫn cần chủ dự án xác nhận nếu sử dụng cho kế hoạch nộp bài.


## Cập nhật production và sửa khung Play

- Người dùng yêu cầu “merge vào main”: backend được fast-forward lên `e6ab7b3`, frontend lên `8e9daf8`. Workflow[43594663795](https://github.com/SkyRadar-org/water-pulse-fe/actions/runs/43594663795) hoàn tất build/test/deploy/verify thành công. API production xác nhận 115 xã, nhóm 43/39/33 và bundleJS trùng bản local đã kiểm; xem[production-verification.json](production-verification.json).
- Người dùng báo khung bản đồ/thanh thời gian đổi kích thước khi Play. Đã tái hiện: map top 136,5 → 156 px, timeline height 178,75 → 155,25 px ở 1280×720. Nguồn là thay đổi độ dài tiêu đề/chú thích và dòng hướng dẫn timeline bị ẩn.
- Bản sửa giữ không gian nội dung tự nhiên theo các đoạn chữ của từng chế độ; không cắt chữ, không giả định chiều cao cố định. Đo trước/sauPlay ở 1280×720 và1440×900 đều không đổi vị trí/kích thước; bản đồ 1440×900 vẫn chiếm 60,14% chiều cao. Xem[đo1280×720](playback-layout-regression.json),[đo1440×900](playback-layout-desktop.json) và[ảnhbảnsửa](playback-layout-fixed.png).
- Người dùng xác nhận “Đã hết lỗi, merge vào main đi”; frontend đã fast-forward tiếp lên `5ccc76c`. Bản sửa qua TypeScript/Vite và 10 UX + 4 Worker test. Đã phát hành thành công: [workflow 43595784202](https://github.com/SkyRadar-org/water-pulse-fe/actions/runs/43595784202), build/test/deploy/verify đều success. Bundle JS/CSS production trùng bản đã kiểm; API vẫn 115 xã. Đo trực tiếp production sau khi giao diện tải đủ: khung giữ nguyên trước/sauPlay. Xem [kiểm phát hành](playback-layout-production.json), [hình học production](playback-layout-production-geometry.json), [ảnh production](playback-layout-production.png).
