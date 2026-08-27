# Mô tả kiến trúc tổng thể hệ thống

Sơ đồ tham chiếu: `docs/Week03/So_do_kien_truc_he_thong.svg`

## 1. Luồng dữ liệu tổng thể

Hệ thống nhận đầu vào là một câu truy vấn SQL (`query: str`), có thể đến từ hai nguồn:
- **Khi huấn luyện:** từng dòng trong `train.csv` / `test.csv` (đã cố định ở Tuần 2, stratified split, `random_state=42`).
- **Khi suy luận (Tuần 8):** một câu truy vấn do người dùng nhập vào ứng dụng middleware.

Từ input, hệ thống rẽ thành hai pipeline tiền xử lý chạy song song và độc lập hoàn toàn với nhau:

- **Pipeline 1 — Feature Engineering:** phục vụ Tầng 1 (Random Forest/SVM).
- **Pipeline 2 — Tokenization + Embedding:** phục vụ Tầng 2 và Tầng 3 (LSTM, LSTM+Attention).

Kết quả dự đoán từ cả ba tầng được tổng hợp ở khối so sánh (Precision/Recall/F1/Confusion Matrix, thực hiện ở Tuần 7), và ba mô hình đã huấn luyện được tái sử dụng nguyên trạng trong ứng dụng middleware (Tuần 8).

## 2. Input/Output từng module

Pipeline 1 (`extract_features`): Trích xuất chuỗi truy vấn thô `(query: str)` thành vector đặc trưng thô cố định 15 chiều `(15,)`.
Pipeline 1 (`scaler.transform`): Chuẩn hóa vector đặc trưng thô `(15,)` về cùng thang đo số học.
Pipeline 2 (`tokenizer`): Mã hóa `query: str` thành danh sách token số nguyên có độ dài cố định `(max_len,)` sau khi xử lý cắt/đệm (pad/truncate).
Tầng 1 (`RF/SVM`): Nhận vector 15 chiều đã chuẩn hóa -> Xuất nhãn phân loại nhị phân `(0/1)` kèm xác suất (`proba`).
Tầng 2 (`LSTM`): Nhận chuỗi số nguyên `(max_len,)` -> Xuất xác suất dự báo qua hàm Sigmoid (proba).
Tầng 3 (`LSTM + Attention`): Nhận chuỗi `(max_len,)` -> Xuất xác suất (`proba`) kèm vector trọng số chú ý (`max_len,`) phục vụ giải thích mô hình.
Khối so sánh: Nhận bộ dữ liệu đánh giá (`y_true, y_pred, y_proba`) của cả 3 tầng trên `test.csv` -> Xuất bảng chỉ số đánh giá (metrics) và ma trận nhầm lẫn (Confusion Matrix).
Khối Middleware: Nhận 1 query đơn lẻ từ người dùng -> Thực thi và trả về kết quả dự đoán song song từ cả 3 tầng mô hình.

## 3. Định dạng lưu mô hình

- **Tầng 1:** `.pkl` qua `joblib` — chuẩn phổ biến cho các object scikit-learn (RandomForest, SVC).
- **Tầng 2, 3:** `.h5` — định dạng lưu chuẩn của Keras, gộp kiến trúc + trọng số trong 1 file, đơn giản hóa việc load lại ở middleware.
- Các đối tượng tiền xử lý (`scaler`, `vocab`, `max_len`) được lưu tách riêng khỏi mô hình, trong thư mục `artifacts/`, vì middleware cần load chúng **trước** bước đưa dữ liệu vào mô hình.

## 4. Quy ước thư mục (áp dụng xuyên suốt Tuần 4-8)

models/
├── tier1_rf.pkl
├── tier1_svm.pkl
├── tier2_lstm.h5
└── tier3_lstm_attention.h5

artifacts/
├── tier1_scaler.pkl         # fit chỉ trên train, dùng .transform() cho test/inference
├── feature_order.json       # thứ tự 15 cột cố định
├── vocab.json               # char -> index, xây chỉ trên train
└── max_len.json

results/
├── tier1_metrics.json
├── tier2_metrics.json
├── tier3_metrics.json
└── comparison_table.csv

## 5. Ranh giới giữa hai pipeline

Pipeline 1 và Pipeline 2 **không chia sẻ bất kỳ logic tiền xử lý nào** — Pipeline 1 không dùng tokenizer, Pipeline 2 không dùng vector đặc trưng thủ công. Tuy nhiên cả hai **cùng đọc từ một nguồn `train.csv`/`test.csv` gốc** đã cố định ở Tuần 2, và cùng tuân thủ nguyên tắc: mọi thành phần fit trên dữ liệu (scaler, vocabulary) chỉ được fit trên `train.csv`, không bao giờ dùng `test.csv` để tránh rò rỉ thông tin (data leakage).

Đây là chủ đích thiết kế nhằm đảm bảo so sánh công bằng giữa hướng tiếp cận học máy cổ điển và học sâu trên cùng một bài toán, cùng một tập dữ liệu — cần nêu rõ điểm này khi bảo vệ đồ án để tránh bị hiểu nhầm là thiếu nhất quán giữa hai pipeline.
