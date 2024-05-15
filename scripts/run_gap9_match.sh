#!/bin/sh
./build_gap9_match.sh $1 $2
cd $1
timeout --kill-after=240s 240s make run platform=$2
make clean