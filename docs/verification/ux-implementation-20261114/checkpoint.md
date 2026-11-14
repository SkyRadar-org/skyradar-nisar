# Bàn giao UX_PLAN và bản sửa khung Play

Cập nhật: 19:42 ngày 14/11/2026 (GMT+7). Owner: Codex; Gemini đã phản biện tĩnh phần triển khai ban đầu.

- APPROVED: Người dùng duyệt triển khai; yêu cầu “merge vào main”; sau khi xác nhận hết lỗi khung hình, yêu cầu “Đã hết lỗi, merge vào main đi”. Quyền phát hành đã có; không hỏi lại.
- VERIFIED: Cả hai main đã merge đúng thứ tự. Backend mã/dữ liệu e6ab7b3; frontend bản UX 8e9daf8, rồi bản sửa Play 5ccc76c. Commit tài liệu sau đó không đổi mã/dữ liệu sản phẩm.
- VERIFIED: Bộ dữ liệu 115 đánh giá = 43 ít / 39 trung bình / 33 nhiều nước; 25 chưa đủ = 6 không quan trắc + 19 quan trắc một phần. Mẫu số nước là phần quan trắc; độ phủ là toàn xã OSM. Backend 17 test, frontend 10 UX + 4 Worker và build Cloudflare đã qua.
- VERIFIED: Workflow 43594663795 phát hành UX và 43595784202 phát hành bản sửa Play đều success ở build/test/deploy/verify. API production trả 115 xã, 14/16 HLS và 11/12 SWOT cùng pixel; bundle JS/CSS mới trùng local.
- VERIFIED: Lỗi khung Play đã tái hiện ở 1280×720: map top 136,5 → 156 px, timeline height 178,75 → 155,25 px. Sửa bằng vùng chữ giữ kích thước tự nhiên theo nội dung dài nhất, ẩn guides khỏi cây accessibility. Đo sau sửa ở 1280×720,1440×900 và domain thật: trước/sau Play không đổi vị trí/kích thước. Bản đồ 1440×900 vẫn 60,14% chiều cao. Người dùng cũng xác nhận hết lỗi.
- VERIFIED: Bằng chứng trong production-verification.json, playback-layout-production.json, playback-layout-production-geometry.json và ảnh PNG tương ứng. Đã đọc lại các giá trị stable=true và assets_match_local_build=true.
- CORRECTION: Overview vốn đã có wrapper details ở root.replaceChildren; nhận xét bác Gemini trước đó của Codex là sai và đã được đính chính.
- LESSON (scope UX này): Nghiệm thu Play cần đo khung trước/sau đổi chế độ, thông báo tải và nhãn chất lượng nguồn, không chỉ kiểm ngày ảnh tiến và Pause dừng. Chờ DOM bản đồ sẵn sàng trước khi đo; số đo rỗng lúc trang vừa reload không phải lỗi bố cục.
- COMPLETED_UNVERIFIED: Không có hạng mục được báo xong nhưng chưa kiểm. Không kiểm định khoa học SAR độc lập ngoài các nguồn đối chiếu đã có.
- PENDING: Không còn việc merge/sửa Play trong yêu cầu hiện tại. Các việc ngoài phạm vi như slide/video, ảnh Earthdata mới và Judging Guide 2026 không thuộc lần phát hành này.
- SYNC: Không có memory canonical trong workspace; dùng HANDOFF và checkpoint hiện có. Hai checkout ở main; trạng thái push của bản ghi này phải kiểm bằng Git trước khi kết thúc. Không tạo PR, không force-push, không xóa nhánh hoặc WIP.
