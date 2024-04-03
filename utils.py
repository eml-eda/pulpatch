import subprocess
import json

def gap_get_result(output_path: str, verbose: bool = False, keep_result: bool = False):

    output={"output":[-1,-1,-1,-1]}
    print("Building ...")

    with open(output_path/"gap_output.json","wb") as logfile:
        output1 = subprocess.Popen(["./run_gap9_match.sh",output_path],stdout=subprocess.PIPE)
        output2 = subprocess.Popen(["grep","]}"],stdin=output1.stdout,stdout=logfile)
        output2.wait()

    with open(output_path/"gap_output.json") as logfile:
        output=json.load(logfile)

    if not keep_result:
        subprocess.run(["rm",output_path/"gap_output.json"])
    return output