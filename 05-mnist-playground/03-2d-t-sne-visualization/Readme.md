This folder contains an example using t-sne dimensionality reduction algorithm to visualize fashion-mnist dataset.

# Commands

1. Prepare virtual environment

    ``` shell
    # Check the availability of virtualenv command
    pipx list

    virtualenv -p python3 venv
    source venv/bin/activate
    ```

3. Install dependencies

    ``` shell
    pip3 install -r requirements.txt
    ```

4. Get Fashion-MNIST dataset

    ``` shell
    git submodule add https://github.com/zalandoresearch/fashion-mnist
    ```

5. Open jupyterlab server with virtual environment dependency

    ``` shell
    source venv/bin/activate

    jupyter-lab             \
    --no-browser
    ```