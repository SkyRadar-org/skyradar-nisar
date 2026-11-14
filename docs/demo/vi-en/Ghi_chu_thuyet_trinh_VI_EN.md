# Ghi chú thuyết trình / Speaker notes

## 1

**VI:** Mở bằng quyết định của người quản lý: trước vụ lúa, phải biết khu vực nào cần kiểm tra tiêu thoát nước trước. SkyRadar đưa quan trắc NISAR vào luồng chuẩn bị vụ mùa của cơ quan nông nghiệp, thủy lợi và HTX tại vùng đầu nguồn ĐBSCL. Đây là hỗ trợ ưu tiên kiểm tra, không phải điều khiển bơm hay kết luận đủ điều kiện gieo sạ.

**EN:** Begin with an operational question: which communes need drainage checks before the next rice crop? SkyRadar brings NISAR observations into upper-delta crop preparation for agriculture offices, irrigation teams and cooperatives. It supports checking priorities, not pump control or sowing-readiness certification.

Nguồn / Sources: PROJECT_BRIEF.md §§2,8,10; docs/SOWING_CONDITIONS.md; app screenshot

## 2

**VI:** Luồng minh họa việc canh tác ở vùng đê bao: có thể lấy lũ/phù sa theo kế hoạch, rồi quản lý tiêu nước và chuẩn bị vụ mới. App hiện hỗ trợ hai khâu quan trắc và khoanh vùng cần rà soát. Cống, bơm và lịch gieo sạ do địa phương kiểm tra và quyết định; app chưa tự động tích hợp hoặc tối ưu vận hành những khâu này. Giá trị hướng tới là có bằng chứng cập nhật để phân bổ công kiểm tra và theo dõi thực hiện kế hoạch.

**EN:** The diagram illustrates managed flood intake, drainage and crop preparation. The current app supports observation and commune prioritization. Gate/pump operations and sowing calendars remain with local teams; these are not integrated or automatically optimized by the app. The intended benefit is evidence to focus field checks and monitor the local plan.

Nguồn / Sources: docs/SOWING_CONDITIONS.md §§1,3,4; PROJECT_BRIEF.md §§2,8,10; https://mae.gov.vn/dbscl-chu-dong-ne-han-man-bao-dam-san-xuat-vu-dong-xuan-20262027-23153.htm

## 3

**VI:** Trình diễn luồng sẵn có: từ Tổng quan lọc tỉnh hoặc mức nước để chọn xã; đọc ngày và độ phủ, mở bảng chi tiết với xu hướng đo giữa ảnh cùng quỹ đạo, kiểm ảnh minh chứng và lịch sử mùa. Báo cáo thống kê hỗ trợ xuất CSV; không tuyên bố nút xuất riêng cho danh sách ưu tiên nếu giao diện chỉ xuất bảng báo cáo. Chưa tích hợp lịch thời vụ trong app; việc đối chiếu lịch là bước người dùng thực hiện bên ngoài.

**EN:** Demonstrate existing capabilities: filter province or water-share class in Overview, select a commune, verify acquisition date and coverage, inspect same-track trend, imagery and seasonal history. Reports support CSV export; this is not a claim of a dedicated priority-list export button. The current app does not embed local sowing calendars; users compare them externally.

Nguồn / Sources: water-pulse-fe/src/locales/overview.ts guide; PROJECT_BRIEF.md §§8,9; app screenshot

## 4

**VI:** Các câu ở cột cuối là cách dùng quan trắc để đặt câu hỏi tác nghiệp, không phải chỉ thị bơm. Vĩnh Hưng 61,3% ngày 27/10 ổn định gợi ý cần xác minh tiến độ tiêu thoát. Tân Hồng giảm 50,0→43,7% từ 17–29/10 cho phép theo dõi đà rút khi đối chiếu lịch gieo. Lấp Vò tăng 12,1→20,1% cần hỏi địa phương về kế hoạch lấy nước; radar không tự xác định nguyên nhân ngập. Lịch Tân Hồng 5–11/11 là bối cảnh báo chí, không phải tính năng tích hợp hay thời điểm app khuyến nghị.

**EN:** The final column proposes operational questions, not pump commands. Vĩnh Hưng’s 61.3% steady water share on 27 Oct motivates checking drainage progress. Tân Hồng’s 50.0→43.7% recession from 17–29 Oct can be considered alongside the local calendar. Lấp Vò’s 12.1→20.1% rise warrants checking planned intake with local teams; radar does not identify the cause. Tân Hồng’s reported 5–11 Nov sowing window is external context, not an integrated app feature or app recommendation.

Nguồn / Sources: sowing_check.csv and commune_water_by_date.csv at 7e0b127; PROJECT_BRIEF.md §§7,10; https://baodongthap.vn/xa-tan-hong-tap-trung-san-xuat-ben-vung-vu-dong-xuan-a247109.html

## 5

**VI:** Tối ưu kỹ thuật nằm ở việc không tải toàn bộ file GCOV nhiều GB: đọc bảng chỉ mục, tải đúng khối nén thuộc vùng nghiên cứu song song. Brief báo 0,5–3 phút mỗi ảnh; đây là benchmark trong tài liệu, không phải đo lại ở lượt làm slide. Giữ kết quả trùng từng bit với cách đọc chuẩn. Đưa về 20 m, ngưỡng HH < −14 dB và HV < −22 dB, loại mảng < 3 ha và nước thường xuyên. Tính theo xã và theo quỹ đạo, xuất tệp web/API/CSV. Khả năng tái chạy giúp cập nhật báo cáo theo mỗi đợt ảnh; chưa tuyên bố đã có lịch tự động nhận và phát hành ảnh mới.

**EN:** Technical optimization avoids downloading whole multiGB GCOV files: read the chunk index and fetch only compressed chunks within the study area in parallel. The 0.5–3 min/acquisition figure is the brief’s benchmark, not a new measurement. Values match standard reading bit for bit. Regrid to 20 m; use HH < −14 dB and HV < −22 dB, remove patches < 3 ha and permanent water. Compute per commune/track and export web/API/CSV outputs. The rerunnable pipeline supports updating reports when acquisitions arrive; this does not claim an automatic acquisition/deployment schedule.

Nguồn / Sources: PROJECT_BRIEF.md §5; source reader and config; data/web/manifest.json

## 6

**VI:** Đối chiếu độc lập OPERA DSWx-HLS trên điểm ảnh không mây tháng 8–11, ±2 ngày: NISAR có F1 cao hơn Sentinel-1 ở 14/16 ngày; dải F1 0,57–0,86 so với 0,50–0,78. SWOT cùng pixel cao hơn 11/12 cặp. Đánh giá 115/140 xã đủ quan sát; nhóm 33/39/43, xu hướng đúng 24 giảm, 79 ổn định, 12 tăng. Phần lớn ảnh (29/33) tạm thời. Không suy từ độ khớp bản đồ ra đã tiết kiệm chi phí, nước hay tăng năng suất; cần thử nghiệm với địa phương.

**EN:** Independent OPERA DSWx-HLS comparisons use clear-sky Aug–Nov pixels within ±2 days. NISAR has higher F1 on 14/16 dates, ranges 0.57–0.86 vs 0.50–0.78; same-pixel SWOT is higher on 11/12 pairs. 115/140 communes have sufficient coverage; classes 33/39/43 and trends 24 falling, 79 steady, 12 rising. 29/33 inputs are provisional. Map agreement does not demonstrate cost/water savings or yield gains; local operational trials remain needed.

Nguồn / Sources: vs_dswx_hls.csv; vs_swot.csv; sowing_check.csv; PROJECT_BRIEF.md §§6,10,13

## 7

**VI:** Chốt tác động cụ thể: app giúp cán bộ khoanh vùng kiểm tra, theo dõi thay đổi nước và lấy báo cáo. Mục tiêu là tập trung công kiểm tra và cập nhật kế hoạch sản xuất; cần hợp tác địa phương để đo hiệu quả. Lịch gieo sạ, mặn, rầy và dấu hiệu thu hoạch là hướng phát triển. Chỉ số mặt nước không thay lịch thời vụ hoặc đánh giá đất. Video 29,8 giây có phụ đề Anh là lựa chọn demo đề xuất; bộ slide song ngữ giữ theo yêu cầu của đội.

**EN:** Close with a concrete intended benefit: existing tools let officers target checks, track water change and obtain reports. Operationally, the goal is focused checking and better-informed crop plans; field collaboration is needed to measure that impact. Calendars, salinity, pest data and harvest detection are future integrations, not current features. Surface-water fractions do not replace agronomic calendars or soil checks. The proposed official demo is the 29.8-second video with English subtitles; the bilingual deck follows the team’s explicit request.

Nguồn / Sources: PROJECT_BRIEF.md §§8,10,14; SEPA guidance; NASA Project Submission Guide,13Nov2026
