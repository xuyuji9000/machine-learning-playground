Training a given resnet18 architecture.

Check the published model weights at [resnet_3rd-attempt][1]

# Commands
``` shell
python3 -m venv venv
source ./venv/bin/activate

pip install -r ./requirements.txt

jupyter-lab
```

``` shell
# Upload model weights to huggingface
MODEL_PATH=''
hf upload yogiman/resnet_3rd-attempt ${MODEL_PATH}
```

<!-- Reference -->

[1]: https://huggingface.co/yogiman/resnet_3rd-attempt