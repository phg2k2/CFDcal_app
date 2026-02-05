# CFDCal_App: Phần mềm Tính toán Tham số Khí động lực học (Aerodynamic Calculation Suite)

## 1. Giới thiệu (Overview)
**CFDCal_App** là bộ công cụ chuyên dụng hỗ trợ kỹ sư phân tích mô phỏng (CAE/CFD) xác định nhanh các tham số kỹ thuật đầu vào cho quá trình chia lưới và thiết lập biên dạng (Boundary Conditions).

**Tính năng chính:**
* Tính toán thông số lớp biên (Inflation Layer / Boundary Layer) dựa trên $y^+$.
* Ước lượng tham số mô hình rối (Turbulence Modeling: $k, \epsilon, \omega$).
* Phân tích đặc tính lưu chất và cánh quạt (Propeller & Fluid Properties).

**Kiến trúc hệ thống (Hybrid Architecture):**
* **Core Engine (Backend - C):** Xử lý các thuật toán toán học phức tạp với tốc độ cao, được biên dịch thành thư viện liên kết động (`.so`).
* **User Interface (Frontend - Python/PyQt6):** Giao diện trực quan, hỗ trợ vẽ biểu đồ thời gian thực và tương tác người dùng.

## 2. Yêu cầu hệ thống (Prerequisites)
* Hệ điều hành: Linux (Ubuntu/Debian) hoặc Windows (WSL).
* Python: 3.8 trở lên.
* Trình biên dịch: GCC và GNU Make (để biên dịch Core C).

## 3. Cài đặt Môi trường (Environment Setup)
Trước khi sử dụng, hãy đảm bảo các thư viện Python đã được cài đặt:

```bash
# 1. Tạo và kích hoạt môi trường ảo (Khuyến nghị)
python3 -m venv venv
source venv/bin/activate

# 2. Cài đặt các gói phụ thuộc
pip install -r requirements.txt
```
# Trường hợp 1: Sử dụng thông thường
```bash
python3 app_main.py
```
#Trường hợp 2: Lần đầu cài đặt thì phải biên dịch Core C trước
```bash
# Bước 1: Vào thư mục core và biên dịch
cd core
make clean
make

# Bước 2: Quay lại thư mục gốc và chạy ứng dụng
cd ..
python3 app_main.py
```
#Cấu trúc thư mục
```
CFDCal_App/
├── app_main.py             # Điểm khởi chạy chính
├── requirements.txt        # Danh sách thư viện Python
├── core/                   # PHÂN HỆ TÍNH TOÁN (C Language)
│   ├── src/                # Mã nguồn thuật toán (.c)
│   ├── include/            # Các file header (.h)
│   ├── build/              # Chứa file thư viện .so và file object .o
│   ├── core_test/          # Kiểm thử tự động (Unit Test)
│   └── Makefile            # Kịch bản biên dịch
└── ui/                     # PHÂN HỆ GIAO DIỆN (Python/PyQt6)
    ├── main_window.py      # Cửa sổ chính
    ├── widgets/            # Các thành phần giao diện (Input, Plot...)
    └── layouts/            # Bố cục màn hình
```
Phiên bản hiện tại: 1.0.0
Tác giả: Đặng Anh Phương