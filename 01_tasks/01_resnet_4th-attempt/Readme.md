An [article][1] about resnet18.

# Commands
``` shell
python3 -m venv venv
source ./venv/bin/activate

pip install -r ./requirements.txt

jupyter-lab --no-browser

# The original toronto university data source was too slow
# So, downloading it from the hugging face mirror source.
DATASET_URL='https://huggingface.co/datasets/MIT-OL-AI-D/cifar-10-python/resolve/main/cifar-10-python.tar.gz'

wget ${DATASET_URL} \
-O ./data/cifar-10-python.tar.gz

```

[1]: https://www.geeksforgeeks.org/deep-learning/resnet18-from-scratch-using-pytorch/