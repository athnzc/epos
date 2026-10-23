FROM nvcr.io/nvidia/tensorflow:23.03-tf1-py3

ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y --no-install-recommends \
    cmake ninja-build libosmesa6-dev libgl1-mesa-dev \
    && rm -rf /var/lib/apt/lists/*
RUN python -m pip install --no-cache-dir \
    pybind11==2.10.4 libigl==2.4.1 opencv-python-headless==4.7.0.72 \
    PyYAML==6.0.1 imageio==2.9.0 pypng==0.20220715.0 tabulate==0.8.3

COPY external/bop_renderer /opt/epos-renderer
COPY setup/prepare_renderer.py /opt/prepare_renderer.py
RUN python /opt/prepare_renderer.py \
    && cmake -S /opt/epos-renderer -B /opt/epos-renderer/build \
       -DCMAKE_BUILD_TYPE=Release \
       -Dpybind11_DIR=$(python -m pybind11 --cmakedir) \
    && cmake --build /opt/epos-renderer/build --parallel 4

ENV REPO_PATH=/workspace/epos \
    STORE_PATH=/workspace/epos/store \
    BOP_PATH=/workspace/epos/datasets \
    TF_DATA_PATH=/workspace/epos/store/tf_data \
    TF_MODELS_PATH=/workspace/epos/store/tf_models \
    PYTHONPATH=/workspace/epos:/workspace/epos/external/bop_toolkit:/workspace/epos/external/slim:/opt/epos-renderer/build \
    TF_FORCE_GPU_ALLOW_GROWTH=true
WORKDIR /workspace/epos/scripts
