# Commands

- Convert f16 model to q4_0 model

``` shell
LLAMA_CPP_PATH="/Users/karlxu/Workspace/github/ggerganov/llama.cpp"
cd "${LLAMA_CPP_PATH}"

WORKING_DIR="/Users/karlxu/Workspace/github/xuyuji9000/machine-learning-playground/04-devops/01-tools/02-llama-cpp/03-quantize-to-q4_0"
TARGET_QUANTIZATION="q4_0"

time ./quantize                                                              \
${WORKING_DIR}/models/microsoft/Phi-3.5-mini-instruct-f16.gguf          \
${WORKING_DIR}/models/microsoft/Phi-3.5-mini-instruct-${TARGET_QUANTIZATION}.gguf \
${TARGET_QUANTIZATION}
```


