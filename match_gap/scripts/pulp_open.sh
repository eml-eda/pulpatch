#!/bin/bash
echo "Copying and building the network..."
echo "The PULP SDK is at" $4
echo "The path for the match_gap repository scripts are in" $3
echo "Network is at" $1
echo "Building the network on" $2
source $4/configs/pulp-open.sh
cd $3
pwd
cp $3/pulpopen_lib/Makefile $1
cp $3/pulpopen_lib/gdb_script.sh $1
cp $3/pulpopen_lib/include/* $1/include/
cp $3/pulpopen_lib/src/* $1/src/
cd $1
make all platform=$2 -j 8
cd $1
if [ $5 -gt 0 ]; then
    echo "Running the network"
    timeout --kill-after=240s 240s make run platform=$2
else
    echo "Built the network"
fi
if [ $6 -gt 0 ]; then
    echo "Cleaning the build"
    make clean
fi