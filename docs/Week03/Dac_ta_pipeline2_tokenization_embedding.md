# Đặc tả Pipeline 2 — Tokenization + Embedding — Tuần 3, Ngày 3-4

Sơ đồ tham chiếu: `docs/Week03/So_do_luong_pipeline2.svg`

## 1. Quyết định: character-level tokenization

Giữ nguyên khuyến nghị ban đầu: tokenize theo từng ký tự, không tách theo từ. Lý do: payload SQLi thường dùng ký tự đặc biệt dày đặc (`--`, `#`, `,`, `(`, `)`...) không có ranh giới "từ" rõ ràng — báo cáo Tuần 2 (mục 2.4) đã xác nhận nhóm ký tự đặc biệt là nhóm phân biệt mạnh nhất trong toàn bộ EDA (`n_comment_markers` chênh lệch ~820 lần), nên cần giữ nguyên thông tin ở cấp ký tự thay vì làm mất qua bước tách từ.

## 2. Vocabulary

**Số liệu thực tế tính trên `train.csv`** (24.724 dòng):
- Tổng số ký tự unique xuất hiện: 105
- 11 ký tự có tần suất ≤5 lần: `\x18` (1), `â` (2), `\x80` (2), `\x98` (2), `트` (2), `리` (2), `거` (2), `'` (3), `'` (3), `ü` (4), `^` (5) — chủ yếu là ký tự điều khiển/encoding lỗi và ký tự tiếng Hàn, xác định là nhiễu dữ liệu.
- 94 ký tự còn lại có tần suất ≥21 lần — có khoảng trống tự nhiên giữa tần suất 5 và 21, nên ngưỡng lọc chọn ở bất kỳ giá trị nào trong khoảng 6-20 đều cho cùng một kết quả.

**Ngưỡng lọc chính thức: giữ ký tự có tần suất ≥ 10 lần trong train.csv.** Ký tự dưới ngưỡng và mọi ký tự chưa từng xuất hiện trong train (gặp lúc test/inference) đều gộp vào token `<UNK>`.

**Vocab size chính thức: 96**
- Index 0: `<PAD>` (đệm câu ngắn)
- Index 1: `<UNK>` (ký tự hiếm/không xác định)
- Index 2-95: 94 ký tự thật, thứ tự không ảnh hưởng đến mô hình

Vocabulary được xây **chỉ trên `train.csv`**, không dùng `test.csv`, để tránh rò rỉ thông tin.

## 3. max_len

**max_len = 250**, chọn dựa trên phân bố độ dài thực tế trên toàn bộ `train.csv` (không tách theo nhãn):

| Percentile | Giá trị |
|------------|---------|
| P90        |   154   |
| P95        |   221   |
| P99        |   377   |
| Max        |  5.370  |
| Mean       |  68,92  |

250 nằm giữa P95 và P99 — phủ được nhiều hơn 95% nhưng ít hơn 99% số câu trong train mà không cần cắt. Có 1.082 dòng (~4,4% train) dài hơn 250 ký tự, trong đó 1.046/1.082 (96,7%) là nhãn SQLi — nghĩa là phần dữ liệu bị ảnh hưởng bởi việc cắt bớt tập trung chủ yếu ở lớp cần phát hiện, không phải nhiễu ngẫu nhiên.

## 4. Chiến lược truncating: head+tail

**Vấn đề phát hiện:** phân tích vị trí từ khóa nguy hiểm trong 1.082 dòng dài hơn 250 ký tự cho thấy mâu thuẫn giữa các kỹ thuật tấn công:

| Nhóm kỹ thuật             | Vị trí trung bình (0=đầu, 1=cuối) | Số dòng |
|---------------------------|-----------------------------------|---------|
| `OR`-based                | 0,06 (gần đầu)                    | 464     |
| `UNION`-based             | 0,71 (nghiêng cuối)               | 86      |
| Comment-based (`--`, `#`) | 0,99 (gần như luôn ở cuối)        | 293     |

Không có phương án cắt một phía (chỉ đầu hoặc chỉ cuối) nào bảo toàn được cả hai nhóm vị trí đối lập. Do đó chọn **head+tail truncation**: với câu dài hơn 250 ký tự, giữ lại **125 ký tự đầu + 125 ký tự cuối**, bỏ đoạn giữa. Cách chia đều 125/125 được chọn vì không có bằng chứng định lượng cho thấy cần ưu tiên phía nào hơn.

**Đánh đổi đã chấp nhận:** phức tạp hơn khi code (cần viết hàm cắt tùy chỉnh, không dùng thẳng `keras.preprocessing.sequence.pad_sequences` cho phần truncate — chỉ dùng được cho phần pad).

## 5. Padding

Khi `length(query) ≤ 250`: giữ nguyên nội dung, **post-padding** bằng `<PAD>`=0 vào cuối cho đủ 250. Đây là mặc định của `keras.preprocessing.sequence.pad_sequences`, không cần viết hàm riêng cho trường hợp này. Không có mất thông tin ở bước này (chỉ điền thêm token rỗng), khác với quyết định truncating ở mục 4.

## 6. Embedding

`embedding_dim = 64` — điểm khởi đầu, tinh chỉnh thực nghiệm ở Tuần 5 nếu cần. `Embedding layer`: `input_dim=96` (vocab_size), `output_dim=64`.

## 7. Sơ đồ luồng pipeline

```
Query (str)
  → tokenize theo ký tự → List[char]
  → index hóa theo vocabulary (96 token, <PAD>=0, <UNK>=1)
  → nếu length ≤ 250:
        post-padding bằng <PAD> → sequence (250,)
    nếu length > 250:
        head+tail truncation (125 đầu + 125 cuối) → sequence (250,)
  → Embedding layer (input_dim=96, output_dim=64)
  → Tầng 2 (LSTM) / Tầng 3 (LSTM+Attention)
```

Chi tiết trực quan: xem `docs/Week03/So_do_luong_pipeline2.svg`.

## 8. Artifact cần lưu

Bổ sung vào `artifacts/` (đã tạo ở Ngày 1-2):
- `artifacts/vocab.json` — mapping ký tự → index (96 token), xây chỉ trên train.
- `artifacts/max_len.json` — giá trị 250, cùng ghi chú chiến lược truncating (head+tail, 125/125) để không bị quên khi code Tuần 5.
