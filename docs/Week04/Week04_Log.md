# Week 4 Log — Thi công Tầng 1 (Random Forest / SVM)

## Tóm tắt
- extract_features() (16 đặc trưng) cài đặt và kiểm thử thành công, khớp EDA Tuần 2.
- Artifact tiền xử lý: clip_thresholds.json, tier1_scaler.pkl, feature_order.json.
- Random Forest: CV F1=0.9972, test F1=0.9958.
- SVM: CV F1=0.9950, test F1=0.9938.
- Quyết định: giữ nguyên 16 đặc trưng (has_drop, n_semicolon importance thấp nhưng không gây hại).
- Random Forest chọn làm mô hình chính cho Tầng 1 (nhanh hơn, ít FN hơn SVM).

## File đã tạo trong tuần
- notebooks/03_tier1_feature_engineering.ipynb
- artifacts/clip_thresholds.json, tier1_scaler.pkl, feature_order.json
- datasets/processed/train_features_final.npy, test_features_final.npy
- models/tier1_rf.pkl, models/tier1_svm.pkl
- docs/Week04/BaoCao_Tuan04.docx

## Vấn đề gặp phải
- Không có -> cần đọc kỹ báo cáo

## Việc cần mang sang Tuần 5
- Dùng train_split/val_split (không phải train.csv) cho Tầng 2.
- Tái sử dụng artifacts/vocab.json, max_len.json đã có sẵn từ Tuần 3.