# Bàn giao triển khai UX_PLAN

Cập nhật: 19:17 ngày 14/11/2026 (GMT+7). Owner: Codex; Gemini phản biện tĩnh. Nhánh cả hai repo: `codex/ux-implementation-20261114`.

- APPROVED: Người dùng yêu cầu “Triển khai đi” sau báo cáo phản biện; phạm vi G1–G3 và G4 bản gọn. Người dùng đã duyệt merge vào main bằng tin “merge vào main”; frontend main tự triển khai production.
- VERIFIED: G1 và dữ liệu mới, hình 2/3/5, hợp đồng API, tài liệu đã hoàn tất.115 đánh giá, nhóm 43/39/33;25 chưa đủ đánh giá = 6 không quan trắc + 19 quan trắc một phần. CSV tái lập khớp từng byte.
- VERIFIED: Hero động và CTA Play tháng 8, bằng chứng14/16 HLS và11/12 SWOT cùng pixel; điều khiển nâng cao và nhãn chất lượng ảnh ghép hiện ởVI/EN desktop/mobile.17 backend + 10 UX + 4 Worker test qua; buildCloudflare qua.
- VERIFIED: API workerd200/404 đúng; Play tiến ảnh và Pause ổn địnhVI/EN; phím ←/→, Back/Forward, quỹ đạo 047D, CTA xóa lựa chọn; bản đồ VI 62,3% / EN 64,5% chiều cao desktop. Screenshot và JSON QA trong thư mục.
- VERIFIED: Gemini gọi thật 2 lượt, G1 và frontend PASS phạmvi tĩnh. Codex phụ trách kiểm thực thi, không quy kết model đã chạy test/trình duyệt.
- CORRECTION: Phần hướng dẫn Tổng quan vốn đã bọc details tại root.replaceChildren; Codex đã bác sai Gemini khi chỉ xem nơi định nghĩa section. Đã sửa ghi chú trong báo cáo đánh giá và HANDOFF.
- COMPLETED_UNVERIFIED: Không có phần triển khai nào tuyên bố xong nhưng chưa kiểm; không kiểm định SAR độc lập ngoài các nguồn đối chiếu sẵn có.
- VERIFIED: Đã commit/push hai nhánh và đối chiếu SHA remote khớp local: backend 2f451ad, frontend 8e9daf8; hai checkout sạch tại thời điểm kiểm. Xem delivery.json.
- PENDING: Thực hiện merge backend trước, frontend sau và kiểm workflow/production. Khi phát hành phải cập nhật backend main trước frontend do workflow lấy backend main.
- ASSUMPTION: Giờ đóng băng 09:30/11:00 và Judging Guide 2026 chưa được xác nhận; không dùng để tự thay lịch hoặc phạm vi.
- SYNC: File đã ghi và đọc lại local. Không có memory canonical; dùng HANDOFF hiện có, không tạo kho mới. Chưa PR/merge/deploy.

- APPROVED 19:23 ngày 14/11/2026 (GMT+7): Người dùng yêu cầu “merge vào main”. Đã fetch cả hai repo: main backend f937b04, frontend4f59e90; không có commit mới ngoài bản đã kiểm, hai checkout sạch trước thao tác. Trước khi merge, lưu checkpoint này; chưa coi merge/deploy là hoàn tất.
