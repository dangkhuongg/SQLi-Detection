Dataset chọn: Modified_SQL_Dataset.csv
Tổng số dòng: 30919
Số dòng trùng lặp: 12
Số dòng sau khi loại trùng: 30907
Số dòng train: 24724
Số dòng test: 6181
Tỷ lệ nhãn (toàn bộ dataset):
 Label
0    0.63184
1    0.36816
Name: proportion, dtype: float64
Tỷ lệ nhãn (train):
 Label
0    0.631856
1    0.368144
Name: proportion, dtype: float64
Tỷ lệ nhãn (test):
 Label
0    0.631775
1    0.368225
Name: proportion, dtype: float64
Giá trị null theo cột:
 Query    0
Label    0
dtype: int64

Train: 80% tương đương 24735 mẫu
Test: 20% tương đương 6184

Kết quả sample check 25 dòng sinh ngẫu nhiên: nhãn hoàn toàn hợp lệ

Quyết định cuối cùng:
Chọn này dataset này làm dataset trong đề tài.

EDA:
        kw_UNION     kw_OR   kw_DROP  kw_SELECT     kw_--
Label                                                   
0      0.028549  0.263027  0.002753   0.670465  0.000128
1      0.212371  0.391782  0.003406   0.878269  0.349154

        char_'    char_;    char_=   char_--
Label                                        
0      0.661503  0.032198  0.208872  0.000128
1      1.128433  0.007251  1.205669  0.349154

Mở rộng đặc trưng ký mục:
        char_comma  char_lparen  char_rparen  char_percent  n_comment_markers
Label                                                                       
0        0.335424     0.291704     0.286135      0.030022           0.000640
1        1.808723     3.539991     3.988904      0.196770           0.525599

Tỷ lệ chênh lệch (lớp 1 / lớp 0):
 n_comment_markers    819.809691
char_rparen           13.940589
char_lparen           12.135517
char_percent           6.554025
char_comma             5.392327
dtype: float64

Cấu trúc câu:
        uppercase_ratio  n_whitespace    n_digit
Label                                          
0             0.237200      6.537895   1.707464
1             0.003855     43.993078  18.320589

Zoom lại biểu đồ dài:
        count        mean        std  min   25%   50%    75%     max
Label                                                                
0      15622.0   39.894508  54.977360  1.0  11.0  35.0   55.0  5370.0
1       9102.0  118.736981  96.652344  1.0  51.0  86.0  151.0   456.0       