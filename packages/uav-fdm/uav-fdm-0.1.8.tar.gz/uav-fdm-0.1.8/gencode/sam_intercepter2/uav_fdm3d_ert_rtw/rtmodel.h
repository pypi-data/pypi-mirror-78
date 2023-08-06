//
// File: rtmodel.h
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
  //  Referenced by: '<S1>/Integrator2'

  100.0,

  // Variable: LatLon0
  //  Referenced by: '<S7>/initial_pos'

  { 22.0, 110.0 },

  // Variable: gamma0
  //  Referenced by:
  //    '<S2>/Constant'
  //    '<S2>/Integrator'
  //    '<S30>/int_q'

  0.0,

  // Variable: gs0
  //  Referenced by: '<S6>/Integrator'

  20.0,

  // Variable: hdot_max
  //  Referenced by: '<Root>/Saturation1'

  3.0,

  // Variable: hdot_min
  //  Referenced by: '<Root>/Saturation1'

  -3.0,

  // Variable: k_gamma
  //  Referenced by: '<S2>/Gain'

  0.2,

  // Variable: k_phi
  //  Referenced by: '<S4>/Gain1'

  2.0,

  // Variable: k_tht
  //  Referenced by: '<S30>/Gain2'

  1.6,

  // Variable: p_max
  //  Referenced by: '<S4>/Saturation3'

  1.0,

  // Variable: phi0
  //  Referenced by: '<S4>/Integrator1'

  0.0,

  // Variable: phi_max
  //  Referenced by: '<Root>/Saturation2'

  0.7,

  // Variable: psi0
  //  Referenced by: '<S5>/Integrator1'

  0.0,

  // Variable: tas_max
  //  Referenced by: '<Root>/Saturation'

  24.0,

  // Variable: tas_min
  //  Referenced by: '<Root>/Saturation'

  14.0
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
