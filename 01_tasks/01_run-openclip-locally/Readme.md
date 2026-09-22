- Run openclip locally
- run clip eval \
use `clip_benchmark` command

# Commands

``` shell
virtualenv -p python3 venv
source ./venv/bin/activate
pip install -r requirements.txt
python3 run_openclip.py            # zero-shot demo on a downloaded image
python3 run_openclip.py my.jpg     # or classify your own image

# CLIP benchmark (zero-shot CIFAR-10 classification)
# Note: requires datasets/cifar-10-python.tar.gz (official source www.cs.toronto.edu
# is very slow / truncates; HF mirror used:
#   https://huggingface.co/datasets/liangnanying/cifar-10-python/resolve/main/cifar-10-python.tar.gz
#   sha256: 6d958be074577803d12ecdefd02955f39262c83c16fe9348329d7fe0b5c001ce)
# Two local patches in venv (re-apply after reinstalling venv):
#   1. metrics/zeroshot_classification.py L82: numpy>=2 fix (float() on 1-elem array)
#   2. cli.py run(): use device "mps" on Apple Silicon (upstream only picks cuda/cpu);
#      MPS gave ~7x speedup vs CPU (~70s vs ~8min), acc within fp16 rounding

DATASET='cifar10'
DATASET='stl10'

clip_benchmark eval             \
--dataset "${DATASET}"          \
--dataset_root datasets         \
--model ViT-B-32                \
--pretrained laion2b_s34b_b79k  \
--task zeroshot_classification  \
--batch_size 128                \
--num_workers 8                 \
--output results
```



# Files

- `OPENCLIP_NOTES.md` — what OpenCLIP is, architecture, usage
- `DATASETS.md` — dataset options (resolutions, sizes, mirrors) for further benchmarking
- `run_openclip.py` — zero-shot classification demo (CPU/MPS/CUDA)