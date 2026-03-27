<p align="center">
  <h1 align="center">CECNet</h1>
  <h3 align="center">Camouflage-aware Image-Text Retrieval via Expert Collaboration</h3>
  <p align="center">
    <a href=""><strong>Yao Jiang</strong></a><sup>1</sup> &nbsp;
    <a href=""><strong>Zhongkuan Mao</strong></a><sup>2</sup> &nbsp;
    <a href=""><strong>Xuan Wu</strong></a><sup>1</sup> &nbsp;
    <br>
    <a href=""><strong>Keren Fu</strong></a><sup>1,2,*</sup> &nbsp;
    <a href=""><strong>Qijun Zhao</strong></a><sup>1,2</sup> &nbsp;
  </p>
  <p align="center">
    <sup>1</sup>College of Computer Science, Sichuan University &nbsp;
    <sup>2</sup>National Key Lab of Fundamental Science on Synthetic Vision
  </p>
  <p align="center">
    <em>CVPR 2026 Submission</em>
  </p>
  
  <p align="center">
    <a href="https://arxiv.org"><img src="https://img.shields.io/badge/Paper-CVPR%202026-red?style=flat-square" alt="Paper"></a>
    <a href="#dataset-preparation"><img src="https://img.shields.io/badge/Dataset-CamoIT-green?style=flat-square" alt="Dataset"></a>
    <a href="#citation"><img src="https://img.shields.io/badge/License-MIT-blue?style=flat-square" alt="License"></a>
    <a href="https://github.com/jiangyao-scu/CA-ITR"><img src="https://img.shields.io/badge/GitHub-Code-black?style=flat-square&logo=github" alt="GitHub"></a>
  </p>
</p>

<br>

<table align="center">
  <tr>
    <td align="center"><strong>Figure 1: Motivation</strong></td>
    <td align="center"><strong>Figure 3: Architecture</strong></td>
  </tr>
  <tr>
    <td><img src="images/fig1_motivation.png" width="100%" alt="Motivation"></td>
    <td><img src="images/fig3_architecture.png" width="100%" alt="Architecture"></td>
  </tr>
</table>

---

## Overview

<table>
<tr>
<td width="50%">

### Problem
Current SOTA retrieval models frequently **mismatch** textual descriptions with incorrect visual objects in camouflaged scenes.

</td>
<td width="50%">

### Solution
We propose **CECNet** with dual-branch encoder and **C²GA** mechanism for robust cross-modal alignment.

</td>
</tr>
</table>

<br>

> **TL;DR**: This is the first work to study image-text retrieval in camouflaged scenarios. We construct **CamoIT** dataset (~10.5K samples, 237 categories) and propose **CECNet** achieving **~29%** accuracy boost.

---

## Abstract

Camouflaged scene understanding (CSU) has attracted significant attention due to its broad practical implications. However, in this field, robust **image-text cross-modal alignment** remains under-explored, hindering deeper understanding of camouflaged scenarios.

We formulate a new task dubbed **"camouflage-aware image-text retrieval" (CA-ITR)** and construct a dedicated camouflage image-text retrieval dataset (**CamoIT**), comprising ~10.5K samples with multi-granularity textual annotations. Benchmark results reveal the underlying challenges of CA-ITR for existing cutting-edge retrieval techniques.

We propose a **camouflage-expert collaborative network (CECNet)**, featuring a dual-branch visual encoder with a novel **confidence-conditioned graph attention (C²GA)** mechanism. Experimental results show that CECNet achieves a **~29% CA-ITR accuracy boost**, surpassing seven representative retrieval models.

---

## News

| Date | News |
|:----:|------|
| 2026 | Paper submitted to CVPR 2026 |
| 2026 | CamoIT dataset and code will be released upon acceptance |

---

## Challenges of CA-ITR

<table align="center">
<tr>
<td align="center" width="33%">
<img src="https://img.shields.io/badge/Challenge_1-Object_Perception-orange?style=for-the-badge" alt="Challenge 1"/><br><br>
<b>Camouflaged objects</b> are visually similar to backgrounds, making them hard to perceive
</td>
<td align="center" width="33%">
<img src="https://img.shields.io/badge/Challenge_2-Complex_Content-yellow?style=for-the-badge" alt="Challenge 2"/><br><br>
Images contain <b>intricate backgrounds</b> and multiple elements
</td>
<td align="center" width="33%">
<img src="https://img.shields.io/badge/Challenge_3-Fine_Grained-blue?style=for-the-badge" alt="Challenge 3"/><br><br>
Requires <b>detailed comprehension</b> of object attributes and context
</td>
</tr>
</table>

---

## Method: CECNet

### Architecture

<table align="center">
<tr>
<td>
<img src="images/fig3_architecture.png" width="100%" alt="CECNet Architecture">
</td>
</tr>
<tr>
<td align="center"><em>Figure 3: The overall pipeline of CECNet and C²GA mechanism</em></td>
</tr>
</table>

### Dual-Branch Visual Encoder

| Branch | Model | Purpose |
|--------|-------|---------|
| **Global Context Branch** | CLIP ViT-B/32 | Preserve holistic scene context |
| **Camouflage Expert Branch** | ZoomNeXt (PVT-V2-B5) | Detect and encode camouflaged objects |

### C²GA: Confidence-Conditioned Graph Attention

<table>
<tr>
<td width="60%">

The C²GA mechanism operates in each transformer layer:

1. **Confidence Scores**: Leverage COD masks to compute camouflage confidence per patch
2. **Graph Construction**: 
   - Foreground graph 𝒢_F: Focuses on camouflaged object
   - Background graph 𝒢_B: Captures environmental context
3. **Feature Aggregation**: Separate aggregation prevents feature contamination
4. **Adaptive Fusion**: ADF gate integrates enhanced features stably

</td>
<td width="40%" align="center">

<img src="https://img.shields.io/badge/Feature-12_Layers-purple?style=for-the-badge" alt="12 Layers"/><br><br>
C²GA modules are injected into <b>all 12 transformer layers</b> of CLIP's visual encoder

</td>
</tr>
</table>

### Key Equations

Foreground graph edge weight:
```
W_F(i,j) = M_vᵢ · M_vⱼ · (vᵢ · vⱼᵀ) / (||vᵢ|| ||vⱼ||)
```

Adaptive fusion:
```
F₀ = Σ σ(f([A₀, E₀, G₀])) · [A₀, E₀, G₀]
```

---

## CamoIT Dataset

<table>
<tr>
<td width="60%">

### Statistics

| Metric | Value |
|--------|------:|
| Total Samples | 10,464 |
| Categories | 237 |
| Training Set | ~7,464 |
| Test Set | 3,000 |
| Avg. Caption Length | ~25 words |

### Data Sources

Built upon four COD benchmark datasets:
- **CHAMELEON**
- **CAMO**
- **COD10K**
- **NC4K**

</td>
<td width="40%">

<img src="images/fig2_dataset.png" width="100%" alt="CamoIT Dataset">

<p align="center"><em>Figure 2: Dataset annotation and statistics</em></p>

</td>
</tr>
</table>

### Multi-Granularity Annotations

<table>
<tr>
<th width="15%">Level</th>
<th width="20%">Type</th>
<th width="65%">Example</th>
</tr>
<tr>
<td align="center"><code>Level 1</code></td>
<td>Category Label</td>
<td><em>"A photo of crab."</em></td>
</tr>
<tr>
<td align="center"><code>Level 2</code></td>
<td>Object Description</td>
<td><em>"The crab has a shiny, brown shell."</em></td>
</tr>
<tr>
<td align="center"><code>Level 3</code></td>
<td>Image Caption</td>
<td><em>"A crab with a mottled brown body is perched among a mix of smooth pebbles, coarse sand, and patches of green algae."</em></td>
</tr>
</table>

---

## Results

### Quantitative Results on CamoIT

<table align="center">
<thead>
<tr>
<th rowspan="2">Method</th>
<th colspan="3">Image-to-Text</th>
<th colspan="3">Text-to-Image</th>
</tr>
<tr>
<th>R@1</th><th>R@5</th><th>R@10</th>
<th>R@1</th><th>R@5</th><th>R@10</th>
</tr>
</thead>
<tbody>
<tr>
<td>CFM</td>
<td>30.8</td><td>59.9</td><td>70.3</td>
<td>28.9</td><td>57.2</td><td>68.3</td>
</tr>
<tr>
<td>HREM</td>
<td>34.3</td><td>62.7</td><td>74.0</td>
<td>31.5</td><td>59.9</td><td>71.4</td>
</tr>
<tr>
<td>CUSA</td>
<td>23.9</td><td>53.5</td><td>66.7</td>
<td>23.5</td><td>51.3</td><td>64.3</td>
</tr>
<tr>
<td>LAPS</td>
<td>27.8</td><td>62.0</td><td>73.9</td>
<td>28.2</td><td>58.0</td><td>70.7</td>
</tr>
<tr>
<td>D2S-VSE</td>
<td>37.1</td><td>68.4</td><td>79.5</td>
<td>35.5</td><td>67.5</td><td>78.4</td>
</tr>
<tr>
<td>AVSE</td>
<td>28.1</td><td>59.7</td><td>72.2</td>
<td>26.1</td><td>56.3</td><td>69.7</td>
</tr>
<tr>
<td>CLIP (fine-tuned)</td>
<td>41.3</td><td>69.2</td><td>79.0</td>
<td>41.1</td><td>67.7</td><td>78.4</td>
</tr>
<tr style="background-color: #e8f5e9; font-weight: bold;">
<td>CECNet (Ours)</td>
<td style="color: #2e7d32;">45.8</td><td style="color: #2e7d32;">74.5</td><td style="color: #2e7d32;">83.5</td>
<td style="color: #2e7d32;">44.6</td><td style="color: #2e7d32;">73.9</td><td style="color: #2e7d32;">83.1</td>
</tr>
</tbody>
</table>

### Performance Gains

<table align="center">
<tr>
<td align="center" width="33%">
<img src="https://img.shields.io/badge/29%25-rSum_Boost-success?style=for-the-badge&logo=trendingup" alt="29% Boost"/><br><br>
Over fine-tuned CLIP baseline
</td>
<td align="center" width="33%">
<img src="https://img.shields.io/badge/4.5%25-R@1_Gain-blue?style=for-the-badge" alt="4.5% Gain"/><br><br>
Over D2S-VSE (best competitor)
</td>
<td align="center" width="33%">
<img src="https://img.shields.io/badge/Universal-Applicable-purple?style=for-the-badge" alt="Universal"/><br><br>
Improves AVSE & D2S-VSE when integrated
</td>
</tr>
</table>

### Qualitative Results

<table align="center">
<tr>
<td align="center"><strong>Sentence Retrieval</strong></td>
<td align="center"><strong>Image Retrieval</strong></td>
</tr>
<tr>
<td><img src="images/fig4_sentence_retrieval.png" width="100%" alt="Sentence Retrieval"></td>
<td><img src="images/fig4_image_retrieval.png" width="100%" alt="Image Retrieval"></td>
</tr>
<tr>
<td colspan="2" align="center"><em>Figure 4: Qualitative comparison between CECNet and CLIP</em></td>
</tr>
</table>

### Ablation Study

| Setting | I2T R@1 | T2I R@1 | Analysis |
|---------|:-------:|:-------:|----------|
| Baseline (CLIP) | 41.3 | 41.1 | - |
| Mask modulation (A1) | 28.5 | 30.0 | Disrupts image fidelity |
| Conv fusion (A2) | 42.1 | 41.2 | Simple fusion insufficient |
| Trainable prompt (A3) | 41.8 | 42.2 | Limited improvement |
| Simple addition (B1) | 42.5 | 42.9 | Risk of contamination |
| Linear fusion (B2) | 42.4 | 41.7 | - |
| Vanilla GAT (B3) | 42.9 | 42.3 | - |
| **C²GA (Ours)** | **45.8** | **44.6** | Best performance |

### Impact of COD Models

| COD Model | I2T R@1 | T2I R@1 | S_α | MAE |
|-----------|:-------:|:-------:|:---:|:---:|
| White (baseline) | 41.6 | 41.3 | 0.443 | 0.120 |
| SINet | 42.3 | 42.1 | 0.808 | 0.049 |
| SINet-v2 | 43.3 | 43.1 | 0.843 | 0.037 |
| ZoomNet | 44.0 | 42.9 | 0.851 | 0.033 |
| **ZoomNeXt** | **45.8** | **44.6** | **0.906** | **0.021** |

---

## Getting Started

### Installation

```bash
# Clone the repository
git clone https://github.com/jiangyao-scu/CA-ITR.git
cd CA-ITR

# Create conda environment
conda create -n cecnet python=3.8
conda activate cecnet

# Install PyTorch (adjust for your CUDA version)
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118

# Install dependencies
pip install timm open-clip-torch opencv-python tqdm pandas
```

### Dataset Preparation

1. Download CamoIT dataset (will be released upon paper acceptance)

2. Organize the dataset:
```
data/
├── images/              # Original images
├── mask_zoomnext/       # Pre-computed COD masks
├── train.json           # Training annotations
└── test.json            # Test annotations
```

### Training

CECNet uses a **two-stage training strategy**:

<table>
<tr>
<th>Stage</th>
<th>Description</th>
<th>Command</th>
</tr>
<tr>
<td><b>Stage 1</b></td>
<td>Train C²GA (freeze CLIP)</td>
<td>

```bash
python train.py \
    --output_dir './models/CCGA/' \
    --frozen_clip \
    --ccga_lr 1e-4 \
    --batch_size 128
```

</td>
</tr>
<tr>
<td><b>Stage 2</b></td>
<td>Joint fine-tuning</td>
<td>

```bash
python train.py \
    --output_dir './models/CECNet/' \
    --ccga_lr 1e-5 \
    --clip_lr 1e-6 \
    --resume_path './models/CCGA/CCGAs.pth'
```

</td>
</tr>
</table>

### Evaluation

```bash
# Using pre-computed masks (faster)
python test.py --model_path './models/CECNet/best_model.pth'

# Using online COD inference
python test.py --model_path './models/CECNet/best_model.pth' --Expert
```

---

## Project Structure

```
CA-ITR/
├── CECNet.py              # Main model (CECNet, CCGA, GraphAttention)
├── train.py               # Two-stage training
├── test.py                # Evaluation script
├── dataset.py             # CODDataset class
├── evaluation.py          # R@K metrics
├── methods/
│   ├── zoomnext/          # ZoomNeXt COD expert
│   │   ├── zoomnext.py
│   │   ├── layers.py      # MHSIU, RGPU
│   │   └── ops.py
│   └── backbone/          # Backbone networks
│       ├── pvt_v2_eff.py  # PVT-V2 encoder
│       └── efficientnet.py
├── open_clip/             # Modified OpenCLIP with CCGA
│   ├── model.py
│   ├── transformer.py
│   └── ...
└── images/                # README assets
    ├── fig1_motivation.png
    ├── fig2_dataset.png
    ├── fig3_architecture.png
    ├── fig4_sentence_retrieval.png
    └── fig4_image_retrieval.png
```

---

## Hardware Requirements

| Component | Minimum | Recommended |
|-----------|---------|-------------|
| GPU | 16GB VRAM | 24GB (RTX 3090/4090) |
| CPU | 8 cores | 16 cores |
| RAM | 32GB | 64GB |

Training time on RTX 4090: Stage 1 ~2h | Stage 2 ~1h

---

## Citation

```bibtex
@inproceedings{jiang2026cecnet,
  title={Camouflage-aware Image-Text Retrieval via Expert Collaboration},
  author={Jiang, Yao and Mao, Zhongkuan and Wu, Xuan and Fu, Keren and Zhao, Qijun},
  booktitle={Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR)},
  year={2026}
}
```

---

## Acknowledgements

This work was supported by **NSFC** (No. 62176169) and **Sichuan Science and Technology Program** (2025ZNSFSC0469).

We build upon these excellent projects:

<table>
<tr>
<td align="center"><a href="https://github.com/openai/CLIP">CLIP</a></td>
<td align="center"><a href="https://github.com/mlfoundations/open_clip">OpenCLIP</a></td>
<td align="center"><a href="https://github.com/lartpang/ZoomNeXt">ZoomNeXt</a></td>
<td align="center"><a href="https://github.com/whai362/PVT">PVT-V2</a></td>
</tr>
</table>

---

## Contact

- **Issues**: Open an issue on GitHub
- **Email**: [fkrsuper@scu.edu.cn](mailto:fkrsuper@scu.edu.cn)

<br>

<p align="center">
  <a href="https://github.com/jiangyao-scu/CA-ITR">
    <img src="https://img.shields.io/github/stars/jiangyao-scu/CA-ITR?style=social" alt="GitHub stars">
  </a>
</p>

<p align="center">
  <em>Made with care for the Computer Vision Community</em>
</p>
