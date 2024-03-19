#include <stdio.h>
#include <stdint.h>
#include "tvmgen_default.h"
#include <tvm_runtime.h>
#include <malloc_wrapper.h>
#include <gdb_anchor.h>

int abs(int v) {return v * ((v > 0) - (v < 0)); }

int main(int argc, char** argv) {
  gap9_cluster_init();

  uint32_t output_size = 1000;
  uint8_t *output = (uint8_t*)malloc_wrapper(output_size * sizeof(uint8_t));
  struct tvmgen_default_outputs outputs = { .output = output, };
  
  uint32_t match_input_0_size = 3072;
  uint8_t *match_input_0 = (uint8_t*)malloc_wrapper(match_input_0_size * sizeof(uint8_t));
  // Fill input with 1
  for (uint32_t i = 0; i < match_input_0_size; i++){
    match_input_0[i] = 1;
  }

  struct tvmgen_default_inputs inputs = {
    .match_input_0 = match_input_0
  };

  int32_t status = 0;
  status = tvmgen_default_run(&inputs, &outputs);
  gdb_anchor();
  printf("\n[");
  for(int k=0;k<output_size;k++) {printf("%d",(uint8_t)output[k]);if(k!=output_size-1) printf(", ");}
  printf("]\n");
  free_wrapper(match_input_0);
  free_wrapper(output);
  if(status != 0){
    abort();
  }
  gap9_cluster_close();
  return 0;
}
