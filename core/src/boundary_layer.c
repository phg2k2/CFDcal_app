#include "boundary_layer.h"
#include <math.h>

double skin_friction_coeff(double Re) {
    return pow((2*log10(Re)-0.65), -2.3);
}

double wall_shear_stress(double Cf, double rho, double U) {
    return 0.5 * Cf * rho * U * U;
}

double friction_velocity(double tau_w, double rho) {
    return sqrt(tau_w / rho);
}

double first_layer_height(double y_plus,
                          double mu,
                          double rho,
                          double u_tau) {
    return (y_plus * mu) / (rho * u_tau);
}

double boundary_layer_thickness(double Re, double L) {
    if (Re < 5e5) {
        // Laminar boundary layer thickness
        return 5.0 * L / sqrt(Re);
    } else {
        // Turbulent boundary layer thickness (empirical correlation)
        return 0.37 * L / pow(Re, 0.2);
    }
}

int inflation_layer_count(double y1,
                          double growth_rate,
                          double delta,
                          double* total_thickness) {
    int n = 0;
    double current_height = y1;
    *total_thickness = 0.0;

    do {
        n++;
        *total_thickness += current_height;
        if (*total_thickness >= delta) break;
        current_height *= growth_rate;
    } while (1);

    return n;
}
