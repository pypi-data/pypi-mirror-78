%module uav_fdm
%include "typemaps.i"
%{
#include "uav_fdm.h"
%}

// Now list ISO C/C++ declarations
class uav_fdm
{
public:
    uav_fdm(double lat0, double lon0, double alt0,
            double v_n0, double v_e0, double hdot0);

    void update(double dt, double vg_c, double hdot_c, double psidot_c,
                double *OUTPUT, double *OUTPUT, double *OUTPUT,
                double *OUTPUT, double *OUTPUT, double *OUTPUT);
};
