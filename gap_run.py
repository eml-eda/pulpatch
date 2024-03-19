import os
import argparse
import pathlib
import subprocess
import match
from mako.template import Template

from match.relay.models import create_model_add_convs, create_model_conv_2d
import numpy as np

import tvm

def gap_run_driver(input_type="onnx",relay_mod=None, relay_params=None, filename=None, params_filename=None, output_path="./match_output"):
    pathlib.Path(output_path).mkdir(parents=True)
    pathlib.Path(output_path+"/src").mkdir(parents=True)
    pathlib.Path(output_path+"/include").mkdir(parents=True)
    np.random.seed(0)
    target_name="gap9"
    res=match.match(input_type=input_type,relay_mod=relay_mod,relay_params=relay_params,filename=filename,params_filename=params_filename,
                    target_name=target_name,output_path=output_path)
    main_code_template=Template(filename=os.path.dirname(__file__)+"/demo_template.c")
    template_data_dict=res.__dict__
    template_data_dict["target"]=target_name
    main_code=main_code_template.render(**template_data_dict)
    with open(output_path+"/src/demo.c","w") as demo_file:
        demo_file.write(main_code)
    
    subprocess.run(["./run_gap9_match.sh",output_path])
    

if __name__=="__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "-v", "--verbose", action="count", default=0, help="increase log verbosity"
    )

    parser.add_argument(
        "-d",
        "--debug",
        action="store_const",
        dest="verbose",
        const=2,
        help="log debug messages (same as -vv)",
    )

    parser.add_argument(
        "-i",
        "--input",
        dest="input_type",
        type=str,
        help="Type of the input to compile, possible values are [onnx,relay].",
    )

    parser.add_argument(
        "-f",
        "--filename",
        dest="filename",
        type=str,
        help="Provide the filename of the module to compile.",
    )

    parser.add_argument(
        "-p",
        "--params",
        dest="params_filename",
        type=str,
        help="Provide the filename of the params needed by the module to compile.",
    )

    parser.add_argument(
        "-c",
        "--convexample",
        dest="convexample",
        action="store_true",
        help="compile a simple 2d convolution example, that contains a con2d, a bias add and a requantization step",
    )

    parser.add_argument(
        "-a",
        "--addexample",
        dest="addexample",
        action="store_true",
        help="compile a simple add example between 2 2d convs like the ones in the convexample,"
        + "with a final requantization step",
    )

    parser.add_argument(
        "-o",
        "--output_path",
        dest="output_path",
        type=str,
        help="Provide the output path"
    )

    args = parser.parse_args()
    input_type=args.input_type
    mod=None
    params=None
    filename=args.filename
    params_filename=args.params_filename
    output_path=args.output_path

    if args.convexample:
        mod,params=create_model_conv_2d()
    elif args.addexample:
        mod,params=create_model_add_convs()
    gap_run_driver(
        input_type=input_type,
        relay_mod=mod,
        relay_params=params,
        filename=filename,
        params_filename=params_filename,
        output_path=output_path,
    )