#include "propeller.h"
#include "constants.h"
#include <math.h>

double tip_speed(double radius, double RPM) {
    double angular_velocity = RPM * 2 * get_pi() / 60;
    return radius * angular_velocity;
}

double advance_ratio(double velocity, double RPM, double diameter) {
    double n = RPM / 60.0; // revolutions per second
    return velocity / (n * diameter);
}

double thrust_coefficient(double thrust, double density, double diameter, double RPM) {
    double n = RPM / 60.0; // revolutions per second
    double A = get_pi() * pow(diameter / 2.0, 2); // propeller disk area
    return thrust / (density * n * n * A * pow(diameter, 2));
}

double power_coefficient(double power, double density, double diameter, double RPM) {
    double n = RPM / 60.0; // revolutions per second
    double A = get_pi() * pow(diameter / 2.0, 2); // propeller disk area
    return power / (density * n * n * A * pow(diameter, 3));
}

double local_blade_speed(double radius, double r_ratio, double RPM) {
    double local_radius = radius * r_ratio;
    double angular_velocity = RPM * 2 * get_pi() / 60;
    return local_radius * angular_velocity;
}