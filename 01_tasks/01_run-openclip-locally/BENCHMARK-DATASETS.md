# Image Classification Dataset Options

Beyond CIFAR-10 (32×32, 10 classes, 60k images). Sorted by resolution/size.

## Classic datasets (usable with torchvision / clip_benchmark)

| Dataset                  | Resolution                        | Classes       | Size           | Notes                                                                              |
|--------------------------|-----------------------------------|---------------|----------------|------------------------------------------------------------------------------------|
| MNIST / Fashion-MNIST    | 28×28                             | 10            | ~11 MB         | Grayscale, easier than CIFAR                                                       |
| SVHN                     | 32×32                             | 10            | ~180 MB        | Street-view digits, same size as CIFAR-10                                          |
| **STL-10**               | **96×96**                         | 10            | ~130 MB        | Same classes as CIFAR-10, ~5× pixels — the natural “CIFAR but sharper” step up     |
| Tiny ImageNet            | 64×64                             | 200           | ~250 MB        | Downscaled ImageNet                                                                |
| Caltech-101 / 256        | ~300–500 px                       | 101 / 256     | ~130 MB        | Object categories                                                                  |
| Food-101                 | ~300 px                           | 101           | ~230 MB        | CLIP zero-shot ~90%+ — dramatic demo                                               |
| Flowers-102 (Oxford)     | ~500 px                           | 102           | ~345 MB        | Fine-grained; clip_benchmark name is `flowers`; measured ViT-B/32 zero-shot 71.6%  |
| Oxford-IIIT Pets         | ~512 px                           | 37            | ~750 MB        | Fine-grained cats/dogs                                                             |
| CUB-200 (birds)          | ~500 px                           | 200           | ~1 GB          | Very hard, fine-grained                                                            |
| ImageNet-1k              | ~420–500 px (used at 224×224)     | 1000          | ~150 GB        | The classic; gated on HF, huge download                                            |
| OpenImages V7            | Variable                          | 600           | ~9 M images    | Google, multi-label                                                                |
| iNaturalist              | Variable                          | 5000+ species | ~2.7 M images   | Nature                                                                            |

## Modern / web-scale (how CLIP itself was trained)

- **LAION-400M / LAION-5B / LAION-COCO** — image–text pairs scraped from the web
- **DataComp** (2023) — billion-scale benchmark of curated image-text subsets
- **CC12M / CC3M** (Conceptual Captions), **RedCaps**, **ShareGPT4V** — caption datasets

## clip_benchmark: dataset collections

`clip_benchmark` supports many of the above out of the box:

```shell
# single dataset
clip_benchmark eval --dataset stl10 --dataset_root datasets \
  --model ViT-B-32 --pretrained laion2b_s34b_b79k \
  --task zeroshot_classification --output results_stl10.json

# whole VTAB collection (~20 small datasets incl. stl10, food-101, oxford_pets,
# oxford_flowers_102, caltech101, cifar100, mnist, svhn, ...)
clip_benchmark eval --dataset vtab --model ViT-B-32 \
  --pretrained laion2b_s34b_b79k --output vtab.json
```

Names to try with `--dataset`: `cifar10`, `cifar100`, `stl10`, `svhn`, `mnist`,
`food-101`, `caltech101`, `caltech256`, `oxford-pets`, `oxford_flowers_102`,
`imagenet1k`, `imagenet_v2`, `imagenet-a`, `imagenet-r`, `imagenet-sketch`,
`country211`, `dtd`, `kitti`, `emnist_*`, `voc2007`, `voc2008`, `lsun`,
`n24news`, `multilingual_`…, plus retrieval sets (`mscoco_t2i`, `mscoco_i2t`,
`flickr30k_*`, `vqa_*`, `sbd`) under the `retrieval` collection.

## Download sources & mirrors

⚠️ The official source `www.cs.toronto.edu` (CIFAR, STL-10) is extremely slow /
truncated downloads from this network (observed ~60 KB/s, connection drops).

| Source | URL | Speed here |
|---|---|---|
| HF mirror for CIFAR-10 (used, verified sha256 `6d958be0…`) | `https://huggingface.co/datasets/liangnanying/cifar-10-python/resolve/main/cifar-10-python.tar.gz` | ~1.7 MB/s ✅ |
| HF Datasets hub | `https://huggingface.co/datasets/<org>/<name>` (e.g. `Maifeld/cifar10`, `tritonlib/stl10`, `frgarcia/food101`) | fast ✅ |
| HF mirror (CN) | `https://hf-mirror.com/…` (set `HF_ENDPOINT=https://hf-mirror.com`) | good in CN |
| ModelScope (CN) | `pip install modelscope` → `modelscope download --dataset …` | good in CN |
| OpenDataLab (CN) | `https://opendatalab.com` | good in CN |
| TensorFlow Datasets | `pip install tensorflow_datasets` → `tfds.load("cifar10")` (GCS-backed) | untested |
| Kaggle | many CIFAR/ImageNet copies, needs `kaggle` API token | untested |

## Local files in this folder

- `datasets/cifar-10-batches-py/` — extracted CIFAR-10 (pickle files, planar RGB)
- `datasets/cifar-10-python.tar.gz` — official archive (from HF mirror, checksum-verified)
- `datasets/stl10_binary/` — extracted STL-10 (raw .bin files, one per split)
- `datasets/flowers-102/` — Flowers-102 (102flowers.tgz + jpg/, labels in .mat files)
- `cifar10_pics/*.png`, `stl10_pics/*.png` — one upscaled example image per class
- `cifar10_examples.png`, `stl10_examples.png` — labeled 10-class grids
- `results_cpu.json` / `results_mps.json` — CIFAR-10 zero-shot (acc1 ≈ 0.935)
- `results_stl10.json` — STL-10 zero-shot (acc1 0.966)
- `results_flowers.json` — Flowers-102 zero-shot (acc1 0.716, acc5 0.876)
