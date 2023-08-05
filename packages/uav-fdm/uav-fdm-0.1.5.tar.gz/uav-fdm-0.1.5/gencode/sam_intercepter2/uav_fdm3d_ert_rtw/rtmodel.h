//
// File: rtmodel.h
//
// Code generated for Simulink model 'uav_fdm3d'.
//
// Model version                  : 1.16
// Simulink Coder version         : 9.0 (R2018b) 24-May-2018
// C/C++ source code generated on : Sun Aug 30 11:34:49 2020
//
// Target selection: ert.tlc
// Embedded hardware selection: Intel->x86-64 (Windows64)
// Code generation objectives: Unspecified
// Validation result: Not run
//
#ifndef RTW_HEADER_rtmodel_h_
#define RTW_HEADER_rtmodel_h_
#include "uav_fdm3d.h"

//
//  ROOT_IO_FORMAT: 0 (Individual arguments)
//  ROOT_IO_FORMAT: 1 (Structure reference)
//  ROOT_IO_FORMAT: 2 (Part of model data structure)

# define ROOT_IO_FORMAT                1
#if 0

// Example parameter data definition with initial values
static P_uav_fdm3d_T uav_fdm3d_P = {
  // Variable: Alt0
  //  Referenced by: '<S1>/Constant'

  100.0,

  // Variable: LatLon0
  //  Referenced by: '<S5>/initial_pos'

  { 22.0, 110.0 },

  // Variable: hdot0
  //  Referenced by: '<S3>/hdot'

  0.0,

  // Variable: v_e0
  //  Referenced by: '<S3>/v_e'

  0.0,

  // Variable: v_n0
  //  Referenced by: '<S3>/v_n'

  20.0
};                                     // Modifiable parameters

#endif

#define MODEL_CLASSNAME                uav_fdmModelClass
#define MODEL_STEPNAME                 step
#endif                                 // RTW_HEADER_rtmodel_h_

//
// File trailer for generated code.
//
// [EOF]
//
