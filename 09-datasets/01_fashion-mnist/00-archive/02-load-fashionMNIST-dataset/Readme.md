This folder documents an example about using [zalandoresearch/fashion-mnist](https://github.com/zalandoresearch/fashion-mnist) 's own util `mnist_reader` to load fashion-MNIST dataset.

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
