# Commands

``` shell

AUDIO_FILE_PATH="./data/GKwRIJIKXS3LAzoZMwLsGIQf.m4a"
OUTPUT_DIR="./output"

# --model 
# tiny, base, small, medium, large
time whisper "${AUDIO_FILE_PATH}"   \
--model small                        \
--language Chinese                  \
--output_format srt                 \
--initial_prompt "请将内容翻译成中文"  \
--output_dir "${OUTPUT_DIR}"
```
