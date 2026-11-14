**Thời gian báo cáo:** 18:57 GMT+7, ngày 14/11/2026
**Verdict:** **PASS**

Dựa trên kiểm tra tĩnh độc lập các file đính kèm cho cổng G1 (ghi nhận kết quả thực chạy từ Codex: `sowing`, `figures --csv-only` và 17 pytest pass; không tự chạy lệnh/test), toàn bộ yêu cầu kỹ thuật của G1 đã được giải quyết đúng và chặt chẽ.

---

### Kết quả rà soát chi tiết theo từng hạng mục

#### 1. Logic chọn ảnh và ngưỡng độ phủ (`selection`)
- **`src/skyradar_nisar/sowing.py` (`assess_communes`)**:
  - Lọc đầu vào `float(row["valid_km2"]) >= 5`.
  - Xác định tập hợp hợp lệ trên toàn bộ chuỗi quan trắc của xã theo diện tích toàn xã từ OSM: `eligible = [r for r in observations if area and float(r["valid_km2"]) >= 0.5 * area]`.
  - Nhờ lọc `eligible` trên `observations` trước khi chọn `max(eligible or fallback, key=lambda r: (r["date"], float(r["valid_km2"]), r["track"]))`, một lát cắt hẹp (sliver `< 50%` diện tích xã) ở ngày mới hơn không thể ghi đè ảnh hợp lệ cũ hơn trên cùng track hoặc khác track.
  - Phép so sánh `float(r["valid_km2"]) >= 0.5 * area` được thực hiện trên số thực **trước khi làm tròn** `observed_pct = round(observed, 6)` và `status_pct = round(pct, 1)`.
  - Tie-break `(r["date"], float(r["valid_km2"]), r["track"])` đảm bảo tính tất định khi có hai quan trắc cùng ngày.
- **`src/skyradar_nisar/figures.py` (`fig3`)**:
  - Đã đồng bộ điều kiện lọc `float(r["valid_km2"]) >= max(5, 0.5 * float(p["area_km2"]))` và đọc diện tích từ `communes_aoi.geojson`.
- **`water-pulse-be/tests/test_coverage_selection.py`**:
  - Bao phủ đầy đủ các ca biên: sliver mới hơn trên cùng track (`047D`, `083A`), sát ngưỡng trước làm tròn (`49.9999` vs `50`, `36.73 / 73.93`), và tính tất định cùng ngày.

#### 2. Xử lý thiếu diện tích hoặc dữ liệu rỗng (`empty / missing area`)
- **`src/skyradar_nisar/sowing.py` (`assess_communes`, `main`)**:
  - `area = float(areas.get(oid) or 0)` kết hợp `area = area if math.isfinite(area) and area > 0 else None` chặn toàn bộ trường hợp `area_km2` bị thiếu (`None`), bằng `0`, âm hoặc không hữu hạn. Khi `area is None`, `eligible` rỗng, xã rơi vào `status = "partial"` và `observed_pct = None`, không bao giờ bị phân loại nhầm thành xã cạn nước (`ready`).
  - Trong `main()`, kiểm tra `if not table: raise ValueError(...)` ngăn việc ghi đè file CSV rỗng hoặc lỗi `IndexError` tại `table[0]` khi không có quan trắc nào đạt `>= 5 km2`.
- **`water-pulse-be/app/frontend.py` (`commune_collection`)**:
  - `observed = 100 * last["valid_km2"] / area if last and area and area > 0 else None` an toàn trước `area` thiếu hoặc `<= 0`.

#### 3. Chặn nhánh lọt lưới `no_flood` (`no_flood bypass`)
- **`water-pulse-be/app/frontend.py` (`commune_collection`)**:
  - Cờ độ phủ được kiểm tra chặt: `sufficient = bool(sowing and sowing["status"] != "partial" and observed is not None and observed >= 50)`.
  - Khi `not sufficient`, `status` bị ép về `"uncertain"`.
  - Nhánh `if sufficient and peak_pct is not None and peak_pct < 5: status = "no_flood"` bắt buộc `sufficient == True`, triệt tiêu hoàn toàn khả năng một xã thiếu độ phủ (`partial` hoặc không có trong `sowing_check.csv`) bị gán nhãn `"no_flood"`.

#### 4. Đường dẫn dữ liệu đầu ra và cơ chế fallback (`output data & fallback`)
- **`src/skyradar_nisar/sowing.py` (`main`) & `src/skyradar_nisar/figures.py` (`fig2`, `fig3`)**:
  - Đọc dữ liệu ưu tiên từ `C.PROCESSED` và tự động fallback sang `C.WEB / "stats"` khi chạy độc lập không có thư mục `processed`.
  - `sowing.py` ghi đồng thời kết quả ra `{stats / "sowing_check.csv", C.WEB / "stats/sowing_check.csv"}`, đảm bảo `data/web/stats/sowing_check.csv` luôn được cập nhật.
- **Lưu ý nhỏ (không chặn PASS - `water-pulse-be/app/data.py`)**:
  - `DATA_DIR` ưu tiên `_HERE / "data"` (`water-pulse-be/data`) trước `_HERE.parent / "data" / "web"` nếu `water-pulse-be/data/manifest.json` tồn tại. Nếu đóng gói bản deploy dùng `water-pulse-be/data`, cần đảm bảo chạy `scripts/sync_data.sh` sau khi chạy `sowing.py` để đồng bộ `sowing_check.csv` từ `data/web/stats`.

#### 5. API Enum và thống kê số lượng (`API enum / counts`)
- **`water-pulse-be/app/main.py` (`sowing_check`)**:
  - Đã thêm `"partial"` vào `Literal["ready", "draining", "still_wet", "partial"]`.
  - Giữ `counts_all` tính riêng cho 3 nhóm đủ điều kiện (`ready: 43`, `draining: 39`, `still_wet: 33` — tổng 115 xã) và tách bạch `partial_count: 16`.
- **`water-pulse-be/tests/test_frontend.py` & `test_api.py`**:
  - Đối chiếu khớp 140 xã: 115 xã `coverage_sufficient=True` (`43/39/33`), 16 xã `partial` (trong đó Xã Sơn Kiên `15416586` có `observed_pct ~ 19.64%`, `status="uncertain"`, `coverage_sufficient=False`), và 9 xã không có quan trắc `>= 5 km2` cũng về `status="uncertain"`.
  - Phần `choropleth_composite` giữ nguyên theo đúng định hướng chỉ làm bằng chứng quan trắc playback, không dùng để đánh giá toàn xã.
