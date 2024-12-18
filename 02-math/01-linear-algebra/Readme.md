# Commands

1. Prepare Python virtual environment

    ```bash
    virtualenv -p python3 venv
    source .venv/bin/activate
    ```
2. Install dependencies

    ```bash
    pip freeze > requirements.txt
    pip install -r requirements.txt
    ```

3. Start Jupyter Lab

    ```bash
    jupyter-lab
    ```
