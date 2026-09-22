Run openclip locally

# Commands

``` shell
virtualenv -p python3 venv
source ./venv/bin/activate
pip install -r requirements.txt
python3 run_openclip.py            # zero-shot demo on a downloaded image
python3 run_openclip.py my.jpg     # or classify your own image
```

# Files

- `OPENCLIP_NOTES.md` — what OpenCLIP is, architecture, usage
- `run_openclip.py` — zero-shot classification demo (CPU/MPS/CUDA)