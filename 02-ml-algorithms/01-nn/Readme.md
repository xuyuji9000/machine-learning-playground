This folder documents learning examples of neural network ( **NN** ) foundational concepts / algorithms.

Like:

- gradient descent
- loss function
- ...

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
