Step through pytorch model layers. \
Using [CNN 1st attempt weights][1] in this experiment.

# Commands

## 1. Environment Setup
``` shell

python3 -m venv venv
source ./venv/bin/activate

pip install -r ./requirements.txt

jupyter-lab --no-browser
```





## 2. Download Model

```shell
# Download model from Hugging Face
# - architecture
# - weights
# - support utils
# included
hf download \
yogiman/cnn \
--local-dir ./model/

```





## 3. Download dataset
``` shell
# Down validation, training dataset
# curl command to mitigate default torchvison default download failure
mkdir -p data/MNIST/raw/

BASE="https://ossci-datasets.s3.amazonaws.com/mnist"
curl -L -o data/MNIST/raw/train-images-idx3-ubyte.gz "$BASE/train-images-idx3-ubyte.gz"
curl -L -o data/MNIST/raw/train-labels-idx1-ubyte.gz "$BASE/train-labels-idx1-ubyte.gz"
curl -L -o data/MNIST/raw/t10k-images-idx3-ubyte.gz "$BASE/t10k-images-idx3-ubyte.gz"
curl -L -o data/MNIST/raw/t10k-labels-idx1-ubyte.gz "$BASE/t10k-labels-idx1-ubyte.gz"

```

<!-- Reference -->
[1]: https://huggingface.co/yogiman/cnn/blob/main/1st-attempt/simple_cnn_mnist_20261007_112945.safetensors
[2]: https://www.digitalocean.com/community/tutorials/pytorch-hooks-gradient-clipping-debugging
[3]: https://docs.pytorch.org/docs/2.14/generated/torch.Tensor.register_hook.html
