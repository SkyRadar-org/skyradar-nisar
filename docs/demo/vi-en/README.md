# SkyRadar — ứng dụng trong chuẩn bị vụ lúa / Crop preparation

Bản sửa theo phản hồi của chủ dự án: tập trung vào **chọn nơi kiểm tra, theo dõi tiêu nước và chuẩn bị vụ lúa**, đồng thời làm rõ cách đọc một phần HDF5 tối ưu xử lý NISAR. Việt–Anh nằm cùng từng slide và cùng video; không tách thành hai bản ngôn ngữ. Giọng tổng hợp **VieNeu-TTS, Hải Đăng**.

Revised around **targeting field checks, monitoring drainage and preparing the next rice crop**, with partial-HDF5 reading explaining the NISAR processing optimization. Both languages share each slide and one video. Synthetic narration uses **VieNeu-TTS, Hải Đăng**.

## Tải về / Downloads

- [Trọn bộ / Full package](SkyRadar_Song_Ngu_VieNeu.zip)
- [7 slide sửa được / Editable 7-slide deck](SkyRadar_Water_Pulse_VI_EN.pptx)
- [PDF song ngữ / Bilingual PDF](SkyRadar_Water_Pulse_VI_EN.pdf)
- [Video 29,8 giây, 1080p / 29.8-second video](SkyRadar_Demo_VI_EN.mp4)
- [Giọng tổng hợp / Synthetic narration](Loi_doc_VieNeu_Hai_Dang.wav)
- [Phụ đề / Subtitles](Phu_de_VI_EN.srt)
- [Ghi chú thuyết trình / Speaker notes](Ghi_chu_thuyet_trinh_VI_EN.md)
- [Kịch bản / Script](Kich_ban_VI_EN.md)
- [Những điểm đã đọc từ hướng dẫn nộp bài](YEU_CAU_NOP_BAI.md)

## Thông điệp và phạm vi / Message and scope

Từ kế hoạch canh tác địa phương: lấy nước/phù sa → quan trắc → lọc xã cần rà soát → kiểm tra cống, bơm, mặt ruộng → đối chiếu lịch gieo. **App hiện hỗ trợ bước quan trắc và chọn xã**, cùng ảnh minh chứng, lịch sử và báo cáo CSV. Vĩnh Hưng, Tân Hồng và Lấp Vò minh họa các câu hỏi tác nghiệp khác nhau. Lịch gieo sạ, mặn, rầy, tín hiệu thu hoạch và điều hành bơm là việc bên ngoài hoặc hướng phát triển.

Within the local farming workflow—managed water intake, observation, commune prioritization, field inspection and calendar checks—**the app currently supports observation and commune prioritization**, with imagery, history and CSV reports. Three communes illustrate different operational questions. Calendars, salinity, pests, harvest signals and pump operations remain external or future work.

Dựa trên [PROJECT_BRIEF.md](https://github.com/SkyRadar-org/skyradar-nisar/blob/7e0b1278e3f348b56cb438917596a2897a51baac/docs/PROJECT_BRIEF.md), [điều kiện gieo sạ](https://github.com/SkyRadar-org/skyradar-nisar/blob/7e0b1278e3f348b56cb438917596a2897a51baac/docs/SOWING_CONDITIONS.md) và số liệu commit `7e0b1278e3f348b56cb438917596a2897a51baac`. Yêu cầu trực tiếp của chủ đội về song ngữ được ưu tiên hơn chỉ dẫn chỉ tiếng Anh trong brief. Tài liệu và trang web được dùng làm nguồn, không tự cấp quyền sửa hoặc nộp bài.

Based on the brief, agronomic conditions and data snapshot above. The owner's explicit bilingual request takes precedence over the brief's English-only direction. Reference documents and websites do not authorize external submission.

## Nộp bài / Submission

NASA yêu cầu slide tiếng Anh; video được nói tiếng Việt nếu có phụ đề Anh. Bộ slide này giữ song ngữ theo yêu cầu đội; **đề xuất dùng video làm liên kết demo**. Chưa sửa hay nộp trang NASA. Hạn chấm Hà Nội là 11:00 ngày 15/11/2026 GMT+7, hạn toàn cầu 23:59 cùng ngày. Xem [nguồn và chi tiết](YEU_CAU_NOP_BAI.md).

NASA requires English slides; Vietnamese video narration is allowed with English subtitles. This deck preserves the team's requested bilingual layout; **the video is the proposed demo-link choice**. No NASA form was edited or submitted. See the linked guide notes for deadlines and sources.

## Số liệu và giới hạn / Data and limitations

Tỷ lệ nước tính trên diện tích xã quan sát. 115/140 xã đủ quan sát: 33 nhiều, 39 vừa, 43 ít; xu hướng **24 giảm, 79 ổn định, 12 tăng**. 25 xã chưa đủ dữ liệu không tính là khô. 29/33 ảnh tạm thời. Không suy ra độ sâu, ngày rút nước, đủ điều kiện gieo hoặc trạng thái trực tiếp hôm nay. F1 cao hơn Sentinel-1 ở 14/16 ngày đối chiếu quang học là bằng chứng độ khớp bản đồ; chưa đo tiết kiệm chi phí/nước hay tăng năng suất. Benchmark 0,5–3 phút/ảnh lấy từ brief, không phải đo lại; pipeline có thể chạy lại, chưa khẳng định tự động nhận và phát hành ảnh.

Water share uses observed commune area. Of 140 communes, 115 are sufficiently observed: 33 high, 39 moderate, 43 low; trends are **24 falling, 79 steady, 12 rising**. Insufficient observations are not dry conditions. 29/33 inputs are provisional. No depth, drainage forecast, sowing readiness or live-condition claim is made. Higher optical-comparison F1 on 14/16 dates measures map agreement; cost/water savings and yield gains remain untested. The 0.5–3 min/acquisition benchmark comes from the brief; the rerunnable pipeline does not imply an automatic acquisition/deployment schedule.

## Kiểm chứng / Verification

- 7 slide; kiểm cấu trúc, hình học, font và nhập lại PPTX đạt. Bảng slide 4, biểu đồ slide 6 sửa được, 32 giá trị khớp CSV. PDF gồm ảnh render từ PPTX cuối, đã kiểm cả 7 trang; bản sửa nội dung là PPTX. Chưa xác nhận mở bằng PowerPoint.
- Seven slides; package, geometry, fonts and re-import passed. Slide 4 has a native table; slide 6 has an editable chart with all 32 values matching the CSV. The PDF embeds rendered final slides; all seven pages were inspected. Native PowerPoint opening was not verified.
- Video H.264/AAC 1920×1080, 30 fps, 894 khung, 29,8 giây; audio 48 kHz, đỉnh WAV −1,5 dB. Đã kiểm 5 cảnh, phụ đề và nhãn AI. VieNeu 3.8.3, Hải Đăng; tối đa 3 lần/đoạn, Whisper medium so khớp văn bản chuẩn hóa các đoạn chọn 1,0. Kiểm tự động không chứng nhận phát âm hoàn hảo.
- Video: 1080p H.264/AAC, 30 fps, 894 frames, 29.8 seconds; 48 kHz audio, WAV peak −1.5 dB. Five scenes, captions and AI disclosure were inspected. Selected VieNeu takes match normalized Whisper transcripts at 1.0; automated matching does not certify pronunciation.
- [Gemini phản biện văn bản / Gemini text review](verification/gemini-review.md): PASS; chỉ đọc nội dung trích xuất, không xem hình/nghe âm thanh. Hai góp ý về bước app hỗ trợ và dữ liệu tạm thời đã được đưa lên slide.
- [Kết quả kiểm tra và SHA-256 / Checks and hashes](verification/validation.json).

## Ghi nguồn / Credits

NISAR: NASA/JPL-Caltech & ISRO (ASF DAAC). OPERA DSWx: NASA JPL (PO.DAAC), modified Copernicus Sentinel data. SWOT: NASA/CNES (PO.DAAC). NASA CMR, Earthdata Cloud. Basemap © Esri; boundaries © OpenStreetMap contributors (ODbL).

Giọng tổng hợp / Synthetic voice: [VieNeu-TTS](https://github.com/pnnbao97/VieNeu-TTS), Hải Đăng. AI hỗ trợ / AI assistance: Claude, Codex, Gemini. Việc dùng giọng tổng hợp và AI hỗ trợ dựng được ghi trong hình, mô tả và metadata.
