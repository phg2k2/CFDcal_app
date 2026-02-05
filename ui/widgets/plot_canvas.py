import numpy as np
import matplotlib.pyplot as plt
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QGroupBox
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

class PlotCanvas(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        self.setLayout(layout)
        
        self.fig = Figure(figsize=(5, 6), tight_layout=True)
        self.canvas = FigureCanvas(self.fig)
        self.ax = self.fig.add_subplot(111)
        layout.addWidget(self.canvas)

    def draw_inflation_layers(self, y1, growth_rate, n_layers, delta_theory):
        """
        Vẽ mặt cắt lưới Inflation với thang đo Logarit để quan sát lớp sát tường.
        """
        self.ax.clear()
        
        # Thiết lập thang đo log cho trục Y
        self.ax.set_yscale('log')
        
        y_coords = [0]
        current_h = y1
        total_s = 0
        
        # Tính toán tọa độ các lớp
        layers_y = []
        for i in range(n_layers):
            y_start = total_s
            total_s += current_h
            y_end = total_s
            layers_y.append((y_start, y_end))
            current_h *= growth_rate

        # Vẽ các lớp lưới
        for i, (ystart, yend) in enumerate(layers_y):
            # Lưu ý: Trong thang log, ta không thể vẽ từ 0, 
            # nên lớp đầu tiên sẽ được vẽ từ một giá trị rất nhỏ (ví dụ y1 * 0.1)
            display_start = ystart if ystart > 0 else y1 * 0.5
            
            color_val = 0.2 + (0.6 * (i / n_layers))
            self.ax.axhspan(display_start, yend, 
                            facecolor='steelblue', 
                            alpha=1.0 - color_val, 
                            edgecolor='white', 
                            linewidth=0.5)

        # Vẽ đường Delta lý thuyết
        self.ax.axhline(y=delta_theory, color='red', linestyle='--', 
                        linewidth=2, label=f'Delta: {delta_theory*1000:.2f} mm')

        # Định dạng đồ thị chuyên nghiệp
        self.ax.set_title(f"Cấu trúc lưới Inflation (Thang Log - n={n_layers})", fontweight='bold')
        self.ax.set_ylabel("Khoảng cách cách tường (m) - Log Scale")
        self.ax.set_xticks([])
        
        # Thiết lập giới hạn trục Y: từ 1/2 của y1 đến trên delta một chút
        self.ax.set_ylim(y1 * 0.5, max(layers_y[-1][1], delta_theory) * 2)
        
        self.ax.grid(True, which="both", ls=":", alpha=0.5)
        self.ax.legend(loc='upper right')
        
        self.canvas.draw()