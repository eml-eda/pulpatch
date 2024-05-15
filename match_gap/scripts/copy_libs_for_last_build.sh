#!/bin/sh
cp Makefile $1
cp gdb_script.sh $1
#cp -r BUILD $1/
cp dory_lib $1/dory -R
cp gap9_lib/include/* $1/include/
cp gap9_lib/src/* $1/src/