//
// File: uav_fdm3d.h
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
#ifndef RTW_HEADER_uav_fdm3d_h_
#define RTW_HEADER_uav_fdm3d_h_
#include <string.h>
#include <cmath>
#include <float.h>
#include <math.h>
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
  real_T Switch;                       // '<S18>/Switch'
  real_T TrigonometricFunction1;       // '<S25>/Trigonometric Function1'
  real_T TrigonometricFunction2;       // '<S25>/Trigonometric Function2'
  real_T Switch_h;                     // '<S19>/Switch'
  real_T Product1;                     // '<S3>/Product1'
  real_T Product;                      // '<S3>/Product'
  real_T Product2;                     // '<S3>/Product2'
  real_T Gain1;                        // '<S6>/Gain1'
  real_T at_c;                         // '<S6>/Sum1'
  real_T Gain1_o;                      // '<S2>/Gain1'
  real_T q_c;                          // '<S30>/Gain2'
  real_T Gain2;                        // '<S2>/Gain2'
  real_T psidot;                       // '<S5>/Divide'
  real_T p_c;                          // '<S4>/Saturation3'
  real_T Sum3_n;                       // '<S6>/Sum3'
  real_T q;                            // '<S30>/q_dyn'
  real_T p;                            // '<S4>/p_ctrl'
} B_uav_fdm3d_T;

// Block states (default storage) for system '<Root>'
typedef struct {
  int_T Integrator1_IWORK;             // '<S6>/Integrator1'
  int_T Integrator1_IWORK_m;           // '<S2>/Integrator1'
} DW_uav_fdm3d_T;

// Continuous states (default storage)
typedef struct {
  real_T Xn;                           // '<S1>/Integrator3'
  real_T Xe;                           // '<S1>/Integrator5'
  real_T h;                            // '<S1>/Integrator2'
  real_T Integrator1_CSTATE;           // '<S5>/Integrator1'
  real_T Integrator_CSTATE;            // '<S6>/Integrator'
  real_T Integrator_CSTATE_a;          // '<S2>/Integrator'
  real_T Integrator1_CSTATE_g;         // '<S6>/Integrator1'
  real_T Integrator1_CSTATE_n;         // '<S2>/Integrator1'
  real_T int_q_CSTATE;                 // '<S30>/int_q'
  real_T Integrator1_CSTATE_a;         // '<S4>/Integrator1'
  real_T TransferFcn_CSTATE;           // '<S6>/Transfer Fcn'
  real_T q_dyn_CSTATE;                 // '<S30>/q_dyn'
  real_T p_ctrl_CSTATE;                // '<S4>/p_ctrl'
} X_uav_fdm3d_T;

// Periodic continuous state vector (global)
typedef int_T PeriodicIndX_uav_fdm3d_T[1];
typedef real_T PeriodicRngX_uav_fdm3d_T[2];

// State derivatives (default storage)
typedef struct {
  real_T Xn;                           // '<S1>/Integrator3'
  real_T Xe;                           // '<S1>/Integrator5'
  real_T h;                            // '<S1>/Integrator2'
  real_T Integrator1_CSTATE;           // '<S5>/Integrator1'
  real_T Integrator_CSTATE;            // '<S6>/Integrator'
  real_T Integrator_CSTATE_a;          // '<S2>/Integrator'
  real_T Integrator1_CSTATE_g;         // '<S6>/Integrator1'
  real_T Integrator1_CSTATE_n;         // '<S2>/Integrator1'
  real_T int_q_CSTATE;                 // '<S30>/int_q'
  real_T Integrator1_CSTATE_a;         // '<S4>/Integrator1'
  real_T TransferFcn_CSTATE;           // '<S6>/Transfer Fcn'
  real_T q_dyn_CSTATE;                 // '<S30>/q_dyn'
  real_T p_ctrl_CSTATE;                // '<S4>/p_ctrl'
} XDot_uav_fdm3d_T;

// State disabled
typedef struct {
  boolean_T Xn;                        // '<S1>/Integrator3'
  boolean_T Xe;                        // '<S1>/Integrator5'
  boolean_T h;                         // '<S1>/Integrator2'
  boolean_T Integrator1_CSTATE;        // '<S5>/Integrator1'
  boolean_T Integrator_CSTATE;         // '<S6>/Integrator'
  boolean_T Integrator_CSTATE_a;       // '<S2>/Integrator'
  boolean_T Integrator1_CSTATE_g;      // '<S6>/Integrator1'
  boolean_T Integrator1_CSTATE_n;      // '<S2>/Integrator1'
  boolean_T int_q_CSTATE;              // '<S30>/int_q'
  boolean_T Integrator1_CSTATE_a;      // '<S4>/Integrator1'
  boolean_T TransferFcn_CSTATE;        // '<S6>/Transfer Fcn'
  boolean_T q_dyn_CSTATE;              // '<S30>/q_dyn'
  boolean_T p_ctrl_CSTATE;             // '<S4>/p_ctrl'
} XDis_uav_fdm3d_T;

// Invariant block signals (default storage)
typedef const struct tag_ConstB_uav_fdm3d_T {
  real_T UnitConversion;               // '<S24>/Unit Conversion'
  real_T SinCos_o1;                    // '<S10>/SinCos'
  real_T SinCos_o2;                    // '<S10>/SinCos'
  real_T Sum;                          // '<S28>/Sum'
  real_T Product1;                     // '<S29>/Product1'
  real_T Sum1;                         // '<S29>/Sum1'
  real_T sqrt_m;                       // '<S29>/sqrt'
  real_T Product2;                     // '<S25>/Product2'
  real_T Sum1_l;                       // '<S25>/Sum1'
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
  real_T tas_c;                        // '<Root>/tas_c'
  real_T hdot_c;                       // '<Root>/hdot_c'
  real_T phi_c;                        // '<Root>/phi_c'
  real_T w_n;                          // '<Root>/w_n'
  real_T w_e;                          // '<Root>/w_e'
} ExtU_uav_fdm3d_T;

// External outputs (root outports fed by signals with default storage)
typedef struct {
  real_T time_stamp;                   // '<Root>/time_stamp'
  real_T lat;                          // '<Root>/lat'
  real_T lon;                          // '<Root>/lon'
  real_T ASL;                          // '<Root>/ASL'
  real_T Vn;                           // '<Root>/Vn'
  real_T Ve;                           // '<Root>/Ve'
  real_T hdot;                         // '<Root>/hdot'
  real_T phi;                          // '<Root>/phi'
  real_T psi_t;                        // '<Root>/psi_t'
  real_T gamma;                        // '<Root>/gamma'
  real_T gs;                           // '<Root>/gs'
  real_T tas;                          // '<Root>/tas'
} ExtY_uav_fdm3d_T;

// Parameters (default storage)
struct P_uav_fdm3d_T_ {
  real_T Alt0;                         // Variable: Alt0
                                       //  Referenced by: '<S1>/Integrator2'

  real_T LatLon0[2];                   // Variable: LatLon0
                                       //  Referenced by: '<S7>/initial_pos'

  real_T gamma0;                       // Variable: gamma0
                                       //  Referenced by:
                                       //    '<S2>/Constant'
                                       //    '<S2>/Integrator'
                                       //    '<S30>/int_q'

  real_T gs0;                          // Variable: gs0
                                       //  Referenced by: '<S6>/Integrator'

  real_T hdot_max;                     // Variable: hdot_max
                                       //  Referenced by: '<Root>/Saturation1'

  real_T hdot_min;                     // Variable: hdot_min
                                       //  Referenced by: '<Root>/Saturation1'

  real_T k_gamma;                      // Variable: k_gamma
                                       //  Referenced by: '<S2>/Gain'

  real_T k_phi;                        // Variable: k_phi
                                       //  Referenced by: '<S4>/Gain1'

  real_T k_tht;                        // Variable: k_tht
                                       //  Referenced by: '<S30>/Gain2'

  real_T p_max;                        // Variable: p_max
                                       //  Referenced by: '<S4>/Saturation3'

  real_T phi0;                         // Variable: phi0
                                       //  Referenced by: '<S4>/Integrator1'

  real_T phi_max;                      // Variable: phi_max
                                       //  Referenced by: '<Root>/Saturation2'

  real_T psi0;                         // Variable: psi0
                                       //  Referenced by: '<S5>/Integrator1'

  real_T tas_max;                      // Variable: tas_max
                                       //  Referenced by: '<Root>/Saturation'

  real_T tas_min;                      // Variable: tas_min
                                       //  Referenced by: '<Root>/Saturation'

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
  real_T odeY[13];
  real_T odeF[3][13];
  ODE3_IntgData intgData;

  //
  //  DataMapInfo:
  //  The following substructure contains information regarding
  //  structures generated in the model's C API.

  struct {
    rtwCAPI_ModelMappingInfo mmi;
    void* dataAddress[15];
    int32_T* vardimsAddress[15];
    RTWLoggingFcnPtr loggingPtrs[15];
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
    boolean_T firstInitCondFlag;
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
  PeriodicIndX_uav_fdm3d_T uav_fdm3d_PeriodicIndX;// Block periodic continuous states 
  PeriodicRngX_uav_fdm3d_T uav_fdm3d_PeriodicRngX;

  // Real-Time Model
  RT_MODEL_uav_fdm3d_T uav_fdm3d_M;

  // Continuous states update member function
  void rt_ertODEUpdateContinuousStates(RTWSolverInfo *si );

  // Derivatives member function
  void uav_fdm3d_derivatives();
};

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
//  '<S1>'   : 'uav_fdm3d/Position'
//  '<S2>'   : 'uav_fdm3d/gamma_dyn'
//  '<S3>'   : 'uav_fdm3d/gs2tas'
//  '<S4>'   : 'uav_fdm3d/phi_dyn'
//  '<S5>'   : 'uav_fdm3d/psi_dyn'
//  '<S6>'   : 'uav_fdm3d/v_dyn'
//  '<S7>'   : 'uav_fdm3d/Position/Flat Earth to LLA'
//  '<S8>'   : 'uav_fdm3d/Position/Flat Earth to LLA/LatLong wrap'
//  '<S9>'   : 'uav_fdm3d/Position/Flat Earth to LLA/LatLong wrap1'
//  '<S10>'  : 'uav_fdm3d/Position/Flat Earth to LLA/LongLat_offset'
//  '<S11>'  : 'uav_fdm3d/Position/Flat Earth to LLA/pos_deg'
//  '<S12>'  : 'uav_fdm3d/Position/Flat Earth to LLA/LatLong wrap/Latitude Wrap 90'
//  '<S13>'  : 'uav_fdm3d/Position/Flat Earth to LLA/LatLong wrap/Wrap Longitude'
//  '<S14>'  : 'uav_fdm3d/Position/Flat Earth to LLA/LatLong wrap/Latitude Wrap 90/Compare To Constant'
//  '<S15>'  : 'uav_fdm3d/Position/Flat Earth to LLA/LatLong wrap/Latitude Wrap 90/Wrap Angle 180'
//  '<S16>'  : 'uav_fdm3d/Position/Flat Earth to LLA/LatLong wrap/Latitude Wrap 90/Wrap Angle 180/Compare To Constant'
//  '<S17>'  : 'uav_fdm3d/Position/Flat Earth to LLA/LatLong wrap/Wrap Longitude/Compare To Constant'
//  '<S18>'  : 'uav_fdm3d/Position/Flat Earth to LLA/LatLong wrap1/Latitude Wrap 90'
//  '<S19>'  : 'uav_fdm3d/Position/Flat Earth to LLA/LatLong wrap1/Wrap Longitude'
//  '<S20>'  : 'uav_fdm3d/Position/Flat Earth to LLA/LatLong wrap1/Latitude Wrap 90/Compare To Constant'
//  '<S21>'  : 'uav_fdm3d/Position/Flat Earth to LLA/LatLong wrap1/Latitude Wrap 90/Wrap Angle 180'
//  '<S22>'  : 'uav_fdm3d/Position/Flat Earth to LLA/LatLong wrap1/Latitude Wrap 90/Wrap Angle 180/Compare To Constant'
//  '<S23>'  : 'uav_fdm3d/Position/Flat Earth to LLA/LatLong wrap1/Wrap Longitude/Compare To Constant'
//  '<S24>'  : 'uav_fdm3d/Position/Flat Earth to LLA/LongLat_offset/Angle Conversion2'
//  '<S25>'  : 'uav_fdm3d/Position/Flat Earth to LLA/LongLat_offset/Find Radian//Distance'
//  '<S26>'  : 'uav_fdm3d/Position/Flat Earth to LLA/LongLat_offset/Find Radian//Distance/Angle Conversion2'
//  '<S27>'  : 'uav_fdm3d/Position/Flat Earth to LLA/LongLat_offset/Find Radian//Distance/denom'
//  '<S28>'  : 'uav_fdm3d/Position/Flat Earth to LLA/LongLat_offset/Find Radian//Distance/e'
//  '<S29>'  : 'uav_fdm3d/Position/Flat Earth to LLA/LongLat_offset/Find Radian//Distance/e^4'
//  '<S30>'  : 'uav_fdm3d/gamma_dyn/tht_dyn'

#endif                                 // RTW_HEADER_uav_fdm3d_h_

//
// File trailer for generated code.
//
// [EOF]
//
