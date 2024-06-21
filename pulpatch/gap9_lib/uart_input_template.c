#include <stdio.h>
#include <stdint.h>
#include "tvmgen_default.h"
#include <tvm_runtime.h>
#include <malloc_wrapper.h>
#include <gdb_anchor.h>
int abs(int v) {return v * ((v > 0) - (v < 0)); }

GAP_L2_DATA int32_t uart_status;
GAP_L2_DATA int32_t inference_status;
struct pi_device uart;
//#define DEBUG_UART 1

int main(int argc, char** argv) {
  % if target!="x86":
  gap9_cluster_init();
  % endif

  uint32_t output_size = ${match_output["size"]};
  uint8_t *output = (uint8_t*)malloc_wrapper(output_size * ${match_output["prec"]} * sizeof(uint8_t));
  
  struct tvmgen_default_outputs outputs = { .output = output, };

  % for match_input in match_inputs:
  uint32_t ${match_input["name"]}_size = ${match_input["size"]};
  uint8_t *${match_input["name"]} = (uint8_t*)malloc_wrapper(${match_input["name"]}_size * ${match_input["prec"]} * sizeof(uint8_t));
  % endfor
  struct tvmgen_default_inputs inputs = {
    % for idx,match_input in enumerate(match_inputs):
    % if idx>0:
    ,
    % endif
    .${match_input["name"]} = ${match_input["name"]}
    % endfor
  };

  // Enable MUX_GROUP_UART1
    pi_pad_function_set(PI_PAD_065, PI_PAD_FUNC0);
    pi_pad_function_set(PI_PAD_066, PI_PAD_FUNC0);

    // Pad 44 and 45 are dedicated to i2c2 by default. We need to configure the MUX_GROUP_UART1 to dedicate them to UART1 (FTDI).
    pi_pad_mux_group_set(PI_PAD_044, PI_PAD_MUX_GROUP_UART1_RX);
    pi_pad_mux_group_set(PI_PAD_045, PI_PAD_MUX_GROUP_UART1_TX);

  struct pi_uart_conf conf;
  /* Init & open uart. */
  pi_uart_conf_init(&conf);
  /*
  typedef struct pi_uart_conf
  {
      uint32_t baudrate_bps;  // Required baudrate, in baud per second. 
      uint8_t stop_bit_count; // Number of stop bits, 1 stop bit (default) or
                                2 stop bits  
      uint8_t parity_mode;    // 1 to activate it, 0 to deactivate it. Even. 
      uint8_t word_size;      // Word size, in bits. 
      uint8_t enable_rx;      // 1 to activate reception, 0 to deactivate it. 
      uint8_t enable_tx;      // 1 to activate transmission, 0 to deactivate it. 
      uint8_t uart_id;        // Uart interface ID. 
      uint8_t use_ctrl_flow;  // 1 to activate control flow. 
      uint8_t is_usart;       // 1 to activate usart 
      uint8_t usart_polarity; // If 1, the clock polarity is reversed. 
      uint8_t usart_phase;    // If 0, the data are sampled on the first clock
          edge, otherwise on the second clock edge. 
      uint8_t use_fast_clk;   // If 0, use fll periph as source otherwise 
                                use external fast clock. 
      uint32_t rts_pad;       // RTS pad number 
  }pi_uart_conf_t;
  */
  conf.uart_id = 1;
  conf.enable_tx = 1;
  conf.enable_rx = 1;
  conf.baudrate_bps = 115200;
  conf.word_size = PI_UART_WORD_SIZE_8_BITS;
  conf.parity_mode = 0;
  conf.use_fast_clk = 0;              // Enable the fast clk for uart
  conf.use_ctrl_flow = 0;             // Enable the HW Flow Control
  
  conf.stop_bit_count = PI_UART_STOP_BITS_TWO;

  pi_open_from_conf(&uart, &conf);
  if (pi_uart_open(&uart))
  {
      printf("Uart open failed !\n");
      pmsis_exit(-1);
  }

  uart_status=0;
  pi_uart_write(&uart,&uart_status,sizeof(int32_t));
  printf("Ready...\n");
  while(1)
  {
      // Get the size of the buffer
      pi_uart_read(&uart, &uart_status, sizeof(int32_t));
      printf("Received status %d...\n",uart_status);
      // If the sender sends anything that is not 0 we finish
      if(!uart_status)
      {
        % for match_input in match_inputs:
        pi_uart_read(&uart, ${match_input["name"]}, ${match_input["name"]}_size * ${match_input["prec"]});
        % endfor
        #ifdef DEBUG_UART
        printf("Received input ${match_input['name']}...\n");
        for(int i=0;i<${match_input["name"]}_size;i++) printf("%d, ",match_input_0[i]);
        printf("\n");
        #endif 
        printf("Running inference...\n");
        //start_g_perf_counter();
        inference_status = tvmgen_default_run(&inputs, &outputs);
        //stop_g_perf_counter();
        //int32_t cycles=get_acc_perf_counter();
        /* Write on uart the size of the result and then the result. */
        printf("Inference finished with status %d...\n",inference_status);
        /* Write on uart the size of the result and then the result. */
        pi_uart_write(&uart, &inference_status, sizeof(int32_t));
        if(!inference_status){
          #ifdef DEBUG_UART
          printf("Output...\n");
          for(int i=0;i<output_size;i++) printf("%d, ",output[i]);
          printf("\n");
          #endif  
          pi_uart_write(&uart, output, (output_size* ${match_output["prec"]} *sizeof(uint8_t)) + 4);
        }
      }
      else{
        printf("Received finish command...\n");
        break;
      }
  }

  pi_uart_close(&uart);

  % for match_input in match_inputs:
  free_wrapper(${match_input["name"]});
  % endfor
  free_wrapper(output);
  % if target!="x86":
  gap9_cluster_close();
  % endif
  return 0;
}
