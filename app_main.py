import sys
import os
from PyQt6.QtWidgets import QApplication

# Ép sử dụng xcb để tránh lỗi "Failed to create wl_display" trên Linux
os.environ["QT_QPA_PLATFORM"] = "xcb"

def get_resource_path(relative_path):
    """ Xử lý đường dẫn động cho cả môi trường phát triển và sau khi đóng gói """
    try:
        base_path = sys._MEIPASS # Thư mục tạm của PyInstaller
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

from ui.main_window import CFDAeroApp

def main():
    app = QApplication(sys.argv)
    
    # Nạp giao diện QSS rành mạch
    style_path = get_resource_path("ui/resources/style.qss")
    if os.path.exists(style_path):
        with open(style_path, "r") as f:
            app.setStyleSheet(f.read())
    else:
        print(f"Cảnh báo: Không tìm thấy file style.qss tại {style_path}")

    # Đường dẫn thư viện lõi C đã xử lý động
    lib_path = get_resource_path("core/build/libcfdcalc.so")
    
    window = CFDAeroApp(lib_path)
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()