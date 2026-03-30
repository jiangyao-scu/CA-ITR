<div align="center">

<img src="https://img.icons8.com/fluency/96/camouflage.png" width="80">

<h1>
  <a href="#">CECNet</a>: Camouflage-aware Image-Text Retrieval
</h1>

<h3>via Expert Collaboration</h3>

**CVPR 2026 Submission**

<p align="center">
  <a href="#">
    <img src="https://img.shields.io/badge/Paper-CVPR%202026-red?style=for-the-badge&logo=arxiv" alt="Paper">
  </a>
  <a href="#-camoit-dataset">
    <img src="https://img.shields.io/badge/Dataset-CamoIT-green?style=for-the-badge&logo=huggingface" alt="Dataset">
  </a>
  <a href="#">
    <img src="https://img.shields.io/badge/License-MIT-blue?style=for-the-badge" alt="License">
  </a>
  <a href="https://github.com/jiangyao-scu/CA-ITR">
    <img src="https://img.shields.io/badge/Code-GitHub-black?style=for-the-badge&logo=github" alt="Code">
  </a>
</p>

<p align="center">
  <a href="#">
    <img src="https://img.shields.io/badge/Python-3.8+-blue?style=flat-square&logo=python&logoColor=white" alt="Python">
  </a>
  <a href="#">
    <img src="https://img.shields.io/badge/PyTorch-2.0+-orange?style=flat-square&logo=pytorch&logoColor=white" alt="PyTorch">
  </a>
  <a href="https://github.com/jiangyao-scu/CA-ITR/stargazers">
    <img src="https://img.shields.io/github/stars/jiangyao-scu/CA-ITR?style=flat-square&logo=apachespark&logoColor=white&color=yellow" alt="Stars">
  </a>
  <a href="https://github.com/jiangyao-scu/CA-ITR/network/members">
    <img src="https://img.shields.io/github/forks/jiangyao-scu/CA-ITR?style=flat-square&logo=gitfork&logoColor=white&color=teal" alt="Forks">
  </a>
  <a href="https://github.com/jiangyao-scu/CA-ITR/issues">
    <img src="https://img.shields.io/github/issues/jiangyao-scu/CA-ITR?style=flat-square&logo=githubissues&logoColor=white&color=purple" alt="Issues">
  </a>
</p>

**Yao Jiang**<sup>1</sup> · **Zhongkuan Mao**<sup>2</sup> · **Xuan Wu**<sup>1</sup> · **Keren Fu**<sup>1,2,✉</sup> · **Qijun Zhao**<sup>1,2</sup>

<sup>1</sup>College of Computer Science, Sichuan University &nbsp;&nbsp; <sup>2</sup>National Key Lab of Fundamental Science on Synthetic Vision

<img src="images/Figure3.png" width="92%" alt="CECNet Architecture">

</div>

---

## 📋 目录

- [🚀 亮点](#-highlights)
- [📖 摘要](#-abstract)
- [💡 动机](#-motivation)
- [🏗️ 方法](#%EF%B8%8F-method)
- [📊 CamoIT 数据集](#-camoit-dataset)
- [📈 实验结果](#-results)
- [🔧 快速开始](#-getting-started)
- [📁 项目结构](#-project-structure)
- [📝 引用](#-citation)
- [🙏 致谢](#-acknowledgements)

---

## 🚀 亮点

<table>
<tr>
<td width="50%" align="center">

### 🎯 首创工作

首个伪装场景图文检索研究

**First work** on image-text retrieval in camouflaged scenarios

</td>
<td width="50%" align="center">

### 📊 CamoIT 数据集

~10.5K 样本 · 237 类别

Multi-granularity annotations

</td>
</tr>
<tr>
<td width="50%" align="center">

### 🚀 显著提升

**~29%** 准确率提升

vs. fine-tuned CLIP baseline

</td>
<td width="50%" align="center">

### 🔧 通用设计

可集成到 AVSE、D2S-VSE 等

Universal plug-and-play design

</td>
</tr>
</table>

---

## 📖 摘要

> 伪装场景理解 (CSU) 因其广泛的实际应用价值而备受关注。然而，该领域中鲁棒的**图文跨模态对齐**仍待探索。
> 
> 我们提出了新任务 **CA-ITR** (伪装感知图文检索) 并构建 **CamoIT** 数据集 (~10.5K样本, 237类别)。通过设计具有 **C²GA** 机制的 **CECNet** 模型，实现了 **~29%** 的准确率提升。

---

## 💡 动机

<img src="images/Figure1.png" width="100%" alt="Motivation">

现有 SOTA 检索模型在伪装场景中频繁出现**文本描述与视觉对象不匹配**的问题。CA-ITR 面临三大独特挑战：

| | 挑战 | 描述 |
|:---:|:---:|:---|
| 🎭 | **目标感知** | 伪装目标与背景视觉相似，难以识别 |
| 🌿 | **内容复杂** | 图像包含复杂背景和多种元素 |
| 🔍 | **细粒度理解** | 需要对目标属性进行详细理解 |

---

## 🏗️ 方法

### 架构概览

<img src="images/Figure3.png" width="100%" alt="CECNet Architecture">

CECNet 采用**双分支视觉编码器**架构：

| 分支 | 模型 | 功能 |
|:---|:---|:---|
| 🌐 **全局上下文分支** | CLIP ViT-B/32 | 捕获整体场景上下文 |
| 🎯 **伪装专家分支** | ZoomNeXt (PVT-V2-B5) | 检测伪装目标 |

### C²GA: 置信度条件图注意力

C²GA 机制注入到**全部 12 个 Transformer 层**：

1. 利用 COD 掩码计算每个 patch 的伪装置信度
2. 构建独立的前景图 (𝒢_F) 和背景图 (𝒢_B)
3. 独立聚合特征以防止污染
4. 自适应数据融合 (ADF) 实现稳定特征整合

---

## 📊 CamoIT 数据集

<img src="images/Figure2.png" width="100%" alt="CamoIT Dataset">

### 数据集统计

| 统计项 | 数值 |
|:---:|:---:|
| 总样本数 | 10,464 |
| 类别数 | 237 |
| 训练集 / 测试集 | ~7,464 / 3,000 |
| 平均描述长度 | ~25 词 |

**数据来源**: CHAMELEON · CAMO · COD10K · NC4K

### 多粒度标注

| 层级 | 类型 | 示例 |
|:---:|:---|:---|
| Level 1 | 类别 | *"A photo of crab."* |
| Level 2 | 目标 | *"The crab has a shiny, brown shell."* |
| Level 3 | 描述 | *"A crab with a mottled brown body is perched among smooth pebbles..."* |

---

## 📈 实验结果

### 主要结果 (CamoIT 测试集)

| 方法 | I2T R@1 | I2T R@5 | I2T R@10 | T2I R@1 | T2I R@5 | T2I R@10 |
|:---|:---:|:---:|:---:|:---:|:---:|:---:|
| CFM | 30.8 | 59.9 | 70.3 | 28.9 | 57.2 | 68.3 |
| HREM | 34.3 | 62.7 | 74.0 | 31.5 | 59.9 | 71.4 |
| CUSA | 23.9 | 53.5 | 66.7 | 23.5 | 51.3 | 64.3 |
| LAPS | 27.8 | 62.0 | 73.9 | 28.2 | 58.0 | 70.7 |
| D2S-VSE | 37.1 | 68.4 | 79.5 | 35.5 | 67.5 | 78.4 |
| AVSE | 28.1 | 59.7 | 72.2 | 26.1 | 56.3 | 69.7 |
| CLIP (fine-tuned) | 41.3 | 69.2 | 79.0 | 41.1 | 67.7 | 78.4 |
| **CECNet (Ours)** | **45.8** ✨ | **74.5** | **83.5** | **44.6** ✨ | **73.9** | **83.1** |
| *提升* | *+4.5 ↑* | *+5.3 ↑* | *+4.5 ↑* | *+3.5 ↑* | *+6.2 ↑* | *+4.7 ↑* |

### 定性结果

<img src="images/Figure4.png" width="100%" alt="Qualitative Results">

### 消融实验

| 设置 | I2T R@1 | T2I R@1 |
|:---|:---:|:---:|
| Baseline (CLIP) | 41.3 | 41.1 |
| + Mask modulation | 28.5 ↓ | 30.0 ↓ |
| + Conv fusion | 42.1 | 41.2 |
| + Trainable prompt | 41.8 | 42.2 |
| + Simple addition | 42.5 | 42.9 |
| + Linear fusion | 42.4 | 41.7 |
| + Vanilla GAT | 42.9 | 42.3 |
| **+ C²GA (Ours)** | **45.8** ✨ | **44.6** ✨ |

### COD 模型影响

| COD 模型 | I2T R@1 | T2I R@1 | S_α ↑ | MAE ↓ |
|:---|:---:|:---:|:---:|:---:|
| White (no detection) | 41.6 | 41.3 | 0.443 | 0.120 |
| SINet | 42.3 | 42.1 | 0.808 | 0.049 |
| SINet-v2 | 43.3 | 43.1 | 0.843 | 0.037 |
| ZoomNet | 44.0 | 42.9 | 0.851 | 0.033 |
| **ZoomNeXt** | **45.8** ✨ | **44.6** ✨ | **0.906** | **0.021** |

---

## 🔧 快速开始

### 环境安装

```bash
git clone https://github.com/jiangyao-scu/CA-ITR.git
cd CA-ITR

conda create -n cecnet python=3.8
conda activate cecnet

pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
pip install timm open-clip-torch opencv-python tqdm pandas
```

### 数据集准备

```
data/
├── images/              # 原始图像
├── mask_zoomnext/       # 预计算的 COD 掩码
├── train.json
└── test.json
```

### 两阶段训练

**Stage 1**: 训练 C²GA (冻结 CLIP)

```bash
python train.py --output_dir './models/CCGA/' --frozen_clip --ccga_lr 1e-4
```

**Stage 2**: 联合微调

```bash
python train.py --output_dir './models/CECNet/' --ccga_lr 1e-5 --clip_lr 1e-6 \
    --resume_path './models/CCGA/CCGAs.pth'
```

### 评估

```bash
# 使用预计算掩码 (更快)
python test.py --model_path './models/CECNet/best_model.pth'

# 在线 COD 推理
python test.py --model_path './models/CECNet/best_model.pth' --Expert
```

---

## 📁 项目结构

```
CA-ITR/
├── CECNet.py              # 主模型
├── train.py               # 训练脚本
├── test.py                # 评估脚本
├── dataset.py             # 数据集类
├── evaluation.py          # 评估指标
├── methods/
│   ├── zoomnext/          # COD 专家模型
│   └── backbone/          # PVT-V2, EfficientNet
├── open_clip/             # 修改版 OpenCLIP
└── images/                # README 资源
```

---

## 💻 硬件需求

| 组件 | 最低要求 | 推荐配置 |
|:---|:---|:---|
| GPU | 16GB 显存 | 24GB (RTX 3090/4090) |
| RAM | 32GB | 64GB |

RTX 4090 训练时间: **Stage 1 ~2h** · **Stage 2 ~1h**

---

## 📝 引用

如果您发现本项目有帮助，请引用：

```bibtex
@inproceedings{jiang2026cecnet,
  title={Camouflage-aware Image-Text Retrieval via Expert Collaboration},
  author={Jiang, Yao and Mao, Zhongkuan and Wu, Xuan and Fu, Keren and Zhao, Qijun},
  booktitle={CVPR},
  year={2026}
}
```

---

## 🙏 致谢

本研究由 **国家自然科学基金** (No. 62176169) 和 **四川省科技计划** (2025ZNSFSC0469) 支持。

本项目基于以下开源工作构建：

[![CLIP](https://img.shields.io/badge/CLIP-OpenAI-lightgrey?style=flat-square)](https://github.com/openai/CLIP)
[![OpenCLIP](https://img.shields.io/badge/OpenCLIP-MLFoundations-lightgrey?style=flat-square)](https://github.com/mlfoundations/open_clip)
[![ZoomNeXt](https://img.shields.io/badge/ZoomNeXt-COD-lightgrey?style=flat-square)](https://github.com/lartpang/ZoomNeXt)
[![PVT-V2](https://img.shields.io/badge/PVT--V2-Backbone-lightgrey?style=flat-square)](https://github.com/whai362/PVT)

---

<div align="center">

### 🌟 如果这个项目对您有帮助，请给一个 Star！

[![Star History Chart](https://api.star-history.com/svg?repos=jiangyao-scu/CA-ITR&type=Date)](https://star-history.com/#jiangyao-scu/CA-ITR&Date)

**联系我们**: [fkrsuper@scu.edu.cn](mailto:fkrsuper@scu.edu.cn)

</div>
