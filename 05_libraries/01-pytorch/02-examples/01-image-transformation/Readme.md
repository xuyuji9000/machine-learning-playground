# Introduction

- PyTorch models expect input in tensor format
- Each image model has its own expactation of the input data dimension

A input image need to be transformed.
So, it can fit the Pytorch and image model expectation.

# Commands

1. Prepare virtual environment

    ``` shell
    # Check the availability of virtualenv command
    pipx list

    virtualenv -p python3 venv
    source venv/bin/activate
    ```
2. Install dependencies

    ``` shell
    pip3 install -r requirements.txt
    ```

3. Start JupyterLab

    ``` shell
    source venv/bin/activate

    jupyter-lab             \
    --no-browser
    ```
