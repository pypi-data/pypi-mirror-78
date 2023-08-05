//
// File: uav_fdm3d.cpp
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
#include "uav_fdm3d_capi.h"
#include "uav_fdm3d.h"
#include "uav_fdm3d_private.h"

//     Initialize pressure and temperature tables.
void InitCalcAtmosCOESA(real_T *temperature76, real_T *pressureRatio76)
{
  if (temperature76[0] != TEMPERATURE0 ) {
    int_T k;
    temperature76[0] = TEMPERATURE0;
    pressureRatio76[0] = 1.0;

    // set up the data at the 1976 altitude breakpoints
    for (k=0; k<(NUM1976PTS-1); k++) {
      if (tempGradient76[k] != 0.0) {
        temperature76[k+1] = temperature76[k] +
          tempGradient76[k]*(altitude76[k+1] - altitude76[k]);
        pressureRatio76[k+1] = pressureRatio76[k] *
          std::exp(std::log(temperature76[k]/temperature76[k+1]) * GMR/
                   tempGradient76[k]);
      } else {
        temperature76[k+1] = temperature76[k];
        pressureRatio76[k+1] = pressureRatio76[k] *
          std::exp((-GMR)*(altitude76[k+1] - altitude76[k])/temperature76[k]);
      }
    }
  }
}

//
//     Using cached pressure and temperature tables, find the
//     working interval and perform logarithmic interpolation.
//
void CalcAtmosCOESA(const real_T *altitude, real_T *temp, real_T *pressure,
                    real_T *density, real_T *speedofsound, real_T *temperature76,
                    real_T *pressureRatio76, int_T numPoints)
{
  int_T i;
  for (i=0; i < numPoints; i++) {
    int_T bottom = 0;
    int_T top = NUM1976PTS-1;
    int_T idx;

    // Find altitude interval using binary search
    //
    //  Deal with the extreme cases first:
    //    if altitude <= altitude76[bottom] then return idx = bottom
    //    if altitude >= altitude76[top]    then return idx = top

    if (altitude[i] <= altitude76[bottom]) {
      idx = bottom;
    } else if (altitude[i] >= altitude76[top]) {
      idx = NUM1976PTS-2;
    } else {
      for (;;) {
        idx = (bottom + top)/2;
        if (altitude[i] < altitude76[idx]) {
          top = idx - 1;
        } else if (altitude[i] >= altitude76[idx+1]) {
          bottom = idx + 1;
        } else {
          // we have altitude76[idx] <= altitude[i] < altitude76[idx+1],
          //  so break and just use idx

          break;
        }
      }
    }

    // Interval has been obtained, now do linear temperature
    //  interpolation and log pressure interpolation.

    if (tempGradient76[idx] != 0.0 ) {
      temp[i] = temperature76[idx] +
        tempGradient76[idx] * (altitude[i] - altitude76[idx]);
      pressure[i] = PRESSURE0 * pressureRatio76[idx] *
        std::pow(temperature76[idx]/temp[i], GMR/tempGradient76[idx]);
    } else {
      temp[i] = temperature76[idx];
      pressure[i] = PRESSURE0 * pressureRatio76[idx] *
        std::exp((-GMR)*(altitude[i] - altitude76[idx]) / temperature76[idx]);
    }

    density[i] = pressure[i] / ((R_HAT/MOL_WT)*temp[i]);
    speedofsound[i] = std::sqrt(GAMMA*temp[i]*(R_HAT/MOL_WT));
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
  int_T nXc = 6;
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
  real_T rtb_radlat;
  real_T rtb_VectorConcatenate[9];
  boolean_T rtb_Compare_d;
  real_T rtb_sincos_o1_idx_1;
  real_T rtb_Product_idx_1;
  real_T y;
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

  // Integrator: '<S3>/hdot'
  uav_fdm3d_B.hdot = uav_fdm3d_X.hdot;

  // Integrator: '<S3>/v_e'
  uav_fdm3d_B.v_e = uav_fdm3d_X.v_e;

  // Integrator: '<S3>/v_n'
  uav_fdm3d_B.v_n = uav_fdm3d_X.v_n;

  // Trigonometry: '<S3>/Trigonometric Function2' incorporates:
  //   Math: '<S3>/Math Function'
  //   Math: '<S3>/Math Function1'
  //   Sqrt: '<S3>/Sqrt'
  //   Sum: '<S3>/Sum'

  rtb_radlat = atan2(uav_fdm3d_B.hdot, std::sqrt(uav_fdm3d_B.v_e *
    uav_fdm3d_B.v_e + uav_fdm3d_B.v_n * uav_fdm3d_B.v_n));

  // Trigonometry: '<S3>/Trigonometric Function1'
  y = atan2(uav_fdm3d_B.v_e, uav_fdm3d_B.v_n);

  // Trigonometry: '<S7>/sincos' incorporates:
  //   Gain: '<S3>/Gain'
  //   Gain: '<S3>/Gain1'

  rtb_Product_idx_1 = std::cos(-rtb_radlat);
  rtb_sincos_o1_idx_1 = std::sin(-rtb_radlat);
  rtb_radlat = std::cos(-y);
  y = std::sin(-y);

  // Fcn: '<S7>/Fcn11'
  rtb_VectorConcatenate[0] = rtb_Product_idx_1 * rtb_radlat;

  // Fcn: '<S7>/Fcn21'
  rtb_VectorConcatenate[1] = -rtb_Product_idx_1 * y;

  // Fcn: '<S7>/Fcn31'
  rtb_VectorConcatenate[2] = rtb_sincos_o1_idx_1;

  // Fcn: '<S7>/Fcn12'
  rtb_VectorConcatenate[3] = y;

  // Fcn: '<S7>/Fcn22'
  rtb_VectorConcatenate[4] = rtb_radlat;

  // Fcn: '<S7>/Fcn32'
  rtb_VectorConcatenate[5] = 0.0;

  // Fcn: '<S7>/Fcn13'
  rtb_VectorConcatenate[6] = -rtb_sincos_o1_idx_1 * rtb_radlat;

  // Fcn: '<S7>/Fcn23'
  rtb_VectorConcatenate[7] = rtb_sincos_o1_idx_1 * y;

  // Fcn: '<S7>/Fcn33'
  rtb_VectorConcatenate[8] = rtb_Product_idx_1;

  // Sum: '<S5>/Sum1' incorporates:
  //   Constant: '<S1>/Constant'
  //   Integrator: '<S3>/Integrator2'

  uav_fdm3d_B.Sum1 = uav_fdm3d_X.h - uav_fdm3d_P.Alt0;

  // Product: '<S3>/Product1'
  for (rtb_Compare_o = 0; rtb_Compare_o < 3; rtb_Compare_o++) {
    uav_fdm3d_B.Product1[rtb_Compare_o] = 0.0;
    uav_fdm3d_B.Product1[rtb_Compare_o] += rtb_VectorConcatenate[rtb_Compare_o] *
      0.0;
    uav_fdm3d_B.Product1[rtb_Compare_o] += rtb_VectorConcatenate[rtb_Compare_o +
      6] * 0.0;
  }

  // End of Product: '<S3>/Product1'

  // Gain: '<S3>/Gain2'
  uav_fdm3d_B.Gain2 = -uav_fdm3d_B.Product1[2];

  // Outport: '<Root>/ASL'
  uav_fdm3d_Y.ASL = uav_fdm3d_B.Sum1;

  // S-Function (saeroatmos): '<S4>/S-Function'
  {
    // S-Function Block: <S4>/S-Function
    real_T *temp_table = (real_T *) &uav_fdm3d_DW.SFunction_temp_table[0];
    real_T *pres_table = (real_T *) &uav_fdm3d_DW.SFunction_pres_table[0];

    // COESA
    CalcAtmosCOESA( &uav_fdm3d_B.Sum1, &uav_fdm3d_B.SFunction_o1,
                   &uav_fdm3d_B.SFunction_o3, &uav_fdm3d_B.SFunction_o4,
                   &uav_fdm3d_B.SFunction_o2, temp_table, pres_table, 1);
  }

  // Outport: '<Root>/Vn'
  uav_fdm3d_Y.Vn = uav_fdm3d_B.v_n;

  // Outport: '<Root>/Ve'
  uav_fdm3d_Y.Ve = uav_fdm3d_B.v_e;

  // Outport: '<Root>/Vd' incorporates:
  //   Gain: '<S3>/Gain4'

  uav_fdm3d_Y.Vd = -uav_fdm3d_B.hdot;
  if (rtmIsMajorTimeStep((&uav_fdm3d_M))) {
    // Switch: '<S27>/Switch' incorporates:
    //   Abs: '<S27>/Abs'
    //   Constant: '<S28>/Constant'
    //   Constant: '<S5>/initial_pos'
    //   RelationalOperator: '<S28>/Compare'

    if (std::abs(uav_fdm3d_P.LatLon0[0]) > 180.0) {
      // Signum: '<S24>/Sign1' incorporates:
      //   Bias: '<S27>/Bias'
      //   Bias: '<S27>/Bias1'
      //   Constant: '<S27>/Constant2'
      //   Math: '<S27>/Math Function1'

      uav_fdm3d_B.Switch = rt_modd(uav_fdm3d_P.LatLon0[0] + 180.0, 360.0) +
        -180.0;
    } else {
      // Signum: '<S24>/Sign1'
      uav_fdm3d_B.Switch = uav_fdm3d_P.LatLon0[0];
    }

    // End of Switch: '<S27>/Switch'

    // Abs: '<S24>/Abs1'
    rtb_radlat = std::abs(uav_fdm3d_B.Switch);

    // RelationalOperator: '<S26>/Compare' incorporates:
    //   Constant: '<S26>/Constant'

    rtb_Compare_d = (rtb_radlat > 90.0);

    // Switch: '<S24>/Switch'
    if (rtb_Compare_d) {
      // Signum: '<S24>/Sign1' incorporates:
      //   Bias: '<S24>/Bias'
      //   Bias: '<S24>/Bias1'
      //   Gain: '<S24>/Gain'
      //   Product: '<S24>/Divide1'

      if (uav_fdm3d_B.Switch < 0.0) {
        uav_fdm3d_B.Switch = -1.0;
      } else {
        if (uav_fdm3d_B.Switch > 0.0) {
          uav_fdm3d_B.Switch = 1.0;
        }
      }

      uav_fdm3d_B.Switch *= -(rtb_radlat + -90.0) + 90.0;
    }

    // End of Switch: '<S24>/Switch'

    // UnitConversion: '<S32>/Unit Conversion'
    // Unit Conversion - from: deg to: rad
    // Expression: output = (0.0174533*input) + (0)
    rtb_radlat = 0.017453292519943295 * uav_fdm3d_B.Switch;

    // Trigonometry: '<S33>/Trigonometric Function1'
    rtb_sincos_o1_idx_1 = std::sin(rtb_radlat);

    // Sum: '<S33>/Sum1' incorporates:
    //   Constant: '<S33>/Constant'
    //   Product: '<S33>/Product1'

    rtb_sincos_o1_idx_1 = 1.0 - uav_fdm3d_ConstB.sqrt_m *
      uav_fdm3d_ConstB.sqrt_m * rtb_sincos_o1_idx_1 * rtb_sincos_o1_idx_1;

    // Product: '<S31>/Product1' incorporates:
    //   Constant: '<S31>/Constant1'
    //   Sqrt: '<S31>/sqrt'

    rtb_Product_idx_1 = 6.378137E+6 / std::sqrt(rtb_sincos_o1_idx_1);

    // Trigonometry: '<S31>/Trigonometric Function1' incorporates:
    //   Product: '<S31>/Product3'

    uav_fdm3d_B.TrigonometricFunction1 = atan2(1.0, rtb_Product_idx_1 *
      uav_fdm3d_ConstB.Sum1_l / rtb_sincos_o1_idx_1);

    // Trigonometry: '<S31>/Trigonometric Function2' incorporates:
    //   Product: '<S31>/Product4'
    //   Trigonometry: '<S31>/Trigonometric Function'

    uav_fdm3d_B.TrigonometricFunction2 = atan2(1.0, rtb_Product_idx_1 * std::cos
      (rtb_radlat));

    // Switch: '<S15>/Switch1' incorporates:
    //   Constant: '<S15>/Constant'
    //   Constant: '<S15>/Constant1'

    if (rtb_Compare_d) {
      rtb_Compare_o = 180;
    } else {
      rtb_Compare_o = 0;
    }

    // End of Switch: '<S15>/Switch1'

    // Sum: '<S15>/Sum' incorporates:
    //   Constant: '<S5>/initial_pos'

    uav_fdm3d_B.Switch_h = (real_T)rtb_Compare_o + uav_fdm3d_P.LatLon0[1];

    // Switch: '<S25>/Switch' incorporates:
    //   Abs: '<S25>/Abs'
    //   Bias: '<S25>/Bias'
    //   Bias: '<S25>/Bias1'
    //   Constant: '<S25>/Constant2'
    //   Constant: '<S29>/Constant'
    //   Math: '<S25>/Math Function1'
    //   RelationalOperator: '<S29>/Compare'

    if (std::abs(uav_fdm3d_B.Switch_h) > 180.0) {
      uav_fdm3d_B.Switch_h = rt_modd(uav_fdm3d_B.Switch_h + 180.0, 360.0) +
        -180.0;
    }

    // End of Switch: '<S25>/Switch'
  }

  // Sum: '<S5>/Sum' incorporates:
  //   Integrator: '<S3>/Integrator3'
  //   Integrator: '<S3>/Integrator5'
  //   Product: '<S16>/rad lat'
  //   Product: '<S16>/x*cos'
  //   Product: '<S16>/y*sin'
  //   Sum: '<S16>/Sum'
  //   UnitConversion: '<S17>/Unit Conversion'

  // Unit Conversion - from: rad to: deg
  // Expression: output = (57.2958*input) + (0)
  uav_fdm3d_Y.lat = (uav_fdm3d_X.Xn * uav_fdm3d_ConstB.SinCos_o2 -
                     uav_fdm3d_X.Xe * uav_fdm3d_ConstB.SinCos_o1) *
    uav_fdm3d_B.TrigonometricFunction1 * 57.295779513082323 + uav_fdm3d_B.Switch;

  // Switch: '<S21>/Switch' incorporates:
  //   Abs: '<S21>/Abs'
  //   Constant: '<S22>/Constant'
  //   RelationalOperator: '<S22>/Compare'

  if (std::abs(uav_fdm3d_Y.lat) > 180.0) {
    // Sum: '<S5>/Sum' incorporates:
    //   Bias: '<S21>/Bias'
    //   Bias: '<S21>/Bias1'
    //   Constant: '<S21>/Constant2'
    //   Math: '<S21>/Math Function1'

    uav_fdm3d_Y.lat = rt_modd(uav_fdm3d_Y.lat + 180.0, 360.0) + -180.0;
  }

  // End of Switch: '<S21>/Switch'

  // Abs: '<S18>/Abs1'
  rtb_radlat = std::abs(uav_fdm3d_Y.lat);

  // Switch: '<S18>/Switch' incorporates:
  //   Constant: '<S14>/Constant'
  //   Constant: '<S14>/Constant1'
  //   Constant: '<S20>/Constant'
  //   RelationalOperator: '<S20>/Compare'
  //   Switch: '<S14>/Switch1'

  if (rtb_radlat > 90.0) {
    // Signum: '<S18>/Sign1'
    if (uav_fdm3d_Y.lat < 0.0) {
      // Sum: '<S5>/Sum'
      uav_fdm3d_Y.lat = -1.0;
    } else {
      if (uav_fdm3d_Y.lat > 0.0) {
        // Sum: '<S5>/Sum'
        uav_fdm3d_Y.lat = 1.0;
      }
    }

    // End of Signum: '<S18>/Sign1'

    // Sum: '<S5>/Sum' incorporates:
    //   Bias: '<S18>/Bias'
    //   Bias: '<S18>/Bias1'
    //   Gain: '<S18>/Gain'
    //   Outport: '<Root>/lat'
    //   Product: '<S18>/Divide1'

    uav_fdm3d_Y.lat *= -(rtb_radlat + -90.0) + 90.0;
    rtb_Compare_o = 180;
  } else {
    rtb_Compare_o = 0;
  }

  // End of Switch: '<S18>/Switch'

  // Sum: '<S14>/Sum' incorporates:
  //   Integrator: '<S3>/Integrator3'
  //   Integrator: '<S3>/Integrator5'
  //   Product: '<S16>/rad long '
  //   Product: '<S16>/x*sin'
  //   Product: '<S16>/y*cos'
  //   Sum: '<S16>/Sum1'
  //   Sum: '<S5>/Sum'
  //   UnitConversion: '<S17>/Unit Conversion'

  uav_fdm3d_Y.lon = ((uav_fdm3d_X.Xn * uav_fdm3d_ConstB.SinCos_o1 +
                      uav_fdm3d_X.Xe * uav_fdm3d_ConstB.SinCos_o2) *
                     uav_fdm3d_B.TrigonometricFunction2 * 57.295779513082323 +
                     uav_fdm3d_B.Switch_h) + (real_T)rtb_Compare_o;

  // Switch: '<S19>/Switch' incorporates:
  //   Abs: '<S19>/Abs'
  //   Constant: '<S23>/Constant'
  //   RelationalOperator: '<S23>/Compare'

  if (std::abs(uav_fdm3d_Y.lon) > 180.0) {
    // Outport: '<Root>/lon' incorporates:
    //   Bias: '<S19>/Bias'
    //   Bias: '<S19>/Bias1'
    //   Constant: '<S19>/Constant2'
    //   Math: '<S19>/Math Function1'

    uav_fdm3d_Y.lon = rt_modd(uav_fdm3d_Y.lon + 180.0, 360.0) + -180.0;
  }

  // End of Switch: '<S19>/Switch'

  // Outport: '<Root>/time_stamp' incorporates:
  //   Clock: '<Root>/Clock'

  uav_fdm3d_Y.time_stamp = (&uav_fdm3d_M)->Timing.t[0];
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
      // Update absolute timer for sample time: [0.1s, 0.0s]
      // The "clockTick1" counts the number of times the code of this task has
      //  been executed. The resolution of this integer timer is 0.1, which is the step size
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

  // Derivatives for Integrator: '<S3>/hdot'
  _rtXdot->hdot = uav_fdm3d_B.Gain2;

  // Derivatives for Integrator: '<S3>/v_e'
  _rtXdot->v_e = uav_fdm3d_B.Product1[1];

  // Derivatives for Integrator: '<S3>/v_n'
  _rtXdot->v_n = uav_fdm3d_B.Product1[0];

  // Derivatives for Integrator: '<S3>/Integrator2'
  _rtXdot->h = uav_fdm3d_B.hdot;

  // Derivatives for Integrator: '<S3>/Integrator3'
  _rtXdot->Xn = uav_fdm3d_B.v_n;

  // Derivatives for Integrator: '<S3>/Integrator5'
  _rtXdot->Xe = uav_fdm3d_B.v_e;
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
  rtsiSetSolverData(&(&uav_fdm3d_M)->solverInfo, (void *)&(&uav_fdm3d_M)
                    ->intgData);
  rtsiSetSolverName(&(&uav_fdm3d_M)->solverInfo,"ode3");
  rtmSetTPtr(getRTM(), &(&uav_fdm3d_M)->Timing.tArray[0]);
  (&uav_fdm3d_M)->Timing.stepSize0 = 0.1;

  // block I/O
  (void) memset(((void *) &uav_fdm3d_B), 0,
                sizeof(B_uav_fdm3d_T));

  // states (continuous)
  {
    (void) memset((void *)&uav_fdm3d_X, 0,
                  sizeof(X_uav_fdm3d_T));
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

  // Start for S-Function (saeroatmos): '<S4>/S-Function'
  {
    real_T *temp_table = (real_T *) &uav_fdm3d_DW.SFunction_temp_table[0];
    real_T *pres_table = (real_T *) &uav_fdm3d_DW.SFunction_pres_table[0];

    // COESA
    //
    //  Initialize COESA pressure and temperature tables.

    InitCalcAtmosCOESA( temp_table, pres_table );
  }

  // InitializeConditions for Integrator: '<S3>/hdot'
  uav_fdm3d_X.hdot = uav_fdm3d_P.hdot0;

  // InitializeConditions for Integrator: '<S3>/v_e'
  uav_fdm3d_X.v_e = uav_fdm3d_P.v_e0;

  // InitializeConditions for Integrator: '<S3>/v_n'
  uav_fdm3d_X.v_n = uav_fdm3d_P.v_n0;

  // InitializeConditions for Integrator: '<S3>/Integrator2'
  uav_fdm3d_X.h = 0.0;

  // InitializeConditions for Integrator: '<S3>/Integrator3'
  uav_fdm3d_X.Xn = 0.0;

  // InitializeConditions for Integrator: '<S3>/Integrator5'
  uav_fdm3d_X.Xe = 0.0;
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
