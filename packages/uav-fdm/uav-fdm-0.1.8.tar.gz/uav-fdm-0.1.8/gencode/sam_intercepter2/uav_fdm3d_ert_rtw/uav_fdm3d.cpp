//
// File: uav_fdm3d.cpp
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
#include "uav_fdm3d_capi.h"
#include "uav_fdm3d.h"
#include "uav_fdm3d_private.h"

// State reduction function
void local_stateReduction(real_T* x, int_T* p, int_T n, real_T* r)
{
  int_T i, j;
  for (i = 0, j = 0; i < n; ++i, ++j) {
    int_T k = p[i];
    real_T lb = r[j++];
    real_T xk = x[k]-lb;
    real_T rk = r[j]-lb;
    int_T q = (int_T) std::floor(xk/rk);
    if (q) {
      x[k] = xk-q*rk+lb;
    }
  }
}

//
// This function updates continuous states using the ODE3 fixed-step
// solver algorithm
//
void uav_fdmModelClass::rt_ertODEUpdateContinuousStates(RTWSolverInfo *si )
{
  // Solver Matrices
  static const real_T rt_ODE3_A[3] = {
    1.0/2.0, 3.0/4.0, 1.0
  };

  static const real_T rt_ODE3_B[3][3] = {
    { 1.0/2.0, 0.0, 0.0 },

    { 0.0, 3.0/4.0, 0.0 },

    { 2.0/9.0, 1.0/3.0, 4.0/9.0 }
  };

  time_T t = rtsiGetT(si);
  time_T tnew = rtsiGetSolverStopTime(si);
  time_T h = rtsiGetStepSize(si);
  real_T *x = rtsiGetContStates(si);
  ODE3_IntgData *id = (ODE3_IntgData *)rtsiGetSolverData(si);
  real_T *y = id->y;
  real_T *f0 = id->f[0];
  real_T *f1 = id->f[1];
  real_T *f2 = id->f[2];
  real_T hB[3];
  int_T i;
  int_T nXc = 13;
  rtsiSetSimTimeStep(si,MINOR_TIME_STEP);

  // Save the state values at time t in y, we'll use x as ynew.
  (void) memcpy(y, x,
                (uint_T)nXc*sizeof(real_T));

  // Assumes that rtsiSetT and ModelOutputs are up-to-date
  // f0 = f(t,y)
  rtsiSetdX(si, f0);
  uav_fdm3d_derivatives();

  // f(:,2) = feval(odefile, t + hA(1), y + f*hB(:,1), args(:)(*));
  hB[0] = h * rt_ODE3_B[0][0];
  for (i = 0; i < nXc; i++) {
    x[i] = y[i] + (f0[i]*hB[0]);
  }

  rtsiSetT(si, t + h*rt_ODE3_A[0]);
  rtsiSetdX(si, f1);
  this->step();
  uav_fdm3d_derivatives();

  // f(:,3) = feval(odefile, t + hA(2), y + f*hB(:,2), args(:)(*));
  for (i = 0; i <= 1; i++) {
    hB[i] = h * rt_ODE3_B[1][i];
  }

  for (i = 0; i < nXc; i++) {
    x[i] = y[i] + (f0[i]*hB[0] + f1[i]*hB[1]);
  }

  rtsiSetT(si, t + h*rt_ODE3_A[1]);
  rtsiSetdX(si, f2);
  this->step();
  uav_fdm3d_derivatives();

  // tnew = t + hA(3);
  // ynew = y + f*hB(:,3);
  for (i = 0; i <= 2; i++) {
    hB[i] = h * rt_ODE3_B[2][i];
  }

  for (i = 0; i < nXc; i++) {
    x[i] = y[i] + (f0[i]*hB[0] + f1[i]*hB[1] + f2[i]*hB[2]);
  }

  rtsiSetT(si, tnew);
  local_stateReduction(x, rtsiGetPeriodicContStateIndices(si), 1,
                       rtsiGetPeriodicContStateRanges(si));
  rtsiSetSimTimeStep(si,MAJOR_TIME_STEP);
}

real_T rt_modd(real_T u0, real_T u1)
{
  real_T y;
  boolean_T yEq;
  real_T q;
  y = u0;
  if (u0 == 0.0) {
    y = 0.0;
  } else {
    if (u1 != 0.0) {
      y = std::fmod(u0, u1);
      yEq = (y == 0.0);
      if ((!yEq) && (u1 > std::floor(u1))) {
        q = std::abs(u0 / u1);
        yEq = (std::abs(q - std::floor(q + 0.5)) <= DBL_EPSILON * q);
      }

      if (yEq) {
        y = 0.0;
      } else {
        if ((u0 < 0.0) != (u1 < 0.0)) {
          y += u1;
        }
      }
    }
  }

  return y;
}

// Model step function
void uav_fdmModelClass::step()
{
  boolean_T rtb_Compare_d;
  real_T rtb_Abs1;
  real_T rtb_Sum1_b;
  real_T rtb_Abs;
  int32_T rtb_Compare_o;
  if (rtmIsMajorTimeStep((&uav_fdm3d_M))) {
    // set solver stop time
    rtsiSetSolverStopTime(&(&uav_fdm3d_M)->solverInfo,(((&uav_fdm3d_M)
      ->Timing.clockTick0+1)*(&uav_fdm3d_M)->Timing.stepSize0));
  }                                    // end MajorTimeStep

  // Update absolute time of base rate at minor time step
  if (rtmIsMinorTimeStep((&uav_fdm3d_M))) {
    (&uav_fdm3d_M)->Timing.t[0] = rtsiGetT(&(&uav_fdm3d_M)->solverInfo);
  }

  if (rtmIsMajorTimeStep((&uav_fdm3d_M))) {
    // Switch: '<S21>/Switch' incorporates:
    //   Abs: '<S21>/Abs'
    //   Constant: '<S22>/Constant'
    //   Constant: '<S7>/initial_pos'
    //   RelationalOperator: '<S22>/Compare'

    if (std::abs(uav_fdm3d_P.LatLon0[0]) > 180.0) {
      // Signum: '<S18>/Sign1' incorporates:
      //   Bias: '<S21>/Bias'
      //   Bias: '<S21>/Bias1'
      //   Constant: '<S21>/Constant2'
      //   Math: '<S21>/Math Function1'

      uav_fdm3d_B.Switch = rt_modd(uav_fdm3d_P.LatLon0[0] + 180.0, 360.0) +
        -180.0;
    } else {
      // Signum: '<S18>/Sign1'
      uav_fdm3d_B.Switch = uav_fdm3d_P.LatLon0[0];
    }

    // End of Switch: '<S21>/Switch'

    // Abs: '<S18>/Abs1'
    rtb_Abs1 = std::abs(uav_fdm3d_B.Switch);

    // RelationalOperator: '<S20>/Compare' incorporates:
    //   Constant: '<S20>/Constant'

    rtb_Compare_d = (rtb_Abs1 > 90.0);

    // Switch: '<S18>/Switch'
    if (rtb_Compare_d) {
      // Signum: '<S18>/Sign1' incorporates:
      //   Bias: '<S18>/Bias'
      //   Bias: '<S18>/Bias1'
      //   Gain: '<S18>/Gain'
      //   Product: '<S18>/Divide1'

      if (uav_fdm3d_B.Switch < 0.0) {
        uav_fdm3d_B.Switch = -1.0;
      } else {
        if (uav_fdm3d_B.Switch > 0.0) {
          uav_fdm3d_B.Switch = 1.0;
        }
      }

      uav_fdm3d_B.Switch *= -(rtb_Abs1 + -90.0) + 90.0;
    }

    // End of Switch: '<S18>/Switch'

    // UnitConversion: '<S26>/Unit Conversion'
    // Unit Conversion - from: deg to: rad
    // Expression: output = (0.0174533*input) + (0)
    rtb_Abs1 = 0.017453292519943295 * uav_fdm3d_B.Switch;

    // Trigonometry: '<S27>/Trigonometric Function1'
    rtb_Sum1_b = std::sin(rtb_Abs1);

    // Sum: '<S27>/Sum1' incorporates:
    //   Constant: '<S27>/Constant'
    //   Product: '<S27>/Product1'

    rtb_Sum1_b = 1.0 - uav_fdm3d_ConstB.sqrt_m * uav_fdm3d_ConstB.sqrt_m *
      rtb_Sum1_b * rtb_Sum1_b;

    // Product: '<S25>/Product1' incorporates:
    //   Constant: '<S25>/Constant1'
    //   Sqrt: '<S25>/sqrt'

    rtb_Abs = 6.378137E+6 / std::sqrt(rtb_Sum1_b);

    // Trigonometry: '<S25>/Trigonometric Function1' incorporates:
    //   Product: '<S25>/Product3'

    uav_fdm3d_B.TrigonometricFunction1 = atan2(1.0, rtb_Abs *
      uav_fdm3d_ConstB.Sum1_l / rtb_Sum1_b);

    // Trigonometry: '<S25>/Trigonometric Function2' incorporates:
    //   Product: '<S25>/Product4'
    //   Trigonometry: '<S25>/Trigonometric Function'

    uav_fdm3d_B.TrigonometricFunction2 = atan2(1.0, rtb_Abs * std::cos(rtb_Abs1));

    // Switch: '<S9>/Switch1' incorporates:
    //   Constant: '<S9>/Constant'
    //   Constant: '<S9>/Constant1'

    if (rtb_Compare_d) {
      rtb_Compare_o = 180;
    } else {
      rtb_Compare_o = 0;
    }

    // End of Switch: '<S9>/Switch1'

    // Sum: '<S9>/Sum' incorporates:
    //   Constant: '<S7>/initial_pos'

    uav_fdm3d_B.Switch_h = (real_T)rtb_Compare_o + uav_fdm3d_P.LatLon0[1];

    // Switch: '<S19>/Switch' incorporates:
    //   Abs: '<S19>/Abs'
    //   Bias: '<S19>/Bias'
    //   Bias: '<S19>/Bias1'
    //   Constant: '<S19>/Constant2'
    //   Constant: '<S23>/Constant'
    //   Math: '<S19>/Math Function1'
    //   RelationalOperator: '<S23>/Compare'

    if (std::abs(uav_fdm3d_B.Switch_h) > 180.0) {
      uav_fdm3d_B.Switch_h = rt_modd(uav_fdm3d_B.Switch_h + 180.0, 360.0) +
        -180.0;
    }

    // End of Switch: '<S19>/Switch'
  }

  // Sum: '<S7>/Sum' incorporates:
  //   Integrator: '<S1>/Integrator3'
  //   Integrator: '<S1>/Integrator5'
  //   Product: '<S10>/rad lat'
  //   Product: '<S10>/x*cos'
  //   Product: '<S10>/y*sin'
  //   Sum: '<S10>/Sum'
  //   UnitConversion: '<S11>/Unit Conversion'

  // Unit Conversion - from: rad to: deg
  // Expression: output = (57.2958*input) + (0)
  uav_fdm3d_Y.lat = (uav_fdm3d_X.Xn * uav_fdm3d_ConstB.SinCos_o2 -
                     uav_fdm3d_X.Xe * uav_fdm3d_ConstB.SinCos_o1) *
    uav_fdm3d_B.TrigonometricFunction1 * 57.295779513082323 + uav_fdm3d_B.Switch;

  // Switch: '<S15>/Switch' incorporates:
  //   Abs: '<S15>/Abs'
  //   Constant: '<S16>/Constant'
  //   RelationalOperator: '<S16>/Compare'

  if (std::abs(uav_fdm3d_Y.lat) > 180.0) {
    // Sum: '<S7>/Sum' incorporates:
    //   Bias: '<S15>/Bias'
    //   Bias: '<S15>/Bias1'
    //   Constant: '<S15>/Constant2'
    //   Math: '<S15>/Math Function1'

    uav_fdm3d_Y.lat = rt_modd(uav_fdm3d_Y.lat + 180.0, 360.0) + -180.0;
  }

  // End of Switch: '<S15>/Switch'

  // Abs: '<S12>/Abs1'
  rtb_Abs1 = std::abs(uav_fdm3d_Y.lat);

  // Switch: '<S12>/Switch' incorporates:
  //   Constant: '<S14>/Constant'
  //   Constant: '<S8>/Constant'
  //   Constant: '<S8>/Constant1'
  //   RelationalOperator: '<S14>/Compare'
  //   Switch: '<S8>/Switch1'

  if (rtb_Abs1 > 90.0) {
    // Signum: '<S12>/Sign1'
    if (uav_fdm3d_Y.lat < 0.0) {
      // Sum: '<S7>/Sum'
      uav_fdm3d_Y.lat = -1.0;
    } else {
      if (uav_fdm3d_Y.lat > 0.0) {
        // Sum: '<S7>/Sum'
        uav_fdm3d_Y.lat = 1.0;
      }
    }

    // End of Signum: '<S12>/Sign1'

    // Sum: '<S7>/Sum' incorporates:
    //   Bias: '<S12>/Bias'
    //   Bias: '<S12>/Bias1'
    //   Gain: '<S12>/Gain'
    //   Outport: '<Root>/lat'
    //   Product: '<S12>/Divide1'

    uav_fdm3d_Y.lat *= -(rtb_Abs1 + -90.0) + 90.0;
    rtb_Compare_o = 180;
  } else {
    rtb_Compare_o = 0;
  }

  // End of Switch: '<S12>/Switch'

  // Sum: '<S8>/Sum' incorporates:
  //   Integrator: '<S1>/Integrator3'
  //   Integrator: '<S1>/Integrator5'
  //   Product: '<S10>/rad long '
  //   Product: '<S10>/x*sin'
  //   Product: '<S10>/y*cos'
  //   Sum: '<S10>/Sum1'
  //   Sum: '<S7>/Sum'
  //   UnitConversion: '<S11>/Unit Conversion'

  uav_fdm3d_Y.lon = ((uav_fdm3d_X.Xn * uav_fdm3d_ConstB.SinCos_o1 +
                      uav_fdm3d_X.Xe * uav_fdm3d_ConstB.SinCos_o2) *
                     uav_fdm3d_B.TrigonometricFunction2 * 57.295779513082323 +
                     uav_fdm3d_B.Switch_h) + (real_T)rtb_Compare_o;

  // Switch: '<S13>/Switch' incorporates:
  //   Abs: '<S13>/Abs'
  //   Constant: '<S17>/Constant'
  //   RelationalOperator: '<S17>/Compare'

  if (std::abs(uav_fdm3d_Y.lon) > 180.0) {
    // Outport: '<Root>/lon' incorporates:
    //   Bias: '<S13>/Bias'
    //   Bias: '<S13>/Bias1'
    //   Constant: '<S13>/Constant2'
    //   Math: '<S13>/Math Function1'

    uav_fdm3d_Y.lon = rt_modd(uav_fdm3d_Y.lon + 180.0, 360.0) + -180.0;
  }

  // End of Switch: '<S13>/Switch'

  // Outport: '<Root>/time_stamp' incorporates:
  //   Clock: '<Root>/Clock'

  uav_fdm3d_Y.time_stamp = (&uav_fdm3d_M)->Timing.t[0];

  // Outport: '<Root>/ASL' incorporates:
  //   Integrator: '<S1>/Integrator2'

  uav_fdm3d_Y.ASL = uav_fdm3d_X.h;

  // Product: '<S6>/Product' incorporates:
  //   Integrator: '<S2>/Integrator'
  //   Integrator: '<S6>/Integrator'
  //   Trigonometry: '<S6>/Cos'

  uav_fdm3d_Y.gs = uav_fdm3d_X.Integrator_CSTATE * std::cos
    (uav_fdm3d_X.Integrator_CSTATE_a);

  // Product: '<S3>/Product1' incorporates:
  //   Integrator: '<S5>/Integrator1'
  //   Trigonometry: '<S3>/Cos'

  uav_fdm3d_B.Product1 = std::cos(uav_fdm3d_X.Integrator1_CSTATE) *
    uav_fdm3d_Y.gs;

  // Outport: '<Root>/Vn'
  uav_fdm3d_Y.Vn = uav_fdm3d_B.Product1;

  // Sum: '<S3>/Sum5' incorporates:
  //   Inport: '<Root>/w_n'

  uav_fdm3d_Y.tas = uav_fdm3d_B.Product1 + uav_fdm3d_U.w_n;

  // Math: '<S3>/Math Function1'
  rtb_Abs1 = uav_fdm3d_Y.tas * uav_fdm3d_Y.tas;

  // Product: '<S3>/Product' incorporates:
  //   Integrator: '<S5>/Integrator1'
  //   Trigonometry: '<S3>/Sin'

  uav_fdm3d_B.Product = std::sin(uav_fdm3d_X.Integrator1_CSTATE) *
    uav_fdm3d_Y.gs;

  // Sum: '<S3>/Sum4' incorporates:
  //   Inport: '<Root>/w_e'

  uav_fdm3d_Y.tas = uav_fdm3d_B.Product + uav_fdm3d_U.w_e;

  // Product: '<S3>/Product2' incorporates:
  //   Integrator: '<S2>/Integrator'
  //   Trigonometry: '<S3>/Tan'

  uav_fdm3d_B.Product2 = uav_fdm3d_Y.gs * std::tan
    (uav_fdm3d_X.Integrator_CSTATE_a);

  // Sqrt: '<S3>/Sqrt' incorporates:
  //   Math: '<S3>/Math Function'
  //   Math: '<S3>/Math Function2'
  //   Sum: '<S3>/Sum6'

  uav_fdm3d_Y.tas = std::sqrt((uav_fdm3d_Y.tas * uav_fdm3d_Y.tas + rtb_Abs1) +
    uav_fdm3d_B.Product2 * uav_fdm3d_B.Product2);

  // Saturate: '<Root>/Saturation' incorporates:
  //   Inport: '<Root>/tas_c'

  if (uav_fdm3d_U.tas_c > uav_fdm3d_P.tas_max) {
    rtb_Abs1 = uav_fdm3d_P.tas_max;
  } else if (uav_fdm3d_U.tas_c < uav_fdm3d_P.tas_min) {
    rtb_Abs1 = uav_fdm3d_P.tas_min;
  } else {
    rtb_Abs1 = uav_fdm3d_U.tas_c;
  }

  // End of Saturate: '<Root>/Saturation'

  // Gain: '<S6>/Gain1' incorporates:
  //   Gain: '<S6>/Gain'
  //   Sum: '<S6>/Sum'

  uav_fdm3d_B.Gain1 = (rtb_Abs1 - uav_fdm3d_Y.tas) * 1.6 * 0.625;

  // Gain: '<S6>/Gain2' incorporates:
  //   Gain: '<S6>/Gain4'

  uav_fdm3d_B.p_c = 1.6 * -uav_fdm3d_Y.tas;

  // Integrator: '<S6>/Integrator1' incorporates:
  //   Gain: '<S6>/Gain5'

  if (uav_fdm3d_DW.Integrator1_IWORK != 0) {
    uav_fdm3d_X.Integrator1_CSTATE_g = -uav_fdm3d_B.p_c;
  }

  // Sum: '<S6>/Sum1' incorporates:
  //   Integrator: '<S6>/Integrator1'

  uav_fdm3d_B.at_c = uav_fdm3d_B.p_c + uav_fdm3d_X.Integrator1_CSTATE_g;

  // Outport: '<Root>/hdot'
  uav_fdm3d_Y.hdot = uav_fdm3d_B.Product2;

  // Outport: '<Root>/Ve'
  uav_fdm3d_Y.Ve = uav_fdm3d_B.Product;

  // Saturate: '<Root>/Saturation1' incorporates:
  //   Inport: '<Root>/hdot_c'

  if (uav_fdm3d_U.hdot_c > uav_fdm3d_P.hdot_max) {
    rtb_Abs1 = uav_fdm3d_P.hdot_max;
  } else if (uav_fdm3d_U.hdot_c < uav_fdm3d_P.hdot_min) {
    rtb_Abs1 = uav_fdm3d_P.hdot_min;
  } else {
    rtb_Abs1 = uav_fdm3d_U.hdot_c;
  }

  // End of Saturate: '<Root>/Saturation1'

  // Gain: '<S2>/Gain' incorporates:
  //   Integrator: '<S2>/Integrator'
  //   Sum: '<S2>/Sum'
  //   Trigonometry: '<Root>/Atan2'

  uav_fdm3d_B.p_c = (atan2(rtb_Abs1, uav_fdm3d_Y.gs) -
                     uav_fdm3d_X.Integrator_CSTATE_a) * uav_fdm3d_P.k_gamma;

  // Gain: '<S2>/Gain1'
  uav_fdm3d_B.Gain1_o = 3.0 * uav_fdm3d_B.p_c;

  // Integrator: '<S2>/Integrator1' incorporates:
  //   Constant: '<S2>/Constant'
  //   Sum: '<S2>/Sum3'

  if (uav_fdm3d_DW.Integrator1_IWORK_m != 0) {
    uav_fdm3d_X.Integrator1_CSTATE_n = uav_fdm3d_P.gamma0 - uav_fdm3d_B.p_c;
  }

  // Gain: '<S30>/Gain2' incorporates:
  //   Integrator: '<S2>/Integrator1'
  //   Integrator: '<S30>/int_q'
  //   Sum: '<S2>/Sum1'
  //   Sum: '<S30>/Sum2'

  uav_fdm3d_B.q_c = ((uav_fdm3d_B.p_c + uav_fdm3d_X.Integrator1_CSTATE_n) -
                     uav_fdm3d_X.int_q_CSTATE) * uav_fdm3d_P.k_tht;

  // Gain: '<S2>/Gain2' incorporates:
  //   Integrator: '<S2>/Integrator'
  //   Integrator: '<S30>/int_q'
  //   Sum: '<S2>/Sum2'

  uav_fdm3d_B.Gain2 = (uav_fdm3d_X.int_q_CSTATE -
                       uav_fdm3d_X.Integrator_CSTATE_a) * 3.0;

  // Product: '<S5>/Divide' incorporates:
  //   Gain: '<S5>/Gain'
  //   Integrator: '<S4>/Integrator1'
  //   Trigonometry: '<S5>/Tan'

  uav_fdm3d_B.psidot = 9.8 * std::tan(uav_fdm3d_X.Integrator1_CSTATE_a) /
    uav_fdm3d_Y.gs;

  // Outport: '<Root>/phi' incorporates:
  //   Integrator: '<S4>/Integrator1'

  uav_fdm3d_Y.phi = uav_fdm3d_X.Integrator1_CSTATE_a;

  // Saturate: '<Root>/Saturation2' incorporates:
  //   Inport: '<Root>/phi_c'

  if (uav_fdm3d_U.phi_c > uav_fdm3d_P.phi_max) {
    rtb_Abs1 = uav_fdm3d_P.phi_max;
  } else if (uav_fdm3d_U.phi_c < -uav_fdm3d_P.phi_max) {
    rtb_Abs1 = -uav_fdm3d_P.phi_max;
  } else {
    rtb_Abs1 = uav_fdm3d_U.phi_c;
  }

  // End of Saturate: '<Root>/Saturation2'

  // Gain: '<S4>/Gain1' incorporates:
  //   Integrator: '<S4>/Integrator1'
  //   Sum: '<S4>/Sum1'

  uav_fdm3d_B.p_c = (rtb_Abs1 - uav_fdm3d_X.Integrator1_CSTATE_a) *
    uav_fdm3d_P.k_phi;

  // Saturate: '<S4>/Saturation3'
  if (uav_fdm3d_B.p_c > uav_fdm3d_P.p_max) {
    uav_fdm3d_B.p_c = uav_fdm3d_P.p_max;
  } else {
    if (uav_fdm3d_B.p_c < -uav_fdm3d_P.p_max) {
      uav_fdm3d_B.p_c = -uav_fdm3d_P.p_max;
    }
  }

  // End of Saturate: '<S4>/Saturation3'

  // Outport: '<Root>/gamma' incorporates:
  //   Integrator: '<S2>/Integrator'

  uav_fdm3d_Y.gamma = uav_fdm3d_X.Integrator_CSTATE_a;

  // Sum: '<S6>/Sum3' incorporates:
  //   Gain: '<S6>/Gain3'
  //   Integrator: '<S2>/Integrator'
  //   TransferFcn: '<S6>/Transfer Fcn'
  //   Trigonometry: '<S6>/Sin'

  uav_fdm3d_B.Sum3_n = 3.0 * uav_fdm3d_X.TransferFcn_CSTATE - 9.8 * std::sin
    (uav_fdm3d_X.Integrator_CSTATE_a);

  // Outport: '<Root>/psi_t' incorporates:
  //   Integrator: '<S5>/Integrator1'

  uav_fdm3d_Y.psi_t = uav_fdm3d_X.Integrator1_CSTATE;

  // TransferFcn: '<S30>/q_dyn'
  uav_fdm3d_B.q = 0.0;
  uav_fdm3d_B.q += 7.0 * uav_fdm3d_X.q_dyn_CSTATE;

  // TransferFcn: '<S4>/p_ctrl'
  uav_fdm3d_B.p = 0.0;
  uav_fdm3d_B.p += 6.0 * uav_fdm3d_X.p_ctrl_CSTATE;
  if (rtmIsMajorTimeStep((&uav_fdm3d_M))) {
    // Update for Integrator: '<S6>/Integrator1'
    uav_fdm3d_DW.Integrator1_IWORK = 0;

    // Update for Integrator: '<S2>/Integrator1'
    uav_fdm3d_DW.Integrator1_IWORK_m = 0;
  }                                    // end MajorTimeStep

  if (rtmIsMajorTimeStep((&uav_fdm3d_M))) {
    rt_ertODEUpdateContinuousStates(&(&uav_fdm3d_M)->solverInfo);

    // Update absolute time for base rate
    // The "clockTick0" counts the number of times the code of this task has
    //  been executed. The absolute time is the multiplication of "clockTick0"
    //  and "Timing.stepSize0". Size of "clockTick0" ensures timer will not
    //  overflow during the application lifespan selected.

    ++(&uav_fdm3d_M)->Timing.clockTick0;
    (&uav_fdm3d_M)->Timing.t[0] = rtsiGetSolverStopTime(&(&uav_fdm3d_M)
      ->solverInfo);

    {
      // Update absolute timer for sample time: [0.05s, 0.0s]
      // The "clockTick1" counts the number of times the code of this task has
      //  been executed. The resolution of this integer timer is 0.05, which is the step size
      //  of the task. Size of "clockTick1" ensures timer will not overflow during the
      //  application lifespan selected.

      (&uav_fdm3d_M)->Timing.clockTick1++;
    }
  }                                    // end MajorTimeStep
}

// Derivatives for root system: '<Root>'
void uav_fdmModelClass::uav_fdm3d_derivatives()
{
  XDot_uav_fdm3d_T *_rtXdot;
  _rtXdot = ((XDot_uav_fdm3d_T *) (&uav_fdm3d_M)->derivs);

  // Derivatives for Integrator: '<S1>/Integrator3'
  _rtXdot->Xn = uav_fdm3d_B.Product1;

  // Derivatives for Integrator: '<S1>/Integrator5'
  _rtXdot->Xe = uav_fdm3d_B.Product;

  // Derivatives for Integrator: '<S1>/Integrator2'
  _rtXdot->h = uav_fdm3d_B.Product2;

  // Derivatives for Integrator: '<S5>/Integrator1'
  _rtXdot->Integrator1_CSTATE = uav_fdm3d_B.psidot;

  // Derivatives for Integrator: '<S6>/Integrator'
  _rtXdot->Integrator_CSTATE = uav_fdm3d_B.Sum3_n;

  // Derivatives for Integrator: '<S2>/Integrator'
  _rtXdot->Integrator_CSTATE_a = uav_fdm3d_B.Gain2;

  // Derivatives for Integrator: '<S6>/Integrator1'
  _rtXdot->Integrator1_CSTATE_g = uav_fdm3d_B.Gain1;

  // Derivatives for Integrator: '<S2>/Integrator1'
  _rtXdot->Integrator1_CSTATE_n = uav_fdm3d_B.Gain1_o;

  // Derivatives for Integrator: '<S30>/int_q'
  _rtXdot->int_q_CSTATE = uav_fdm3d_B.q;

  // Derivatives for Integrator: '<S4>/Integrator1'
  _rtXdot->Integrator1_CSTATE_a = uav_fdm3d_B.p;

  // Derivatives for TransferFcn: '<S6>/Transfer Fcn'
  _rtXdot->TransferFcn_CSTATE = 0.0;
  _rtXdot->TransferFcn_CSTATE += -3.0 * uav_fdm3d_X.TransferFcn_CSTATE;
  _rtXdot->TransferFcn_CSTATE += uav_fdm3d_B.at_c;

  // Derivatives for TransferFcn: '<S30>/q_dyn'
  _rtXdot->q_dyn_CSTATE = 0.0;
  _rtXdot->q_dyn_CSTATE += -7.0 * uav_fdm3d_X.q_dyn_CSTATE;
  _rtXdot->q_dyn_CSTATE += uav_fdm3d_B.q_c;

  // Derivatives for TransferFcn: '<S4>/p_ctrl'
  _rtXdot->p_ctrl_CSTATE = 0.0;
  _rtXdot->p_ctrl_CSTATE += -6.0 * uav_fdm3d_X.p_ctrl_CSTATE;
  _rtXdot->p_ctrl_CSTATE += uav_fdm3d_B.p_c;
}

// Model initialize function
void uav_fdmModelClass::initialize()
{
  // Registration code

  // initialize real-time model
  (void) memset((void *)(&uav_fdm3d_M), 0,
                sizeof(RT_MODEL_uav_fdm3d_T));

  {
    // Setup solver object
    rtsiSetSimTimeStepPtr(&(&uav_fdm3d_M)->solverInfo, &(&uav_fdm3d_M)
                          ->Timing.simTimeStep);
    rtsiSetTPtr(&(&uav_fdm3d_M)->solverInfo, &rtmGetTPtr((&uav_fdm3d_M)));
    rtsiSetStepSizePtr(&(&uav_fdm3d_M)->solverInfo, &(&uav_fdm3d_M)
                       ->Timing.stepSize0);
    rtsiSetdXPtr(&(&uav_fdm3d_M)->solverInfo, &(&uav_fdm3d_M)->derivs);
    rtsiSetContStatesPtr(&(&uav_fdm3d_M)->solverInfo, (real_T **) &(&uav_fdm3d_M)
                         ->contStates);
    rtsiSetNumContStatesPtr(&(&uav_fdm3d_M)->solverInfo, &(&uav_fdm3d_M)
      ->Sizes.numContStates);
    rtsiSetNumPeriodicContStatesPtr(&(&uav_fdm3d_M)->solverInfo, &(&uav_fdm3d_M
      )->Sizes.numPeriodicContStates);
    rtsiSetPeriodicContStateIndicesPtr(&(&uav_fdm3d_M)->solverInfo,
      &(&uav_fdm3d_M)->periodicContStateIndices);
    rtsiSetPeriodicContStateRangesPtr(&(&uav_fdm3d_M)->solverInfo,
      &(&uav_fdm3d_M)->periodicContStateRanges);
    rtsiSetErrorStatusPtr(&(&uav_fdm3d_M)->solverInfo, (&rtmGetErrorStatus
      ((&uav_fdm3d_M))));
    rtsiSetRTModelPtr(&(&uav_fdm3d_M)->solverInfo, (&uav_fdm3d_M));
  }

  rtsiSetSimTimeStep(&(&uav_fdm3d_M)->solverInfo, MAJOR_TIME_STEP);
  (&uav_fdm3d_M)->intgData.y = (&uav_fdm3d_M)->odeY;
  (&uav_fdm3d_M)->intgData.f[0] = (&uav_fdm3d_M)->odeF[0];
  (&uav_fdm3d_M)->intgData.f[1] = (&uav_fdm3d_M)->odeF[1];
  (&uav_fdm3d_M)->intgData.f[2] = (&uav_fdm3d_M)->odeF[2];
  getRTM()->contStates = ((X_uav_fdm3d_T *) &uav_fdm3d_X);
  getRTM()->periodicContStateIndices = ((int_T*) uav_fdm3d_PeriodicIndX);
  getRTM()->periodicContStateRanges = ((real_T*) uav_fdm3d_PeriodicRngX);
  rtsiSetSolverData(&(&uav_fdm3d_M)->solverInfo, (void *)&(&uav_fdm3d_M)
                    ->intgData);
  rtsiSetSolverName(&(&uav_fdm3d_M)->solverInfo,"ode3");
  rtmSetTPtr(getRTM(), &(&uav_fdm3d_M)->Timing.tArray[0]);
  (&uav_fdm3d_M)->Timing.stepSize0 = 0.05;
  rtmSetFirstInitCond(getRTM(), 1);

  // block I/O
  (void) memset(((void *) &uav_fdm3d_B), 0,
                sizeof(B_uav_fdm3d_T));

  // states (continuous)
  {
    (void) memset((void *)&uav_fdm3d_X, 0,
                  sizeof(X_uav_fdm3d_T));
  }

  // Periodic continuous states
  {
    (void) memset((void*) uav_fdm3d_PeriodicIndX, 0,
                  1*sizeof(int_T));
    (void) memset((void*) uav_fdm3d_PeriodicRngX, 0,
                  2*sizeof(real_T));
  }

  // states (dwork)
  (void) memset((void *)&uav_fdm3d_DW, 0,
                sizeof(DW_uav_fdm3d_T));

  // external inputs
  (void)memset(&uav_fdm3d_U, 0, sizeof(ExtU_uav_fdm3d_T));

  // external outputs
  (void) memset((void *)&uav_fdm3d_Y, 0,
                sizeof(ExtY_uav_fdm3d_T));

  // Initialize DataMapInfo substructure containing ModelMap for C API
  uav_fdm3d_InitializeDataMapInfo((&uav_fdm3d_M), &uav_fdm3d_P);

  // InitializeConditions for Integrator: '<S1>/Integrator3'
  uav_fdm3d_X.Xn = 0.0;

  // InitializeConditions for Integrator: '<S1>/Integrator5'
  uav_fdm3d_X.Xe = 0.0;

  // InitializeConditions for Integrator: '<S1>/Integrator2'
  uav_fdm3d_X.h = uav_fdm3d_P.Alt0;

  // InitializeConditions for Integrator: '<S5>/Integrator1'
  uav_fdm3d_X.Integrator1_CSTATE = uav_fdm3d_P.psi0;

  // InitializeConditions for Integrator: '<S6>/Integrator'
  uav_fdm3d_X.Integrator_CSTATE = uav_fdm3d_P.gs0;

  // InitializeConditions for Integrator: '<S2>/Integrator'
  uav_fdm3d_X.Integrator_CSTATE_a = uav_fdm3d_P.gamma0;

  // InitializeConditions for Integrator: '<S6>/Integrator1' incorporates:
  //   Integrator: '<S2>/Integrator1'

  if (rtmIsFirstInitCond((&uav_fdm3d_M))) {
    uav_fdm3d_X.Integrator1_CSTATE_g = 0.0;
    uav_fdm3d_X.Integrator1_CSTATE_n = 0.0;
  }

  uav_fdm3d_DW.Integrator1_IWORK = 1;

  // End of InitializeConditions for Integrator: '<S6>/Integrator1'

  // InitializeConditions for Integrator: '<S2>/Integrator1'
  uav_fdm3d_DW.Integrator1_IWORK_m = 1;

  // InitializeConditions for Integrator: '<S30>/int_q'
  uav_fdm3d_X.int_q_CSTATE = uav_fdm3d_P.gamma0;

  // InitializeConditions for Integrator: '<S4>/Integrator1'
  uav_fdm3d_X.Integrator1_CSTATE_a = uav_fdm3d_P.phi0;

  // InitializeConditions for TransferFcn: '<S6>/Transfer Fcn'
  uav_fdm3d_X.TransferFcn_CSTATE = 0.0;

  // InitializeConditions for TransferFcn: '<S30>/q_dyn'
  uav_fdm3d_X.q_dyn_CSTATE = 0.0;

  // InitializeConditions for TransferFcn: '<S4>/p_ctrl'
  uav_fdm3d_X.p_ctrl_CSTATE = 0.0;

  // InitializeConditions for root-level periodic continuous states
  {
    int_T rootPeriodicContStateIndices[1] = { 3 };

    real_T rootPeriodicContStateRanges[2] = { -3.1415926535897931,
      3.1415926535897931 };

    (void) memcpy((void*)uav_fdm3d_PeriodicIndX, rootPeriodicContStateIndices,
                  1*sizeof(int_T));
    (void) memcpy((void*)uav_fdm3d_PeriodicRngX, rootPeriodicContStateRanges,
                  2*sizeof(real_T));
  }

  // set "at time zero" to false
  if (rtmIsFirstInitCond((&uav_fdm3d_M))) {
    rtmSetFirstInitCond(getRTM(), 0);
  }
}

// Model terminate function
void uav_fdmModelClass::terminate()
{
  // (no terminate code required)
}

// Constructor
uav_fdmModelClass::uav_fdmModelClass()
{
  static const P_uav_fdm3d_T uav_fdm3d_P_temp = {
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
  };                                   // Modifiable parameters

  // Initialize tunable parameters
  uav_fdm3d_P = uav_fdm3d_P_temp;
}

// Destructor
uav_fdmModelClass::~uav_fdmModelClass()
{
  // Currently there is no destructor body generated.
}

// Real-Time Model get method
RT_MODEL_uav_fdm3d_T * uav_fdmModelClass::getRTM()
{
  return (&uav_fdm3d_M);
}

//
// File trailer for generated code.
//
// [EOF]
//
