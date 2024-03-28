import os
import argparse
import pathlib
import match
from mako.template import Template
import numpy as np

from utils import gap_get_result

def gap_run_match(input_type="onnx",relay_mod=None, relay_params=None, filename=None, params_filename=None, output_path="./match_output",verbose:bool=False,compare_x86:bool=True):
    pathlib.Path(output_path).mkdir(parents=True,exist_ok=True)
    pathlib.Path(output_path+"/src").mkdir(parents=True,exist_ok=True)
    pathlib.Path(output_path+"/include").mkdir(parents=True,exist_ok=True)
    np.random.seed(0)
    res=match.match(input_type=input_type,relay_mod=relay_mod,relay_params=relay_params,filename=filename,params_filename=params_filename,
                    target_name="gap9",output_path=output_path)
    main_code_template=Template(filename=os.path.dirname(__file__)+"/demo_template.c")
    template_data_dict=res.__dict__
    template_data_dict["target"]="gap9"
    main_code=main_code_template.render(**template_data_dict)
    with open(pathlib.Path(output_path)/"src/demo.c","w") as demo_file:
        demo_file.write(main_code)
    gap_result=gap_get_result(pathlib.Path(output_path),verbose=verbose)

    if verbose:
        print("Gap result:")
        print(gap_result["output"])

    if compare_x86:

        x86_result=match.x86_run_match(input_type=input_type,relay_mod=relay_mod,relay_params=relay_params,filename=filename,params_filename=params_filename,output_path=pathlib.Path("./x86_test"))
        
        if verbose:
            print("\n\nx86 result:")
            print(x86_result)
        
        gap_result["correct"]=str(np.ma.allclose(np.asarray(x86_result["output"]).reshape(int(res.match_output["shape"][1]),int(res.match_output["shape"][2]),int(res.match_output["shape"][3])).transpose(1,2,0).flatten().astype(np.uint8),np.asarray(gap_result['output']).astype(np.uint8)))
    
    return gap_result

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
        mod,params=match.create_model_conv_2d()
    elif args.addexample:
        mod,params=match.create_model_add_convs()
    compare_x86=False
    compare_x86=True
    res_=gap_run_match(
        input_type=input_type,
        relay_mod=mod,
        relay_params=params,
        filename=filename,
        params_filename=params_filename,
        output_path=output_path,
        compare_x86=compare_x86
    )
    if compare_x86:
        print("Result is","" if res_["correct"] else "NOT","correct")
    else:
        print("Result is",res_)