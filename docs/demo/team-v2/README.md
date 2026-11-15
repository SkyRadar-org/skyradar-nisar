# SkyRadar — bộ slide/video v2 do đội cập nhật

Đây là bộ mới nhất do chủ dự án gửi ngày 15/11/2026, thay cho bộ demo tại `../vi-en/`. Giữ nguyên cả 5 tệp gốc trong ZIP; các bản ngôn ngữ do đội cung cấp, không được Codex biên soạn lại.

This is the revised package supplied by Team SkyRadar on 15 November 2026, superseding the earlier demo package. All five supplied files are preserved byte for byte.

## Tệp mới / Updated files

- [Slide Việt–Anh trên cùng trang / Bilingual slides](SkyRadar_pitch_EN-VI_v2.pdf)
- [Slide tiếng Anh, 7 trang / English slides](SkyRadar_pitch_EN_v2.pdf)
- [Slide tiếng Việt / Vietnamese slides](SkyRadar_pitch_VI_v2.pdf)
- [Video phụ đề Anh, nguyên bản / Original video with English captions](SkyRadar_pitch_30s_EN_sub.mp4)
- [Video phụ đề Việt, nguyên bản / Original video with Vietnamese captions](SkyRadar_pitch_30s_VI_sub.mp4)
- [Video dùng cho liên kết demo / Official demo-link video](SkyRadar_pitch_30s_EN_sub_submission.mp4)

Bản video dùng cho liên kết demo có cùng luồng hình và âm thanh với nguyên bản phụ đề Anh. Chỉ bổ sung metadata khai báo lời đọc tổng hợp AI, không mã hóa lại. Hash luồng nén hình và âm thanh đã đối chiếu trùng nhau. GitHub có thể hiện “View raw”/“Download raw file”; tải hoặc mở video công khai không cần đăng nhập.

The demo-link version adds synthetic-narration metadata without re-encoding. Its compressed video and audio stream hashes match the supplied English-caption version. GitHub may require clicking “View raw” or “Download raw file”; no account is required to access the public file.

## Kiểm tra / Checks

- Mỗi PDF 7 trang; đã trích xuất nội dung và render kiểm bố cục 21 trang. Đây là PDF do đội gửi, chưa có PPTX nguồn trong ZIP.
- Cả hai video 1920×1080, H.264/AAC, 30 fps, 894 khung hình, 29,8 giây; âm thanh 48 kHz.
- Video mới dùng lời đọc tiếng Anh, có nhãn “Voice-over: AI text-to-speech”. Tệp gốc không xác định tên bộ máy/giọng đọc; không gán thông tin VieNeu–Hải Đăng của video cũ cho bản mới.
- Bản Việt–Anh giữ hai ngôn ngữ trên cùng slide. Có thêm bản EN và VI nguyên bản của đội để tiện dùng; video demo chính là bản phụ đề Anh.
- Đây là kiểm tra cấu trúc, thời lượng, mẫu hình ảnh và bảo toàn tệp; không phải kiểm chứng khoa học hay xác nhận của ban tổ chức.
- [Dấu vân tay và kết quả kiểm tra / Manifest](manifest.json)

Each PDF contains 7 pages; all 21 pages were rendered and inspected. Both supplied videos are 29.8-second 1080p H.264/AAC files. The revised narration is English and visibly labeled as AI text-to-speech; the supplied files do not identify the voice engine. The earlier VieNeu–Hải Đăng attribution is not applied to this revision.

## Khai báo AI / AI disclosure

The revised video contains synthetic English narration, visibly disclosed on screen. The demo-link MP4 also acknowledges synthetic audio in container metadata. Voice-engine identity was not supplied. Claude, Codex, Gemini and Copilot are credited in the team's revised slides for assistance with code and documents. Actual app recordings and satellite imagery remain project evidence; no synthetic satellite observations are claimed.

## Trạng thái bài thi / Submission status

Đang cập nhật liên kết v2 trên trang SkyRadar; việc commit tệp không tự nộp lại bài thi. Trạng thái nộp được ghi tại [hồ sơ nộp bài](../../SUBMISSION_STATUS_20261115.md).

Publishing these files does not itself resubmit the NASA project. The submission record above tracks the form update separately.
