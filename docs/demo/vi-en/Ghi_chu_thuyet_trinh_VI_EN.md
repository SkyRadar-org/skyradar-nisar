# Ghi chú thuyết trình / Speaker notes

## 1

**VI:** Mây che khuất mặt nước khi địa phương theo dõi rút nước để chuẩn bị vụ Đông Xuân. Vùng thí điểm gồm 140 xã đầu nguồn. Tỷ lệ nước tính trên phần xã quan sát được; chưa có mặt nạ ruộng lúa và không quyết định xuống giống.

**EN:** Clouds hide surface water during drainage and winter–spring crop preparation. The pilot covers 140 upper-delta communes. Water share refers to observed commune land, with no rice-field mask or sowing-readiness decision.

Nguồn / Sources: PROJECT_BRIEF.md §§2,4,10; ảnh chụp ứng dụng / app screenshot https://nisar-flood.skyradar.vn/?lang=vi; © Esri, © OpenStreetMap contributors

## 2

**VI:** Mặt nước phẳng phản xạ sóng đi xa vệ tinh nên thường tối ở HH và HV. Dùng 33 ảnh GCOV trên 047D,083A,148D. Mỗi quỹ đạo lặp 12 ngày; 29/33 sản phẩm là tạm thời.

**EN:** Calm open water reflects radar energy away and can look dark in HH and HV. We use 33 GCOV acquisitions on 047D,083A,148D. Each track repeats every 12 days; 29/33 source products are provisional.

Nguồn / Sources: PROJECT_BRIEF.md §§3–5,10,13; data/web/manifest.json; data/web/radar/2026-10-03_047D.jpg

## 3

**VI:** Chỉ đọc các khối HDF5 thuộc vùng nghiên cứu. Trung bình HH/HV theo công suất tuyến tính trên lưới 20 m. Hiệu chỉnh ngưỡng trên đúng hai ngày DSWx-S1. Chọn ảnh gần nhất đạt độ phủ ít nhất 50% toàn xã. Thống kê tách từng quỹ đạo. Xu hướng so hai ảnh cùng quỹ đạo cách không quá 24 ngày, quy về 12 ngày; không phải dự báo. Chưa dùng mặt nạ ruộng lúa.

**EN:** Read only HDF5 chunks in the study area. Average HH/HV in linear power on a 20 m grid. Calibrate thresholds on two DSWx-S1 dates only. Select the latest image with at least 50% full-commune coverage. Keep statistics separate by track. Trend compares same-track images within 24 days, normalized to 12 days; it is not a forecast. No rice-field mask.

Nguồn / Sources: PROJECT_BRIEF.md §§5,10,13; src/skyradar_nisar/config.py; sowing.py; data/web/stats/calibration.json

## 4

**VI:** Tân Hồng có 50,0% nước ngày 17/10 và 43,7% ngày 29/10/2026 trên phần diện tích quan sát, cùng quỹ đạo. Nước giảm không đồng nghĩa đã đủ điều kiện xuống giống. Người dùng xem ngày, độ phủ, bằng chứng ảnh và lịch sử từng quỹ đạo để ưu tiên kiểm tra thực địa.

**EN:** Tân Hồng has 50.0% observed water on 17 Oct and 43.7% on 29 Oct 2026, from the same track. Falling water does not establish sowing readiness. Inspect dates, coverage, image evidence and track-specific history to prioritize field checks.

Nguồn / Sources: PROJECT_BRIEF.md §§7–10,13; sowing_check.csv tại / at 7e0b127; ảnh ứng dụng / app screenshot

## 5

**VI:** NISAR có F1 cao hơn Sentinel-1 ở 14/16 ngày ảnh quang học không mây trong mùa lũ 8–11, đối chiếu OPERA DSWx-HLS ±2 ngày. Không suy rộng cho mọi mùa hoặc mọi địa điểm. Bảng SWOT có 13 hàng nhưng chỉ 12 cặp có cả hai cảm biến trên cùng pixel; 11 cặp NISAR cao hơn. Biểu đồ sửa được được dựng lại có chủ đích từ đúng các giá trị CSV, không nội suy.

**EN:** NISAR has higher F1 than Sentinel-1 on 14/16 clear-sky optical comparison dates in Aug–Nov, using OPERA DSWx-HLS within ±2 days. Do not generalize to every place or season. SWOT has 13 rows but 12 same-pixel comparison pairs; NISAR is higher on 11. The editable chart is intentionally rebuilt from the exact CSV values without interpolation.

Nguồn / Sources: PROJECT_BRIEF.md §§6,13; data/web/stats/vs_dswx_hls.csv; vs_swot.csv tại / at 7e0b127

## 6

**VI:** 115 xã có ảnh quan sát ít nhất 50% toàn xã:33 nhiều nước,39 vừa,43 ít. Cùng 115 xã có 24 giảm,79 ổn định,12 tăng. 25 xã còn lại chưa đủ quan sát, không tính là khô. Tỷ lệ cao và xu hướng giảm có thể đồng thời đúng. Chênh lệch 16+9 và 19+6 trong nguồn không được đưa lên slide; chỉ tổng25 được thống nhất.

**EN:** 115 communes have coverage of at least 50% of full commune area:33 high,39 moderate,43 low water. The same115 have24 falling,79 steady,12 rising trends. The remaining25 lack sufficient observations and are never counted as dry. High water and falling water can coexist. Omit the inconsistent partial/no-observation split and use the agreed total25.

Nguồn / Sources: PROJECT_BRIEF.md §§7,10,13; sowing_check.csv tại / at 7e0b127

## 7

**VI:** Công cụ đo mặt nước mở, chưa dùng mặt nạ ruộng lúa. Không quyết định ngày xuống giống, không cảnh báo thời gian thực, không dự báo nước rút hay khẳng định lớp ngập dưới tán đã kiểm chứng. Đối chiếu mới với sản phẩm vệ tinh, chưa khảo sát thực địa. Cần đặt quan sát cạnh lịch thời vụ và thông tin địa phương.

**EN:** The tool measures open surface water without a rice-field mask. It does not decide sowing dates, provide real-time alerts, predict drainage, or validate sub-canopy flooding. Validation uses satellite products, not field surveys. Use the observations alongside local calendars and conditions.

Nguồn / Sources: PROJECT_BRIEF.md §§10,14; https://github.com/SkyRadar-org/skyradar-nisar; người dùng yêu cầu bản song ngữ Việt–Anh cùng trang / user requested bilingual content on each slide
