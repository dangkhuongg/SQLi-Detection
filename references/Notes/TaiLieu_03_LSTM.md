# LSTM
**Tác giả / Năm**
- Yuqi Chen, Guangjun, Liang Qun Wang
- Năm: 2025

**Nguồn**
- TechScience

**Mục đích / Nội dung chính**
- Nghiên cứu và so sánh các mô hình Deep Learning gồm CNN, CNN-RNN và CNN-LSTM trong việc phát hiện SQL Injection và XSS.

**Dataset**
- Dữ liệu gồm ba nhóm: Normal, SQL Injection và XSS.
- Normal:
  - Training: 24.000
  - Validation: 10.000
  - Test: 4.000
- SQL Injection:
  - Training: 25.000
  - Validation: 10.000
  - Test: 4.000
- XSS:
  - Training: 25.000
  - Validation: 10.000
  - Test: 4.000
- Tổng cộng: 116.000 mẫu.

**Phương pháp**
Raw Samples
↓
Data Cleansing
↓
Sample Classification & Labeling
↓
Data Set
↓
Segmentation Processing
↓
Training Data Set
↓
Word Vector Training
↓
CNN
↓
CNN-LSTM
↓
Model Optimization
↓
Test Data
↓
Evaluation Results

**Kết quả chính**
| Model    |    Accuracy |     Recall |         F1 |
| -------- | ----------: | ---------: | ---------: |
| CNN      |      97.38% |     97.75% |     97.89% |
| CNN-RNN  |     95.802% |     95.94% |     95.50% |
| CNN-LSTM | **98.352%** | **98.04%** | **98.86%** |
- CNN-LSTM đạt kết quả cao nhất trong ba mô hình theo các chỉ số được báo cáo.

**Điều học được / áp dụng được cho đồ án**
- Cung cấp nền tảng để hiểu cách sử dụng LSTM trong bài toán
  phát hiện SQL Injection.

- Cho thấy dữ liệu SQL có thể được tiền xử lý, phân đoạn và
  chuyển thành vector trước khi đưa vào mô hình Deep Learning.

- Cho thấy trong kiến trúc CNN-LSTM, CNN có thể được sử dụng
  để trích xuất đặc trưng, sau đó LSTM tiếp tục xử lý các
  đặc trưng theo tính chất tuần tự.

- Giúp hiểu pipeline từ dữ liệu SQL thô → preprocessing →
  segmentation → word vector → CNN → LSTM → classification.

- Là cơ sở tham khảo cho Tầng 2 LSTM của đồ án, trong đó
  mô hình sẽ học trực tiếp từ biểu diễn chuỗi token/ký tự
  theo kiến trúc đã được GVHD chốt.

**Hạn chế**
- Paper tập trung vào kiến trúc CNN-LSTM, trong khi Tầng 2
  của đồ án sử dụng LSTM làm baseline độc lập.
- Paper chưa phải là cơ sở trực tiếp cho Tầng 3 LSTM + Attention;
  cơ chế Attention sẽ được khảo sát ở Tài liệu 4.
- Phạm vi nghiên cứu của paper bao gồm cả SQL Injection và XSS,
  trong khi đồ án tập trung vào phát hiện SQL Injection.