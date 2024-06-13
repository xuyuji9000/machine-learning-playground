# Commands

1. Setup environment

    ``` shell
    virtualenv -p python3.11 venv

    source ./venv/bin/activate
    ```

2. Install requirements

    ``` shell
    pip install -r ./requirements.txt
    ```

3. Running **open-webui**

    ``` shell
    export WEBUI_AUTH=false

    open-webui serve
    ```
