
# Commands

1. Prepare virtual environment

    ``` shell
    # Check the availability of virtualenv command
    pipx list

    virtualenv -p python3 venv
    source venv/bin/activate
    ```

2. Get Fashion-MNIST dataset

    ``` shell
    git submodule add https://github.com/zalandoresearch/fashion-mnist
    ```

3. Open jupyterlab server with virtual environment dependency

    ``` shell
    source venv/bin/activate

    jupyter-lab             \
    --no-browser
    ```


<!---

2. Install dependencies

    ``` shell
    pip3 install -r requirements.txt
    ```
--->