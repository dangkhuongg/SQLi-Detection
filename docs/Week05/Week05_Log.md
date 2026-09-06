# Nhật ký nghiên cứu — Tuần 5

**Đề tài:** Hệ thống tự động phát hiện truy vấn SQL bất thường (SQL Injection) bằng học máy
**Giai đoạn:** Thi công Tầng 2 — LSTM baseline
**Notebook:** `notebooks/04_tier2_lstm_baseline.ipynb`

---

## Ngày 1 — Cài đặt query_to_sequence()

- Viết hàm chuyển câu truy vấn thành sequence số nguyên, tái sử dụng nguyên trạng `artifacts/vocab.json` và `artifacts/max_len.json` từ Tuần 3 (không tính lại vocab/max_len).
- 3 test case: câu ngắn (padding), câu dài (head+tail truncation), ký tự lạ (UNK mapping).
- **Sự cố phát hiện:** test case ban đầu cho head+tail truncation dùng phần đầu/cuối chỉ 100 ký tự, ngắn hơn `HEAD_LEN`/`TAIL_LEN`=125 → assertion tự nhiên trả `False` dù hàm không có lỗi. Đã thiết kế lại test case (150 ký tự mỗi đầu) để kiểm chứng đúng ranh giới cắt. Bài học: cần đảm bảo dữ liệu test case đủ lớn hơn ngưỡng đang kiểm tra, không chỉ đủ để chạy không lỗi.
- Kết quả: cả 3 test case đạt yêu cầu, bao gồm xác nhận không lệch off-by-one tại vị trí nối 124/125.
- Áp dụng lên toàn bộ dữ liệu, lưu 3 ma trận: `train_split_sequences.npy` (19.779, 250), `val_split_sequences.npy` (4.945, 250), `test_sequences.npy` (6.181, 250).

## Ngày 2 — Kiến trúc mô hình

- Cài đặt `Embedding(96,64) → LSTM(64, return_sequences=False) → Dropout(0.2) → Dense(1, sigmoid)` đúng đặc tả Tuần 3.
- **Sự cố phát hiện:** Keras 3 (TF 2.16+) không tự build `Sequential` model chỉ từ khai báo lớp — `model.summary()` lần đầu hiển thị toàn bộ `Output Shape = ?` và `Param# = 0 (unbuilt)`. Khắc phục bằng cách thêm `layers.Input(shape=(250,))` làm lớp đầu tiên.
- Sau khi build đúng: tổng 39.233 tham số, đã đối chiếu khớp bằng công thức tay cho từng lớp (Embedding 6.144, LSTM 33.024, Dense 65).

## Ngày 3 — Thử nghiệm 3 epoch

- Thời gian: 184,1 giây cho 3 epoch → ước tính ~30,7 phút cho 30 epoch, khả thi.
- **Quan sát đáng chú ý:** val_loss giảm mạnh ở epoch 2 (0,2324) rồi thoái lui gần như hoàn toàn ở epoch 3 (0,6177). Đúng loại rủi ro đã lường trước trong kế hoạch Tuần 5.
- Precision cao/ổn định (0,81–0,99), Recall thấp/dao động mạnh (0,12–0,97) → tín hiệu mất cân bằng lớp ảnh hưởng đến lớp thiểu số (SQLi).
- **Quyết định (đã trao đổi và chốt):**
  1. Áp dụng `class_weight='balanced'` cho huấn luyện chính thức.
  2. Không đổi `learning_rate` dù quan sát dao động (thông số đã chốt Tuần 3, cần giữ nguyên cho Tầng 3). Tiến hành huấn luyện đầy đủ luôn, tin tưởng `EarlyStopping(patience=5, restore_best_weights=True)` sẽ tự chọn epoch tốt nhất.

## Ngày 4 — Huấn luyện chính thức

- `class_weight` tính bằng `sklearn.utils.class_weight.compute_class_weight('balanced')`: lớp 0 = 0,7913, lớp 1 = 1,3581. Đã kiểm chứng khớp công thức tay.
- Dừng ở epoch 27 (= epoch tốt nhất 22 + patience 5) — đúng cơ chế EarlyStopping, không có gì bất thường.
- **Đối chiếu với lo ngại ở Ngày 3:** dao động thoái lui không lặp lại nghiêm trọng khi huấn luyện đủ dài. Sau bước nhảy hội tụ ở epoch 3, mô hình ổn định dần, chỉ còn nhiễu nhỏ ở vài epoch (8–9, 14, 16). Kết luận: dao động ở Ngày 3 là nhiễu giai đoạn đầu huấn luyện, không phải vấn đề learning rate hay cấu trúc.
- Kết quả tại epoch 22 (best): train P/R = 0,9990/0,9971 — val P/R = 0,9983/0,9956 — val_loss = 0,0141.
- Thời gian huấn luyện tổng: 28,50 phút.

## Ngày 5 — Đánh giá test.csv

- Đánh giá trên model tại epoch 22 (giữ tự động nhờ `restore_best_weights=True`), trên đúng `test.csv` (6.181 dòng) dùng chung với Tầng 1.
- Kết quả LSTM: Precision 0,9987 — Recall 0,9930 — F1 0,995814 — Confusion Matrix TN=3902, FP=3, FN=16, TP=2260.
- **Kiểm tra nhất quán:** TN+FP=3905 và FN+TP=2276 khớp đúng ở cả 3 mô hình (RF/SVM/LSTM) — xác nhận dùng chung một test.csv, không có sai lệch dữ liệu.
- **So sánh:** F1 của RF (0,995818) và LSTM (0,995814) gần như trùng khớp tuyệt đối (chênh lệch 0,000004) — không đủ ý nghĩa để kết luận mô hình nào vượt trội. SVM thấp hơn rõ rệt (0,993826).
- Đây là kết quả trùng khớp với rủi ro đã lường trước trong kế hoạch Tuần 5 (16 đặc trưng thủ công của Tầng 1 đã nắm bắt tốt tín hiệu phân biệt, deep learning không có nhiều dư địa cải thiện thêm) — phát hiện thực nghiệm hợp lệ, để phân tích sâu ở Tuần 7.
- Ghi nhận riêng: LSTM Precision cao hơn RF (FP=3 so với 5) nhưng Recall thấp hơn (FN=16 so với 14) — cần thảo luận thêm ở Tuần 7 khi đủ dữ liệu 3 tầng, chưa kết luận vội.

## Ngày 6 — Lưu model và báo cáo

- Lưu `models/tier2_lstm.h5` (trọng số epoch 22).
- Lưu `artifacts/tier2_class_weight_decision.json` — ghi rõ giá trị/phương pháp để tái lập chính xác ở Tầng 3 (Tuần 6).
- Lưu `artifacts/tier2_training_history.json` — toàn bộ lịch sử loss/precision/recall qua epoch.
- Lưu `docs/Week05/model_comparison_tier1_tier2.csv` — bảng so sánh 3 mô hình.
- Hoàn thành `docs/Week05/BaoCao_Tuan05.docx`.

## Ngày 7 — Review

- Cập nhật nhật ký này.
- Checklist cuối tuần: xem `docs/Week05/BaoCao_Tuan05.docx`, mục 7.
- Commit lên GitHub.

---

## Vấn đề kỹ thuật đã gặp và bài học (tổng hợp)

1. **Test case không đủ chặt** (Ngày 1): thiết kế test case cần đảm bảo dữ liệu thử vượt rõ ràng ngưỡng đang kiểm tra, không chỉ "chạy không lỗi".
2. **Keras 3 unbuilt model** (Ngày 2): `Sequential` cần lớp `Input` tường minh để build ngay, nếu không `model.summary()` không phản ánh được kiến trúc thật.
3. **Dao động huấn luyện giai đoạn đầu** (Ngày 3–4): thử nghiệm ngắn (2-3 epoch) có thể cho tín hiệu gây hiểu lầm về độ ổn định; cần đối chiếu lại với kết quả huấn luyện đầy đủ trước khi kết luận có vấn đề về learning rate hay không.

## Chuẩn bị cho Tuần 6 (Tầng 3 — LSTM + Attention)

- Giữ nguyên tuyệt đối: `learning_rate=0.001`, `batch_size=64`, `epochs` tối đa=30, `EarlyStopping(patience=5)`.
- Tái sử dụng đúng quyết định + giá trị `class_weight` đã chốt tuần này (đọc từ `artifacts/tier2_class_weight_decision.json`).
- Thay đổi kiến trúc hợp lệ duy nhất: `LSTM(return_sequences=True)` để giữ toàn bộ hidden state cho lớp Attention.
- Chuẩn bị sẵn hạ tầng trích xuất/lưu trọng số Attention ngay khi cài đặt (không để dồn đến Tuần 7).
- Tâm thế: khả năng Attention cải thiện rất ít hoặc không cải thiện so với Tầng 2 là kịch bản hợp lý cần chuẩn bị, không phải dấu hiệu lỗi.
