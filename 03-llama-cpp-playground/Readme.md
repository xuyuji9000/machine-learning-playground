# Commands

1. Prepare virtual environment

    ``` shell
    # check virtualenv binary in pipx
    pipx list

    virtualenv -p python3 venv

    source ./venv/bin/activate

    pip3 install -r ./requirements.txt
    ```

2. Import the `llama_cpp_python` library

    ``` python
    from llama_cpp import Llama
    ```
