#include "turbulence.h"
#include <math.h>

double turbulent_intensity(double Re) {
    if (Re <= 0) {
        return 0.0;
    }
    return 0.16 * pow(Re, -1.0 / 8.0);
}

double turbulent_length_scale(double L) {
    return 0.07 * L;
}