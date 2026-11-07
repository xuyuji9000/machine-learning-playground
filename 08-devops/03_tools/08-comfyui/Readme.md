# Commands

- setup python virtual environment 

``` shell
cd ~/Workspace/github/comfyanonymous/ComfyUI

virtualenv -p python3 venv
source venv/bin/activate
pip install -r ./requirements.txt

```

- list available models
``` shell
cd ~/Workspace/github/comfyanonymous/ComfyUI
ls -1 ./models/checkpoints/
```

- start

``` shell
python main.py

http://127.0.0.1:8188
```