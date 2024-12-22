This folder documents the learning examples of HuggingFace platform.

# Commands

1. Install HuggingFace command line client on Mac

    ``` shell
    brew update

    export HOMEBREW_NO_AUTO_UPDATE=1

    brew install --verbose huggingface-cli
    ```

2. Downloading files from HuggingFace repository

    ``` shell
    # Refer to the .token file for the token
    HUGGINGFACE_TOKEN=`cat .token`

    huggingface-cli download                                \
    --resume-download                                       \
    --token ${HUGGINGFACE_TOKEN}                            \
    --local-dir ./models/microsoft/Phi-3.5-mini-instruct    \
    microsoft/Phi-3.5-mini-instruct
    ```