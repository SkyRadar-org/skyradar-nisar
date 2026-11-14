# SkyRadar NISAR Water Pulse — Việt–Anh / Vietnamese–English

Bộ trình bày song ngữ: Việt–Anh nằm **cùng mỗi slide và cùng video**. Lời đọc tiếng Việt dùng **VieNeu-TTS, Hải Đăng**; hai ngôn ngữ phụ đề xuất hiện đồng thời.

Bilingual presentation: Vietnamese and English share **each slide and one video**. Vietnamese narration uses **VieNeu-TTS, Hải Đăng**, with both subtitle languages visible together.

## Tải về / Downloads

- [Trọn bộ / Full package](SkyRadar_Song_Ngu_VieNeu.zip)
- [Bản trình chiếu sửa được, 7 trang / Editable 7-slide deck](SkyRadar_Water_Pulse_VI_EN.pptx)
- [PDF song ngữ / Bilingual PDF](SkyRadar_Water_Pulse_VI_EN.pdf)
- [Video 29,8 giây, 1080p / 29.8-second 1080p video](SkyRadar_Demo_VI_EN.mp4)
- [Âm thanh VieNeu–Hải Đăng / VieNeu–Hải Đăng narration](Loi_doc_VieNeu_Hai_Dang.wav)
- [Phụ đề song ngữ / Bilingual subtitles](Phu_de_VI_EN.srt)
- [Ghi chú thuyết trình / Speaker notes](Ghi_chu_thuyet_trinh_VI_EN.md)
- [Kịch bản / Script](Kich_ban_VI_EN.md)

## Nguồn và giới hạn / Sources and limits

Dựa trên [PROJECT_BRIEF.md](../../PROJECT_BRIEF.md), số liệu tại commit `7e0b1278e3f348b56cb438917596a2897a51baac`. Theo yêu cầu trực tiếp của chủ dự án, bộ này có hai ngôn ngữ chung một sản phẩm, thay cho chỉ dẫn chỉ tiếng Anh trong brief.

Based on [PROJECT_BRIEF.md](../../PROJECT_BRIEF.md) and data at commit `7e0b1278e3f348b56cb438917596a2897a51baac`. The owner explicitly requested both languages in each artifact, replacing the brief's English-only direction.

Tỷ lệ nước tính trên phần diện tích xã quan sát được. Chỉ 115/140 xã đủ quan sát để đánh giá, gồm 33 nhiều nước, 39 vừa, 43 ít; xu hướng 24 giảm, 79 ổn định, 12 tăng. 25 xã chưa đủ quan sát không bị tính là khô. Không suy ra độ sâu nước, điều kiện xuống giống, dự báo nước rút, quan trắc trực tiếp hôm nay hoặc kiểm chứng thực địa.

Water share refers to observed commune area. Only 115/140 communes have sufficient coverage: 33 high, 39 moderate, 43 low water share; trends are 24 falling, 79 steady, 12 rising. The 25 insufficiently observed communes are not counted as dry. The results do not establish water depth, sowing readiness, drainage forecasts, live conditions or field validation.

## Kiểm tra / Validation

- Đủ 7 slide; cấu trúc, bố cục, font và nhập lại PPTX đạt. Biểu đồ F1 sửa được, có bảng số nhúng; 32 giá trị khớp CSV. PDF được render và kiểm đủ 7 trang. Chưa xác nhận mở bằng PowerPoint.
- Seven slides; PPTX package, geometry, fonts and re-import passed. The editable F1 chart embeds its data, with all 32 values matching the CSV. All seven PDF pages were rendered and inspected. Native PowerPoint opening was not verified.
- Video H.264/AAC, 1920 × 1080, 30 fps, 894 khung hình, 29,8 giây. WAV 48 kHz, đỉnh âm thanh −1,5 dB. Phụ đề nằm ngoài vùng giao diện chính.
- Video: H.264/AAC, 1920 × 1080, 30 fps, 894 frames, 29.8 seconds. WAV: 48 kHz, peak −1.5 dB. Captions sit outside the main application image.
- VieNeu `3.8.3`, preset Hải Đăng. Tạo nhiều lần cho đoạn chưa rõ, chọn lại bằng Whisper medium; điểm so khớp văn bản chuẩn hóa của các đoạn chọn từ 0,9907 đến 1,0. Đây là kiểm tự động, không chứng nhận phát âm hoàn hảo.
- VieNeu `3.8.3`, Hải Đăng preset. Unclear segments were regenerated and selected with Whisper medium; selected normalized text-match scores range from 0.9907 to 1.0. This automated check does not certify perfect pronunciation.
- [Gemini phản biện văn bản / Gemini static text review](verification/gemini-review.md); các góp ý nhỏ đã được Codex đối chiếu và bổ sung. Gemini không tự xem hình, nghe âm thanh hoặc chạy kiểm tra.
- [Kiểm tra và dấu vân tay / Verification and checksums](verification/validation.json).

## Ghi nguồn / Credits

NISAR: NASA/JPL-Caltech & ISRO (ASF DAAC). OPERA DSWx: NASA JPL (PO.DAAC), modified Copernicus Sentinel data. SWOT: NASA/CNES (PO.DAAC). NASA CMR and Earthdata Cloud. Bản đồ nền / Basemap © Esri; ranh giới / boundaries © OpenStreetMap contributors (ODbL).

Giọng / Voice: [VieNeu-TTS](https://github.com/pnnbao97/VieNeu-TTS), Hải Đăng. Hỗ trợ AI / AI assistance: Claude, Codex, Gemini; đội rà soát / team reviewed.
