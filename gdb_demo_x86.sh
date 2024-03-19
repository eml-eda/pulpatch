set print elements 0
set print repeats 0
set pagination off
set max-value-size unlimited
break gdb_anchor
run
n
n
n
set logging file ./demo_x86.txt
set logging on
print /d *output@output_size
set logging off
