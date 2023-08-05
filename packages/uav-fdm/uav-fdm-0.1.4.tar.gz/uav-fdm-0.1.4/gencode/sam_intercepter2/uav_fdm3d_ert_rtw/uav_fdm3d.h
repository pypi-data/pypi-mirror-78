//
// File: uav_fdm3d.h
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
#ifndef RTW_HEADER_uav_fdm3d_h_
#define RTW_HEADER_uav_fdm3d_h_
#include <cmath>
#include <float.h>
#include <math.h>
#include <string.h>
#include <stddef.h>
#include "rtw_modelmap.h"
#ifndef uav_fdm3d_COMMON_INCLUDES_
# define uav_fdm3d_COMMON_INCLUDES_
#include "rtwtypes.h"
#include "rtw_continuous.h"
#include "rtw_solver.h"
#endif                                 // uav_fdm3d_COMMON_INCLUDES_

#include "uav_fdm3d_types.h"
#include <stddef.h>

// Macros for accessing real-time model data structure
#ifndef rtmGetContStateDisabled
# define rtmGetContStateDisabled(rtm)  ((rtm)->contStateDisabled)
#endif

#ifndef rtmSetContStateDisabled
# define rtmSetContStateDisabled(rtm, val) ((rtm)->contStateDisabled = (val))
#endif

#ifndef rtmGetContStates
# define rtmGetContStates(rtm)         ((rtm)->contStates)
#endif

#ifndef rtmSetContStates
# define rtmSetContStates(rtm, val)    ((rtm)->contStates = (val))
#endif

#ifndef rtmGetContTimeOutputInconsistentWithStateAtMajorStepFlag
# define rtmGetContTimeOutputInconsistentWithStateAtMajorStepFlag(rtm) ((rtm)->CTOutputIncnstWithState)
#endif

#ifndef rtmSetContTimeOutputInconsistentWithStateAtMajorStepFlag
# define rtmSetContTimeOutputInconsistentWithStateAtMajorStepFlag(rtm, val) ((rtm)->CTOutputIncnstWithState = (val))
#endif

#ifndef rtmGetDataMapInfo
# define rtmGetDataMapInfo(rtm)        ((rtm)->DataMapInfo)
#endif

#ifndef rtmSetDataMapInfo
# define rtmSetDataMapInfo(rtm, val)   ((rtm)->DataMapInfo = (val))
#endif

#ifndef rtmGetDerivCacheNeedsReset
# define rtmGetDerivCacheNeedsReset(rtm) ((rtm)->derivCacheNeedsReset)
#endif

#ifndef rtmSetDerivCacheNeedsReset
# define rtmSetDerivCacheNeedsReset(rtm, val) ((rtm)->derivCacheNeedsReset = (val))
#endif

#ifndef rtmGetIntgData
# define rtmGetIntgData(rtm)           ((rtm)->intgData)
#endif

#ifndef rtmSetIntgData
# define rtmSetIntgData(rtm, val)      ((rtm)->intgData = (val))
#endif

#ifndef rtmGetOdeF
# define rtmGetOdeF(rtm)               ((rtm)->odeF)
#endif

#ifndef rtmSetOdeF
# define rtmSetOdeF(rtm, val)          ((rtm)->odeF = (val))
#endif

#ifndef rtmGetOdeY
# define rtmGetOdeY(rtm)               ((rtm)->odeY)
#endif

#ifndef rtmSetOdeY
# define rtmSetOdeY(rtm, val)          ((rtm)->odeY = (val))
#endif

#ifndef rtmGetPeriodicContStateIndices
# define rtmGetPeriodicContStateIndices(rtm) ((rtm)->periodicContStateIndices)
#endif

#ifndef rtmSetPeriodicContStateIndices
# define rtmSetPeriodicContStateIndices(rtm, val) ((rtm)->periodicContStateIndices = (val))
#endif

#ifndef rtmGetPeriodicContStateRanges
# define rtmGetPeriodicContStateRanges(rtm) ((rtm)->periodicContStateRanges)
#endif

#ifndef rtmSetPeriodicContStateRanges
# define rtmSetPeriodicContStateRanges(rtm, val) ((rtm)->periodicContStateRanges = (val))
#endif

#ifndef rtmGetZCCacheNeedsReset
# define rtmGetZCCacheNeedsReset(rtm)  ((rtm)->zCCacheNeedsReset)
#endif

#ifndef rtmSetZCCacheNeedsReset
# define rtmSetZCCacheNeedsReset(rtm, val) ((rtm)->zCCacheNeedsReset = (val))
#endif

#ifndef rtmGetdX
# define rtmGetdX(rtm)                 ((rtm)->derivs)
#endif

#ifndef rtmSetdX
# define rtmSetdX(rtm, val)            ((rtm)->derivs = (val))
#endif

#ifndef rtmGetErrorStatus
# define rtmGetErrorStatus(rtm)        ((rtm)->errorStatus)
#endif

#ifndef rtmSetErrorStatus
# define rtmSetErrorStatus(rtm, val)   ((rtm)->errorStatus = (val))
#endif

#ifndef rtmGetStopRequested
# define rtmGetStopRequested(rtm)      ((rtm)->Timing.stopRequestedFlag)
#endif

#ifndef rtmSetStopRequested
# define rtmSetStopRequested(rtm, val) ((rtm)->Timing.stopRequestedFlag = (val))
#endif

#ifndef rtmGetStopRequestedPtr
# define rtmGetStopRequestedPtr(rtm)   (&((rtm)->Timing.stopRequestedFlag))
#endif

#ifndef rtmGetT
# define rtmGetT(rtm)                  (rtmGetTPtr((rtm))[0])
#endif

#ifndef rtmGetTPtr
# define rtmGetTPtr(rtm)               ((rtm)->Timing.t)
#endif

// Block signals (default storage)
typedef struct {
  real_T hdot;                         // '<S3>/hdot'
  real_T v_e;                          // '<S3>/v_e'
  real_T v_n;                          // '<S3>/v_n'
  real_T Sum1;                         // '<S5>/Sum1'
  real_T Product1[3];                  // '<S3>/Product1'
  real_T Gain2;                        // '<S3>/Gain2'
  real_T SFunction_o1;                 // '<S4>/S-Function'
  real_T SFunction_o2;                 // '<S4>/S-Function'
  real_T SFunction_o3;                 // '<S4>/S-Function'
  real_T SFunction_o4;                 // '<S4>/S-Function'
  real_T Switch;                       // '<S24>/Switch'
  real_T TrigonometricFunction1;       // '<S31>/Trigonometric Function1'
  real_T TrigonometricFunction2;       // '<S31>/Trigonometric Function2'
  real_T Switch_h;                     // '<S25>/Switch'
} B_uav_fdm3d_T;

// Block states (default storage) for system '<Root>'
typedef struct {
  real_T SFunction_temp_table[8];      // '<S4>/S-Function'
  real_T SFunction_pres_table[8];      // '<S4>/S-Function'
} DW_uav_fdm3d_T;

// Continuous states (default storage)
typedef struct {
  real_T hdot;                         // '<S3>/hdot'
  real_T v_e;                          // '<S3>/v_e'
  real_T v_n;                          // '<S3>/v_n'
  real_T h;                            // '<S3>/Integrator2'
  real_T Xn;                           // '<S3>/Integrator3'
  real_T Xe;                           // '<S3>/Integrator5'
} X_uav_fdm3d_T;

// State derivatives (default storage)
typedef struct {
  real_T hdot;                         // '<S3>/hdot'
  real_T v_e;                          // '<S3>/v_e'
  real_T v_n;                          // '<S3>/v_n'
  real_T h;                            // '<S3>/Integrator2'
  real_T Xn;                           // '<S3>/Integrator3'
  real_T Xe;                           // '<S3>/Integrator5'
} XDot_uav_fdm3d_T;

// State disabled
typedef struct {
  boolean_T hdot;                      // '<S3>/hdot'
  boolean_T v_e;                       // '<S3>/v_e'
  boolean_T v_n;                       // '<S3>/v_n'
  boolean_T h;                         // '<S3>/Integrator2'
  boolean_T Xn;                        // '<S3>/Integrator3'
  boolean_T Xe;                        // '<S3>/Integrator5'
} XDis_uav_fdm3d_T;

// Invariant block signals (default storage)
typedef const struct tag_ConstB_uav_fdm3d_T {
  real_T UnitConversion;               // '<S30>/Unit Conversion'
  real_T SinCos_o1;                    // '<S16>/SinCos'
  real_T SinCos_o2;                    // '<S16>/SinCos'
  real_T Sum;                          // '<S34>/Sum'
  real_T Product1;                     // '<S35>/Product1'
  real_T Sum1;                         // '<S35>/Sum1'
  real_T sqrt_m;                       // '<S35>/sqrt'
  real_T Product2;                     // '<S31>/Product2'
  real_T Sum1_l;                       // '<S31>/Sum1'
} ConstB_uav_fdm3d_T;

#ifndef ODE3_INTG
#define ODE3_INTG

// ODE3 Integration Data
typedef struct {
  real_T *y;                           // output
  real_T *f[3];                        // derivatives
} ODE3_IntgData;

#endif

// External inputs (root inport signals with default storage)
typedef struct {
  real_T v_c;                          // '<Root>/v_c'
  real_T hdot_c;                       // '<Root>/hdot_c'
  real_T psidot_c;                     // '<Root>/psidot_c'
} ExtU_uav_fdm3d_T;

// External outputs (root outports fed by signals with default storage)
typedef struct {
  real_T time_stamp;                   // '<Root>/time_stamp'
  real_T lat;                          // '<Root>/lat'
  real_T lon;                          // '<Root>/lon'
  real_T ASL;                          // '<Root>/ASL'
  real_T Vn;                           // '<Root>/Vn'
  real_T Ve;                           // '<Root>/Ve'
  real_T Vd;                           // '<Root>/Vd'
} ExtY_uav_fdm3d_T;

// Parameters (default storage)
struct P_uav_fdm3d_T_ {
  real_T Alt0;                         // Variable: Alt0
                                       //  Referenced by: '<S1>/Constant'

  real_T LatLon0[2];                   // Variable: LatLon0
                                       //  Referenced by: '<S5>/initial_pos'

  real_T hdot0;                        // Variable: hdot0
                                       //  Referenced by: '<S3>/hdot'

  real_T v_e0;                         // Variable: v_e0
                                       //  Referenced by: '<S3>/v_e'

  real_T v_n0;                         // Variable: v_n0
                                       //  Referenced by: '<S3>/v_n'

};

// Real-time Model Data Structure
struct tag_RTM_uav_fdm3d_T {
  const char_T *errorStatus;
  RTWSolverInfo solverInfo;
  X_uav_fdm3d_T *contStates;
  int_T *periodicContStateIndices;
  real_T *periodicContStateRanges;
  real_T *derivs;
  boolean_T *contStateDisabled;
  boolean_T zCCacheNeedsReset;
  boolean_T derivCacheNeedsReset;
  boolean_T CTOutputIncnstWithState;
  real_T odeY[6];
  real_T odeF[3][6];
  ODE3_IntgData intgData;

  //
  //  DataMapInfo:
  //  The following substructure contains information regarding
  //  structures generated in the model's C API.

  struct {
    rtwCAPI_ModelMappingInfo mmi;
    void* dataAddress[5];
    int32_T* vardimsAddress[5];
    RTWLoggingFcnPtr loggingPtrs[5];
  } DataMapInfo;

  //
  //  Sizes:
  //  The following substructure contains sizes information
  //  for many of the model attributes such as inputs, outputs,
  //  dwork, sample times, etc.

  struct {
    int_T numContStates;
    int_T numPeriodicContStates;
    int_T numSampTimes;
  } Sizes;

  //
  //  Timing:
  //  The following substructure contains information regarding
  //  the timing information for the model.

  struct {
    uint32_T clockTick0;
    time_T stepSize0;
    uint32_T clockTick1;
    SimTimeStep simTimeStep;
    boolean_T stopRequestedFlag;
    time_T *t;
    time_T tArray[2];
  } Timing;
};

extern const ConstB_uav_fdm3d_T uav_fdm3d_ConstB;// constant block i/o

// Function to get C API Model Mapping Static Info
extern const rtwCAPI_ModelMappingStaticInfo*
  uav_fdm3d_GetCAPIStaticMap(void);

// Class declaration for model uav_fdm3d
class uav_fdmModelClass {
  // public data and function members
 public:
  // External inputs
  ExtU_uav_fdm3d_T uav_fdm3d_U;

  // External outputs
  ExtY_uav_fdm3d_T uav_fdm3d_Y;

  // model initialize function
  void initialize();

  // model step function
  void step();

  // model terminate function
  void terminate();

  // Constructor
  uav_fdmModelClass();

  // Destructor
  ~uav_fdmModelClass();

  // Real-Time Model get method
  RT_MODEL_uav_fdm3d_T * getRTM();

  // private data and function members
 private:
  // Tunable parameters
  P_uav_fdm3d_T uav_fdm3d_P;

  // Block signals
  B_uav_fdm3d_T uav_fdm3d_B;

  // Block states
  DW_uav_fdm3d_T uav_fdm3d_DW;
  X_uav_fdm3d_T uav_fdm3d_X;           // Block continuous states

  // Real-Time Model
  RT_MODEL_uav_fdm3d_T uav_fdm3d_M;

  // Continuous states update member function
  void rt_ertODEUpdateContinuousStates(RTWSolverInfo *si );

  // Derivatives member function
  void uav_fdm3d_derivatives();
};

//-
//  These blocks were eliminated from the model due to optimizations:
//
//  Block '<S1>/1//2' : Unused code path elimination
//  Block '<S3>/Math Function2' : Unused code path elimination
//  Block '<S3>/Sqrt1' : Unused code path elimination
//  Block '<S3>/Sum1' : Unused code path elimination
//  Block '<S9>/Unit Conversion' : Unused code path elimination
//  Block '<S11>/Unit Conversion' : Unused code path elimination
//  Block '<S12>/Unit Conversion' : Unused code path elimination
//  Block '<S13>/Unit Conversion' : Unused code path elimination
//  Block '<S1>/Divide' : Unused code path elimination
//  Block '<S1>/q_bar' : Unused code path elimination
//  Block '<S8>/Reshape (9) to [3x3] column-major' : Reshape block reduction
//  Block '<S10>/Unit Conversion' : Eliminated nontunable gain of 1


//-
//  The generated code includes comments that allow you to trace directly
//  back to the appropriate location in the model.  The basic format
//  is <system>/block_name, where system is the system number (uniquely
//  assigned by Simulink) and block_name is the name of the block.
//
//  Use the MATLAB hilite_system command to trace the generated code back
//  to the model.  For example,
//
//  hilite_system('<S3>')    - opens system 3
//  hilite_system('<S3>/Kp') - opens and selects block Kp which resides in S3
//
//  Here is the system hierarchy for this model
//
//  '<Root>' : 'uav_fdm3d'
//  '<S1>'   : 'uav_fdm3d/EOM3D'
//  '<S2>'   : 'uav_fdm3d/vehicle level'
//  '<S3>'   : 'uav_fdm3d/EOM3D/6th Order Point Mass Flight Model'
//  '<S4>'   : 'uav_fdm3d/EOM3D/COESA Atmosphere Model'
//  '<S5>'   : 'uav_fdm3d/EOM3D/Flat Earth to LLA'
//  '<S6>'   : 'uav_fdm3d/EOM3D/gravity'
//  '<S7>'   : 'uav_fdm3d/EOM3D/6th Order Point Mass Flight Model/Rotation Angles to Direction Cosine Matrix'
//  '<S8>'   : 'uav_fdm3d/EOM3D/6th Order Point Mass Flight Model/Rotation Angles to Direction Cosine Matrix/Create 3x3 Matrix'
//  '<S9>'   : 'uav_fdm3d/EOM3D/COESA Atmosphere Model/Density Conversion'
//  '<S10>'  : 'uav_fdm3d/EOM3D/COESA Atmosphere Model/Length Conversion'
//  '<S11>'  : 'uav_fdm3d/EOM3D/COESA Atmosphere Model/Pressure Conversion'
//  '<S12>'  : 'uav_fdm3d/EOM3D/COESA Atmosphere Model/Temperature Conversion'
//  '<S13>'  : 'uav_fdm3d/EOM3D/COESA Atmosphere Model/Velocity Conversion'
//  '<S14>'  : 'uav_fdm3d/EOM3D/Flat Earth to LLA/LatLong wrap'
//  '<S15>'  : 'uav_fdm3d/EOM3D/Flat Earth to LLA/LatLong wrap1'
//  '<S16>'  : 'uav_fdm3d/EOM3D/Flat Earth to LLA/LongLat_offset'
//  '<S17>'  : 'uav_fdm3d/EOM3D/Flat Earth to LLA/pos_deg'
//  '<S18>'  : 'uav_fdm3d/EOM3D/Flat Earth to LLA/LatLong wrap/Latitude Wrap 90'
//  '<S19>'  : 'uav_fdm3d/EOM3D/Flat Earth to LLA/LatLong wrap/Wrap Longitude'
//  '<S20>'  : 'uav_fdm3d/EOM3D/Flat Earth to LLA/LatLong wrap/Latitude Wrap 90/Compare To Constant'
//  '<S21>'  : 'uav_fdm3d/EOM3D/Flat Earth to LLA/LatLong wrap/Latitude Wrap 90/Wrap Angle 180'
//  '<S22>'  : 'uav_fdm3d/EOM3D/Flat Earth to LLA/LatLong wrap/Latitude Wrap 90/Wrap Angle 180/Compare To Constant'
//  '<S23>'  : 'uav_fdm3d/EOM3D/Flat Earth to LLA/LatLong wrap/Wrap Longitude/Compare To Constant'
//  '<S24>'  : 'uav_fdm3d/EOM3D/Flat Earth to LLA/LatLong wrap1/Latitude Wrap 90'
//  '<S25>'  : 'uav_fdm3d/EOM3D/Flat Earth to LLA/LatLong wrap1/Wrap Longitude'
//  '<S26>'  : 'uav_fdm3d/EOM3D/Flat Earth to LLA/LatLong wrap1/Latitude Wrap 90/Compare To Constant'
//  '<S27>'  : 'uav_fdm3d/EOM3D/Flat Earth to LLA/LatLong wrap1/Latitude Wrap 90/Wrap Angle 180'
//  '<S28>'  : 'uav_fdm3d/EOM3D/Flat Earth to LLA/LatLong wrap1/Latitude Wrap 90/Wrap Angle 180/Compare To Constant'
//  '<S29>'  : 'uav_fdm3d/EOM3D/Flat Earth to LLA/LatLong wrap1/Wrap Longitude/Compare To Constant'
//  '<S30>'  : 'uav_fdm3d/EOM3D/Flat Earth to LLA/LongLat_offset/Angle Conversion2'
//  '<S31>'  : 'uav_fdm3d/EOM3D/Flat Earth to LLA/LongLat_offset/Find Radian//Distance'
//  '<S32>'  : 'uav_fdm3d/EOM3D/Flat Earth to LLA/LongLat_offset/Find Radian//Distance/Angle Conversion2'
//  '<S33>'  : 'uav_fdm3d/EOM3D/Flat Earth to LLA/LongLat_offset/Find Radian//Distance/denom'
//  '<S34>'  : 'uav_fdm3d/EOM3D/Flat Earth to LLA/LongLat_offset/Find Radian//Distance/e'
//  '<S35>'  : 'uav_fdm3d/EOM3D/Flat Earth to LLA/LongLat_offset/Find Radian//Distance/e^4'

#endif                                 // RTW_HEADER_uav_fdm3d_h_

//
// File trailer for generated code.
//
// [EOF]
//
