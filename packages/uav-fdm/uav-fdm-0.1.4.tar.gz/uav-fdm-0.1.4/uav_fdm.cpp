#include "uav_fdm.h"

#include "uav_fdm3d.h"

#define CAPI_MDL uav_fdm3d

#define CAT_I(a, b) a##b
#define CAT(a, b) CAT_I(a, b)

#define ap_GetCAPIStaticMap_fcn CAT(CAPI_MDL,_GetCAPIStaticMap)

#include <iostream>
#include <fstream>
#include <vector>
#include <regex>
#include <string>


std::vector<std::string> scan_param(uav_fdmModelClass *Obj)
{
    std::vector<std::string> head;

    const rtwCAPI_ModelMappingStaticInfo *sm = ap_GetCAPIStaticMap_fcn();
	
    if (sm)
    {
        //unsigned int n = rtwCAPI_GetNumBlockParametersFromStaticMap(sm);
        unsigned int m = rtwCAPI_GetNumModelParametersFromStaticMap(sm);
        rtwCAPI_ModelParameters const *prm = rtwCAPI_GetModelParametersFromStaticMap(sm);
        rtwCAPI_DataTypeMap const *dtm = rtwCAPI_GetDataTypeMapFromStaticMap(sm);
        rtwCAPI_DimensionMap const *dmm = rtwCAPI_GetDimensionMapFromStaticMap(sm);
        uint_T const *dam = rtwCAPI_GetDimensionArrayFromStaticMap(sm);
        rtwCAPI_ModelMappingInfo *MMI = &(rtmGetDataMapInfo(Obj->getRTM()).mmi);
        void **da = rtwCAPI_GetDataAddressMap(MMI);
        for (unsigned int i = 0; i < m; ++i)
        {
            const char *name = rtwCAPI_GetModelParameterName(prm, i);
            int idx = rtwCAPI_GetModelParameterAddrIdx(prm, i);
            uint16_t dti = rtwCAPI_GetModelParameterDataTypeIdx(prm, i);
            uint16_t dmi = rtwCAPI_GetModelParameterDimensionIdx(prm, i);
            uint8_t ss = rtwCAPI_GetDataTypeSLId(dtm, dti);
            uint16_t dai = rtwCAPI_GetDimArrayIndex(dmm, dmi);
            uint8_t nd = rtwCAPI_GetNumDims(dmm, dmi);
            uint16_t n = 1;
            for (int j = 0; j < nd; ++j)
            {
                n *= dam[dai + j];
            }
            head.push_back(std::string(name));
            for (int j = 1; j < n; ++j)
            {
                head.push_back(std::string(name) + "(" + std::to_string(j) + ")");
            }
        }
    }
    return head;
}

void setup_param(uav_fdmModelClass *Obj, const std::vector<std::string> &head, const std::vector<double> &onecase)
{
    const rtwCAPI_ModelMappingStaticInfo *sm = ap_GetCAPIStaticMap_fcn();
    if (sm)
    {
        //unsigned int n = rtwCAPI_GetNumBlockParametersFromStaticMap(sm);
        unsigned int m = rtwCAPI_GetNumModelParametersFromStaticMap(sm);
        rtwCAPI_ModelParameters const *prm = rtwCAPI_GetModelParametersFromStaticMap(sm);
        rtwCAPI_DataTypeMap const *dtm = rtwCAPI_GetDataTypeMapFromStaticMap(sm);
        rtwCAPI_DimensionMap const *dmm = rtwCAPI_GetDimensionMapFromStaticMap(sm);
        uint_T const *dam = rtwCAPI_GetDimensionArrayFromStaticMap(sm);
        rtwCAPI_ModelMappingInfo *MMI = &(rtmGetDataMapInfo(Obj->getRTM()).mmi);
        void **da = rtwCAPI_GetDataAddressMap(MMI);
        for (unsigned int i = 0; i < m; ++i)
        {
            const char *name = rtwCAPI_GetModelParameterName(prm, i);
            int idx = rtwCAPI_GetModelParameterAddrIdx(prm, i);
            uint16_t dti = rtwCAPI_GetModelParameterDataTypeIdx(prm, i);
            uint16_t dmi = rtwCAPI_GetModelParameterDimensionIdx(prm, i);
            uint8_t ss = rtwCAPI_GetDataTypeSLId(dtm, dti);
            uint16_t dai = rtwCAPI_GetDimArrayIndex(dmm, dmi);
            uint8_t nd = rtwCAPI_GetNumDims(dmm, dmi);
            uint16_t n = 1;
            for (int j = 0; j < nd; ++j)
            {
                n *= dam[dai + j];
            }
            int j = 0;
            for (auto i = head.begin(); i != head.end(); ++i, ++j)
            {
                if (i->find(name) != std::string::npos)
                {
                    int param_idx = 0;
                    double param_value = onecase[j];
                    std::smatch result;
					std::regex pattern("(.*)\\((\\d{1,})\\)");
                    if (std::regex_match(*i, result, pattern))
                    {
                        param_idx = std::stoi(result[2].str());
                    }
                    switch (ss)
                    {
                    case SS_DOUBLE:
                    {
                        double *d = (double *)da[idx];
                        d[param_idx] = param_value;
						std::cout << name << "(" <<  param_idx  << ")=" << d[param_idx] << std::endl;
                    }
                    break;
                    case SS_SINGLE:
                    {
                        float *s = (float *)da[idx];
                        s[param_idx] = param_value;
						std::cout << name << "(" <<  param_idx  << ")=" << s[param_idx] << std::endl;
                    }
                    break;
                    case SS_INT8:
                    {
                        int8_T *c = (int8_T *)da[idx];
                        c[param_idx] = param_value;
						std::cout << name << "(" <<  param_idx  << ")=" << (int)c[param_idx] << std::endl;

                    }
                    break;
                    case SS_INT16:
                    {
                        int16_T *h = (int16_T *)da[idx];
                        h[param_idx] = param_value;
						std::cout << name << "(" <<  param_idx  << ")=" << h[param_idx] << std::endl;
                    }
                    break;
                    case SS_INT32:
                    {
                        int32_T *I = (int32_T *)da[idx];
                        I[param_idx] = param_value;
						std::cout << name << "(" <<  param_idx  << ")=" << I[param_idx] << std::endl;
                    }
                    break;
                    case SS_UINT8:
                    {
                        uint8_T *c = (uint8_T *)da[idx];
                        c[param_idx] = param_value;
						std::cout << name << "(" <<  param_idx  << ")=" << (int)c[param_idx] << std::endl;
                    }
                    break;
                    case SS_UINT16:
                    {
                        uint16_T *h = (uint16_T *)da[idx];
                        h[param_idx] = param_value;
						std::cout << name << "(" <<  param_idx  << ")=" << h[param_idx] << std::endl;
                    }
                    break;
                    case SS_UINT32:
                    {
                        uint32_T *I = (uint32_T *)da[idx];
                        I[param_idx] = param_value;
						std::cout << name << "(" <<  param_idx  << ")=" << I[param_idx] << std::endl;
                    }
                    break;
                    }
                }
            }
        }
    }
}


uav_fdm::uav_fdm(double lat0, double lon0, double alt0,
                 double v_n0, double v_e0, double hdot0)
{
    fdm3d = new uav_fdmModelClass;
    fdm3d->initialize();

        std::cout << "Parameters in the mdl:" << std::endl;
        std::vector<std::string> heads = scan_param(fdm3d);
        for (auto i = heads.begin(); i != heads.end(); ++i)
        {
            std::cout << '\t' << *i << std::endl;
        }
        std::vector<std::string> param_name;
        std::vector<double> param_val;
        param_name.push_back("LatLon0");
        param_val.push_back(lat0);
        param_name.push_back("LatLon0(1)");
        param_val.push_back(lon0);
        param_name.push_back("Alt0");
        param_val.push_back(alt0);
        param_name.push_back("v_n0");
        param_val.push_back(v_n0);
        param_name.push_back("v_e0");
        param_val.push_back(v_e0);
        param_name.push_back("hdot0");
        param_val.push_back(hdot0);
        setup_param(fdm3d, param_name, param_val);
}

void uav_fdm::update(double dt, double vg_c, double hdot_c, double psidot_c,
                     double *lat, double *lon, double *alt,
                     double *v_n, double *v_e, double *v_d)
{
    double t0 = fdm3d->uav_fdm3d_Y.time_stamp;
    fdm3d->uav_fdm3d_U.v_c = vg_c;
    fdm3d->uav_fdm3d_U.hdot_c = hdot_c;
    fdm3d->uav_fdm3d_U.psidot_c = psidot_c;
    double t1;
    do {
      fdm3d->step();
      t1 = fdm3d->uav_fdm3d_Y.time_stamp;
    } while (t1 - t0 < dt);
    *lat = fdm3d->uav_fdm3d_Y.lat;
    *lon = fdm3d->uav_fdm3d_Y.lon;
    *alt = fdm3d->uav_fdm3d_Y.ASL;
    *v_n = fdm3d->uav_fdm3d_Y.Vn;
    *v_e = fdm3d->uav_fdm3d_Y.Ve;
    *v_d = fdm3d->uav_fdm3d_Y.Vd;
}
