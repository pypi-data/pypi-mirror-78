#ifndef RTW_HEADER_uav_fdm3d_cap_host_h_
#define RTW_HEADER_uav_fdm3d_cap_host_h_
#ifdef HOST_CAPI_BUILD
#include "rtw_capi.h"
#include "rtw_modelmap.h"

typedef struct {
  rtwCAPI_ModelMappingInfo mmi;
} uav_fdm3d_host_DataMapInfo_T;

#ifdef __cplusplus

extern "C" {

#endif

  void uav_fdm3d_host_InitializeDataMapInfo(uav_fdm3d_host_DataMapInfo_T
    *dataMap, const char *path);

#ifdef __cplusplus

}
#endif
#endif                                 // HOST_CAPI_BUILD
#endif                                 // RTW_HEADER_uav_fdm3d_cap_host_h_

// EOF: uav_fdm3d_capi_host.h
