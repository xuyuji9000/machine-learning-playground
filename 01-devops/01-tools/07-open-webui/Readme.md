# Commands

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
