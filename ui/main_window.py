from PyQt6.QtWidgets import QMainWindow, QTabWidget, QWidget, QGridLayout, QMessageBox
from ui.layouts.main_layouts import MainGridLayout
from ui.widgets.input_panel import InputPanel
from ui.widgets.output_table import OutputTable
from ui.widgets.plot_canvas import PlotCanvas
from core.python.cfd_bridge import CFDBridge

class CFDAeroApp(QMainWindow):
    def __init__(self, lib_path):
        super().__init__()
        self.bridge = CFDBridge(lib_path)
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("UAV Boundary Layer Calculator - Aerospace Engineering")
        self.resize(1300, 850)

        # Hệ thống Tab chính
        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)

        # --- TAB 1: KHÍ ĐỘNG LỰC HỌC (VTOL/AIRFLOW) ---
        self.tab_aero = QWidget()
        self.setup_aero_tab()
        self.tabs.addTab(self.tab_aero, "Phân tích VTOL")

        # --- TAB 2: CHONG CHÓNG (PROPELLER) ---
        self.tab_prop = QWidget()
        self.setup_prop_tab()
        self.tabs.addTab(self.tab_prop, "Phân tích Chong chóng")

    def setup_aero_tab(self):
        layout = MainGridLayout(self.tab_aero)
        
        # Cấu hình tham số Aero
        aero_params = [
            ("U_inf", "Vận tốc dòng tự do", "15.0", "m/s"),
            ("L", "Chiều dài đặc trưng", "0.6133", "m"),
            ("y_plus", "Mục tiêu y+", "1.0", "-"),
            ("r", "Độ phát triển lưới (r)", "1.1", "-")
        ]
        
        self.aero_input = InputPanel(title="Thông số đầu vào VTOL", params=aero_params)
        self.aero_output = OutputTable(title="Kết quả lớp biên")
        self.aero_plot = PlotCanvas()

        layout.assemble(self.aero_input, self.aero_output, self.aero_plot)

        self.aero_input.submitted.connect(self.run_aero_analysis)

    def setup_prop_tab(self):
        layout = MainGridLayout(self.tab_prop)
        
        # Cấu hình tham số Propeller (RPM, Radius, V_inf từ propeller.c)
        prop_params = [
            ("RPM", "Tốc độ vòng quay", "7045.0", "rpm"),
            ("Radius", "Bán kính cánh quạt", "0.327", "m"),
            ("y_plus", "Mục tiêu y+", "1.0", "-"),
            ("Gr", "Tỷ lệ lưới (Gr)", "1.1", "-"),
            ("L", "Chiều dài đặc trưng", "0.0208", "m"),
            ("r_ratio", "Tỷ lệ bán kính", "0.75", "-")
        ]
        
        self.prop_input = InputPanel(title="Thông số hoạt động Chong chóng", params=prop_params)
        self.prop_output = OutputTable(title="Kết quả Động lực học")
        self.prop_plot = PlotCanvas()

        layout.assemble(self.prop_input, self.prop_output, self.prop_plot)

        self.prop_input.submitted.connect(self.run_prop_analysis)

    def run_aero_analysis(self, data):
        try:
            # Gọi tính toán từ lõi C thông qua Bridge
            res = self.bridge.vtol_calculations(
                data['y_plus'], data['U_inf'], data['r'], data['L']
            )
            
            # Hiển thị kết quả rành mạch cho tờ trình
            display = {
                "Số Reynolds (Re)": f"{res['reynolds_number']:.2e}",
                "Độ dày lớp biên (δ)": f"{res['boundary_layer_thickness']*1000:.2f} mm",
                "Chiều cao y1": f"{res['first_layer_height']*1000:.4f} mm",
                "Số lớp biên (n)": f"{res['number_layers_count']}",
                "Tổng dày thực tế": f"{res['total_inflation_thickness']*1000:.2f} mm"
            }
            self.aero_output.update_results(display)
            
            # Vẽ đồ thị trực quan thang Log
            self.aero_plot.draw_inflation_layers(
                y1=res['first_layer_height'],
                growth_rate=data['r'],
                n_layers=res['number_layers_count'],
                delta_theory=res['boundary_layer_thickness']
            )
        except Exception as e:
            QMessageBox.critical(self, "Lỗi Thực thi", f"Kiểm tra lõi C: {str(e)}")

    def run_prop_analysis(self, data):
        """Xử lý bài toán Chong chóng và vẽ lưới trực quan tại vị trí r_ratio"""
        try:
            # Gọi hàm propeller_calculations với tham số từ UI
            res = self.bridge.propeller_calculations(
                data['y_plus'], data['RPM'], data['Gr'], 
                data['Radius'], data['L'], data['r_ratio']
            )
            
            # Cập nhật bảng kết quả cho chong chóng
            display = {
                f"Vận tốc đầu mút (V_tip)": f"{res['tip_speed']:.2f} m/s",
                f"Số Mach đầu mút": f"{res['mach_number']:.3f}",
                f"Re tại {data['r_ratio']*100}%": f"{res['reynolds_number']:.2e}",
                "Số lớp biên cần thiết": f"{res['number_layers_count']}",
                "Tổng bề dày thực tế": f"{res['total_inflation_thickness']*1000:.2f} mm"
            }
            self.prop_output.update_results(display)
            
            # Vẽ đồ thị mô phỏng các lớp lưới tại vị trí cánh quạt được chọn
            self.prop_plot.draw_inflation_layers(
                y1=res['first_layer_height'],
                growth_rate=data['Gr'],
                n_layers=res['number_layers_count'],
                delta_theory=res['boundary_layer_thickness']
            )
        except Exception as e:
            QMessageBox.critical(self, "Lỗi Chong chóng", f"Chi tiết: {str(e)}")