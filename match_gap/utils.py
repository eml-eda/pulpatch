import signal
import subprocess
import json
import pathlib
import os

def gap_get_result(output_path: str, verbose: bool = False, keep_result: bool = False,
                   board: bool = False, run: bool=True, timeout: int = 300,
                   clean: bool=True, gap_sdk_path="/gap_sdk"):

    output={"output":[-1,-1,-1,-1],"correct":False,"run":run}
    print("Building ...")

    with open(output_path/"gap_output.json","wb") as logfile:
        output1 = subprocess.Popen([str(pathlib.Path(os.path.dirname(__file__)))+"/scripts/run_gap9_match.sh",
                                    output_path,"board" if board else "gvsoc",
                                    str(pathlib.Path(os.path.dirname(__file__))),
                                    gap_sdk_path,
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

def gap_run_on_background(output_path: str, gap_sdk_path="/gap_sdk", board: bool=False):
    output1 = subprocess.Popen([str(pathlib.Path(os.path.dirname(__file__)))+"/scripts/run_bg_gap9_match.sh",
                                output_path,"board" if board else "gvsoc",
                                gap_sdk_path])