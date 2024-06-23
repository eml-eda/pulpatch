# Starting from Ubuntu 20.04
FROM ubuntu:22.04
SHELL   ["/bin/bash", "-c"]
# Update and upgrade the system
RUN apt update && apt upgrade -y

# Install all the needed dependencies
RUN DEBIAN_FRONTEND=noninteractive TZ=Europe/Rome apt install -y \
    autoconf \
    automake \
    bison \
    build-essential \
    cmake \
    curl \
    device-tree-compiler \
    doxygen \
    flex \
    git \
    graphicsmagick-libmagick-dev-compat \
    graphviz \
    gtkwave \
    libfdt-dev \
    libftdi-dev \
    libftdi1 \
    libjpeg-dev \
    libsdl2-dev \
    libsdl2-ttf-dev \
    libsndfile1-dev \
    libtool \
    libusb-1.0-0-dev \
    ninja-build \
    pkg-config \
    python3-pip \
    qtbase5-dev \
    libqt5charts5-dev \
    rsync \
    texinfo \
    wget \
    qt6-base-dev \
    libqt6serialport6-dev \
    libgl1-mesa-dev \
    unzip \
    sudo \
    gdb \
    autoconf \
    automake \
    autotools-dev \
    curl \
    libmpc-dev \
    libmpfr-dev \
    libgmp-dev \
    gawk \
    build-essential \
    bison \
    flex \
    texinfo \
    gperf \
    libtool \
    patchutils \
    bc \
    zlib1g-dev \
    build-essential \
    git \
    libftdi-dev \
    libftdi1 \
    doxygen \
    python3-pip \
    libsdl2-dev \
    curl \
    cmake \
    libusb-1.0-0-dev \
    scons \
    gtkwave \
    libsndfile1-dev \
    rsync \
    autoconf \
    automake \
    texinfo \
    libtool \
    pkg-config \
    libsdl2-ttf-dev \
    vim
# libncurses5 is needed for using pulps gdb
WORKDIR /
RUN git clone --recursive https://github.com/eml-eda/match.git
RUN cd match
RUN make all
# General
RUN apt-get update && apt-get install -y sudo cmake

# utility
RUN apt-get install -y vim 

RUN apt-get install -y python3 python3-dev python3-setuptools gcc libtinfo-dev zlib1g-dev build-essential cmake libedit-dev libxml2-dev

# Change directory to /
WORKDIR /

RUN wget https://github.com/pulp-platform/pulp-riscv-gnu-toolchain/releases/download/v1.0.16/v1.0.16-pulp-riscv-gcc-ubuntu-18.tar.bz2

RUN tar -xf v1.0.16-pulp-riscv-gcc-ubuntu-18.tar.bz2

RUN rm v1.0.16-pulp-riscv-gcc-ubuntu-18.tar.bz2

RUN mv /v1.0.16-pulp-riscv-gcc-ubuntu-18 /pulp_toolchain

WORKDIR /pulp_toolchain

# Make the sourceme.sh file executable
RUN chmod +x sourceme.sh

# Source the sourceme.sh file
RUN /bin/bash -c "source sourceme.sh"

WORKDIR /

RUN git clone --recursive https://github.com/pulp-platform/pulp-sdk.git

WORKDIR /pulp-sdk

RUN git submodule update --remote --recursive

RUN rm -r tools/gvsoc

WORKDIR /pulp-sdk/tools

RUN git clone --recursive https://github.com/eml-eda/gvsoc.git

WORKDIR /pulp-sdk

RUN pip3 install argcomplete pyelftools prettytable six mako rich

ENV PULP_RISCV_GCC_TOOLCHAIN=/pulp_toolchain

RUN /bin/bash -c "source configs/pulp-open.sh"

RUN chmod +x configs/pulp-open.sh

COPY docker/pulp-open/build_open.sh .

RUN /bin/bash -c "source build_open.sh"
# RUN git submodule update --remote --init --recursive
RUN pip3 install -e .
# Setting up dependencies for tvm
RUN dpkg --add-architecture i386 && apt-get update && apt-get install -y git python3 python3-dev python3-setuptools gcc libtinfo-dev zlib1g-dev build-essential cmake libedit-dev libxml2-dev python3-pip llvm gcc-multilib libc6-dbg:i386 gdb curl libncurses5 unzip sudo rsync
RUN git submodule update --init --recursive
# Installing dependencies of the python package
RUN pip3 install numpy decorator attrs scipy pytest 

RUN pip3 install --user typing-extensions psutil scipy numpy decorator attrs pybind11
WORKDIR /match
RUN echo "export TVM_HOME=/match/match-tvm" >> /root/.bashrc
RUN echo "export PYTHONPATH=${TVM_HOME}/python:/match/zigzag:${PYTHONPATH}" >> /root/.bashrc
RUN python3 setup.py install --user
WORKDIR /match/zigzag
RUN pip3 install --user numpy networkx sympy matplotlib onnx tqdm multiprocessing_on_dill
WORKDIR /match
