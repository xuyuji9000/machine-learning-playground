This folder contains an example about using t-sne algorithm to do dimentionality reduction on the fashion-mnist dataset to 3d.

And visualize the 3d data.

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
    pip3 install        \
    -r requirements.txt
    ```

4. Open jupyterlab server with virtual environment dependency

    ``` shell
    source venv/bin/activate

    jupyter-lab             \
    --no-browser
    ```
