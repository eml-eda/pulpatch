# Run DNNs on GAP9 with MATCH!

This repository serves as a wrapper for MATCH with GAP9, supporting currently both the cluster and the NE16 accelerator.

The user is reccomended to check the usage section of MATCH(https://github.com/eml-eda/match/blob/main/README.md)

# Installation

## Docker

To use MATCH the user should clone the MATCH repository and from there clone the current repository, put in the deps folder the gap9 SDK, and from the root of match build the docker image.
```
$ git clone --recursive https://github.com/eml-eda/match.git
$ cd match
$ cd docker
$ git clone --recursive https://github.com/eml-eda/match_gap9.git gap
$ cd gap
$ mkdir deps
$ cd deps
$ cp /path/to/sdk gap9_sdk
$ cd ../../../
$ docker build . -f docker/gap/Dockerfile -t gap-match
```

## Local

If the user has the Gap9 SDK already installed in a Ubuntu machine, the user shall follow these steps
```
$ git clone --recursive https://github.com/eml-eda/match_gap9.git
$ cd match_gap9
$ python3 setup.py install --user
$ cd ..
$ git clone --recursive https://github.com/eml-eda/match.git
$ cd match
$ make all
```

## Usage

> [!IMPORTANT]
> Currently this tool expects all the paths to be **absolute**

This tool compiles and run a network over GAP9, to use it the user should run the gap_run.py script, which expects some parameters:
- `-o path` : output path of the network
- `-f input_file` : path to the file defining the network in ONNX (or relay as well; in that case the user shall also use the -p path argument to define the file used to store the weights and other parameters of the TVM Relay IR network)
- `-i input_type` : type of the input, which currently can be either onnx or relay
- `--ne16` : if the user wants to generate a network using also the NE16 accelerator
- `--cluster` : if the user wants to generate a network using also the cluster
- `--board` : to run the network over a phisical board instead of GvSoC
- `-g` : we need to provide the absolute path to the GAP_SDK(defaults to /home/gap_sdk/private)

> [!IMPORTANT]
> The default configuration compiles the network on OPT level 3 with GCC, the user can modify this parameter, if the network doesn't run on the board this may be the primary issue.

> [!IMPORTANT]
> MATCH prefers a network generated through PLINIO currently.

# Examples

Thanks to MATCH there are available already a few network examples, for example to target a 2d convolution with batchnorm and requantization the user can use the -c flag.

Therefore to target the cluster for this small network the user can run the following script:
```
$ python3 match_gap/run.py -c -o output_path --cluster -g /home/gap_sdk_private
```

There also bigger network available already, for example a small mobilenet
```
$ python3 match_gap/run.py -o output_path --cluster -i onnx -f /path/to/match/examples/small_mobilenet_V1.onnx -g /home/gap_sdk_private
```

There are also a few tests of 2d convolutions and depthwise convolutions that the user can run over both NE16 and the cluster separetely

```
$ pytest -v test.py
```
