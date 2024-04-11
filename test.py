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
    act = [True]
    strides = [(1, 1),(2,2)]
    #strides=[(2, 2)]
    kernel_and_padding = [[[3,3],(1,1)]]
    layout=[]
    # small convs -- 24KB fits all fine
    #layout+=[[(8,8),(8,8)],[(16,16),(8,8)],[(32,32),(8,8)],[(64,64),(8,8)],[(128,128),(8,8)]]
    # medium convs
    layout+=[[(16,16),(32,32)],[(32,32),(32,32)],[(64,64),(32,32)],[(128,128),(32,32)]]
    # large convs
    layout+=[[(16,16),(64,64)],[(32,32),(64,64)],[(64,64),(64,64)]]#,[(128,128),(64,64)]]
    # last one of the chosen set
    #layout=[layout[0],layout[1]]
    #layout=[[(16,1),(16,16)],[(32,1),(32,32)]]
    dev=["ne16_single"]
    dev.append("cluster")
    combination = [weight_bits, act, strides, kernel_and_padding,layout,dev]
    test_params = list(itertools.product(*combination))
    test_ids = ["id" + str(i) + "_" + test_params[i][5] for i in range(len(test_params))]
    return test_params, test_ids

test_params, test_ids = conv_get_test_params()
@pytest.mark.parametrize("test_params", test_params, ids=test_ids)
def test_conv2d(test_params, tmp_path):
    weight_bits, act, strides, kernel_and_padding, layout_shapes, dev = test_params
    print("Dev::",dev)
    dev_arr=dev.split("_")
    dev=dev_arr[0]
    channel_size=layout_shapes[0]
    input_pad=None
    inp_size=layout_shapes[1]
    input_shape=[1,channel_size[1],inp_size[0],inp_size[1]]
    if "ne16" in dev and channel_size[1]%16!=0:
        input_pad=((0,0),(0,16-channel_size[1]%16),(0,0),(0,0))
    kernel_size = kernel_and_padding[0]
    padding = kernel_and_padding[1]
    kernel_values_= np.ones(shape=(channel_size[0], input_shape[1], kernel_size[1], kernel_size[0]))
    if "ne16" in dev and channel_size[1]%16!=0:
        kernel_values_=np.pad(kernel_values_,pad_width=((0,0),(0,16-channel_size[1]%16),(0,0),(0,0)))
        channel_size=tuple([channel_size[0],channel_size[1]+(16-channel_size[1]%16)])
    bias_values_=[1 for i in range(channel_size[0])]
    ir_module, params = match.create_model_conv_2d(
        input_shape = tuple(input_shape),
        weights_shape = tuple([channel_size[0], channel_size[1], kernel_size[0],kernel_size[1]]),
        weight_bits = weight_bits,
        act = act,
        padding = padding,
        strides = strides,
        weights_values = np.array(kernel_values_,dtype=np.int8),
        bias_values = np.array(bias_values_,dtype=np.int32),
        shift_bits = 8,
        depthwise = False,
        input_pad=input_pad
    )
    # Run the test

    gap_out=gap_run_match(relay_mod=ir_module, relay_params=params, output_path=str(tmp_path.absolute()),compare_x86=True,
                      accelerator_active="ne16" in dev,cluster_active="cluster" in dev,single_core="single" in dev_arr,board="board" in dev)
    
    print(f"Gap correct? {gap_out['correct']}")

    assert gap_out["correct"]

@pytest.mark.parametrize("test_params", test_params, ids=test_ids)
def test_dw_conv2d(test_params, tmp_path):
    weight_bits, act, strides, kernel_and_padding, layout_shapes, dev = test_params
    print("Dev::",dev)
    dev_arr=dev.split("_")
    dev=dev_arr[0]
    channel_size=layout_shapes[0]
    inp_size=layout_shapes[1]
    kernel_size = kernel_and_padding[0]
    padding = kernel_and_padding[1]
    kernel_values_= np.ones(shape=(channel_size[0], 1, kernel_size[1], kernel_size[0]))
    bias_values_=[1 for i in range(channel_size[0])]
    ir_module, params = match.create_model_conv_2d(
        input_shape = tuple([1,channel_size[1],inp_size[0],inp_size[1]]),
        weights_shape = tuple([channel_size[0], 1, kernel_size[0],kernel_size[1]]),
        weight_bits = weight_bits,
        act = act,
        padding = padding,
        strides = strides,
        weights_values = np.array(kernel_values_,dtype=np.int8),
        bias_values = np.array(bias_values_,dtype=np.int32),
        shift_bits = 8,
        depthwise = True
    )
    # Run the test
    gap_out=gap_run_match(relay_mod=ir_module, relay_params=params, output_path=str(tmp_path.absolute()),compare_x86=True,
                      accelerator_active="ne16" in dev,cluster_active="cluster" in dev,single_core="single" in dev_arr,board="board" in dev)
    
    print(f"Gap correct? {gap_out['correct']}")

    assert gap_out["correct"]