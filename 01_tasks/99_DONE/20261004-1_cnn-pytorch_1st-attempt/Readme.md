# Commands
``` shell
python3 -m venv venv
source ./venv/bin/activate

pip install -r ./requirements.txt

jupyter-lab --no-browser

```

``` shell
# Upload local model weights 
# to remote huggingface repository
LOCAL_PATH=''

REPO_ID='yogiman/cnn'
PATH_IN_REPO='1st-attempt/'

hf upload ${REPO_ID}  ${LOCAL_PATH} ${PATH_IN_REPO}
```

``` shell
# curl command to mitigate default torchvison default download failure
mkdir -p data/MNIST/raw/

BASE="https://ossci-datasets.s3.amazonaws.com/mnist"
curl -L -o data/MNIST/raw/train-images-idx3-ubyte.gz "$BASE/train-images-idx3-ubyte.gz"
curl -L -o data/MNIST/raw/train-labels-idx1-ubyte.gz "$BASE/train-labels-idx1-ubyte.gz"
curl -L -o data/MNIST/raw/t10k-images-idx3-ubyte.gz "$BASE/t10k-images-idx3-ubyte.gz"
curl -L -o data/MNIST/raw/t10k-labels-idx1-ubyte.gz "$BASE/t10k-labels-idx1-ubyte.gz"

```

# Model Weights URL
[yogiman/cnn-torch_1st-attempt](https://huggingface.co/yogiman/cnn-torch_1st-attempt)
