# Starting from Ubuntu 20.04
FROM ubuntu:22.04
SHELL   ["/bin/bash", "-c"]
# Setting values for tzdata
ENV DEBIAN_FRONTEND=noninteractive
# libncurses5 is needed for using pulps gdb
COPY . /match
COPY docker-gap/gap9_sdk /gap9_sdk
COPY docker-gap/dory /dory

# General
RUN apt-get update && apt-get install -y sudo cmake

# utility
RUN apt-get install -y vim 

RUN apt-get install -y python3 python3-dev python3-setuptools gcc libtinfo-dev zlib1g-dev build-essential cmake libedit-dev libxml2-dev

# Pulp-sdk requirements
WORKDIR /gap9_sdk
RUN cat requirements_apt_ubuntu_22_04.md | xargs apt install -y
# Pulp toolchain
WORKDIR /
RUN  git clone https://github.com/GreenWaves-Technologies/gap_riscv_toolchain_ubuntu.git
RUN  cd gap_riscv_toolchain_ubuntu && \
    ./install.sh /gap9-toolchain && \
    rm -r /gap_riscv_toolchain_ubuntu
ENV PATH="${PATH}:/gap9-toolchain"
ENV GAP_RISCV_GCC_TOOLCHAIN="/gap9-toolchain"
# Pulp sdk installazione
WORKDIR /gap9_sdk
# chown per risolvere i problemi di copia di windows
RUN chmod -R 775 /gap9_sdk &&\
    source configs/gap9_evk_audio.sh &&\
    pip install -r requirements.txt -r tools/nntool/requirements.txt -r utils/gapy_v2/requirements.txt && \
    make clean all && \
    echo "source /gap9_sdk/configs/gap9_evk_audio.sh" >> /root/.bashrc

# install DORY, fork with GAP9_TVM, in local for now
WORKDIR /dory
# RUN git clone https://github.com/francescodaghero/dory.git
# WORKDIR /dory
# RUN git submodule update --remote --init --recursive
RUN pip3 install -e .
# Setting up dependencies for tvm
RUN dpkg --add-architecture i386 && apt-get update && apt-get install -y git python3 python3-dev python3-setuptools gcc libtinfo-dev zlib1g-dev build-essential cmake libedit-dev libxml2-dev python3-pip llvm gcc-multilib libc6-dbg:i386 gdb curl libncurses5 unzip sudo rsync
RUN git submodule update --init --recursive
# Installing dependencies of the python package
RUN pip3 install numpy decorator attrs scipy pytest 

WORKDIR /match-tvm
RUN pip3 install --user typing-extensions psutil scipy numpy decorator attrs pybind11
WORKDIR /match
RUN echo "export TVM_HOME=/match/match-tvm" >> /root/.bashrc
RUN echo "export PYTHONPATH=${TVM_HOME}/python:/match/zigzag:${PYTHONPATH}" >> /root/.bashrc
RUN python3 setup.py install --user
WORKDIR /match/zigzag
RUN pip3 install --user numpy networkx sympy matplotlib onnx tqdm multiprocessing_on_dill
WORKDIR /match
