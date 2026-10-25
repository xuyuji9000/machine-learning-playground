This directory document a way of using whisper with Apple's CoreML.
github [repository](https://github.com/ggerganov/whisper.cpp) .

# Commands

- prepare Python virtual environment and install dependencies

``` shell
python3.12 -m venv venv
source venv/bin/activate

# symbolic link of the requirements.txt
# ln -s ORIGINAL_FILE_PATH ./TARGET_FILE_PATH
pip install -r requirements.txt
pip install git+https://github.com/openai/whisper.git
```

- download whisper.cpp model
``` shell
sh ./models/download-ggml-model.sh base.en
```


- generate core ml model

``` shell
./models/generate-coreml-model.sh base.en
```

