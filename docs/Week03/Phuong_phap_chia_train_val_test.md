# Phương pháp chia Train/Validation/Test — Tuần 3

## 1. Nguyên tắc chung

`test.csv` (6.181 dòng, cố định từ Tuần 2, `random_state=42`) giữ nguyên vai trò tập đánh giá cuối cùng, dùng chung cho cả 3 tầng, không bị động đến trong suốt quá trình thiết kế và huấn luyện.

`train.csv` (24.724 dòng) được chia tiếp thành `train_split`/`val_split` để phục vụ theo dõi overfitting khi huấn luyện Tầng 2, 3.

## 2. Kết quả chia thực tế

Chia theo tỷ lệ **80/20**, có `stratify` theo nhãn, `random_state=42`:

| Tập         | Số dòng | Tỷ lệ lớp 0 | Tỷ lệ lớp 1 |
|-------------|---------|-------------|-------------|
| train_split | 19.779  | 63,18%      | 36,82%      |
| val_split   | 4.945   | 63,20%      | 36,80%      |

Chênh lệch tỷ lệ nhãn giữa hai tập chỉ ~0,012%, xác nhận `stratify` hoạt động đúng, tương tự mức độ đồng nhất đã đạt được khi chia `train.csv`/`test.csv` ở Tuần 2.

**Vị trí lưu:** `datasets/processed/train_split.csv`, `datasets/processed/val_split.csv` — thư mục con mới, bổ sung vào `datasets/` đã có sẵn từ khung project ban đầu.

## 3. Phương pháp áp dụng khác nhau giữa các tầng

**Tầng 1 (Random Forest/SVM):** dùng cross-validation `k=5` trên toàn bộ `train.csv` (không dùng `train_split`/`val_split` riêng). Lý do: đây là baseline không huấn luyện theo epoch, không cần theo dõi learning curve — cross-validation cho ước lượng hiệu năng ổn định hơn khi dùng toàn bộ dữ liệu train thay vì trích một phần ra làm validation cố định.

**Tầng 2, 3 (LSTM, LSTM+Attention):** dùng `train_split` để huấn luyện, `val_split` cố định để theo dõi `val_loss` qua từng epoch, làm cơ sở cho `EarlyStopping(patience=5)` đã chốt ở Ngày 4-5.

**Lưu ý khi trình bày ở buổi bảo vệ đồ án:** việc dùng hai phương pháp khác nhau (cross-validation cho Tầng 1, train/val cố định cho Tầng 2-3) là hợp lý về mặt kỹ thuật — xuất phát từ bản chất huấn luyện khác nhau giữa mô hình học máy cổ điển (không có khái niệm epoch) và mô hình học sâu (huấn luyện lặp qua nhiều epoch, cần tín hiệu dừng sớm). Đây không phải sự thiếu nhất quán, mà là lựa chọn phù hợp với đặc thù từng loại mô hình — cần giải thích rõ điểm này nếu hội đồng đặt câu hỏi.
