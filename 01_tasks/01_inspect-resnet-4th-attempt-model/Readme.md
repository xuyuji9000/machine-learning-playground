This is a python template directory for easy duplication.

# Commands
``` shell
python3 -m venv venv
source ./venv/bin/activate

pip install -r ./requirements.txt

jupyter-lab --no-browser
```

```shell
           REPO_ID='yogiman/resnet'
MODEL_WEIGHTS_FILE='4th-attempt/resnet18_cifar10_20261006_184045.pth'

hf download             \
--local-dir ./model/    \
${REPO_ID}              \
${MODEL_WEIGHTS_FILE}

```