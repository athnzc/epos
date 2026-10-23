#!/usr/bin/env bash
STORE_PATH_HOST=$1
BOP_PATH_HOST=$2
set -euo pipefail
repo_path="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"
exec docker -H unix:///var/run/docker.sock run --rm --pull=never \
  --user "$(id -u):$(id -g)" --shm-size=2g \
  -v $BOP_PATH_HOST:/workspace/epos/datasets \
  -v $STORE_PATH_HOST/tf_data:/workspace/epos/tf_data \
  -v $STORE_PATH_HOST/tf_models:/workspace/epos/tf_models \
  -e TF_CPP_MIN_LOG_LEVEL=3 -e BOP_PATH=/workspace/epos/datasets \
  -e TF_MODELS_PATH=/workspace/epos/tf_models -e OMP_NUM_THREADS=8 -e OPENBLAS_NUM_THREADS=1 -e TF_DATA_PATH=/workspace/epos/tf_data \
  --mount "type=bind,src=$repo_path,dst=/workspace/epos" -v $(pwd)/dataset_params.py:/workspace/epos/external/bop_toolkit/bop_toolkit_lib/dataset_params.py \
  epos:pose python infer.py --model=spaghetti-spraying-xc65-f64 \
  --checkpoint_name=model.ckpt-100000 --vis=true \
  --task_type=localization --fitting_method=progressive_x \
  --oracle_instance_masks=false --orientation_prior_refine=false \
  --infer_name=standard-rgb-test
