#ifndef CFD_NONDIMENSIONAL_H
#define CFD_NONDIMENSIONAL_H

double reynolds_number(double density, double velocity, double characteristic_length, double dynamic_viscosity);
double mach_number(double velocity, double speed_of_sound);
double prandtl_number(double specific_heat, double dynamic_viscosity, double thermal_conductivity);

#endif // CFD_NONDIMENSIONAL_H