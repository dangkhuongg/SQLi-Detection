## Survey

**Tác giả / Năm**
Maha Alghawazi, Daniyal Alghazzawi, Suaad Alarifi
Năm: 2022

**Nguồn:** 
Journal of Cybersecurity and Privacy

**DOI** 
10.3390/jcp2040039

**Phương pháp**
- Survey phân loại các phương pháp phát hiện SQLInjection thành các nhóm:
Học có giám sát: khoảng 89%.
Học không giám sát: khoảng 4%.
Học hỗn hợp: khoảng 3%.
Các phương pháp khác: khoảng 4%.

- Các thuật toán Machine Learning được đề cập gồm:
SVM
Decision Tree
Random Forest
Naive Bayes
k-NN
Logistic Regression
Boosting và Ensemble
Reinforcement Learning

- Các phương pháp Deep Learning được đề cập gồm:
LSTM
CNN
Bi-LSTM
MLP

**Dataset**
- HTTP/HTTPS requests, Web Access Logs, Mã nguồn ứng dụng, Raw SQL commands, NoSQL

**Kết quả chính**
- Survey cho thấy phần lớn các nghiên cứu sử dụnghọc có giám sát (khoảng 89%), trong khi học không giám sát vàhọc hỗn hợp chiếm tỷ lệ nhỏ hơn.
- Các metrics thường được sử dụng để đánh giá gồm:
    Accuracy
    Recall
    Precision
    F1-Score
TP, TN, FP, FN
Confusion Matrix
- Survey đồng thời nhấn mạnh các vấn đề liên quan đến chất lượngdataset, sự mất cân bằng dữ liệu và nguy cơ overfitting trong cácnghiên cứu phát hiện SQLi.

**Điều học được / áp dụng được cho đồ án**
- Cung cấp cái nhìn tổng quan về các hướng tiếp cận MachineLearning và Deep Learning trong phát hiện SQL Injection.
- Giúp định vị ba hướng mô hình của đồ án:

Tầng 1 --- Random Forest / SVM: đại diện cho hướngMachine Learning cổ điển.

Tầng 2 --- LSTM: đại diện cho hướng Deep Learning xử lýdữ liệu dạng chuỗi.

Tầng 3 --- LSTM + Attention: hướng cải tiến dựa trên cơchế Attention.

- Nhấn mạnh tầm quan trọng của việc xây dựng một dataset chấtlượng cao, đặc biệt trong bối cảnh dữ liệu SQLi có thể thiếuhụt, mất cân bằng và gây nguy cơ overfitting.
- Cung cấp cơ sở để lựa chọn các evaluation metrics mang tínhhọc thuật như Precision, Recall, F1-Score và Confusion Matrix.
- Giúp nhìn nhận bài toán SQL Injection dưới góc độ phân loại bằngML/DL và hiểu rằng cách biểu diễn dữ liệu đầu vào có vai tròquan trọng đối với mô hình.

**Hạn chế**
Phụ thuộc quá mức vào học có giám sát, dẫn đến gánh nặng gánnhãn dữ liệu.

Khan hiếm và khó tìm được các bộ dữ liệu SQLi mẫu có chất lượngcao.

Nhiều dataset phụ thuộc vào nền tảng học thuật và mã nguồn mở.

Thiếu hụt các nghiên cứu về tự sinh dữ liệu mới (DatasetGeneration) bằng trí tuệ nhân tạo.

Thiếu nghiên cứu về Adversarial Attacks để kiểm thử độ bềnvững của hệ thống phát hiện.

Mất cân bằng dữ liệu và nguy cơ overfitting do thiếu các mẫutấn công đa dạng.

Xu hướng tập trung đề xuất mô hình mới thay vì đánh giá thực tếvà sâu hơn các mô hình đã tồn tại.