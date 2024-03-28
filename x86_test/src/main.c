#include <stdio.h>
#include <stdint.h>
#include "tvmgen_default.h"
#include <tvm_runtime.h>

int abs(int v) {return v * ((v > 0) - (v < 0)); }

int main(int argc, char** argv) {
  // TODO: print otherwise malloc is corrupted
  printf("\tMatch x86: inputs filled with ones\n");

  uint32_t output_size = 4096;
  uint8_t *output = (uint8_t*)malloc(output_size * sizeof(uint8_t));
  struct tvmgen_default_outputs outputs = { .output = output, };
  
  uint32_t input_0_size = 4096;
  uint8_t *input_0 = (uint8_t*)malloc(input_0_size * sizeof(uint8_t));
  // Fill input with 1
  for (uint32_t i = 0; i < input_0_size; i++){
    input_0[i] = 1;
  }

  struct tvmgen_default_inputs inputs = {
    .input_0 = input_0
  };

  int32_t status = 0;
  status = tvmgen_default_run(&inputs, &outputs);
  printf("\n{\"output\":[");
  for(int k=0;k<output_size;k++) {printf("%d",(uint8_t)output[k]);if(k!=output_size-1) printf(", ");}
  printf("]}\n");
  // TODO: free causes SEG FAULT
  //free(input_0);
  //free(output);
  if(status != 0){
    abort();
  }
  return 0;
}
