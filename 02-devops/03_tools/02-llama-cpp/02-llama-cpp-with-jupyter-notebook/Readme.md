# Commands

1. Prepare Python virtual environment and dependency

    ``` shell
    virtualenv -p python3 venv
    source venv/bin/activate

    pip3 install                        \
    --requirement ./requirements.txt
    ```

2. Start JupyterLab

    ``` shell
    source venv/bin/activate

    jupyter-lab             \
    --no-browser
    ```

3. Download model from HuggingFace

    ``` shell
    HUGGINGFACE_TOKEN=""
    REPO_ID="TheBloke/zephyr-7B-beta-GGUF"
    FILENAME="zephyr-7b-beta.Q4_K_M.gguf"
    

    huggingface-cli download            \
    --resume-download                   \
    --token ${HUGGINGFACE_TOKEN}        \
    --local-dir ./models/               \
    "${REPO_ID}" "${FILENAME}"
    ```

4. Running with built-in server

    ``` shell
    pip install 'llama-cpp-python[server]'

    python3 -m llama_cpp.server --model models/llama-model.gguf

    # check localhost:8000/docs
    ```
