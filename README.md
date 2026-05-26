[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/downloads/)
[![PyTorch](https://img.shields.io/badge/PyTorch-2.2%2B-red.svg)](https://pytorch.org/)
[![CUDA](https://img.shields.io/badge/CUDA-12.1-green.svg)](https://developer.nvidia.com/cuda-toolkit)
[![SAE-lens](https://img.shields.io/badge/SAE--lens-0.4%2B-orange.svg)](https://github.com/jbloomAus/SAELens)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Venue](https://img.shields.io/badge/EMNLP-2026-purple.svg)](#)

> **Auditing Intersectional Bias in Clinical LLMs: Sparse Autoencoders Reveal Race-HIV Stigma Circuits**
>
> *Anonymous submission to EMNLP 2026 (ARR May 2026)*

---

## TL;DR

**Racial bias in a clinical LLM compounds with HIV-positive status beyond additive prediction, and chain-of-thought reasoning never discloses it.** We use Gemma Scope SAE latents to show that the Black racial identity latent co-fires with HIV-specific stigma concepts (noncompliance, substance use) in a superadditive pattern confirmed by factorial ANOVA. Contrastive Activation Editing (CAE) removes only the stigma-coupled component of the race-encoding decoder direction while preserving clinically relevant information, reducing demographic parity gaps by 73% with 98% accuracy retained.

---

## Overview

BiasScope is a framework for auditing and mitigating intersectional bias in clinical language models using sparse autoencoders (SAEs). The pipeline has three stages:

1. **Intersectional Bias Audit** -- Identify race-encoding SAE latents, quantify co-firing with stigma concepts, and test for superadditive Race x HIV-Status interactions via factorial ANOVA.
2. **Causal Verification** -- Steer the Black latent during generation to confirm causal influence on clinical predictions; analyze chain-of-thought for unfaithful reasoning.
3. **Contrastive Activation Editing (CAE)** -- Decompose the race decoder direction into stigma-coupled and clinically relevant components; subtract only the former during inference.

---

## Key Results

| Method | DPG (T3) | DPG (T4) | EOG (T4) | MedQA | HIV Acc |
|--------|----------|----------|----------|-------|---------|
| Vanilla | 0.71+/-.03 | 0.19+/-.02 | 0.21+/-.03 | 62.3 | 71.8 |
| Zero-ablation | 0.67+/-.03 | 0.17+/-.02 | 0.19+/-.03 | 58.7 | 66.9 |
| Prompting | 0.48+/-.04 | 0.12+/-.02 | 0.14+/-.03 | 62.1 | 71.2 |
| Linear ablation | 0.31+/-.03 | 0.08+/-.02 | 0.10+/-.02 | 60.2 | 68.5 |
| **CAE (ours)** | **0.19+/-.02** | **0.04+/-.01** | **0.05+/-.02** | **61.4** | **70.1** |

---

## Installation

```bash
git clone https://github.com/anonymous/biasscope.git
cd biasscope
conda create -n biasscope python=3.10 -y
conda activate biasscope
pip install -r requirements.txt
```

---

## Project Structure

```
biasscope/
|-- README.md
|-- LICENSE
|-- requirements.txt
|-- configs/
|   `-- default.yaml
|-- data/templates/
|-- src/
|   |-- extraction/         # SAE activation extraction
|   |-- probing/            # Race probe training
|   |-- cofiring/           # Jaccard co-firing analysis
|   |-- steering/           # Latent steering
|   |-- cae/                # Contrastive Activation Editing
|   |-- evaluation/         # DPG, EOG, bootstrap CI
|   `-- utils/              # Model loading, configs
|-- scripts/
|   |-- 01_generate_vignettes.py
|   |-- 02_extract_activations.py
|   |-- 03_train_probe.py
|   |-- 04_cofiring_analysis.py
|   |-- 05_factorial_anova.py
|   |-- 06_steering.py
|   |-- 07_cae_project.py
|   |-- 08_cae_inference.py
|   |-- 09_evaluate.py
|   |-- 10_ablation_grid.py
|   `-- run_all_baselines.sh
|-- notebooks/
`-- results/
```

---

## Quick Start

### Full pipeline

```bash
# Step 1: Generate benchmark (requires OpenAI API key)
python scripts/01_generate_vignettes.py --config configs/default.yaml

# Step 2-4: Extract activations, train probe, co-firing analysis
python scripts/02_extract_activations.py --config configs/default.yaml
python scripts/03_train_probe.py --config configs/default.yaml
python scripts/04_cofiring_analysis.py --config configs/default.yaml

# Step 5-6: Factorial ANOVA and steering
python scripts/05_factorial_anova.py --config configs/default.yaml
python scripts/06_steering.py --config configs/default.yaml

# Step 7-9: CAE projection, inference, evaluation
python scripts/07_cae_project.py --config configs/default.yaml
python scripts/08_cae_inference.py --config configs/default.yaml
python scripts/09_evaluate.py --config configs/default.yaml
```

### Run all baselines (Table 5)

```bash
bash scripts/run_all_baselines.sh
```

---

## Benchmark

**2,004 counterfactual vignettes** in a 2x2 factorial design:

|  | Black | White |
|--|-------|-------|
| **HIV+** | 501 | 501 |
| **HIV-** | 501 | 501 |

**6 clinical scenarios** (20 templates): neurocognitive complaint, substance use screening, pain management, psychiatric evaluation, medication adherence, routine follow-up.

**4 probe tasks**: T1 Diagnosis (free text), T2 Treatment (free text), T3 Risk (1-5 Likert), T4 Referral (Yes/No).

---

## Method: Contrastive Activation Editing

CAE decomposes the race decoder direction **d_r** into stigma-coupled and clinical components:

```
d_r^stigma = D_S (D_S^T D_S)^{-1} D_S^T d_r     (projection)
h' = h - alpha * f_r^t * d_r^stigma               (editing)
```

**Key properties**: conditional (no-op when Black latent inactive), targeted (only stigma component removed), efficient (+1.1 ms/token, 13% overhead).

---

## Computational Requirements

| Stage | Time | GPUs |
|-------|------|------|
| Vignette generation | 3.2 h | 0 |
| SAE extraction | 4.5 h | 4 |
| Probe + co-firing + ANOVA | ~10 min | 0 |
| Steering (500 vignettes) | 1.8 h | 4 |
| CAE inference (2,004 vignettes) | 3.6 h | 4 |
| Full ablation grid | 28 h | 4 |
| **Total (without ablation)** | **~13 h** | |

Hardware: 4x NVIDIA A100 80GB, AMD EPYC 7763, 512 GB RAM.

---

## License

MIT License with Responsible Use clause. See [LICENSE](LICENSE).

The benchmark and code are intended for **bias auditing and mitigation research**. Pre-computed steering vectors are not released to prevent misuse.
