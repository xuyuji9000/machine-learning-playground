This folder contains an example of using [mnist library](https://github.com/datapythonista/mnist) to load [fashion-mnist dataset](https://github.com/zalandoresearch/fashion-mnist?tab=readme-ov-file).


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

4. Open jupyterlab server with virtual environment dependency

    ``` shell
    source venv/bin/activate

    jupyter-lab             \
    --no-browser
    ```
