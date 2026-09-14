# SQLi-Detection

Hệ thống tự động phát hiện truy vấn SQL bất thường (SQL Injection) bằng học máy.

## Mục tiêu
Đồ án ngành - so sánh 3 mô hình phát hiện SQL Injection:
- Tầng 1: Random Forest / SVM (đặc trưng thủ công)
- Tầng 2: LSTM (chuỗi token/ký tự)
- Tầng 3: LSTM + Attention (cải tiến)

## Cấu trúc project
- `app/` — ứng dụng middleware demo (Streamlit)
- `artifacts/`
- `datasets/` — dữ liệu raw và đã xử lý (không commit dữ liệu lớn, xem mục Dataset)
- `docs/` — báo cáo theo từng tuần
- `models/` — model đã huấn luyện (lưu ý: có thể không commit file lớn)
- `notebooks/` — notebook thử nghiệm
- `reference/` — đề tài nghiên cứu liên quan
- `src/` — mã nguồn chính (preprocessing, feature_engineering, training, utils)

## Cài đặt môi trường
\`\`\`bash
python -m venv venv
venv\Scripts\activate      # Windows
pip install -r requirements.txt
\`\`\`

## Dataset
Modified_SQL_Dataset.csv, Kaggle, vói 30.919 câu truy vấn SQL được gán nhãn nhị phân (0 - hợp lệ, 1 - SQLi)

## Tiến độ
Hoàn thành
