# OWASP SQL Injection

- **Tác giả / Năm:** OWASP Foundation; Contributors: kingthorin, zbraiterman / Không xác định năm xuất bản cụ thể
- **Nguồn:** OWASP Community — SQL Injection
- **Nguồn bổ sung:**
  - OWASP — Blind SQL Injection
  - OWASP Web Security Testing Guide — Testing for SQL Injection

- **Mục đích / Nội dung chính của tài liệu:**
  - Giải thích SQL Injection và cách thức xảy ra.
  - Trình bày các hậu quả của SQL Injection.
  - Minh họa SQL Injection thông qua các ví dụ.
  - Trình bày một số cách tiếp cận để phòng chống SQL Injection.

- **Phương pháp:**
  - Đây là tài liệu kỹ thuật/wiki, không phải nghiên cứu thực nghiệm Machine Learning.
  - Không có dataset train/test.
  - Không có mô hình ML.
  - Không có quy trình đánh giá Precision/Recall/F1.

- **Kết quả chính:**
  - SQL Injection là việc đưa/chèn SQL query thông qua dữ liệu đầu vào từ client vào ứng dụng, làm ảnh hưởng đến việc thực thi các câu lệnh SQL đã được định trước.
  - SQL Injection xảy ra khi dữ liệu từ nguồn không đáng tin cậy đi vào chương trình và được sử dụng để xây dựng truy vấn SQL động.
  - Hậu quả:
    - Confidentiality: có thể làm lộ dữ liệu nhạy cảm trong cơ sở dữ liệu.
    - Authentication: trong một số trường hợp có thể vượt qua cơ chế xác thực nếu câu lệnh SQL được xây dựng không an toàn.
    - Authorization: có thể thay đổi thông tin liên quan đến phân quyền nếu thông tin này được lưu trong SQL database.
    - Integrity: có thể làm thay đổi hoặc xóa dữ liệu.
  - Ví dụ minh họa cho thấy input của người dùng có thể làm thay đổi cấu trúc hoặc logic của truy vấn SQL.
  - Một ví dụ cho thấy việc đưa điều kiện luôn đúng vào truy vấn có thể làm thay đổi phạm vi dữ liệu được trả về.
  - Các cách tiếp cận phòng chống được đề cập:
    - Input validation
    - Allow list
    - Deny list
    - Escaping
    - Stored procedures
    - Parameterized queries
  - OWASP chỉ ra rằng deny list có thể tồn tại loopholes/bypass; escaping thủ công và stored procedures cũng không loại bỏ hoàn toàn nguy cơ SQL Injection.
  - Parameterized SQL statements có thể cung cấp mức đảm bảo bảo mật tốt hơn và giảm yêu cầu bảo trì so với một số cách tiếp cận khác.
  - Blind SQL Injection là một dạng SQL Injection trong đó thông tin được suy luận dựa trên phản hồi của ứng dụng thay vì nhận trực tiếp dữ liệu từ database.
  - Tautology/Boolean-based SQL Injection có thể sử dụng điều kiện logic luôn đúng để làm thay đổi kết quả của truy vấn.

- **Điều học được / áp dụng được cho đồ án:**
  - Đầu vào của hệ thống là các truy vấn SQL cần được phân loại. Trong đồ án, truy vấn sẽ được tiền xử lý và biểu diễn dưới dạng đặc trưng thủ công hoặc chuỗi token/ký tự tùy theo từng tầng mô hình.
  - Mục tiêu phân loại là xác định truy vấn thuộc nhóm bình thường hay SQL Injection.
  - SQL Injection có nhiều dạng biểu diễn và cách khai thác khác nhau. Vì vậy dataset cần có sự đa dạng về truy vấn bình thường và truy vấn SQL Injection, đồng thời nhãn dữ liệu phải được xác định rõ ràng.
  - Khi khảo sát dataset cần chú ý đến số lượng mẫu, chất lượng nhãn, tính đa dạng và khả năng xuất hiện dữ liệu trùng lặp giữa train/test.
  - Tài liệu cho thấy một số cách tiếp cận dựa trên deny list có thể tồn tại loopholes/bypass. Đây là cơ sở để đặt vấn đề về khả năng nhận diện các biến thể SQL Injection bằng các quy tắc cố định.
  - Trong đồ án, nhận xét này là một động cơ để khảo sát các phương pháp học máy và học sâu trong việc tự động phân loại truy vấn SQL. Hiệu quả của các mô hình sẽ được kiểm chứng thực nghiệm bằng Precision, Recall và F1-score ở các bước sau.

- **Hạn chế của tài liệu (nếu có):**
  - Không phải paper nghiên cứu thực nghiệm.
  - Không đánh giá mô hình Machine Learning/Deep Learning.
  - Không cung cấp dataset để huấn luyện.
  - Không đi sâu vào bài toán tự động phát hiện SQL Injection bằng Machine Learning/Deep Learning.