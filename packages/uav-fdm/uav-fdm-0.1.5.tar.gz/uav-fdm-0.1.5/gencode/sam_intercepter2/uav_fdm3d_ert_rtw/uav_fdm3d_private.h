//
// File: uav_fdm3d_private.h
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
#ifndef RTW_HEADER_uav_fdm3d_private_h_
#define RTW_HEADER_uav_fdm3d_private_h_
#include "rtwtypes.h"
#include "builtin_typeid_types.h"

// Private macros used by the generated code to access rtModel
#ifndef rtmIsMajorTimeStep
# define rtmIsMajorTimeStep(rtm)       (((rtm)->Timing.simTimeStep) == MAJOR_TIME_STEP)
#endif

#ifndef rtmIsMinorTimeStep
# define rtmIsMinorTimeStep(rtm)       (((rtm)->Timing.simTimeStep) == MINOR_TIME_STEP)
#endif

#ifndef rtmSetTPtr
# define rtmSetTPtr(rtm, val)          ((rtm)->Timing.t = (val))
#endif

#ifndef ATMOS_TYPEDEF

typedef enum { COESA = 1, MILHDBK310, MILSTD210C } AtmosTypeIdx;

typedef enum { PROFILE = 1, ENVELOPE } ModelIdx;

typedef enum { HIGHTEMP = 1, LOWTEMP, HIGHDENSITY,
  LOWDENSITY, HIGHPRESSURE, LOWPRESSURE } VarIdx;

typedef enum { PP1 = 1, PP10 } PPercentIdx;

typedef enum { K5 = 1, K10, K20, K30, K40 } PAltIdx;

typedef enum { EXTREME = 1, P1, P5, P10, P20 } EPercentIdx;

#define ATMOS_TYPEDEF
#endif                                 // ATMOS_TYPEDEF

#ifndef ATMOS_DEFINE
#define PRESSURE0                      101325.0                  //  N/m^2                  
#define TEMPERATURE0                   288.15                    //  K                      
#define GRAV_CONST                     9.80665                   //  m/s^2                  
#define MOL_WT                         28.9644                   //  kg/kgmol (air)         
#define R_HAT                          8314.32                   //  J/kgmol.K (gas const.) 
#define GAMMA                          1.4                       //  (specific heat ratio) 
#define GMR                            ( GRAV_CONST * MOL_WT / R_HAT )
#define ATMOS_DEFINE
#endif                                 // ATMOS_DEFINE

#ifndef COESA76_DEFINE_DATA

// 1976 COESA atmosphere model
#define NUM1976PTS                     8

static real_T altitude76[NUM1976PTS] = {// in meters (m)
  0.0, 11000.0, 20000.0, 32000.0, 47000.0, 51000.0, 71000.0, 84852.0 };

static real_T tempGradient76[NUM1976PTS] = {// in K/m
  (-0.0065), 0.0, 0.0010, 0.0028, 0.0, -0.0028, -0.0020, -0.0020 };

#define COESA76_DEFINE_DATA
#endif                                 // COESA76_DEFINE_DATA

extern real_T rt_modd(real_T u0, real_T u1);
void InitCalcAtmosCOESA(real_T *temperature76, real_T *pressureRatio76);
void CalcAtmosCOESA(const real_T *altitude, real_T *temp, real_T *pressure,
                    real_T *density, real_T *speedofsound, real_T *temperature76,
                    real_T *pressureRatio76, int_T numPoints);

// private model entry point functions
extern void uav_fdm3d_derivatives();

#endif                                 // RTW_HEADER_uav_fdm3d_private_h_

//
// File trailer for generated code.
//
// [EOF]
//
