import ctypes
import os

# Định nghĩa các kiểu dữ liệu ctypes để code rành mạch
D = ctypes.c_double
I = ctypes.c_int
P = ctypes.POINTER(D)

class CFDBridge:
    def __init__(self, lib_path):
        """Khởi tạo và nạp thư viện lõi C (.so hoặc .dll)"""
        if not os.path.exists(lib_path):
            raise FileNotFoundError(f"Không tìm thấy thư viện tại: {lib_path}")
        
        self.lib = ctypes.CDLL(os.path.abspath(lib_path))
        self._register_api()

    def _register_api(self):
        """Đăng ký Prototype cho toàn bộ hàm trong lõi C"""
        api_config = {
            # Hằng số môi trường
            "get_air_density": (D, []),
            "get_mu_air": (D, []),
            
            # Các hàm không thứ nguyên và lớp biên
            "mach_number": (D, [D, D]),
            "reynolds_number": (D, [D, D, D, D]),
            "skin_friction_coeff": (D, [D]),
            "wall_shear_stress": (D, [D, D, D]),
            "friction_velocity": (D, [D, D]),
            "first_layer_height": (D, [D, D, D, D]),
            "boundary_layer_thickness": (D, [D, D]),
            
            # Hàm tính số lớp lưới (Sử dụng con trỏ double* để lấy tổng độ dày)
            "inflation_layer_count": (I, [D, D, D, P]), 
            
            # Tính toán chong chóng
            "tip_speed": (D, [D, D]),
            "local_blade_speed": (D, [D, D, D]),
        }

        for func_name, (res, args) in api_config.items():
            try:
                func = getattr(self.lib, func_name)
                func.restype = res
                func.argtypes = args
            except AttributeError:
                print(f"⚠️ Cảnh báo: Hàm '{func_name}' chưa được định nghĩa trong lõi C.")

    def vtol_calculations(self, target_y_plus,freestream_velocity, growth_rate, characteristic_length):
        
        air_density = self.lib.get_air_density()
        mu_air = self.lib.get_mu_air()
        
        reynolds_num = self.lib.reynolds_number(air_density, freestream_velocity, characteristic_length, mu_air)
        skin_friction = self.lib.skin_friction_coeff(reynolds_num)
        shear_stress = self.lib.wall_shear_stress(skin_friction, air_density, freestream_velocity)
        friction_vel = self.lib.friction_velocity(shear_stress, air_density)
        first_layer_h = self.lib.first_layer_height(target_y_plus, mu_air, air_density, friction_vel)
        boundary_layer_thick = self.lib.boundary_layer_thickness(reynolds_num, characteristic_length)
        
        total_thickness = D(0.0)
        n_layers = self.lib.inflation_layer_count(first_layer_h, growth_rate, boundary_layer_thick, ctypes.byref(total_thickness))
        
        return {
            "air_density": air_density,
            "mu_air": mu_air,
            "reynolds_number": reynolds_num,
            "skin_friction_coeff": skin_friction,
            "wall_shear_stress": shear_stress,
            "friction_velocity": friction_vel,
            "first_layer_height": first_layer_h,
            "boundary_layer_thickness": boundary_layer_thick,
            "total_inflation_thickness": total_thickness.value,
            "number_layers_count": n_layers
        }
        
    def propeller_calculations(self, target_y_plus, rotational_speed, growth_rate, radius, characteristic_length, r_ratio):
        air_density = self.lib.get_air_density()
        mu_air = self.lib.get_mu_air()
        
        tip_speed = self.lib.tip_speed(radius, rotational_speed)
        local_speed = self.lib.local_blade_speed(radius, r_ratio, rotational_speed)
        
        reynolds_num = self.lib.reynolds_number(air_density, local_speed, characteristic_length, mu_air)
        mach_number = self.lib.mach_number(tip_speed, 340.29)        
        
        skin_friction = self.lib.skin_friction_coeff(reynolds_num)
        shear_stress = self.lib.wall_shear_stress(skin_friction, air_density, local_speed)
        friction_vel = self.lib.friction_velocity(shear_stress, air_density)
        first_layer_h = self.lib.first_layer_height(target_y_plus, mu_air, air_density, friction_vel)
        boundary_layer_thick = self.lib.boundary_layer_thickness(reynolds_num, characteristic_length)
        
        total_thickness = D(0.0)
        n_layers = self.lib.inflation_layer_count(first_layer_h, growth_rate, boundary_layer_thick, ctypes.byref(total_thickness))
        
        return {
            "tip_speed": tip_speed,
            "reynolds_number": reynolds_num,
            "mach_number": mach_number,
            "skin_friction_coeff": skin_friction,
            "wall_shear_stress": shear_stress,
            "friction_velocity": friction_vel,
            "first_layer_height": first_layer_h,
            "boundary_layer_thickness": boundary_layer_thick,
            "total_inflation_thickness": total_thickness.value,
            "number_layers_count": n_layers
        }