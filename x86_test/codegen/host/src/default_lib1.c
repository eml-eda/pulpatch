// tvm target: c -keys=arm_cpu,cpu -device=arm_cpu
#define TVM_EXPORTS
#include "tvm/runtime/c_runtime_api.h"
#include "tvm/runtime/c_backend_api.h"
#include <math.h>
#include <stdbool.h>
#ifdef __cplusplus
extern "C"
#endif
TVM_DLL int32_t tvmgen_default_fused_multiply_add_right_shift_clip_cast(int32_t* p0, uint8_t* T_cast, uint8_t* global_const_workspace_4_var, uint8_t* global_workspace_5_var);
#ifdef __cplusplus
extern "C"
#endif
TVM_DLL int32_t tvmgen_default_fused_nn_conv2d(uint8_t* p0, int32_t* output_unpack, uint8_t* global_const_workspace_2_var, uint8_t* global_workspace_3_var);
#ifdef __cplusplus
extern "C"
#endif
TVM_DLL int32_t tvmgen_default___tvm_main__(uint8_t* input_0_buffer_var, uint8_t* output_buffer_var, uint8_t* global_const_workspace_0_var, uint8_t* global_workspace_1_var);
#ifdef __cplusplus
extern "C"
#endif
TVM_DLL int32_t tvmgen_default_fused_multiply_add_right_shift_clip_cast(int32_t* p0, uint8_t* T_cast, uint8_t* global_const_workspace_4_var, uint8_t* global_workspace_5_var) {
  void* fused_multiply_constant_let = (&(global_const_workspace_4_var[2304]));
  void* fused_constant_1_let = (&(global_const_workspace_4_var[2368]));
  for (int32_t ax0_ax1_fused_ax2_fused = 0; ax0_ax1_fused_ax2_fused < 4096; ++ax0_ax1_fused_ax2_fused) {
    for (int32_t ax3_inner = 0; ax3_inner < 16; ++ax3_inner) {
      int32_t cse_var_1 = (ax0_ax1_fused_ax2_fused >> 8);
      int32_t v_ = ((p0[(((ax0_ax1_fused_ax2_fused & 255) * 16) + ax3_inner)] * ((int32_t*)fused_constant_1_let)[cse_var_1]) + ((int32_t*)fused_multiply_constant_let)[cse_var_1]) >> 4;
      int32_t v__1 = (v_) < (255) ? (v_) : (255);
      T_cast[((ax0_ax1_fused_ax2_fused * 16) + ax3_inner)] = ((uint8_t)((v__1) > (0) ? (v__1) : (0)));
    }
  }
  return 0;
}

#ifdef __cplusplus
extern "C"
#endif
TVM_DLL int32_t tvmgen_default_fused_nn_conv2d(uint8_t* p0, int32_t* output_unpack, uint8_t* global_const_workspace_2_var, uint8_t* global_workspace_3_var) {
  void* fused_constant_let = (&(global_const_workspace_2_var[0]));
  void* data_vec_let = (&(global_workspace_3_var[16384]));
  for (int32_t h = 0; h < 8; ++h) {
    for (int32_t w = 0; w < 8; ++w) {
      for (int32_t ci = 0; ci < 16; ++ci) {
        for (int32_t vh = 0; vh < 4; ++vh) {
          for (int32_t vw = 0; vw < 4; ++vw) {
            int32_t cse_var_3 = (w * 2);
            int32_t cse_var_2 = ((h * 2) + vh);
            int32_t cse_var_1 = (cse_var_3 + vw);
            ((uint8_t*)data_vec_let)[(((((h * 2048) + (w * 256)) + (ci * 16)) + (vh * 4)) + vw)] = (((((1 <= cse_var_2) && (cse_var_2 < 17)) && (1 <= cse_var_1)) && (cse_var_1 < 17)) ? p0[((((((ci * 256) + (h * 32)) + (vh * 16)) + cse_var_3) + vw) - 17)] : (uint8_t)0);
          }
        }
      }
    }
  }
  for (int32_t co_outer = 0; co_outer < 4; ++co_outer) {
    void* conv_let = (&(global_workspace_3_var[32768]));
    for (int32_t h_outer = 0; h_outer < 8; ++h_outer) {
      for (int32_t w_outer = 0; w_outer < 8; ++w_outer) {
        for (int32_t vc_init = 0; vc_init < 4; ++vc_init) {
          for (int32_t vw_init = 0; vw_init < 2; ++vw_init) {
            ((int32_t*)conv_let)[((vw_init * 4) + vc_init)] = 0;
          }
          for (int32_t vw_init_1 = 0; vw_init_1 < 2; ++vw_init_1) {
            ((int32_t*)conv_let)[(((vw_init_1 * 4) + vc_init) + 8)] = 0;
          }
        }
        for (int32_t ci_1 = 0; ci_1 < 16; ++ci_1) {
          for (int32_t vc = 0; vc < 4; ++vc) {
            for (int32_t vw_1 = 0; vw_1 < 2; ++vw_1) {
              int32_t cse_var_4 = ((vw_1 * 4) + vc);
              ((int32_t*)conv_let)[cse_var_4] = (((int32_t*)conv_let)[cse_var_4] + (((int32_t)((uint8_t*)data_vec_let)[((((h_outer * 2048) + (w_outer * 256)) + (ci_1 * 16)) + vw_1)]) * ((int32_t)((int8_t*)fused_constant_let)[(((co_outer * 576) + (ci_1 * 36)) + vc)])));
            }
            for (int32_t vw_2 = 0; vw_2 < 2; ++vw_2) {
              int32_t cse_var_5 = (((vw_2 * 4) + vc) + 8);
              ((int32_t*)conv_let)[cse_var_5] = (((int32_t*)conv_let)[cse_var_5] + (((int32_t)((uint8_t*)data_vec_let)[(((((h_outer * 2048) + (w_outer * 256)) + (ci_1 * 16)) + vw_2) + 4)]) * ((int32_t)((int8_t*)fused_constant_let)[(((co_outer * 576) + (ci_1 * 36)) + vc)])));
            }
          }
          for (int32_t vc_1 = 0; vc_1 < 4; ++vc_1) {
            for (int32_t vw_3 = 0; vw_3 < 2; ++vw_3) {
              int32_t cse_var_6 = ((vw_3 * 4) + vc_1);
              ((int32_t*)conv_let)[cse_var_6] = (((int32_t*)conv_let)[cse_var_6] + (((int32_t)((uint8_t*)data_vec_let)[(((((h_outer * 2048) + (w_outer * 256)) + (ci_1 * 16)) + vw_3) + 1)]) * ((int32_t)((int8_t*)fused_constant_let)[((((co_outer * 576) + (ci_1 * 36)) + vc_1) + 4)])));
            }
            for (int32_t vw_4 = 0; vw_4 < 2; ++vw_4) {
              int32_t cse_var_7 = (((vw_4 * 4) + vc_1) + 8);
              ((int32_t*)conv_let)[cse_var_7] = (((int32_t*)conv_let)[cse_var_7] + (((int32_t)((uint8_t*)data_vec_let)[(((((h_outer * 2048) + (w_outer * 256)) + (ci_1 * 16)) + vw_4) + 5)]) * ((int32_t)((int8_t*)fused_constant_let)[((((co_outer * 576) + (ci_1 * 36)) + vc_1) + 4)])));
            }
          }
          for (int32_t vc_2 = 0; vc_2 < 4; ++vc_2) {
            for (int32_t vw_5 = 0; vw_5 < 2; ++vw_5) {
              int32_t cse_var_8 = ((vw_5 * 4) + vc_2);
              ((int32_t*)conv_let)[cse_var_8] = (((int32_t*)conv_let)[cse_var_8] + (((int32_t)((uint8_t*)data_vec_let)[(((((h_outer * 2048) + (w_outer * 256)) + (ci_1 * 16)) + vw_5) + 2)]) * ((int32_t)((int8_t*)fused_constant_let)[((((co_outer * 576) + (ci_1 * 36)) + vc_2) + 8)])));
            }
            for (int32_t vw_6 = 0; vw_6 < 2; ++vw_6) {
              int32_t cse_var_9 = (((vw_6 * 4) + vc_2) + 8);
              ((int32_t*)conv_let)[cse_var_9] = (((int32_t*)conv_let)[cse_var_9] + (((int32_t)((uint8_t*)data_vec_let)[(((((h_outer * 2048) + (w_outer * 256)) + (ci_1 * 16)) + vw_6) + 6)]) * ((int32_t)((int8_t*)fused_constant_let)[((((co_outer * 576) + (ci_1 * 36)) + vc_2) + 8)])));
            }
          }
          for (int32_t vc_3 = 0; vc_3 < 4; ++vc_3) {
            for (int32_t vw_7 = 0; vw_7 < 2; ++vw_7) {
              int32_t cse_var_10 = ((vw_7 * 4) + vc_3);
              ((int32_t*)conv_let)[cse_var_10] = (((int32_t*)conv_let)[cse_var_10] + (((int32_t)((uint8_t*)data_vec_let)[(((((h_outer * 2048) + (w_outer * 256)) + (ci_1 * 16)) + vw_7) + 4)]) * ((int32_t)((int8_t*)fused_constant_let)[((((co_outer * 576) + (ci_1 * 36)) + vc_3) + 12)])));
            }
            for (int32_t vw_8 = 0; vw_8 < 2; ++vw_8) {
              int32_t cse_var_11 = (((vw_8 * 4) + vc_3) + 8);
              ((int32_t*)conv_let)[cse_var_11] = (((int32_t*)conv_let)[cse_var_11] + (((int32_t)((uint8_t*)data_vec_let)[(((((h_outer * 2048) + (w_outer * 256)) + (ci_1 * 16)) + vw_8) + 8)]) * ((int32_t)((int8_t*)fused_constant_let)[((((co_outer * 576) + (ci_1 * 36)) + vc_3) + 12)])));
            }
          }
          for (int32_t vc_4 = 0; vc_4 < 4; ++vc_4) {
            for (int32_t vw_9 = 0; vw_9 < 2; ++vw_9) {
              int32_t cse_var_12 = ((vw_9 * 4) + vc_4);
              ((int32_t*)conv_let)[cse_var_12] = (((int32_t*)conv_let)[cse_var_12] + (((int32_t)((uint8_t*)data_vec_let)[(((((h_outer * 2048) + (w_outer * 256)) + (ci_1 * 16)) + vw_9) + 5)]) * ((int32_t)((int8_t*)fused_constant_let)[((((co_outer * 576) + (ci_1 * 36)) + vc_4) + 16)])));
            }
            for (int32_t vw_10 = 0; vw_10 < 2; ++vw_10) {
              int32_t cse_var_13 = (((vw_10 * 4) + vc_4) + 8);
              ((int32_t*)conv_let)[cse_var_13] = (((int32_t*)conv_let)[cse_var_13] + (((int32_t)((uint8_t*)data_vec_let)[(((((h_outer * 2048) + (w_outer * 256)) + (ci_1 * 16)) + vw_10) + 9)]) * ((int32_t)((int8_t*)fused_constant_let)[((((co_outer * 576) + (ci_1 * 36)) + vc_4) + 16)])));
            }
          }
          for (int32_t vc_5 = 0; vc_5 < 4; ++vc_5) {
            for (int32_t vw_11 = 0; vw_11 < 2; ++vw_11) {
              int32_t cse_var_14 = ((vw_11 * 4) + vc_5);
              ((int32_t*)conv_let)[cse_var_14] = (((int32_t*)conv_let)[cse_var_14] + (((int32_t)((uint8_t*)data_vec_let)[(((((h_outer * 2048) + (w_outer * 256)) + (ci_1 * 16)) + vw_11) + 6)]) * ((int32_t)((int8_t*)fused_constant_let)[((((co_outer * 576) + (ci_1 * 36)) + vc_5) + 20)])));
            }
            for (int32_t vw_12 = 0; vw_12 < 2; ++vw_12) {
              int32_t cse_var_15 = (((vw_12 * 4) + vc_5) + 8);
              ((int32_t*)conv_let)[cse_var_15] = (((int32_t*)conv_let)[cse_var_15] + (((int32_t)((uint8_t*)data_vec_let)[(((((h_outer * 2048) + (w_outer * 256)) + (ci_1 * 16)) + vw_12) + 10)]) * ((int32_t)((int8_t*)fused_constant_let)[((((co_outer * 576) + (ci_1 * 36)) + vc_5) + 20)])));
            }
          }
          for (int32_t vc_6 = 0; vc_6 < 4; ++vc_6) {
            for (int32_t vw_13 = 0; vw_13 < 2; ++vw_13) {
              int32_t cse_var_16 = ((vw_13 * 4) + vc_6);
              ((int32_t*)conv_let)[cse_var_16] = (((int32_t*)conv_let)[cse_var_16] + (((int32_t)((uint8_t*)data_vec_let)[(((((h_outer * 2048) + (w_outer * 256)) + (ci_1 * 16)) + vw_13) + 8)]) * ((int32_t)((int8_t*)fused_constant_let)[((((co_outer * 576) + (ci_1 * 36)) + vc_6) + 24)])));
            }
            for (int32_t vw_14 = 0; vw_14 < 2; ++vw_14) {
              int32_t cse_var_17 = (((vw_14 * 4) + vc_6) + 8);
              ((int32_t*)conv_let)[cse_var_17] = (((int32_t*)conv_let)[cse_var_17] + (((int32_t)((uint8_t*)data_vec_let)[(((((h_outer * 2048) + (w_outer * 256)) + (ci_1 * 16)) + vw_14) + 12)]) * ((int32_t)((int8_t*)fused_constant_let)[((((co_outer * 576) + (ci_1 * 36)) + vc_6) + 24)])));
            }
          }
          for (int32_t vc_7 = 0; vc_7 < 4; ++vc_7) {
            for (int32_t vw_15 = 0; vw_15 < 2; ++vw_15) {
              int32_t cse_var_18 = ((vw_15 * 4) + vc_7);
              ((int32_t*)conv_let)[cse_var_18] = (((int32_t*)conv_let)[cse_var_18] + (((int32_t)((uint8_t*)data_vec_let)[(((((h_outer * 2048) + (w_outer * 256)) + (ci_1 * 16)) + vw_15) + 9)]) * ((int32_t)((int8_t*)fused_constant_let)[((((co_outer * 576) + (ci_1 * 36)) + vc_7) + 28)])));
            }
            for (int32_t vw_16 = 0; vw_16 < 2; ++vw_16) {
              int32_t cse_var_19 = (((vw_16 * 4) + vc_7) + 8);
              ((int32_t*)conv_let)[cse_var_19] = (((int32_t*)conv_let)[cse_var_19] + (((int32_t)((uint8_t*)data_vec_let)[(((((h_outer * 2048) + (w_outer * 256)) + (ci_1 * 16)) + vw_16) + 13)]) * ((int32_t)((int8_t*)fused_constant_let)[((((co_outer * 576) + (ci_1 * 36)) + vc_7) + 28)])));
            }
          }
          for (int32_t vc_8 = 0; vc_8 < 4; ++vc_8) {
            for (int32_t vw_17 = 0; vw_17 < 2; ++vw_17) {
              int32_t cse_var_20 = ((vw_17 * 4) + vc_8);
              ((int32_t*)conv_let)[cse_var_20] = (((int32_t*)conv_let)[cse_var_20] + (((int32_t)((uint8_t*)data_vec_let)[(((((h_outer * 2048) + (w_outer * 256)) + (ci_1 * 16)) + vw_17) + 10)]) * ((int32_t)((int8_t*)fused_constant_let)[((((co_outer * 576) + (ci_1 * 36)) + vc_8) + 32)])));
            }
            for (int32_t vw_18 = 0; vw_18 < 2; ++vw_18) {
              int32_t cse_var_21 = (((vw_18 * 4) + vc_8) + 8);
              ((int32_t*)conv_let)[cse_var_21] = (((int32_t*)conv_let)[cse_var_21] + (((int32_t)((uint8_t*)data_vec_let)[(((((h_outer * 2048) + (w_outer * 256)) + (ci_1 * 16)) + vw_18) + 14)]) * ((int32_t)((int8_t*)fused_constant_let)[((((co_outer * 576) + (ci_1 * 36)) + vc_8) + 32)])));
            }
          }
        }
        for (int32_t h_inner = 0; h_inner < 2; ++h_inner) {
          for (int32_t w_inner = 0; w_inner < 2; ++w_inner) {
            for (int32_t co_inner = 0; co_inner < 4; ++co_inner) {
              output_unpack[((((((co_outer * 1024) + (co_inner * 256)) + (h_outer * 32)) + (h_inner * 16)) + (w_outer * 2)) + w_inner)] = ((int32_t*)conv_let)[(((h_inner * 8) + (w_inner * 4)) + co_inner)];
            }
          }
        }
      }
    }
  }
  return 0;
}

#ifdef __cplusplus
extern "C"
#endif
TVM_DLL int32_t tvmgen_default___tvm_main__(uint8_t* input_0_buffer_var, uint8_t* output_buffer_var, uint8_t* global_const_workspace_0_var, uint8_t* global_workspace_1_var) {
  void* sid_1_let = (&(global_workspace_1_var[0]));
  if (tvmgen_default_fused_nn_conv2d(input_0_buffer_var, sid_1_let, global_const_workspace_0_var, global_workspace_1_var) != 0 ) return -1;
  if (tvmgen_default_fused_multiply_add_right_shift_clip_cast(sid_1_let, output_buffer_var, global_const_workspace_0_var, global_workspace_1_var) != 0 ) return -1;
  return 0;
}

