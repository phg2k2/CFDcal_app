#include "nondimensional.h"
#include <math.h>

double reynolds_number(double density, double velocity, double characteristic_length, double dynamic_viscosity) {
    return (density * velocity * characteristic_length) / dynamic_viscosity;
}

double mach_number(double velocity, double speed_of_sound) {
    return velocity / speed_of_sound;
}

double prandtl_number(double specific_heat, double dynamic_viscosity, double thermal_conductivity) {
    return (specific_heat * dynamic_viscosity) / thermal_conductivity;
}