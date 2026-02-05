#include "constants.h"

#define X(name, num, func) static double name = num;
CONSTANTS_LIST
#undef X

#define X(name, num, func) \
    double func(void) { return name; }
CONSTANTS_LIST
#undef X