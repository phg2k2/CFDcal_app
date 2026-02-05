import ctypes
import os
import math

D = ctypes.c_double
I = ctypes.c_int
P = ctypes.POINTER(D)

class CFDCoreTest:
    def __init__(self, lib_path):
        if not os.path.exists(lib_path):
            raise FileNotFoundError(f"Không tìm thấy thư viện tại: {lib_path}")
        
        self.lib = ctypes.CDLL(os.path.abspath(lib_path))
        self._register_functions()

    def _register_functions(self):
        # Cấu trúc: "tên_hàm": (kiểu_trả_về, [danh_sách_tham_số])
        api_config = {
            # Constants & Fluid
            "get_air_density": (D, []),
            "get_mu_air": (D, []),
            "get_cp_air": (D, []),
            "get_k_air": (D, []),
            "get_pi": (D, []),
            "dynamic_viscosity": (D, [D]),
            
            # Non-Dimensional
            "reynolds_number": (D, [D, D, D, D]), # rho, V, L, mu
            "mach_number": (D, [D, D]),
            "prandtl_number": (D, [D, D, D]),
            
            # Boundary Layer
            "skin_friction_coeff": (D, [D]),
            "wall_shear_stress": (D, [D, D, D]), # Cf, rho, U
            "friction_velocity": (D, [D, D]),    # tau_w, rho
            "first_layer_height": (D, [D, D, D, D]), # y+, mu, rho, utau
            "boundary_layer_thickness": (D, [D, D]),
            "inflation_layer_count": (I, [D, D, D, P]),
            
            # Propeller & Turbulence
            "tip_speed": (D, [D, D]),
            "turbulent_intensity": (D, [D]),
        }

        for func_name, (res, args) in api_config.items():
            try:
                func = getattr(self.lib, func_name)
                func.restype = res
                func.argtypes = args
            except AttributeError:
                print(f"⚠️ Warning: Function '{func_name}' not found in library.")

    def run_full_test(self):
        print(f"{'=== CFD CORE UNIT TEST REPORT ===':^50}")
        
        # 1. Test Constants
        rho = self.lib.get_air_density()
        mu = self.lib.get_mu_air()
        print(f"[*] Constants: Rho={rho:.3f}, Mu={mu:.2e}")

        # 2. Test Nondimensional
        U, L = 15.0, 0.6133
        re = self.lib.reynolds_number(rho, U, L, mu)
        print(f"[*] Reynolds: {re:.2e}")

        # 3. Test Boundary Layer Logic
        cf = self.lib.skin_friction_coeff(re)
        tw = self.lib.wall_shear_stress(cf, rho, U)
        utau = self.lib.friction_velocity(tw, rho)
        y1 = self.lib.first_layer_height(1.0, mu, rho, utau)
        delta = self.lib.boundary_layer_thickness(re, L)
        
        # Test Inflation (Pointer handling)
        total_t = D(0.0)
        n_layers = self.lib.inflation_layer_count(y1, 1.1, delta, ctypes.byref(total_t))

        # 4. Show Results in Table
        results = [
            ("Skin Friction (Cf)", f"{cf:.6f}"),
            ("Wall Shear (Tw)", f"{tw:.4f} Pa"),
            ("Friction Vel (u_tau)", f"{utau:.4f} m/s"),
            ("First Layer (y1)", f"{y1:.3e} m"),
            ("BL Thickness (delta)", f"{delta:.4f} m"),
            ("Inflation Layers", f"{n_layers}"),
            ("Total Infl. Thick", f"{total_t.value:.4f} m")
        ]

        print(f"\n{'Metric':<25} | {'Value':<15}")
        print("-" * 45)
        for metric, val in results:
            print(f"{metric:<25} | {val:<15}")

if __name__ == "__main__":
    tester = CFDCoreTest("../build/libcfdcalc.so")
    tester.run_full_test()