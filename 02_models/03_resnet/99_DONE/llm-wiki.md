# ResNet

`03_models/01_resnet` 是一条从「调用现成 ResNet」到「自己写 ResNet18 并在 CIFAR-10 上训练」的学习路径。四次尝试都在 `99_DONE` 里。

## 这条线在学什么

ResNet 用残差连接解决深层网络的梯度消失：块的输出是 `F(x) + shortcut(x)`，而不是只堆卷积。形状不变时 shortcut 是恒等映射；步长或通道数变了，就用 1×1 卷积把输入对齐后再相加。

案例最后落到 CIFAR-10（32×32、10 类），所以结构按小图改过，不是 ImageNet 那套 224×224 的 ResNet。

## 四次尝试

| 尝试 | 目录 | 目标 | 做法 |
|---|---|---|---|
| 第 1 次 | [20260111-1_resnet_1st-attempt](99_DONE/20260111-1_resnet_1st-attempt) | 会加载预训练 ResNet50 | torchvision 官方权重、Hugging Face `microsoft/resnet-50`、本地 `transformers` 加载；用 Albumentations 把图变成 `[1, 3, 224, 224]`；再用 timm 的 `resnet50`（`num_classes=0`）做特征提取 |
| 第 2 次 | [20261005-1_resnet_2nd-attempt](99_DONE/20261005-1_resnet_2nd-attempt) | 会做 ImageNet 推理 | torchvision `resnet18` 官方权重；Resize 256 → CenterCrop 224 → ImageNet 均值/方差；MPS/CUDA/CPU；对一张狗图输出 Top-5 |
| 第 3 次 | [20261005-4_resnet_3rd-attempt](99_DONE/20261005-4_resnet_3rd-attempt) | 会改官方模型并训练 | 仍用 torchvision `resnet18`，随机初始化，改成适合 CIFAR-10；训练 10 个 epoch，权重存 `.pth`，上传到 [yogiman/resnet_3rd-attempt](https://huggingface.co/yogiman/resnet_3rd-attempt) |
| 第 4 次 | [20261007-6_resnet_4th-attempt](99_DONE/20261007-6_resnet_4th-attempt) | 从零实现并可视化 | `resnet.py` 里自己写 `BasicBlock` 和 `ResNet18`；同样训 CIFAR-10，权重存 safetensors，上传到 `yogiman/resnet` 的 `4th-attempt/`；用 torchviz 画出 BasicBlock 计算图 |

第 1、2 次是推理。第 3、4 次才是训练，数据集和优化器几乎一样，差别在模型从哪里来。

## 第 4 次的网络

CIFAR 版 ResNet18，入口不是 ImageNet 的 7×7、stride 2，也没有开头的 max pooling：

1. Stem：`3×3` 卷积，3→64，stride 1，再 BatchNorm + ReLU。空间尺寸仍是 32×32。
2. 四个 stage，每段 2 个 BasicBlock，通道 64 → 128 → 256 → 512。`layer2`、`layer3`、`layer4` 的第一个块 stride 为 2，把特征图减半。
3. `AdaptiveAvgPool2d(1)` 把特征收成 512 维，再 `Linear(512, 10)`。

每个 BasicBlock 是两层 `3×3` 卷积（无 bias）加 BatchNorm。第一层后 ReLU，两层卷积结果加上 shortcut，最后再 ReLU。通道或步长不匹配时，shortcut 换成 `1×1` 卷积 + BatchNorm。

第 3 次是改 torchvision：把 `conv1` 换成同样的 `3×3` stride 1，把 `maxpool` 换成 `Identity`，把全连接从 1000 类改成 10 类。效果和自己写的 CIFAR ResNet18 同一思路，只是残差块仍来自官方实现。

## 训练设置

两边都用 CIFAR-10 的均值 `(0.4914, 0.4822, 0.4465)` 和标准差 `(0.2023, 0.1994, 0.2010)`，增强是随机水平翻转和 `RandomCrop(32, padding=4)`，损失是交叉熵，优化器是 SGD（学习率 0.1、momentum 0.9、weight decay `5e-4`），都只训了 10 个 epoch。

差别主要是：

- 第 3 次 batch size 512，学习率用 `CosineAnnealingLR`（`T_max=200`），权重存 `.pth`。
- 第 4 次训练 batch 128、测试 batch 100，学习率用 `StepLR`（每 30 epoch 乘 0.1），权重存 safetensors。

Notebook 里没有留下最终准确率。
