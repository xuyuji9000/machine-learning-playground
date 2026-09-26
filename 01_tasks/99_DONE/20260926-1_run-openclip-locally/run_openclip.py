"""Run OpenCLIP locally: zero-shot image classification demo.

Usage:
    python run_openclip.py [path/to/image.jpg]

If no image is given, a small demo image is downloaded.
Works on CPU / Apple MPS (no CUDA required).
"""

import sys
import urllib.request
from pathlib import Path

import torch
import open_clip
from PIL import Image

MODEL_NAME = "ViT-B-32"
PRETRAINED = "laion2b_s34b_b79k"  # ~600MB, cached to ~/.cache/huggingface

CANDIDATE_LABELS = [
    "a photo of a cat",
    "a photo of a dog",
    "a photo of a bird",
    "a photo of a car",
    "a photo of an airplane",
    "a photo of a mountain landscape",
    "a photo of a city street",
    "a photo of food",
    "a photo of apartment",
]

# NOTE: use S3 path-style URL. The virtual-host URL
# (https://images.cocodataset.org/...) serves a cert for s3.amazonaws.com,
# which fails hostname verification.
DEMO_IMAGE_URL = (
    "https://s3.amazonaws.com/images.cocodataset.org/val2017/000000037777.jpg"  # two cats on a couch
)


def get_device() -> str:
    if torch.cuda.is_available():
        return "cuda"
    if torch.backends.mps.is_available():
        return "mps"
    return "cpu"


def load_image(path: str | None) -> Image.Image:
    if path:
        return Image.open(path).convert("RGB")
    local = Path("demo_image.jpg")
    if not local.exists():
        print(f"Downloading demo image to {local} ...")
        urllib.request.urlretrieve(DEMO_IMAGE_URL, local)
    return Image.open(local).convert("RGB")


def main() -> None:
    device = get_device()
    print(f"Loading {MODEL_NAME} ({PRETRAINED}) on {device} ... "
          "(weights download once, then cached)")

    model, _, preprocess = open_clip.create_model_and_transforms(
        MODEL_NAME, pretrained=PRETRAINED)
    tokenizer = open_clip.get_tokenizer(MODEL_NAME)
    model = model.to(device).eval()

    image = load_image(sys.argv[1] if len(sys.argv) > 1 else None)
    print(f"Image size: {image.size}")

    img_tensor = preprocess(image).unsqueeze(0).to(device)
    txt_tokens = tokenizer(CANDIDATE_LABELS).to(device)

    with torch.no_grad():
        img_feats = model.encode_image(img_tensor)
        txt_feats = model.encode_text(txt_tokens)
        img_feats /= img_feats.norm(dim=-1, keepdim=True)
        txt_feats /= txt_feats.norm(dim=-1, keepdim=True)
        probs = (100.0 * img_feats @ txt_feats.T).softmax(dim=-1)[0]

    print("\nZero-shot predictions:")
    for prob, label in sorted(zip(probs.tolist(), CANDIDATE_LABELS),
                              reverse=True):
        print(f"  {prob * 100:6.2f}%  {label}")


if __name__ == "__main__":
    main()
