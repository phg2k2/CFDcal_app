#include "boundary_layer.h"
#include "constants.h"
#include "fluid.h"
#include "nondimensional.h"
#include "propeller.h"
#include "turbulence.h"

#include <math.h>
#include <stdio.h>
#include <stdlib.h>

int main(void)
{
    /* 1. INPUT PARAMETERS */
    double U_inf = 15.0;          // m/s
    double L     = 0.6133;        // m
    double rpm   = 7045.0;
    double R     = 0.75;        // m
    double yplus_target = 1.0;

    double AIR_DENSITY = get_air_density();
    double MU_AIR     = get_mu_air();
    /* 2. NON-DIMENSIONAL NUMBERS */
    double Re = reynolds_number(AIR_DENSITY, U_inf, L, MU_AIR);

    /* 3. TURBULENCE / WALL MODEL */
    double Cf    = skin_friction_coeff(Re);
    double tau_w = wall_shear_stress(Cf, AIR_DENSITY, U_inf);
    double u_tau = friction_velocity(tau_w, AIR_DENSITY);

    /* 4. MESH / BOUNDARY LAYER */
    double y1 = first_layer_height(yplus_target, MU_AIR, AIR_DENSITY, u_tau);
    double delta = boundary_layer_thickness(Re, L);

    double total_thickness;
    int n_layers = inflation_layer_count(y1, 1.1, delta, &total_thickness);

    /* 5. PROPELLER */
    double V_tip = tip_speed(rpm, R);

    /* 6. OUTPUT */
    printf("----- CFD CALC RESULTS -----------------\n");
    printf("Reynolds number        : %.3e\n", Re);
    printf("Skin friction coeff    : %.6f\n", Cf);
    printf("Wall shear stress      : %.6f Pa\n", tau_w);
    printf("Friction velocity      : %.6f m/s\n", u_tau);
    printf("First layer height y1  : %.3e m\n", y1);
    printf("BL thickness delta     : %.3e m\n", delta);
    printf("Inflation layers       : %d\n", n_layers);
    printf("Total inflation thick. : %.3e m\n", total_thickness);
    printf("Blade tip speed        : %.2f m/s\n", V_tip);
    printf("----------------------------------------\n");

    return 0;
}
