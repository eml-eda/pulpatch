set print elements 0
set print repeats 0
set pagination off
set max-value-size unlimited
target remote localhost:12345
load
break gdb_anchor
c
n
n
n
set logging file ./demo_x86.txt
set logging on
print int8 *output@output_size
set logging off
