Refer to [machine-learning-playground/issues/6](https://github.com/xuyuji9000/machine-learning-playground/issues/6)

The effort to create a llama 1 "hello world" example has been **DROPPED**.

# Introduction

This folder contains the example about using llama 1 7B model .

# Commands

- Prepare the virtual environment

    ``` shell
    python3 -m venv venv

    source ./venv/bin/activate


    pip3 install jupyter
    pip3 install torch torchvision torchaudio

    pip3 install transformers
    
    ```
- Start jupyter notebook backend for visual studio code

    ``` shell
    source ./venv/bin/activate
    
    jupyter notebook       \
    --no-browser           \
    --NotebookApp.token=''
    ```
