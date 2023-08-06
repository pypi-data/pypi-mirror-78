//
// File: uav_fdm3d_capi.cpp
//
// Code generated for Simulink model 'uav_fdm3d'.
//
// Model version                  : 1.35
// Simulink Coder version         : 9.0 (R2018b) 24-May-2018
// C/C++ source code generated on : Wed Sep  2 10:52:06 2020
//
// Target selection: ert.tlc
// Embedded hardware selection: Intel->x86-64 (Windows64)
// Code generation objectives: Unspecified
// Validation result: Not run
//
#include <stddef.h>
#include "rtw_capi.h"
#ifdef HOST_CAPI_BUILD
#include "uav_fdm3d_capi_host.h"
#define sizeof(s)                      ((size_t)(0xFFFF))
#undef rt_offsetof
#define rt_offsetof(s,el)              ((uint16_T)(0xFFFF))
#define TARGET_CONST
#define TARGET_STRING(s)               (s)
#else                                  // HOST_CAPI_BUILD
#include "builtin_typeid_types.h"
#include "uav_fdm3d.h"
#include "uav_fdm3d_capi.h"
#include "uav_fdm3d_private.h"
#ifdef LIGHT_WEIGHT_CAPI
#define TARGET_CONST
#define TARGET_STRING(s)               (NULL)
#else
#define TARGET_CONST                   const
#define TARGET_STRING(s)               (s)
#endif
#endif                                 // HOST_CAPI_BUILD

// Individual block tuning is not valid when inline parameters is *
//  selected. An empty map is produced to provide a consistent     *
//  interface independent  of inlining parameters.                 *

static rtwCAPI_BlockParameters rtBlockParameters[] = {
  // addrMapIndex, blockPath,
  //  paramName, dataTypeIndex, dimIndex, fixPtIdx

  {
    0, (NULL), (NULL), 0, 0, 0
  }
};

// Tunable variable parameters
static rtwCAPI_ModelParameters rtModelParameters[] = {
  // addrMapIndex, varName, dataTypeIndex, dimIndex, fixPtIndex
  { 0, TARGET_STRING("Alt0"), 0, 0, 0 },

  { 1, TARGET_STRING("LatLon0"), 0, 1, 0 },

  { 2, TARGET_STRING("gamma0"), 0, 0, 0 },

  { 3, TARGET_STRING("gs0"), 0, 0, 0 },

  { 4, TARGET_STRING("hdot_max"), 0, 0, 0 },

  { 5, TARGET_STRING("hdot_min"), 0, 0, 0 },

  { 6, TARGET_STRING("k_gamma"), 0, 0, 0 },

  { 7, TARGET_STRING("k_phi"), 0, 0, 0 },

  { 8, TARGET_STRING("k_tht"), 0, 0, 0 },

  { 9, TARGET_STRING("p_max"), 0, 0, 0 },

  { 10, TARGET_STRING("phi0"), 0, 0, 0 },

  { 11, TARGET_STRING("phi_max"), 0, 0, 0 },

  { 12, TARGET_STRING("psi0"), 0, 0, 0 },

  { 13, TARGET_STRING("tas_max"), 0, 0, 0 },

  { 14, TARGET_STRING("tas_min"), 0, 0, 0 },

  { 0, (NULL), 0, 0, 0 }
};

#ifndef HOST_CAPI_BUILD

// Initialize Data Address
static void uav_fdm3d_InitializeDataAddr(void* dataAddr[], P_uav_fdm3d_T
  *uav_fdm3d_P)
{
  dataAddr[0] = (void*) (&uav_fdm3d_P->Alt0);
  dataAddr[1] = (void*) (&uav_fdm3d_P->LatLon0[0]);
  dataAddr[2] = (void*) (&uav_fdm3d_P->gamma0);
  dataAddr[3] = (void*) (&uav_fdm3d_P->gs0);
  dataAddr[4] = (void*) (&uav_fdm3d_P->hdot_max);
  dataAddr[5] = (void*) (&uav_fdm3d_P->hdot_min);
  dataAddr[6] = (void*) (&uav_fdm3d_P->k_gamma);
  dataAddr[7] = (void*) (&uav_fdm3d_P->k_phi);
  dataAddr[8] = (void*) (&uav_fdm3d_P->k_tht);
  dataAddr[9] = (void*) (&uav_fdm3d_P->p_max);
  dataAddr[10] = (void*) (&uav_fdm3d_P->phi0);
  dataAddr[11] = (void*) (&uav_fdm3d_P->phi_max);
  dataAddr[12] = (void*) (&uav_fdm3d_P->psi0);
  dataAddr[13] = (void*) (&uav_fdm3d_P->tas_max);
  dataAddr[14] = (void*) (&uav_fdm3d_P->tas_min);
}

#endif

// Initialize Data Run-Time Dimension Buffer Address
#ifndef HOST_CAPI_BUILD

static void uav_fdm3d_InitializeVarDimsAddr(int32_T* vardimsAddr[])
{
  vardimsAddr[0] = (NULL);
}

#endif

#ifndef HOST_CAPI_BUILD

// Initialize logging function pointers
static void uav_fdm3d_InitializeLoggingFunctions(RTWLoggingFcnPtr loggingPtrs[])
{
  loggingPtrs[0] = (NULL);
  loggingPtrs[1] = (NULL);
  loggingPtrs[2] = (NULL);
  loggingPtrs[3] = (NULL);
  loggingPtrs[4] = (NULL);
  loggingPtrs[5] = (NULL);
  loggingPtrs[6] = (NULL);
  loggingPtrs[7] = (NULL);
  loggingPtrs[8] = (NULL);
  loggingPtrs[9] = (NULL);
  loggingPtrs[10] = (NULL);
  loggingPtrs[11] = (NULL);
  loggingPtrs[12] = (NULL);
  loggingPtrs[13] = (NULL);
  loggingPtrs[14] = (NULL);
}

#endif

// Data Type Map - use dataTypeMapIndex to access this structure
static TARGET_CONST rtwCAPI_DataTypeMap rtDataTypeMap[] = {
  // cName, mwName, numElements, elemMapIndex, dataSize, slDataId, *
  //  isComplex, isPointer
  { "double", "real_T", 0, 0, sizeof(real_T), SS_DOUBLE, 0, 0 }
};

#ifdef HOST_CAPI_BUILD
#undef sizeof
#endif

// Structure Element Map - use elemMapIndex to access this structure
static TARGET_CONST rtwCAPI_ElementMap rtElementMap[] = {
  // elementName, elementOffset, dataTypeIndex, dimIndex, fxpIndex
  { (NULL), 0, 0, 0, 0 },
};

// Dimension Map - use dimensionMapIndex to access elements of ths structure
static rtwCAPI_DimensionMap rtDimensionMap[] = {
  // dataOrientation, dimArrayIndex, numDims, vardimsIndex
  { rtwCAPI_SCALAR, 0, 2, 0 },

  { rtwCAPI_VECTOR, 2, 2, 0 }
};

// Dimension Array- use dimArrayIndex to access elements of this array
static uint_T rtDimensionArray[] = {
  1,                                   // 0
  1,                                   // 1
  1,                                   // 2
  2                                    // 3
};

// Fixed Point Map
static rtwCAPI_FixPtMap rtFixPtMap[] = {
  // fracSlopePtr, biasPtr, scaleType, wordLength, exponent, isSigned
  { (NULL), (NULL), rtwCAPI_FIX_RESERVED, 0, 0, 0 },
};

// Sample Time Map - use sTimeIndex to access elements of ths structure
static rtwCAPI_SampleTimeMap rtSampleTimeMap[] = {
  // samplePeriodPtr, sampleOffsetPtr, tid, samplingMode
  {
    (NULL), (NULL), 0, 0
  }
};

static rtwCAPI_ModelMappingStaticInfo mmiStatic = {
  // Signals:{signals, numSignals,
  //            rootInputs, numRootInputs,
  //            rootOutputs, numRootOutputs},
  //  Params: {blockParameters, numBlockParameters,
  //           modelParameters, numModelParameters},
  //  States: {states, numStates},
  //  Maps:   {dataTypeMap, dimensionMap, fixPtMap,
  //           elementMap, sampleTimeMap, dimensionArray},
  //  TargetType: targetType

  { (NULL), 0,
    (NULL), 0,
    (NULL), 0 },

  { rtBlockParameters, 0,
    rtModelParameters, 15 },

  { (NULL), 0 },

  { rtDataTypeMap, rtDimensionMap, rtFixPtMap,
    rtElementMap, rtSampleTimeMap, rtDimensionArray },
  "float",

  { 953140730U,
    940850932U,
    2431685157U,
    4085788671U },
  (NULL), 0,
  0
};

// Function to get C API Model Mapping Static Info
const rtwCAPI_ModelMappingStaticInfo*
  uav_fdm3d_GetCAPIStaticMap(void)
{
  return &mmiStatic;
}

// Cache pointers into DataMapInfo substructure of RTModel
#ifndef HOST_CAPI_BUILD

void uav_fdm3d_InitializeDataMapInfo(RT_MODEL_uav_fdm3d_T *const uav_fdm3d_M,
  P_uav_fdm3d_T *uav_fdm3d_P)
{
  // Set C-API version
  rtwCAPI_SetVersion(uav_fdm3d_M->DataMapInfo.mmi, 1);

  // Cache static C-API data into the Real-time Model Data structure
  rtwCAPI_SetStaticMap(uav_fdm3d_M->DataMapInfo.mmi, &mmiStatic);

  // Cache static C-API logging data into the Real-time Model Data structure
  rtwCAPI_SetLoggingStaticMap(uav_fdm3d_M->DataMapInfo.mmi, (NULL));

  // Cache C-API Data Addresses into the Real-Time Model Data structure
  uav_fdm3d_InitializeDataAddr(uav_fdm3d_M->DataMapInfo.dataAddress, uav_fdm3d_P);
  rtwCAPI_SetDataAddressMap(uav_fdm3d_M->DataMapInfo.mmi,
    uav_fdm3d_M->DataMapInfo.dataAddress);

  // Cache C-API Data Run-Time Dimension Buffer Addresses into the Real-Time Model Data structure 
  uav_fdm3d_InitializeVarDimsAddr(uav_fdm3d_M->DataMapInfo.vardimsAddress);
  rtwCAPI_SetVarDimsAddressMap(uav_fdm3d_M->DataMapInfo.mmi,
    uav_fdm3d_M->DataMapInfo.vardimsAddress);

  // Set Instance specific path
  rtwCAPI_SetPath(uav_fdm3d_M->DataMapInfo.mmi, (NULL));
  rtwCAPI_SetFullPath(uav_fdm3d_M->DataMapInfo.mmi, (NULL));

  // Cache C-API logging function pointers into the Real-Time Model Data structure 
  uav_fdm3d_InitializeLoggingFunctions(uav_fdm3d_M->DataMapInfo.loggingPtrs);
  rtwCAPI_SetLoggingPtrs(uav_fdm3d_M->DataMapInfo.mmi,
    uav_fdm3d_M->DataMapInfo.loggingPtrs);

  // Cache the instance C-API logging pointer
  rtwCAPI_SetInstanceLoggingInfo(uav_fdm3d_M->DataMapInfo.mmi, (NULL));

  // Set reference to submodels
  rtwCAPI_SetChildMMIArray(uav_fdm3d_M->DataMapInfo.mmi, (NULL));
  rtwCAPI_SetChildMMIArrayLen(uav_fdm3d_M->DataMapInfo.mmi, 0);
}

#else                                  // HOST_CAPI_BUILD
#ifdef __cplusplus

extern "C" {

#endif

  void uav_fdm3d_host_InitializeDataMapInfo(uav_fdm3d_host_DataMapInfo_T
    *dataMap, const char *path)
  {
    // Set C-API version
    rtwCAPI_SetVersion(dataMap->mmi, 1);

    // Cache static C-API data into the Real-time Model Data structure
    rtwCAPI_SetStaticMap(dataMap->mmi, &mmiStatic);

    // host data address map is NULL
    rtwCAPI_SetDataAddressMap(dataMap->mmi, NULL);

    // host vardims address map is NULL
    rtwCAPI_SetVarDimsAddressMap(dataMap->mmi, NULL);

    // Set Instance specific path
    rtwCAPI_SetPath(dataMap->mmi, path);
    rtwCAPI_SetFullPath(dataMap->mmi, NULL);

    // Set reference to submodels
    rtwCAPI_SetChildMMIArray(dataMap->mmi, (NULL));
    rtwCAPI_SetChildMMIArrayLen(dataMap->mmi, 0);
  }

#ifdef __cplusplus

}
#endif
#endif                                 // HOST_CAPI_BUILD

//
// File trailer for generated code.
//
// [EOF]
//
