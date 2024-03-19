cp Makefile.pulprt $1
cp Makefile.x86 $1/
cp gdb_demo_x86.sh $1/
#cp -r BUILD $1/
cp dory_lib $1/dory -R
cp gap9_include_lib/* $1/include/
cp gap9_src_lib/* $1/src/
cp /match/match/codegen/template/lib/gap9cluster/include/* $1/include
cp /match/match/codegen/template/lib/gap9cluster/src/* $1/src

cp ne16_lib/src/* $1/src/
cp ne16_lib/include/* $1/include/