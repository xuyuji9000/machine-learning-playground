# Commands

1. Build the model file

    ``` shell
    ollama create Phi-3.5-mini-instruct-q8_0 \
    -f ./Modelfile
    ```

2. Prepare open webui

    ``` shell
    # open webui 
    # Requires-Python <3.12.0a1,>=3.11
    virtualenv -p python3.11 venv

    source venv/bin/activate

    pip install -r ./requirements.txt

    ```

3. Start open webui

    ``` shell
    export WEBUI_AUTH=false
    open-webui serve

    localhost:8080
    ```
