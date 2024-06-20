#ifndef PULP_RT_PROFILER_WRAPPER_H
#define PULP_RT_PROFILER_WRAPPER_H

#include <pmsis.h>

// initialization of global performance counter

static volatile int32_t accumulate_perf=0;

void __attribute__((noinline, optimize("O0"))) init_global_perf_counter();

// Total

void __attribute__((noinline, optimize("O0"))) start_perf_counter();

int32_t __attribute__((noinline, optimize("O0"))) stop_perf_counter();

// general

void __attribute__((noinline, optimize("O0"))) start_g_perf_counter();

int32_t __attribute__((noinline, optimize("O0"))) stop_g_perf_counter();

int32_t __attribute__((noinline, optimize("O0"))) get_acc_perf_counter();

#endif // PULP_RT_PROFILER_WRAPPER_H
