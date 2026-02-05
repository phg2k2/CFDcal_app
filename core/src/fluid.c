#include "fluid.h"
#include "constants.h"
#include <math.h>

double dynamic_viscosity(double T) {
    return (get_C1() * pow(T, 1.5)) / (T + get_S());
}

double density_air(double T, double P) {
    // Ideal gas law for air density
    return P / (get_r_air() * T);
}

double thermal_conductivity_air(double T) {
    // Empirical correlation for thermal conductivity of air
    return 0.024 + 7.0e-5 * (T - get_T_ref());
}

double specific_heat_air(double T) {
    // Approximate specific heat capacity of air at constant pressure
    return get_cp_air() + 0.1 * (T - get_T_ref());
}
