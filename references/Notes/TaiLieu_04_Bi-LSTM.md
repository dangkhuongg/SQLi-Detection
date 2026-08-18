## Bi-LSTM

**Tác giả / Năm**
Bingyao Liu, Jiajing Chen, Rui Wang, Junming Huang, Yuanshuai Luo, Jianjun Wei
2024

**Nguồn**
arxiv.org

**Mục đích / Nội dung chính**
- Paper đề xuất mô hình Deep Learning kết hợp Bi-LSTM và Attention Mechanism để tự động phân loại văn bản tin tức.

**Dataset**
- Dataset sử dụng tập dữ liệu tin tức HuffPost. Paper không nêu rõ tổng số mẫu trong phần thông tin đang khảo sát; dữ liệu được chia 80% training và 20% testing.

**Phương pháp**
  Raw text
   ↓
Word2Vec
   ↓
Word representation
   ↓
Feature matrix
   ↓
Bi-LSTM + Attention

**Kết quả chính**
| Model     | Precision |    Recall |        F1 |
| --------- | --------: | --------: | --------: |
| RNN       |     0.876 |     0.857 |     0.863 |
| CNN       |     0.883 |     0.865 |     0.871 |
| LSTM      |     0.896 |     0.873 |     0.886 |
| BiLSTM    |     0.905 |     0.876 |     0.891 |
| Attention |     0.911 |     0.904 |     0.905 |
| Ours      | **0.923** | **0.991** | **0.939** |

**Điều học được / áp dụng cho Tầng 3**
- Cung cấp cơ sở để hiểu cách kết hợp mô hình LSTM hai chiều với Attention trong bài toán phân loại chuỗi.
- Cho thấy Attention có thể nhận các hidden states từ Bi-LSTM, tính trọng số cho từng trạng thái và tổng hợp chúng thành một context vector phục vụ classification.
- Giúp hiểu cách biểu diễn dữ liệu đầu vào bằng Word2Vec trước khi đưa vào mô hình.
- Là tài liệu tham khảo cho việc xây dựng Tầng 3 LSTM + Attention của đồ án. Tuy nhiên, paper sử dụng Bi-LSTM + Attention trên dữ liệu tin tức, nên hiệu quả của Attention đối với SQL Injection vẫn cần được kiểm chứng bằng thực nghiệm của đồ án.
- Là tài liệu tham khảo cho việc xây dựng Tầng 3 LSTM + Attention của đồ án. Tuy nhiên, paper sử dụng Bi-LSTM + Attention trên dữ liệu tin tức, nên hiệu quả của Attention đối với SQL Injection vẫn cần được kiểm chứng bằng thực nghiệm của đồ án.

**Hạn chế / Giới hạn khi tham khảo**
- Paper tập trung vào bài toán phân loại văn bản tin tức trên tập dữ liệu HuffPost, không nghiên cứu phát hiện SQL Injection.
- Paper sử dụng Bi-LSTM + Attention, trong khi kiến trúc đồ án đã chốt là LSTM + Attention. Do đó không thể áp dụng nguyên xi kiến trúc của paper vào đồ án.
- Hiệu quả của Attention đối với bài toán phát hiện SQL Injection chưa được chứng minh bởi paper và cần được  kiểm chứng bằng thực nghiệm của đồ án.