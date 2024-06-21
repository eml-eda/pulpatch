#ifndef GAP_CLUSTER_H
#define GAP_CLUSTER_H


#include <pmsis.h>
extern struct pi_device cluster_dev;
extern struct pi_cluster_task cluster_task;

void gap_cluster_init();

void gap_cluster_close();

#endif //GAP9_CLUSTER_H