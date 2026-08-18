# RF-SVM

- **Tác giả / Năm:** Edwin Peralta-GarciaORCID,Juan Quevedo-MonsalbeORCID,Victor Tuesta-Monteza andJuan Arcila-Diaz, năm 2024

- **Nguồn:** Informatics (MDPI)

- **DOI:**
  10.3390/informatics11020015

- **Mục đích / Nội dung chính của tài liệu:**
  - So sánh các thuật toán ML cổ điển để phát hiện SQLi trong phát hiện SQL Injection trên hệ thống web microservices sử dụng bộ dữ liệu công khai.
  - Câu hỏi nghiên cứu được đặt ra là: thuật toán ML nào hiệu quả nhất để phát hiện SQLi trong các microservices web

- **Phương pháp:**
  - Sử dụng bộ dữ liệu công khai gồm 22.764 câu truy vấn SQL (11.382 Normal và 11.382 SQL Injection).
  - Chia dữ liệu:
    + 80% Train
    + 20% Test.
  - Tiền xử lý dữ liệu và chuyển đổi câu truy vấn SQL thành vector đặc trưng bằng TF-IDF.
  - Huấn luyện và đánh giá: Decision Tree, SVM và Random Forest.
  - Đánh giá bằng: Accuracy, Precision, Recall, F1-score, Confusion Matrix.

- **Kết quả chính:**
  - Random Forest đạt hiệu quả cao nhất trong ba mô hình được đánh giá.

  - Random Forest:
    Accuracy 99%
    Precision 97%
    Recall 98%
    F1-score 99%

  - SVM:
    Accuracy 98%
    Precision 97%
    Recall 98%
    F1-score 98%

  - Paper cũng mô tả nguyên lý hoạt động của SVM và Random Forest để giải thích kết quả.

- **Điều học được / áp dụng được cho đồ án:**
 - Cung cấp cơ sở lý thuyết cho Tầng 1 của đồ án (Random Forest và SVM).

 - Minh họa quy trình phát hiện SQL Injection bằng Machine Learning:
  SQL Query → Vector hóa bằng TF-IDF → Huấn luyện RF/SVM → Đánh giá bằng Precision, Recall, F1 và Confusion Matrix.

  - Chứng minh Random Forest và SVM đều đạt hiệu quả cao trong phát hiện SQL Injection trên bộ dữ liệu công khai.
  - Cho thấy việc biểu diễn truy vấn SQL thành đặc trưng đầu vào là bước quan trọng trước khi huấn luyện mô hình.
  - Có thể tham khảo cách đánh giá mô hình (Accuracy, Precision, Recall, F1 và Confusion Matrix) để áp dụng cho đồ án.
  - Paper sử dụng TF-IDF để biểu diễn truy vấn SQL trước khi huấn luyện RF/SVM. Trong khi đó, đề tài sẽ sử dụng các đặc trưng thủ công được trích xuất từ câu truy vấn SQL theo kiến trúc đã thống nhất. Tuy cách biểu diễn đầu vào khác nhau, cả hai đều hướng tới việc chuyển đổi truy vấn SQL thành dữ liệu số để mô hình Machine Learning có thể xử lý.
  - Kết quả nghiên cứu cho thấy các mô hình Machine Learning truyền thống vẫn đạt hiệu quả rất cao đối với bài toán phát hiện SQL Injection và là baseline phù hợp trước khi so sánh với các mô hình Deep Learning.

- **Hạn chế của tài liệu (nếu có):**
  - Chỉ đánh giá trên bộ dữ liệu khoảng 22.764 mẫu, nhỏ hơn quy mô dữ liệu dự kiến của đồ án.
  - Chỉ nghiên cứu các mô hình Machine Learning truyền thống, chưa so sánh với các mô hình Deep Learning như LSTM.
  - Sử dụng TF-IDF để biểu diễn dữ liệu, chưa đánh giá các phương pháp đặc trưng khác.