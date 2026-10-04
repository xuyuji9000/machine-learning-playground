# Commands
``` shell
python3 -m venv venv
source ./venv/bin/activate

pip install -r ./requirements.txt

jupyter-lab

```

``` shell
# Upload local model weights 
# to remote huggingface repository
MODEL_PATH=''
hf upload yogiman/cnn-torch_1st-attempt ${MODEL_PATH}
```

# Model Weights URL
[yogiman/cnn-torch_1st-attempt](https://huggingface.co/yogiman/cnn-torch_1st-attempt)
