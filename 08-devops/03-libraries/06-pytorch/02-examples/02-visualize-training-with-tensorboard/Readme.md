# Introduction

This example is referencing the following notebook
- relative path: `04-devops/01-tools/06-pytorch/01-official-tutorials/01-first-model/08-train-a-model.ipynb`


# Commands

## Initial Commands

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


## Commands during training

- tensorboard

    ``` shell
    tensorboard --logdir=runs
    ```

