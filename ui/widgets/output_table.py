from PyQt6.QtWidgets import QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QHeaderView, QGroupBox
from PyQt6.QtCore import Qt

class OutputTable(QWidget):
    def __init__(self, title="Kết quả tính toán"):
        super().__init__()
        self.title = title
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        self.setLayout(layout)

        self.group_box = QGroupBox(self.title)
        group_layout = QVBoxLayout()

        self.table = QTableWidget()
        self.table.setColumnCount(2)
        self.table.setHorizontalHeaderLabels(["Thông số", "Giá trị"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table.verticalHeader().setVisible(False)
        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)

        group_layout.addWidget(self.table)
        self.group_box.setLayout(group_layout)
        layout.addWidget(self.group_box)

    def update_results(self, results_dict):
        """Tự động điều chỉnh số hàng dựa trên số lượng kết quả trả về"""
        self.table.setRowCount(len(results_dict))
        for row, (key, value) in enumerate(results_dict.items()):
            name_item = QTableWidgetItem(str(key))
            value_item = QTableWidgetItem(str(value))
            
            value_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            
            self.table.setItem(row, 0, name_item)
            self.table.setItem(row, 1, value_item)