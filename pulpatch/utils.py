import signal
import subprocess
import json
import pathlib
import os

def modify_lib_0(net_path):
    lines=list()
    with open(net_path+"/codegen/host/src/default_lib0.c") as lib_0:
        lines=[line if ".bss.noinit.tvm" not in line else "PI_L2\n" for line in lib_0.readlines()]
    lines=["#include <pmsis.h>\n"]+lines
    subprocess.run(["rm",net_path+"/codegen/host/src/default_lib0.c"])
    with open(net_path+"/codegen/host/src/default_lib0.c","w") as lib_0:
        lib_0.writelines(lines)
    


def get_result(output_path: str, verbose: bool = False, keep_result: bool = False,
                   board: bool = False, run: bool=True, timeout: int = 300,
                   clean: bool=False, sdk_path="/gap_sdk",target:str="gap9"):

    output={"output":[-1,-1,-1,-1],"correct":False,"run":run}
    if target!="gap9":
        modify_lib_0(str(output_path))
    #print("Building ...",output_path,board,sdk_path)
    with open(output_path/"gap_output.json","wb") as logfile:
        #print("Running",str(pathlib.Path(os.path.dirname(__file__)))+("/scripts/run_gap9_match.sh" if target=="gap9" else "/scripts/pulp_open.sh"))
        output1 = subprocess.Popen([str(pathlib.Path(os.path.dirname(__file__)))+("/scripts/run_gap9_match.sh" if target=="gap9" else "/scripts/pulp_open.sh"),
                                    output_path,"board" if board else "gvsoc",
                                    str(pathlib.Path(os.path.dirname(__file__))),
                                    sdk_path,
                                    str(int(run)),
                                    str(int(clean))],
                                   stdout=subprocess.PIPE)
                                   #,preexec_fn=lambda: signal.alarm(timeout))
        if run:
            output2 = subprocess.Popen(["grep","}"],stdin=output1.stdout,stdout=logfile)
            output2.wait()
        else:
            output2 = subprocess.Popen(["tee","gap_output.json"],stdin=output1.stdout,stdout=logfile)
            output2.wait()

    if run:
        with open(output_path/"gap_output.json") as logfile:
            try:
                output=json.load(logfile)
            except json.JSONDecodeError:
                pass

    if not keep_result:
        subprocess.run(["rm",output_path/"gap_output.json"])
    return output

def run_on_background(output_path: str, gap_sdk_path="/gap_sdk", board: bool=False):
    subprocess.Popen([str(pathlib.Path(os.path.dirname(__file__)))+"/scripts/run_bg_gap9_match.sh",
                            output_path,"board" if board else "gvsoc",
                            gap_sdk_path])
