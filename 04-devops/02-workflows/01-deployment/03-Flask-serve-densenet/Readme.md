# Commands

1. Create a virtual environment

    ```bash
    virtualenv -p python3 venv
    source ./venv/bin/activate

    pip install -r ./requirements.txt
    ```

2. Run the Flask server

    ```bash
    flask --app main run
    ```

3. Check the URL

    ``` 
    http://127.0.0.1:5000/
    ```

4. Query the predict api from command line 

    ``` shell
    curl -X POST -F file=@images/Koalainputimage.jpg http://127.0.0.1:5000/predict
    curl -X POST -F file=@images/iceland-copy.jpeg http://127.0.0.1:5000/predict
    ```