import signal
import subprocess
import json

def gap_get_result(output_path: str, verbose: bool = False, keep_result: bool = False, board: bool = False,timeout: int = 300, clean: bool=True):

    output={"output":[-1,-1,-1,-1],"correct":False}
    print("Building ...")

    with open(output_path/"gap_output.json","wb") as logfile:
        output1 = subprocess.Popen(["../scripts/run_gap9_match.sh",output_path,"board" if board else "gvsoc"],
                                   stdout=subprocess.PIPE)
                                   #,preexec_fn=lambda: signal.alarm(timeout))
        output2 = subprocess.Popen(["grep","}"],stdin=output1.stdout,stdout=logfile)
        output2.wait()

    with open(output_path/"gap_output.json") as logfile:
        try:
            output=json.load(logfile)
        except json.JSONDecodeError:
            pass

    if not keep_result:
        subprocess.run(["rm",output_path/"gap_output.json"])
    return output