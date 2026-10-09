# OpenCLIP Notes

## What is OpenCLIP?

Open-source implementation of **CLIP** (Contrastive Language–Image Pre-training) by
Mila / mlfoundations (`mlfoundations/open_clip`). Trained on web-scale datasets
(CLAIR, LAION-2B, LAION-5B). Name is a pun: "open" source + "OPEN" dataset.

## Architecture

- **Image encoder**: ViT (B/16, L/14, bigG), ResNet/RN50, ConvNeXt, MobileCLIP...
- **Text encoder**: Transformer
- Both project into a **shared embedding space**; trained contrastively on
  ~400M+ (LAION variants: up to 9.8B) image-text pairs with InfoNCE loss.

## Key capabilities

1. **Zero-shot image classification** — score image against text prompts
   ("a photo of a {label}")
2. **Image ↔ text retrieval** — cross-modal similarity search
3. **Image similarity / dedup** — compare embeddings (cosine similarity)
4. Foundation for Stable Diffusion text encoders, reward models, etc.

## Installation

```shell
pip install open-clip-torch
```

## Model registry

Model + pretrained data are selected by name, e.g.:

```python
model, _, preprocess = open_clip.create_model_and_transforms(
    "ViT-B-32", pretrained="laion2b_s34b_b79k")
```

- List all: `python -m open_clip_model list_models`
- List pretrained tags for a model: `python -m open_clip_model list_pretrained ViT-B-32`
- Checkpoints are downloaded & cached to `~/.cache/huggingface` (or torch hub cache).

## Usage sketch

```python
from PIL import Image
import torch, open_clip

model, _, preprocess = open_clip.create_model_and_transforms(
    "ViT-B-32", pretrained="laion2b_s34b_b79k")
tokenizer = open_clip.get_tokenizer("ViT-B-32")

image = preprocess(Image.open("dog.jpg")).unsqueeze(0)
text = tokenizer(["a dog", "a cat"])

with torch.no_grad(), torch.autocast("cuda"):
    img_f = model.encode_image(image)
    txt_f = model.encode_text(text)
    img_f /= img_f.norm(dim=-1, keepdim=True)
    txt_f /= txt_f.norm(dim=-1, keepdim=True)
    probs = (100.0 * img_f @ txt_f.T).softmax(dim=-1)
```

## Local run in this folder

See `run_openclip.py` — zero-shot classification demo, CPU/MPS compatible.
