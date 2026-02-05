#ifndef CFD_FLUID_H
#define CFD_FLUID_H

double dynamic_viscosity(double T);
double density_air(double T, double P);
double thermal_conductivity_air(double T);
double specific_heat_air(double T);

#endif // CFD_FLUID_H