#!/bin/bash
echo "Running on background the network..."
echo "The GAP SDK is at" $3
echo "Network is at" $1
echo "Building the network on" $2
cd $3
source sourceme.sh 1 <<< 1
cd $1
make run platform=$2 &