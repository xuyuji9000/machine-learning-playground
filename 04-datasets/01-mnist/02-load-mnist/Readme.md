This folder contains an example of loading mnist dataset.

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

3. Open jupyterlab server with virtual environment dependency

    ``` shell
    source venv/bin/activate

    jupyter-lab             \
    --no-browser
    ```

