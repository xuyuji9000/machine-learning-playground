from safetensors import safe_open

file_path = "/Users/karlxu/Workspace/github/comfyanonymous/ComfyUI/models/checkpoints/sd_xl_base_1.0.safetensors"

with safe_open(file_path, framework="pt") as f:
    for key in f.keys():
        print(key)