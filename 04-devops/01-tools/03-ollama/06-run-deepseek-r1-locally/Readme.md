This folder contains an example of comparing the performance of CPU and GPU when running deepseek-r1:1.5b.

# Commands

- pull deepseek-r1 1.5b

    ``` shell
    ollama pull deepseek-r1:1.5b
    ```

- Python virtual environment and dependencies

    ``` shell
    # open webui 
    # Requires-Python <3.12.0a1,>=3.11
    python3.11 -m venv venv

    source venv/bin/activate

    pip install -r ./requirements.txt

    ```

- Start open webui

    ``` shell
    export WEBUI_AUTH=false
    open-webui serve

    localhost:8080
    ```
