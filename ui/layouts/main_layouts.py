from PyQt6.QtWidgets import QGridLayout, QWidget

class MainGridLayout(QGridLayout):
    def __init__(self, parent_widget=None):
        super().__init__(parent_widget)
        self.init_layout()

    def init_layout(self):
        """Thiết lập các thông số khung sườn cho layout"""
        # Khoảng cách giữa các Widgets (Padding)
        self.setSpacing(15) 
        
        # Khoảng cách với mép cửa sổ (Margin)
        self.setContentsMargins(10, 10, 10, 10)

        # Thiết lập tỉ lệ co giãn: Cột 1 (Index 1) rộng gấp đôi Cột 0
        self.setColumnStretch(0, 1)
        self.setColumnStretch(1, 2)
        
        # Thiết lập tỉ lệ hàng: Hàng dưới (Output) có thể giãn nhiều hơn nếu cần
        self.setRowStretch(0, 1)
        self.setRowStretch(1, 1)

    def assemble(self, input_widget, output_widget, plot_widget):
        """Lắp ghép các mảnh module vào đúng vị trí tọa độ"""
        
        # Input Panel: Hàng 0, Cột 0
        self.addWidget(input_widget, 0, 0)
        
        # Output Table: Hàng 1, Cột 0
        self.addWidget(output_widget, 1, 0)
        
        # Plot Canvas: Hàng 0, Cột 1, Chiếm 2 hàng (rowSpan=2)
        self.addWidget(plot_widget, 0, 1, 2, 1)