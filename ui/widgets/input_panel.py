from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QGridLayout, QLabel, 
                             QLineEdit, QPushButton, QGroupBox)
from PyQt6.QtCore import pyqtSignal

class InputPanel(QWidget):
    submitted = pyqtSignal(dict)

    def __init__(self, title="Input Parameters", params=None):
        super().__init__()
        # Nếu không truyền params, sử dụng danh sách trống
        self.params_config = params if params else []
        self.title = title
        self.fields = {}
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        self.setLayout(layout)

        # Sử dụng tiêu đề động được truyền vào
        group = QGroupBox(self.title)
        grid = QGridLayout()

        # Tạo các hàng nhập liệu dựa trên cấu hình truyền vào
        for row, (key, label, default, unit) in enumerate(self.params_config):
            grid.addWidget(QLabel(label), row, 0)
            
            line_edit = QLineEdit(default)
            grid.addWidget(line_edit, row, 1)
            self.fields[key] = line_edit
            
            grid.addWidget(QLabel(unit), row, 2)

        group.setLayout(grid)
        layout.addWidget(group)

        self.btn_calc = QPushButton("TÍNH TOÁN")
        self.btn_calc.clicked.connect(self.on_submit)
        layout.addWidget(self.btn_calc)
        layout.addStretch()

    def on_submit(self):
        try:
            # Thu hoạch dữ liệu theo key đã định nghĩa
            data = {key: float(edit.text()) for key, edit in self.fields.items()}
            self.submitted.emit(data)
        except ValueError:
            print("Lỗi: Dữ liệu nhập vào phải là số thực.")