#ifndef CFD_BOUNDARY_LAYER_H
#define CFD_BOUNDARY_LAYER_H

double skin_friction_coeff(double Re);
double wall_shear_stress(double Cf, double air_density, double U);
double friction_velocity(double tau_w, double air_density);

double first_layer_height(double y_plus,
                          double mu,
                          double air_density,
                          double u_tau);

double boundary_layer_thickness(double Re, double L);

int inflation_layer_count(double y1,
                          double growth_rate,
                          double delta,
                          double* total_thickness);


#endif // CFD_BOUNDARY_LAYER_H