# Introduction

In the [toolcall finetuning example](../99_DONE/20261107-1_read-llm-toolcall-finetuning-example_1st-attempt/),   
It did not contain low friction base model to work with.

[Gemini suggested](./Qwen%20Model%20Fine-Tuning%20Guide.pdf) some Qwen based options.

And the [Qwen2.5-3B-Instruct](https://huggingface.co/Qwen/Qwen2.5-3B-Instruct) repo on huggingface
  


STATES

- 🟧 PENDING
- 🟩 DONE

# Actions

1. try out Qwen2.5-3B-Instruct model \

   Status: 🟧 PENDING

# Commands

``` shell
# 1. list available accounts
hf auth list

export HF_XET_HIGH_PERFORMANCE=1
hf download Qwen/Qwen2.5-3B-Instruct

hf cache list
hf cache rm model/Qwen/Qwen2.5-3B-Instruct
```


``` shell
python3 -m venv venv
source ./venv/bin/activate

pip3 install -r ./requirements.txt
```