This is a python template directory for easy duplication.

# Commands
``` shell
# 1. Environment setup
python3 -m venv venv
source ./venv/bin/activate

pip install -r ./requirements.txt

jupyter-lab --no-browser
```

``` shell
DATASET_URL='https://huggingface.co/datasets/MIT-OL-AI-D/cifar-10-python/resolve/main/cifar-10-python.tar.gz'

wget ${DATASET_URL} \
-O ./data/cifar-10-python.tar.gz

```

[1]: https://www.geeksforgeeks.org/deep-learning/contrastive-learning-with-simclr-in-pytorch/

