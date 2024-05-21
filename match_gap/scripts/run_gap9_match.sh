#!/bin/bash
echo "Copying and building the network..."
echo "The GAP SDK is at" $4
echo "The path for the match_gap repository scripts are in" $3
echo "Network is at" $1
echo "Building the network on" $2
cd $4
source sourceme.sh 1 <<< 1
cd $3
pwd
./scripts/build_gap9_match.sh $1 $2 $3
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