# Đặc tả Pipeline 1 — Feature Engineering — Tuần 3, Ngày 2-3

Sơ đồ tham chiếu: `docs/Week03/So_do_luong_pipeline1.svg`

## 1. Điều chỉnh so với budget đặc trưng ban đầu (Tuần 2)

Báo cáo Tuần 2 (mục 3) ghi tổng số đặc trưng đề xuất là 15, nhưng danh sách liệt kê chi tiết trong cùng mục chỉ có 14 tên cụ thể (4 cấu trúc + 6 ký tự đặc biệt + 4 từ khóa). Sau khi rà soát lại, quyết định chính thức cho Tuần 3:

- **Giữ lại cả `n_semicolon` và `has_drop`** (2 đặc trưng mà báo cáo Tuần 2, mục 3.4 đề xuất "cân nhắc loại bỏ") thay vì loại bỏ trước khi có bằng chứng thực nghiệm.
- **Tổng số đặc trưng chính thức cho Tầng 1: 16** (không phải 15 như budget ban đầu) — đây là một thay đổi có chủ đích, ghi nhận lại để tránh gây hiểu nhầm khi đối chiếu ngược với báo cáo Tuần 2.
- **Kế hoạch xử lý:** sau khi huấn luyện Random Forest ở Tuần 4, xem xét feature importance của `n_semicolon`, `has_drop`, `keyword_repeat_count` và các `has_*` — nếu các đặc trưng này có importance thấp do trùng lặp thông tin lẫn nhau, cân nhắc gộp hoặc loại bớt. Nếu dùng SVM, bổ sung kiểm tra ma trận tương quan (correlation matrix) giữa các đặc trưng trước khi huấn luyện để phát hiện đặc trưng dư thừa. Quyết định cuối cùng để dữ liệu quyết định ở Tuần 4, không loại bỏ theo cảm tính ở bước này.

## 2. Danh sách 16 đặc trưng — kiểu dữ liệu và công thức

| Index | Tên | Nhóm | Kiểu | Công thức / định nghĩa | Căn cứ EDA (Tuần 2) |
|---|---|---|---|---|---|
| 0 | `length` | Cấu trúc | int | Số ký tự của câu truy vấn | chênh lệch ~3 lần giữa 2 lớp |
| 1 | `uppercase_ratio` | Cấu trúc | float [0,1] | Số ký tự in hoa / `length` | chênh lệch tuyệt đối lớn (23,72% vs 0,39%), ngược hướng giả định |
| 2 | `n_whitespace` | Cấu trúc | int | Số ký tự khoảng trắng | chênh lệch ~6,7 lần |
| 3 | `n_digit` | Cấu trúc | int | Số ký tự chữ số (0-9) | chênh lệch ~10,7 lần |
| 4 | `n_quote` | Ký tự đặc biệt | int | Số dấu `'` | chênh lệch ~1,7 lần |
| 5 | `n_equal` | Ký tự đặc biệt | int | Số dấu `=` | chênh lệch ~5,8 lần |
| 6 | `n_comma` | Ký tự đặc biệt | int | Số dấu `,` | chênh lệch ~5,4 lần |
| 7 | `n_paren` | Ký tự đặc biệt | int | Tổng số `(` và `)` | chênh lệch ~12-14 lần |
| 8 | `n_percent` | Ký tự đặc biệt | int | Số dấu `%` | chênh lệch ~6,55 lần |
| 9 | `n_comment_markers` | Ký tự đặc biệt | int | Tổng số `--`, `#`, `/* */` | chênh lệch ~820 lần — mạnh nhất toàn EDA |
| 10 | `keyword_repeat_count` | Từ khóa | int | Tổng số lần các từ khóa nguy hiểm lặp lại trong câu | tổng hợp, chưa có số liệu riêng ở Tuần 2 |
| 11 | `n_semicolon` | Bổ trợ | int | Số dấu `;` | chênh lệch ngược hướng giả định (thấp hơn ở lớp SQLi) — giữ lại để Tuần 4 đánh giá lại |
| 12 | `has_union` | Từ khóa | binary (0/1) | Có chứa `UNION` (không phân biệt hoa/thường) | chênh lệch ~7,4 lần |
| 13 | `has_or` | Từ khóa | binary (0/1) | Có chứa `OR` như một từ riêng | chênh lệch ~1,5 lần |
| 14 | `has_select_from` | Từ khóa | binary (0/1) | Có chứa cấu trúc `SELECT...FROM` | thay thế đếm `SELECT` đơn lẻ để giảm nhiễu |
| 15 | `has_drop` | Bổ trợ | binary (0/1) | Có chứa `DROP` | tần suất quá thấp ở cả 2 lớp (<0,4%) — giữ lại để Tuần 4 đánh giá lại |

**Thứ tự cột 0-15 ở trên là thứ tự cố định**, dùng xuyên suốt từ Tuần 4 đến Tuần 8, không thay đổi sau khi bắt đầu code.

## 3. Phương án xử lý outlier và scaling

**Nguyên tắc phân nhóm:** 12 cột đầu (index 0-11) là đặc trưng liên tục (đếm hoặc tỷ lệ) → cần xử lý outlier + scale. 4 cột cuối (index 12-15) là đặc trưng nhị phân → giữ nguyên, không xử lý.

**Với 12 cột liên tục:**
1. **Clip percentile 99**, tính **riêng cho từng cột** (không dùng chung 1 ngưỡng cho cả 12 cột) — áp dụng đồng nhất cho toàn bộ nhóm, không chỉ riêng `length`, vì nhiều đặc trưng ký tự đặc biệt (đặc biệt `n_comment_markers`, `n_paren`, `n_quote`, `n_equal`) có phân bố lệch/sparse tương tự (phần lớn giá trị bằng 0, số ít giá trị dương lớn ở lớp SQLi).
2. **StandardScaler**, fit sau khi đã clip.

Lý do chọn clip thay vì `RobustScaler`: clip loại bỏ hoàn toàn khả năng outlier chi phối việc scale (đổi lấy việc mất thông tin độ lớn thực sự của phần đuôi phân phối), còn `RobustScaler` tuy ít nhạy hơn `StandardScaler` với outlier nhưng vẫn giữ outlier trong dữ liệu, có thể ảnh hưởng đến cây quyết định của Random Forest ở mức độ nhất định.

**Ràng buộc bắt buộc để tránh data leakage:**
- Ngưỡng clip percentile 99 (12 giá trị, mỗi cột một ngưỡng) tính **chỉ trên `train.csv`**.
- `StandardScaler` fit **chỉ trên `train.csv`** (sau khi đã clip).
- Cả hai đều lưu lại thành artifact và tái sử dụng nguyên trạng cho `test.csv` và khi suy luận (Tuần 8) — không tính lại từ dữ liệu mới.

**Artifact cần lưu (bổ sung vào `artifacts/` đã định nghĩa ở Ngày 1-2):**
- `artifacts/clip_thresholds.json` — 12 ngưỡng percentile 99, theo đúng thứ tự cột 0-11.
- `artifacts/tier1_scaler.pkl` — đã có từ Ngày 1-2, giữ nguyên vai trò.
- `artifacts/feature_order.json` — đã có từ Ngày 1-2, cập nhật thành 16 tên cột theo đúng thứ tự ở mục 2.

## 4. Sơ đồ luồng pipeline

```
Query (str)
  → extract_features(query) → vector (16,) raw, thứ tự cột cố định
  → tách theo index:
      vector[0:12]  (12 cột liên tục)
      vector[12:16] (4 cột nhị phân)
  → nhánh liên tục:
      clip(percentile 99, theo từng cột)   [ngưỡng từ train]
      → StandardScaler.transform()          [scaler từ train]
  → nhánh nhị phân: giữ nguyên, không xử lý
  → ghép lại theo đúng thứ tự gốc → vector (16,) hoàn chỉnh
  → Random Forest / SVM (Tuần 4)
```

Chi tiết trực quan: xem `docs/Week03/So_do_luong_pipeline1.svg`.
