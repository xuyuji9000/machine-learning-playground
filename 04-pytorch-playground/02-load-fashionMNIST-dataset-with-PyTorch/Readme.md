This folder containing the learning example about loading [Fashion-MNIST](https://github.com/zalandoresearch/fashion-mnist) dataset with PyTorch.

And PyTorch contains [FashionMNIST](https://pytorch.org/vision/stable/generated/torchvision.datasets.FashionMNIST.html#torchvision.datasets.FashionMNIST) dataset's function reference as well.

# Commands

1. Prepare virtual environment

    ``` shell
    # Check the availability of virtualenv command
    pipx list

    virtualenv -p python3 venv
    source venv/bin/activate
    ```
2. Install dependencies

    ``` shell
    pip3 install -r requirements.txt
    ```

3. Open jupyterlab server with virtual environment dependency

    ``` shell
    source venv/bin/activate

    jupyter-lab
    ```

