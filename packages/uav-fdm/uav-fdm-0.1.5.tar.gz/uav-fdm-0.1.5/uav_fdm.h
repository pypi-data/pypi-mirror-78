
class uav_fdmModelClass;
class uav_fdm
{
public:
    uav_fdm(double lat0, double lon0, double alt0,
            double v_n0, double v_e0, double hdot0);

    void update(double dt, double vg_c, double hdot_c, double psidot_c,
                double *lat, double *lon, double *alt,
                double *v_n, double *v_e, double *v_d);
private:
        uav_fdmModelClass *fdm3d;
};