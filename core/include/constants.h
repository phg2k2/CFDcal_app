#ifndef CFD_CONSTANTS_H
#define CFD_CONSTANTS_H

double get_pi(void);
double get_air_density(void);
double get_mu_air(void);
double get_k_air(void);
double get_cp_air(void);
double get_cv_air(void);
double get_pr_air(void);
double get_g(void);
double get_r_air(void);

double get_C1(void);
double get_S(void);
double get_T_ref(void);
double get_P_ref(void);

#define CONSTANTS_LIST \
    X(PI, 3.14159265358979323846, get_pi)            \
    X(AIR_DENSITY, 1.225, get_air_density)   \
    X(MU_AIR, 1.81e-5, get_mu_air)       \
    X(K_AIR, 0.0257, get_k_air)        \
    X(CP_AIR, 1005.0, get_cp_air)       \
    X(CV_AIR, 718.0, get_cv_air)       \
    X(PR_AIR, 0.71, get_pr_air)       \
    X(G, 9.81, get_g)            \
    X(R_AIR, 287.05, get_r_air)        \
    X(C1, 1.458e-6, get_C1)           \
    X(S, 110.4, get_S)            \
    X(T_REF, 273.15, get_T_ref)        \
    X(P_REF, 101325.0, get_P_ref)

#define X(val, num, func) double func(void);
CONSTANTS_LIST
#undef X

#endif // CFD_CONSTANTS_H