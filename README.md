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

<img src="images/Figure1.png" width="100%" alt="Motivation">

</div>

---

## 📋 Table of Contents

- [🚀 Highlights](#-highlights)
- [📖 Abstract](#-abstract)
- [💡 Motivation](#-motivation)
- [🏗️ Method](#%EF%B8%8F-method)
- [📊 CamoIT Dataset](#-camoit-dataset)
- [📈 Results](#-results)
- [🔧 Getting Started](#-getting-started)
- [📁 Project Structure](#-project-structure)
- [📝 Citation](#-citation)
- [🙏 Acknowledgements](#-acknowledgements)

---

## 🚀 Highlights

<table>
<tr>
<td width="50%" align="center">

### 🎯 First Work

First work on image-text retrieval in camouflaged scenarios

</td>
<td width="50%" align="center">

### 📊 CamoIT Dataset

~10.5K samples · 237 categories

Multi-granularity annotations

</td>
</tr>
<tr>
<td width="50%" align="center">

### 🚀 Significant Boost

**~29%** accuracy improvement

vs. fine-tuned CLIP baseline

</td>
<td width="50%" align="center">

### 🔧 Universal Design

Plug-and-play for AVSE, D2S-VSE, etc.

</td>
</tr>
</table>

---

## 📖 Abstract

> Camouflaged scene understanding (CSU) has attracted significant attention due to its broad practical implications. However, in this field, robust **image-text cross-modal alignment** remains under-explored.
> 
> We formulate a new task dubbed **CA-ITR** (Camouflage-aware Image-Text Retrieval) and construct **CamoIT** dataset (~10.5K samples, 237 categories). We propose **CECNet** with a novel **C²GA** mechanism, achieving **~29%** accuracy boost.

---

## 💡 Motivation

Current SOTA retrieval models frequently **mismatch** textual descriptions with incorrect visual objects in camouflaged scenes. CA-ITR presents three unique challenges:

| | Challenge | Description |
|:---:|:---:|:---|
| 🎭 | **Object Perception** | Camouflaged objects are visually similar to backgrounds |
| 🌿 | **Complex Content** | Images contain intricate backgrounds and multiple elements |
| 🔍 | **Fine-grained Understanding** | Requires detailed comprehension of object attributes |

---

## 🏗️ Method

### Architecture Overview

<img src="images/Figure3.png" width="100%" alt="CECNet Architecture">

CECNet features a **dual-branch visual encoder**:

| Branch | Model | Function |
|:---|:---|:---|
| 🌐 **Global Context Branch** | CLIP ViT-B/32 | Capture holistic scene context |
| 🎯 **Camouflage Expert Branch** | ZoomNeXt (PVT-V2-B5) | Detect camouflaged objects |

### C²GA: Confidence-Conditioned Graph Attention

The C²GA mechanism is injected into **all 12 transformer layers**:

1. Leverage COD masks to compute camouflage confidence per patch
2. Construct separate foreground (𝒢_F) and background (𝒢_B) graphs
3. Aggregate features independently to prevent contamination
4. Adaptive Data Fusion (ADF) for stable feature integration

---

## 📊 CamoIT Dataset

<img src="images/Figure2.png" width="100%" alt="CamoIT Dataset">

### Dataset Statistics

| Statistics | Value |
|:---:|:---:|
| Total Samples | 10,464 |
| Categories | 237 |
| Training / Test | ~7,464 / 3,000 |
| Avg. Caption Length | ~25 words |

**Data Sources**: CHAMELEON · CAMO · COD10K · NC4K

### Multi-Granularity Annotations

| Level | Type | Example |
|:---:|:---|:---|
| Level 1 | Category | *"A photo of crab."* |
| Level 2 | Object | *"The crab has a shiny, brown shell."* |
| Level 3 | Caption | *"A crab with a mottled brown body is perched among smooth pebbles..."* |

---

## 📈 Results

### Main Results on CamoIT

| Method | I2T R@1 | I2T R@5 | I2T R@10 | T2I R@1 | T2I R@5 | T2I R@10 |
|:---|:---:|:---:|:---:|:---:|:---:|:---:|
| CFM | 30.8 | 59.9 | 70.3 | 28.9 | 57.2 | 68.3 |
| HREM | 34.3 | 62.7 | 74.0 | 31.5 | 59.9 | 71.4 |
| CUSA | 23.9 | 53.5 | 66.7 | 23.5 | 51.3 | 64.3 |
| LAPS | 27.8 | 62.0 | 73.9 | 28.2 | 58.0 | 70.7 |
| D2S-VSE | 37.1 | 68.4 | 79.5 | 35.5 | 67.5 | 78.4 |
| AVSE | 28.1 | 59.7 | 72.2 | 26.1 | 56.3 | 69.7 |
| CLIP (fine-tuned) | 41.3 | 69.2 | 79.0 | 41.1 | 67.7 | 78.4 |
| **CECNet (Ours)** | **45.8** ✨ | **74.5** | **83.5** | **44.6** ✨ | **73.9** | **83.1** |
| *Improvement* | *+4.5 ↑* | *+5.3 ↑* | *+4.5 ↑* | *+3.5 ↑* | *+6.2 ↑* | *+4.7 ↑* |

### Qualitative Results

<img src="images/Figure4.png" width="100%" alt="Qualitative Results">

### Impact of COD Models

| COD Model | I2T R@1 | T2I R@1 | S_α ↑ | MAE ↓ |
|:---|:---:|:---:|:---:|:---:|
| White (no detection) | 41.6 | 41.3 | 0.443 | 0.120 |
| SINet | 42.3 | 42.1 | 0.808 | 0.049 |
| SINet-v2 | 43.3 | 43.1 | 0.843 | 0.037 |
| ZoomNet | 44.0 | 42.9 | 0.851 | 0.033 |
| **ZoomNeXt** | **45.8** ✨ | **44.6** ✨ | **0.906** | **0.021** |

---

## 🔧 Getting Started

### Installation

```bash
git clone https://github.com/jiangyao-scu/CA-ITR.git
cd CA-ITR

conda create -n cecnet python=3.8
conda activate cecnet

pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
pip install timm open-clip-torch opencv-python tqdm pandas
```

### Dataset Preparation

```
data/
├── images/              # Original images
├── mask_zoomnext/       # Pre-computed COD masks
├── train.json
└── test.json
```

### Training (Two-Stage)

**Stage 1**: Train C²GA (freeze CLIP)

```bash
python train.py --output_dir './models/CCGA/' --frozen_clip --ccga_lr 1e-4
```

**Stage 2**: Joint fine-tuning

```bash
python train.py --output_dir './models/CECNet/' --ccga_lr 1e-5 --clip_lr 1e-6 \
    --resume_path './models/CCGA/CCGAs.pth'
```

### Evaluation

```bash
# Using pre-computed masks (faster)
python test.py --model_path './models/CECNet/best_model.pth'

# Using online COD inference
python test.py --model_path './models/CECNet/best_model.pth' --Expert
```

---

## 📁 Project Structure

```
CA-ITR/
├── CECNet.py              # Main model
├── train.py               # Training script
├── test.py                # Evaluation script
├── dataset.py             # Dataset class
├── evaluation.py          # Metrics
├── methods/
│   ├── zoomnext/          # COD expert model
│   └── backbone/          # PVT-V2, EfficientNet
├── open_clip/             # Modified OpenCLIP
└── images/                # README assets
```

---

## 💻 Hardware Requirements

| Component | Minimum | Recommended |
|:---|:---|:---|
| GPU | 16GB VRAM | 24GB (RTX 3090/4090) |
| RAM | 32GB | 64GB |

Training time on RTX 4090: **Stage 1 ~2h** · **Stage 2 ~1h**

---

## 📝 Citation

If you find this work helpful, please cite:

```bibtex
@inproceedings{jiang2026cecnet,
  title={Camouflage-aware Image-Text Retrieval via Expert Collaboration},
  author={Jiang, Yao and Mao, Zhongkuan and Wu, Xuan and Fu, Keren and Zhao, Qijun},
  booktitle={CVPR},
  year={2026}
}
```

---

## 🙏 Acknowledgements

This work is supported by **NSFC** (No. 62176169) and **Sichuan Science and Technology Program** (2025ZNSFSC0469).

Built upon:

[![CLIP](https://img.shields.io/badge/CLIP-OpenAI-lightgrey?style=flat-square)](https://github.com/openai/CLIP)
[![OpenCLIP](https://img.shields.io/badge/OpenCLIP-MLFoundations-lightgrey?style=flat-square)](https://github.com/mlfoundations/open_clip)
[![ZoomNeXt](https://img.shields.io/badge/ZoomNeXt-COD-lightgrey?style=flat-square)](https://github.com/lartpang/ZoomNeXt)
[![PVT-V2](https://img.shields.io/badge/PVT--V2-Backbone-lightgrey?style=flat-square)](https://github.com/whai362/PVT)

---

<div align="center">

### 🌟 If you find this project helpful, please give it a star!

[![Star History Chart](https://api.star-history.com/svg?repos=jiangyao-scu/CA-ITR&type=Date)](https://star-history.com/#jiangyao-scu/CA-ITR&Date)

**Contact**: [fkrsuper@scu.edu.cn](mailto:fkrsuper@scu.edu.cn)

</div>