<div align="center">

# CECNet: Camouflage-aware Image-Text Retrieval via Expert Collaboration

[![Paper](https://img.shields.io/badge/Paper-CVPR%202026-red?style=for-the-badge)]()
[![Dataset](https://img.shields.io/badge/Dataset-CamoIT-green?style=for-the-badge)]()
[![License](https://img.shields.io/badge/License-MIT-blue?style=for-the-badge)]()

**CVPR 2026 Submission**

[Paper](#) · [Dataset](#) · [BibTeX](#citation)

---

<img src="images/fig3_architecture.png" width="100%" alt="CECNet Architecture">

</div>

## 📋 Abstract

Camouflaged scene understanding (CSU) has attracted significant attention due to its broad practical implications. However, in this field, robust **image-text cross-modal alignment** remains under-explored, hindering deeper understanding of camouflaged scenarios.

We formulate a new task dubbed **"camouflage-aware image-text retrieval" (CA-ITR)** and construct a dedicated camouflage image-text retrieval dataset (**CamoIT**), comprising ~10.5K samples with multi-granularity textual annotations. Benchmark results reveal the underlying challenges of CA-ITR for existing cutting-edge retrieval techniques.

We propose a **camouflage-expert collaborative network (CECNet)**, featuring a dual-branch visual encoder with a novel **confidence-conditioned graph attention (C²GA)** mechanism. Experimental results show that CECNet achieves a **~29% CA-ITR accuracy boost**, surpassing seven representative retrieval models.

---

## 🔥 News

- **[2026]** Paper submitted to CVPR 2026.
- **[2026]** CamoIT dataset and code will be released upon acceptance.

---

## 🎯 Motivation

Current state-of-the-art retrieval models frequently mismatch textual descriptions with incorrect visual objects in camouflaged scenes. CA-ITR presents unique challenges:

| Challenge | Description |
|-----------|-------------|
| **Object Perception** | Camouflaged objects are visually similar to backgrounds |
| **Complex Content** | Images contain intricate backgrounds and multiple elements |
| **Fine-grained Understanding** | Requires detailed comprehension of object attributes and context |

<div align="center">
<img src="images/fig1_motivation.png" width="90%" alt="Motivation">
</div>

---

## 🏗️ Method

### Architecture Overview

CECNet introduces a **dual-branch visual encoder**:

- **Global Context Branch**: Processes the original image to preserve global context
- **Camouflage Expert Branch**: Uses a COD model (ZoomNeXt) to extract camouflaged object features

### C²GA Mechanism

The **Confidence-Conditioned Graph Attention** mechanism:

1. Leverages camouflage confidence scores from COD masks
2. Constructs separate foreground and background graphs
3. Aggregates features independently to prevent contamination
4. Adaptive gating fusion for stable feature integration

<div align="center">
<img src="images/fig3_architecture.png" width="100%" alt="CECNet Architecture">
</div>

---

## 📊 CamoIT Dataset

### Statistics

| Metric | Value |
|--------|-------|
| Total Samples | ~10.5K |
| Categories | 237 |
| Annotation Levels | 3 |
| Avg. Words/Caption | ~25 |

### Data Sources

CamoIT is built upon four COD benchmark datasets:
- **CHAMELEON**
- **CAMO**
- **COD10K**
- **NC4K**

### Multi-Granularity Annotations

| Level | Type | Example |
|-------|------|---------|
| Level 1 | Category Label | "crab" |
| Level 2 | Object Description | "The crab has a shiny, brown shell" |
| Level 3 | Image Caption | "A crab with a mottled brown body is perched among a mix of smooth pebbles..." |

<div align="center">
<img src="images/fig2_dataset.png" width="90%" alt="CamoIT Dataset">
</div>

---

## 📈 Results

### Quantitative Results on CamoIT

| Method | I2T R@1 | I2T R@5 | I2T R@10 | T2I R@1 | T2I R@5 | T2I R@10 |
|--------|---------|---------|----------|---------|---------|----------|
| CFM | 30.8 | 59.9 | 70.3 | 28.9 | 57.2 | 68.3 |
| HREM | 34.3 | 62.7 | 74.0 | 31.5 | 59.9 | 71.4 |
| CUSA | 23.9 | 53.5 | 66.7 | 23.5 | 51.3 | 64.3 |
| D2S-VSE | 37.1 | 68.4 | 79.5 | 35.5 | 67.5 | 78.4 |
| AVSE | 28.1 | 59.7 | 72.2 | 26.1 | 56.3 | 69.7 |
| CLIP | 41.3 | 69.2 | 79.0 | 41.1 | 67.7 | 78.4 |
| **CECNet (Ours)** | **45.8** | **74.5** | **83.5** | **44.6** | **73.9** | **83.1** |

### Key Findings

- 🚀 **~29% performance boost** over fine-tuned CLIP baseline (rSum metric)
- ✅ **Consistent gains** across different ViT-based retrieval methods
- 🔧 **Universal applicability** - design improves AVSE and D2S-VSE when integrated

### Qualitative Results

<div align="center">
<img src="images/fig4_sentence_retrieval.png" width="45%" alt="Sentence Retrieval">
<img src="images/fig4_image_retrieval.png" width="45%" alt="Image Retrieval">
</div>

---

## 🛠️ Getting Started

### Installation

```bash
# Clone the repository
git clone https://github.com/your-username/CECNet.git
cd CECNet

# Create conda environment
conda create -n cecnet python=3.8
conda activate cecnet

# Install dependencies
pip install -r requirements.txt
```

### Dataset Preparation

1. Download CamoIT dataset from [here](#)
2. Organize the dataset as follows:
```
data/
├── images/
│   ├── train/
│   └── test/
├── masks/
├── annotations/
│   ├── train.json
│   └── test.json
```

### Training

```bash
# Train CECNet
python train.py --config configs/cecnet.yaml
```

### Evaluation

```bash
# Evaluate on CamoIT test set
python evaluate.py --config configs/cecnet.yaml --checkpoint path/to/checkpoint.pth
```

---

## 📁 Project Structure

```
CECNet/
├── configs/
│   └── cecnet.yaml
├── data/
│   └── dataset.py
├── models/
│   ├── cecnet.py
│   ├── c2ga.py
│   └── encoders.py
├── utils/
│   └── utils.py
├── train.py
├── evaluate.py
└── requirements.txt
```

---

## 📜 Citation

If you find this work useful, please consider citing:

```bibtex
@inproceedings{cecnet2026,
  title={Camouflage-aware Image-Text Retrieval via Expert Collaboration},
  author={Anonymous},
  booktitle={Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR)},
  year={2026}
}
```

---

## 🙏 Acknowledgements

This work builds upon several excellent projects:

- [CLIP](https://github.com/openai/CLIP) - Contrastive Language-Image Pre-training
- [ZoomNeXt](https://github.com/lartpang/ZoomNeXt) - COD expert model
- [D2S-VSE](https://github.com/username/D2S-VSE) - Dense-to-Sparse Visual Semantic Embedding

---

## 📧 Contact

For questions and discussions, please open an issue or contact [email].

---

<div align="center">

**Made with ❤️ for the Computer Vision Community**

</div>
