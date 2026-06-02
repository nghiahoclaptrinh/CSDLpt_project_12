# Engine Địa Phương Hóa Truy Vấn: Bán Hàng Khu Vực

Một hệ thống cơ sở dữ liệu phân tán giới thiệu các kỹ thuật **địa phương hóa truy vấn** và **đẩy xuống lựa chọn** để tối ưu hóa dữ liệu được phân mảnh ngang trên nhiều trang web.

## Tổng Quan Dự Án

Dự án này triển khai một engine tối ưu hóa truy vấn có:
- Phân mảnh bảng `Sales` toàn cục theo chiều ngang trên 3 trang web khu vực (North, South, West)
- Phân tích các truy vấn SQL đến và áp dụng **đẩy xuống lựa chọn** để giảm truyền dữ liệu
- Định tuyến truy vấn chỉ tới các trang web cần thiết dựa trên điều kiện WHERE
- Ghi lại chi tiết thực thi của tất cả các truy vấn để phân tích hiệu năng

**Khái Niệm Chính:** Thay vì phát sóng truy vấn tới tất cả các trang web, engine phát hiện các vị từ khu vực (ví dụ: `Region='North'`) và gửi truy vấn cụ thể cho trang web chỉ tới cơ sở dữ liệu liên quan.

## Cấu Trúc Dự Án

```
.
├── engine/
│   ├── fragmenter.py           # Phân mảnh bảng Sales toàn cục thành CSV khu vực
│   ├── create_database.py      # Tải các mảnh vào cơ sở dữ liệu SQLite
│   ├── localizer.py            # Engine địa phương hóa truy vấn (điểm vào chính)
│   ├── executor.py             # Thực thi truy vấn trên tất cả các trang web (phát sóng)
│   ├── api.py                  # API Flask để gửi truy vấn
│   └── benchmark.py            # Benchmarking hiệu năng
│
├── databases/                  # Cơ sở dữ liệu SQLite (3 trang web khu vực)
│   ├── sales_north.db
│   ├── sales_south.db
│   └── sales_west.db
│
├── datasets/
│   ├── fragments/              # Các tệp CSV được phân mảnh
│   │   ├── sales_north.csv
│   │   ├── sales_south.csv
│   │   └── sales_west.csv
│   └── sales.csv               # Bộ dữ liệu toàn cục ban đầu
│
├── logs/
│   ├── query.log               # Nhật ký thực thi truy vấn
│   ├── benchmark.csv           # Chỉ số hiệu năng
│   └── comparison_benchmark.csv # So sánh phát sóng vs Địa phương hóa
│
├── docs/                       # Tài liệu thiết kế
│   ├── PHÂN TÍCH THIẾT KẾ HỆ THỐNG DỰA TRÊN LÝ THUYẾT ÖZSU.docx
│   ├── TÀI LIỆU THIẾT KẾ HỆ THỐNG.docx
│   └── ĐỀ XUẤT ĐỒ ÁN MÔN CƠ SỞ DỮ LIỆU PHÂN TÁN.docx
│
├── requirements.txt            # Các phụ thuộc Python
├── .gitignore                  # Cấu hình Git ignore
└── README.md                   # Tệp này
```

## Yêu Cầu

- Python 3.11+
- pandas
- flask
- sqlite3 (có sẵn với Python)

## Cài Đặt

1. Clone repository:
   ```bash
   git clone https://github.com/nghiahoclaptrinh/CSDLpt_project_12.git
   cd "Distributed project 12"
   ```

2. Cài đặt các phụ thuộc:
   ```bash
   pip install -r requirements.txt
   ```

## Thiết Lập & Khởi Tạo

### Bước 1: Phân Mảnh Bảng Sales Toàn Cục
```bash
python engine/fragmenter.py
```
Điều này tạo 3 mảnh CSV trong `datasets/fragments/`:
- `sales_north.csv`
- `sales_south.csv`
- `sales_west.csv`

### Bước 2: Tạo Cơ Sở Dữ Liệu Khu Vực
```bash
python engine/create_database.py
```
Điều này tải mỗi mảnh vào cơ sở dữ liệu SQLite riêng biệt trong `databases/`:
- `sales_north.db`
- `sales_south.db`
- `sales_west.db`

## Chạy Engine Địa Phương Hóa Truy Vấn

### Chế Độ Tương Tác
```bash
python engine/localizer.py
```
Engine sẽ:
1. Phát hiện trang web đích từ truy vấn
2. Áp dụng tối ưu hóa đẩy xuống lựa chọn
3. Thực thi truy vấn cụ thể cho trang web
4. Ghi lại tất cả các hoạt động vào `logs/query.log`
5. Trả về kết quả tập hợp

**Ví Dụ Truy Vấn:**
```sql
-- Chỉ truy vấn khu vực North
SELECT * FROM Sales WHERE Region='North'

-- Truy vấn tất cả các trang web khớp với điều kiện lượng
SELECT * FROM Sales WHERE Amount > 1000

-- Phát sóng tới tất cả các trang web
SELECT COUNT(*) FROM Sales
```

### Sử Dụng API
```bash
python engine/api.py
```
Truy cập API tại `http://localhost:5000` và gửi truy vấn qua các yêu cầu POST.

### Benchmarking
Chạy các bài kiểm tra hiệu năng so sánh phát sóng và địa phương hóa:
```bash
python engine/benchmark.py
python engine/compare_benchmark.py
```

Kết quả được lưu vào:
- `logs/benchmark.csv` – Hiệu năng truy vấn đơn lẻ
- `logs/comparison_benchmark.csv` – So sánh phát sóng và Địa phương hóa

## Cách Đẩy Xuống Lựa Chọn Hoạt Động

**Không Có Đẩy Xuống (Phát Sóng):**
```
Truy Vấn Toàn Cục
    ↓
[Truy Vấn tới DB North] → 10 hàng
[Truy Vấn tới DB South] → 15 hàng
[Truy Vấn tới DB West]  → 8 hàng
    ↓
Truyền Mạng: 33 hàng
    ↓
Lọc phía máy khách
Kết quả: 10 hàng (chỉ North)
```

**Với Đẩy Xuống Lựa Chọn (Địa Phương Hóa):**
```
Truy Vấn Toàn Cục (WHERE Region='North')
    ↓
Phân Tích & Phát Hiện Region='North'
    ↓
[Truy Vấn tới DB North] → 10 hàng
    ↓
Truyền Mạng: 10 hàng
    ↓
Kết quả: 10 hàng
```

**Lợi Ích Hiệu Năng:** Giảm lưu lượng mạng và thời gian thực thi truy vấn bằng cách tránh truy cập trang web không cần thiết.

## Ghi Nhật Ký & Giám Sát

Tất cả các truy vấn được ghi vào `logs/query.log` với:
- Dấu thời gian
- Truy vấn ban đầu
- Các trang web đích được chọn
- Số hàng được trả về
- Thời gian thực thi

Ví dụ mục nhật ký:
```
============================
TIME: 2026-06-02 14:30:45.123456
QUERY: SELECT * FROM Sales WHERE Region='North'
TARGET SITES: ['North']
ROWS RETURNED: 10
EXECUTION TIME: 0.045623
```

## Nguyên Tắc Thiết Kế

Dự án này giới thiệu các khái niệm chính từ **Thiết Kế Cơ Sở Dữ Liệu Phân Tán của Özsu & Valduriez**:

1. **Phân Mảnh Ngang** – Bảng Sales được chia theo Region
2. **Đẩy Xuống Lựa Chọn** – Di chuyển điều kiện lọc đến các trang web mảnh
3. **Địa Phương Hóa Truy Vấn** – Định tuyến truy vấn đến các mảnh liên quan
4. **Tối Ưu Hóa Phân Tán** – Giảm thiểu I/O mạng và tính toán
