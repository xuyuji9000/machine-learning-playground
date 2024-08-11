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
    HUGGINGFACE_TOKEN=""

    huggingface-cli download            \
    --resume-download                   \
    --token ${HUGGINGFACE_TOKEN}        \
    --local-dir ./                      \
    microsoft/Phi-3-mini-4k-instruct  
    ```