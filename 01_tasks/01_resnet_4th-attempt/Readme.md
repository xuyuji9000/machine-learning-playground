An [article][1] about resnet18.

# Commands

``` shell
# Prepare python virtual environment
# Install dependency
# Run jupyter-lab as headless backend

python3 -m venv venv
source ./venv/bin/activate

pip install -r ./requirements.txt

jupyter-lab --no-browser
```

``` shell
# The original toronto university data source was too slow
# So, downloading it from the hugging face mirror source.
DATASET_URL='https://huggingface.co/datasets/MIT-OL-AI-D/cifar-10-python/resolve/main/cifar-10-python.tar.gz'

wget ${DATASET_URL} \
-O ./data/cifar-10-python.tar.gz

```

``` shell
# Upload model weights to huggingface
MODEL_PATH='./model/resnet18_cifar10_20261006_184045.pth'
REMOTE_PATH='./4th-attempt/'

hf upload yogiman/resnet ${MODEL_PATH} ${REMOTE_PATH}


```

[1]: https://www.geeksforgeeks.org/deep-learning/resnet18-from-scratch-using-pytorch/