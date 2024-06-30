Check the model card of [zephyr-7B-beta-GGUF](https://huggingface.co/TheBloke/zephyr-7B-beta-GGUF).

It seems the **Q4_K_M** is the suggested quantization method.

So, using **zephyr-7b-beta.Q4_K_M.gguf** model for the following experiment.

# Commands
1. Prepare Python virtual environment and dependency

    ``` shell
    virtualenv -p python3 venv
    source venv/bin/activate

    pip3 install                        \
    --requirement ./requirements.txt
    ```

2. Download model from HuggingFace

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

3. Execute the model

    ``` shell
    source venv/bin/activate

    python3 ./main.py
    ```