
class uav_fdmModelClass;
class uav_fdm
{
public:
    uav_fdm(double lat0, double lon0, double alt0,
            double gs0, double gamma0, double psi0, double phi0);

    void update(double dt, double tas_c, double hdot_c, double phi_c,
                double w_n, double w_e,
                double *time_stamp,
                double *lat, double *lon, double *alt,
                double *v_n, double *v_e, double *hdot,
                double *phi, 
                double *psi_t, double *gamma, double *gs,
                double *tas);
private:
        uav_fdmModelClass *fdm3d;
};