#ifndef CFD_PROPELLER_H
#define CFD_PROPELLER_H

double tip_speed(double radius, double rpm);
double advance_ratio(double velocity, double rpm, double diameter);
double thrust_coefficient(double thrust, double density, double diameter, double rpm);
double power_coefficient(double power, double density, double diameter, double rpm);
double local_blade_speed(double radius, double r_ratio, double rpm);

#endif // CFD_PROPELLER_H