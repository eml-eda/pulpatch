from gap_run import gap_run_match
import pytest
import numpy as np
import pytest
import pathlib

from typing import Dict
import json

import match

def conv_get_test_params():
    """
    This function is used to generate test parameter combinations for
    * Conv2D layers
    * DWConv2D layers

    Why not use pytest.mark.parametrize?
    --> this generates very long filenames with the tmp_path fixture
    --> long paths end up in the debug section of the output binary
    --> pulp RISC-V GDB will crash :(

    This method has some upsides:
    + Conv2D and DWConv2D use the same test params
    + GDB doesn't crash :)

    It has a very obvious downside:
    - Testnames are now very cryptic e.g. "id3, id4" :(
    """
    import itertools
    weight_bits = [8]
    act = [False]#, True]
    strides = [(1, 1)]
    #strides=[(2, 2)]
    kernel_and_padding = [[[3,3],(1,1)]]
    layout=[]
    # small convs -- 24KB fits all fine
    #layout+=[[(8,8),(8,8)],[(16,16),(8,8)],[(32,32),(8,8)],[(64,64),(8,8)],[(128,128),(8,8)]]
    # medium convs
    layout+=[[(16,16),(32,32)],[(32,32),(32,32)],[(64,64),(32,32)],[(128,128),(32,32)]]
    # large convs
    layout+=[[(16,16),(64,64)],[(32,32),(64,64)],[(64,64),(64,64)],[(128,128),(64,64)]]
    # last one of the chosen set
    #layout=[layout[0]]
    combination = [weight_bits, act, strides, kernel_and_padding,layout]
    test_params = list(itertools.product(*combination))
    test_ids = ["id" + str(i) for i in range(len(test_params))]
    return test_params, test_ids

def get_test_params():
    """
    This function is used to generate test parameter combinations for
    * Conv2D layers
    * DWConv2D layers

    Why not use pytest.mark.parametrize?
    --> this generates very long filenames with the tmp_path fixture
    --> long paths end up in the debug section of the output binary
    --> pulp RISC-V GDB will crash :(

    This method has some upsides:
    + Conv2D and DWConv2D use the same test params
    + GDB doesn't crash :)

    It has a very obvious downside:
    - Testnames are now very cryptic e.g. "id3, id4" :(
    """
    import itertools
    weight_bits = [8]
    act = [False, True]
    strides = [(1, 1)]#, (2, 2)]
    kernel_and_padding = [[[7, 7], (3, 3)],
                          [[5, 5], (2, 2)], 
                          [[3, 3], (1, 1)], 
                          [[1, 1], (0, 0)],
                          [[7, 5], (3, 2)]]
    combination = [weight_bits, act, strides, kernel_and_padding]
    test_params = list(itertools.product(*combination))
    test_ids = ["id" + str(i) for i in range(len(test_params))]
    return test_params, test_ids

test_params, test_ids = conv_get_test_params()
@pytest.mark.parametrize("test_params", test_params, ids=test_ids)
def test_conv2d(test_params, tmp_path:str=""):
    weight_bits, act, strides, kernel_and_padding, layout_shapes = test_params
    ones=True
    #ones=False
    # Set random seed for reproducible testing
    #np.random.seed(516418415)
    channel_size=layout_shapes[0]
    inp_size=layout_shapes[1]
    kernel_size = kernel_and_padding[0]
    padding = kernel_and_padding[1]
    kernel_values_= np.ones(shape=(channel_size[0], channel_size[1], kernel_size[1], kernel_size[0]))
    bias_values_=[0 if not ones else 0 for i in range(channel_size[0])]
    shift_bits=0
    ir_module, params = match.create_model_conv_2d(
        input_shape= tuple([1,channel_size[1],inp_size[0],inp_size[1]]),
        weights_shape = tuple([channel_size[0], channel_size[1], kernel_size[0],kernel_size[1]]),
        weight_bits = weight_bits,
        act = act,
        padding = padding,
        strides = strides,
        shift_bits = shift_bits,
        weights_values=np.array(kernel_values_,dtype=np.int8),
        bias_values=np.array(bias_values_,dtype=np.int32)
    )
    # Run the test
    out=gap_run_match(relay_mod=ir_module, relay_params=params, output_path=tmp_path,compare_x86=True,accelerator_active=True)
    print(out)
    return out

#@pytest.mark.parametrize("test_params", test_params, ids=test_ids)
#def test_dw_conv2d(run, test_params, compare_with_x86:bool=False, tmp_path:str=""):
#    weight_bits, act, strides, kernel_and_padding, layout_shapes  = test_params
#    import single_layer.relay_dw_conv2d 
#    from single_layer.utils import numpy_to_array
#    # Set random seed for reproducible testing
#    ones=True
#    np.random.seed(0)
#    channel_size=layout_shapes[0]
#    inp_size=layout_shapes[1]
#    kernel_size = kernel_and_padding[0]
#    padding = kernel_and_padding[1]
#    kernel_values_= np.ones(shape=(channel_size[0], 1, kernel_size[1], kernel_size[0]))
#    bias_values_=[0 if not ones else 0 for i in range(channel_size[0])]
#    shift_bits=0
#    ir_module, params = single_layer.relay_dw_conv2d.create_model(
#        input_shape= tuple([1,channel_size[1],inp_size[0],inp_size[1]]),
#        weights_shape = tuple([channel_size[0], 1, kernel_size[0],kernel_size[1]]),
#        weight_bits = weight_bits,
#        act = act,
#        padding = padding,
#        strides = strides,
#        shift_bits = 0,
#        weights_values=numpy_to_array(np.array(kernel_values_,dtype=np.int8),'int8'),
#        bias_values=numpy_to_array(np.array(bias_values_,dtype=np.int32),'int32')
#            )
#    # Run the test
#    #run=True
#    #compare_with_x86=True
#    out=driver(ir_module, params, run, tmp_path,compare_with_x86=compare_with_x86,out_channels=channel_size[0],out_height=inp_size[0]/strides[0],out_width=inp_size[1]/strides[1])
#    #print(out)
#    return out
#
#@pytest.mark.parametrize("weight_bits", [8], ids = ["digital"])
#@pytest.mark.parametrize("act", [False], ids = ["no_relu"])
#def test_dense(run, weight_bits, act, tmp_path):
#    import single_layer.relay_dense
#    # Set random seed for reproducible testing
#    np.random.seed(0)
#    ir_module, params, weights_shape = single_layer.relay_dense.create_model(
#        weight_bits = weight_bits,
#        act = act,
#        shift_bits = 5
#            )
#    # Run the test
#    out=driver(ir_module,params,run,tmp_path,out_channels=weights_shape[0],out_height=1,out_width=1)
#    #print(out)
#    return out
#
#
#def test_add(run, tmp_path):
#    import single_layer.relay_add
#    # Set random seed for reproducible testing
#    np.random.seed(0)
#    ir_module, params,inp_size = single_layer.relay_add.create_model(
#        shift_bits = 0
#            )
#    # Run the test
#    out=driver(ir_module, params, run, tmp_path, no_of_inputs=2, out_channels=inp_size[1],out_height=inp_size[2],out_width=inp_size[3])
#    #print(out)
#    return out
#
#
#def run_full_network(run, compare_with_x86,directory, network, out_channels:int=1,out_height:int=1,out_width:int=1):
#    np.random.seed(0)
#    ir_module, params = network(
#        weight_bits = 8,
#        # Disable manually inserted layout transforms
#        add_layout_transforms = False,
#        mixed = False)
#    out=driver(ir_module, params, run, directory,compare_with_x86=compare_with_x86,out_channels=out_channels,out_height=out_height,out_width=out_width)
#    print(out)
#    #breakpoint()
#    return out
#
#
#def test_mlperf_tiny_ds_cnn(run:bool=False,compare_with_x86:bool=False, tmp_path:str=""):
#    return run_full_network(run, compare_with_x86,tmp_path, mlperf_tiny.relay_ds_cnn.create_model,out_channels=12)
#
#
#def test_mlperf_tiny_resnet(run:bool=False,compare_with_x86:bool=False, tmp_path:str=""):
#    return run_full_network(run, compare_with_x86,tmp_path, mlperf_tiny.relay_resnet.create_model,out_channels=12)
#
#
#def test_mlperf_tiny_mobilenet(run:bool=False,compare_with_x86:bool=False, tmp_path:str=""):
#    return run_full_network(run, compare_with_x86,tmp_path, mlperf_tiny.relay_mobilenet.create_model,out_channels=4)
#
#def test_mlperf_tiny_dae(run:bool=False,compare_with_x86:bool=False, tmp_path:str=""):
#    return run_full_network(run, compare_with_x86,tmp_path, mlperf_tiny.relay_dae.create_model,out_channels=640)
#
#
#if __name__ == "__main__":
#    import os
#    runs={}
#    runs_only_lats={}
#    shared_l1_sizes=[92700//1024,32]#[::-1]
#    compare_with_x86=False
#    dw=False
#    #shared_l1_sizes=[shared_l1_sizes[1]]
#    MLPERFTINYFUNCS={'mlperftiny_dae':test_mlperf_tiny_dae,'mlperftiny_resnet':test_mlperf_tiny_resnet,
#                    'mlperftiny_dscnn':test_mlperf_tiny_ds_cnn,'mlperftiny_mobilenet':test_mlperf_tiny_mobilenet}
#    run_dory_res=True
#    run_zigzag_std_res=True
#    run_zigzag_cme_res=True
#    lpf_limit=13
#    def conv_results(dw: bool=False):
#        test_func=test_conv2d if not dw else test_dw_conv2d
#        conv_layout=dict()
#        # large convs
#        conv_layout={**conv_layout,**{'conv-large1':[(8,8),(64,64)],'conv-large2':[(16,16),(64,64)],'conv-large3':[(32,32),(64,64)],'conv-large4':[(64,64),(64,64)],'conv-large5':[(128,128),(64,64)]}}
#        #conv_layout={**conv_layout,**{'conv-large5':[(128,128),(64,64)]}}
#        # medium convs
#        conv_layout={**conv_layout,**{'conv-medium1':[(8,8),(32,32)],'conv-medium2':[(16,16),(32,32)],'conv-medium3':[(32,32),(32,32)],'conv-medium4':[(64,64),(32,32)],'conv-medium5':[(128,128),(32,32)]}}
#        # small convs
#        conv_layout={**conv_layout,**{'conv-small1':[(8,8),(8,8)],'conv-small2':[(16,16),(8,8)],'conv-small3':[(32,32),(8,8)],'conv-small4':[(64,64),(8,8)],'conv-small5':[(128,128),(8,8)]}}
#        
#        #conv_layout=dict()
#        #conv_layout['conv-large4']=[(64,64),(64,64)]
#        idx=0
#        for name,layout in conv_layout.items():
#            name=('dw_' if dw else '')+name
#            runs[name]={'dory':{},'zigzag':{'std':{},'cost_model':{}}}
#            runs_only_lats[name]={'dory':{},'zigzag':{'std':{},'cost_model':{}}}
#            for size in shared_l1_sizes:
#                # prep
#                runs[name]['dory'][size]={}
#                runs[name]['zigzag']['std'][size]={}
#                runs[name]['zigzag']['cost_model'][size]={}
#                runs_only_lats[name]['dory'][size]={}
#                runs_only_lats[name]['zigzag']['std'][size]={}
#                runs_only_lats[name]['zigzag']['cost_model'][size]={}
#                # dory
#                if run_dory_res:
#                    print('\n\n',name,size,'dory\n\n')
#                    dory_config=utils_config.dory_config(memory_sizes={'L1':size},path_Dory="PULP/GAP9_TVM")
#                    dory_res=test_func(run = True, test_params= (8, True, (1, 1), [[3, 3], (1, 1)], layout), compare_with_x86=compare_with_x86,tmp_path= pathlib.Path(f"./tmp/test_{'dw_conv_2d' if dw else 'conv2d'}_no_run_{idx}_dory"))
#                    runs[name]['dory'][size]=dory_res
#                    runs_only_lats[name]['dory'][size]=dory_res['latencies']
#                    print(dory_res)
#                # zigzag std
#                if run_zigzag_std_res:
#                    print('\n\n',name,size,'std\n\n')
#                    zigzag_std_config=utils_config.zigzag_config(std_cost_model=True,memory_sizes={'shared_l1':size},lpf_limit=lpf_limit)
#                    zigzag_std_res=test_func(run = True, test_params= (8, True, (1, 1), [[3, 3], (1, 1)], layout), compare_with_x86=compare_with_x86,tmp_path= pathlib.Path(f"./tmp/test_{'dw_conv_2d' if dw else 'conv2d'}_{idx}_zstd"))
#                    runs[name]['zigzag']['std'][size]=zigzag_std_res
#                    runs_only_lats[name]['zigzag']['std'][size]=zigzag_std_res['latencies']
#                    print(zigzag_std_res)
#                # zigzag cost model
#                if run_zigzag_cme_res:
#                    print('\n\n',name,size,'cme\n\n')
#                    zigzag_cme_config=utils_config.zigzag_config(std_cost_model=False,forced_temp_mapping=False,memory_sizes={'shared_l1':size},lpf_limit=lpf_limit)
#                    zigzag_cme_res=test_func(run = True, test_params= (8, True, (1, 1), [[3, 3], (1, 1)], layout), compare_with_x86=compare_with_x86,tmp_path= pathlib.Path(f"./tmp/test_{'dw_conv_2d' if dw else 'conv2d'}_{idx}_zcme"))
#                    runs[name]['zigzag']['cost_model'][size]=zigzag_cme_res
#                    runs_only_lats[name]['zigzag']['cost_model'][size]=zigzag_cme_res['latencies']
#                    print(zigzag_cme_res)
#                # dump it
#                runs[name]['name']=name
#                json_object = json.dumps(runs[name], indent=4)
#                with open(f"./results_logging/{'conv' if not dw else 'dw_conv'}/latest_{'conv' if not dw else 'dw_conv'}_runs_{lpf_limit}_it_{idx}.json", "w") as outfile:
#                    outfile.write(json_object)
#                json_object = json.dumps(runs_only_lats[name], indent=4)
#                with open(f"./results_logging/{'conv' if not dw else 'dw_conv'}/latest_{'conv' if not dw else 'dw_conv'}_runs_only_lats_{lpf_limit}_it_{idx}.json", "w") as outfile:
#                    outfile.write(json_object)
#                idx+=1
#    
#    def mlperf_tiny_results():
#        mlperfiny_names=['mlperftiny_dae','mlperftiny_resnet','mlperftiny_dscnn','mlperftiny_mobilenet']
#        #mlperfiny_names=[mlperfiny_names[1],mlperfiny_names[2]]
#        for size in shared_l1_sizes[::-1]:
#            # prep
#            for name in mlperfiny_names:
#                print('\n\n',name,size,'dory\n\n')
#                runs[name]={'dory':{},'zigzag':{'std':{},'cost_model':{}}}
#                runs_only_lats[name]={'dory':{},'zigzag':{'std':{},'cost_model':{}}}
#                runs[name]['dory'][size]={}
#                runs[name]['zigzag']['std'][size]={}
#                runs[name]['zigzag']['cost_model'][size]={}
#                runs_only_lats[name]['dory'][size]={}
#                runs_only_lats[name]['zigzag']['std'][size]={}
#                runs_only_lats[name]['zigzag']['cost_model'][size]={}
#                mlperftiny_network=MLPERFTINYFUNCS[name]
#                # dory
#                if run_dory_res:
#                    dory_config=utils_config.dory_config(memory_sizes={'L1':size},path_Dory="PULP/GAP9_TVM")
#                    dory_res=mlperftiny_network(run=True,compare_with_x86=compare_with_x86,tmp_path= pathlib.Path(f"./tmp/test_{name}_no_run_id0_0_dory"))
#                    runs[name]['dory'][size]=dory_res
#                    runs_only_lats[name]['dory'][size]=dory_res['latencies']
#                # zigzag std
#                if run_zigzag_std_res:
#                    print('\n\n',name,size,'std\n\n')
#                    zigzag_std_config=utils_config.zigzag_config(std_cost_model=True,memory_sizes={'shared_l1':size},lpf_limit=lpf_limit)
#                    zigzag_std_res=mlperftiny_network(run=True,compare_with_x86=compare_with_x86,tmp_path= pathlib.Path(f"./tmp/test_{name}_no_run_id0_0_zigzag_Std"))
#                    runs[name]['zigzag']['std'][size]=zigzag_std_res
#                    runs_only_lats[name]['zigzag']['std'][size]=zigzag_std_res['latencies']
#                # zigzag cost model
#                if run_zigzag_cme_res:
#                    print('\n\n',name,size,'cme\n\n')
#                    zigzag_std_config=utils_config.zigzag_config(std_cost_model=False,memory_sizes={'shared_l1':size},lpf_limit=lpf_limit)
#                    zigzag_cme_res=mlperftiny_network(run=True,compare_with_x86=compare_with_x86,tmp_path= pathlib.Path(f"./tmp/test_{name}_no_run_id0_0_zigzag_cme"))
#                    runs[name]['zigzag']['cost_model'][size]=zigzag_cme_res
#                    runs_only_lats[name]['zigzag']['std'][size]=zigzag_cme_res['latencies']
#                breakpoint()
#                json_object = json.dumps(runs[name], indent=4)
#                with open(f"./results_logging/mlperftiny/latest_runs_{name}_size_{size}_{lpf_limit}.json", "w") as outfile:
#                    outfile.write(json_object)
#                json_object = json.dumps(runs_only_lats[name], indent=4)
#                with open(f"./results_logging/mlperftiny/latest_runs_{name}_only_lats_size_{size}_{lpf_limit}.json", "w") as outfile:
#                    outfile.write(json_object)
#            json_object = json.dumps(runs, indent=4)
#            with open(f"./results_logging/mlperftiny/latest_runs_size_{size}_{lpf_limit}.json", "w") as outfile:
#                outfile.write(json_object)
#            json_object = json.dumps(runs_only_lats, indent=4)
#            with open(f"./results_logging/mlperftiny/latest_runs_only_lats_size_{size}_{lpf_limit}.json", "w") as outfile:
#                outfile.write(json_object)
#    #mlperf_tiny_results()
#    #for lpf_val in [13,100]:
#    #    lpf_limit=lpf_val
#    #    runs={}
#    #    runs_only_lats={}
#    #    conv_results(False)
#    #    conv_results(True)
#    #    json_object = json.dumps(runs, indent=4)
#    #    with open(f"./results_logging/latest_runs_convs_{lpf_limit}.json", "w") as outfile:
#    #        outfile.write(json_object)
#    #    json_object = json.dumps(runs_only_lats, indent=4)
#    #    with open(f"./results_logging/latest_runs_convs_only_lats_{lpf_limit}.json", "w") as outfile:
#    #        outfile.write(json_object)
#    for lpf_val in [13]:
#        lpf_limit=lpf_val
#        runs={}
#        runs_only_lats={}
#        mlperf_tiny_results()
#        json_object = json.dumps(runs, indent=4)
#        with open(f"./results_logging/latest_runs_mlperf_{lpf_limit}.json", "w") as outfile:
#            outfile.write(json_object)
#        json_object = json.dumps(runs_only_lats, indent=4)
#        with open(f"./results_logging/latest_runs_mlperf_only_lats_{lpf_limit}.json", "w") as outfile:
#            outfile.write(json_object)
#    #test_dense(run = False, weight_bits=8,act=False,tmp_path= pathlib.Path("./tmp/test_dense_no_run_id0_0"))#test_params= (8, True, [10, 2]), tmp_path= pathlib.Path("./tmp/test_dense_no_run_id0_0"))
#    #test_mlperf_tiny_mobilenet(run=False, )
#    #layout=[(16,16),(64,64)]
#    #utils_config.zigzag_config(std_cost_model=False,memory_sizes={'shared_l1':128},lpf_limit=9)
#    #test_conv2d(run = True, test_params= (8, True, (1, 1), [[3, 3], (1, 1)], layout), compare_with_x86=compare_with_x86,tmp_path= pathlib.Path("./tmp/test_z_conv"))
#    #test_dw_conv2d(run = True, test_params= (8, True, (1, 1), [[3, 3], (0, 0)], layout), compare_with_x86=compare_with_x86,tmp_path= pathlib.Path("./tmp/test_z_dw"))
#    #test_dw_conv2d(run = True, test_params= (8, True, (1, 1), [[1, 1], (0, 0)], layout), compare_with_x86=compare_with_x86,tmp_path= pathlib.Path("./tmp/test_z_dw_less_4"))
#    #test_conv2d(run = True, test_params= (8, True, (1, 1), [[1, 1], (0, 0)], layout), compare_with_x86=compare_with_x86,tmp_path= pathlib.Path("./tmp/test_z_pointwise"))