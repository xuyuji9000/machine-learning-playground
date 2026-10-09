This is a python template directory for easy duplication.

# Commands
``` shell
# 1. Environment setup
python3 -m venv venv
source ./venv/bin/activate

pip install -r ./requirements.txt

mojokernel install --sys-prefix
jupyter kernelspec list

MOJO_KERNEL_ENGINE=pexpect jupyter-lab --no-browser
```