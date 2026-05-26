[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/downloads/)
[![PyTorch](https://img.shields.io/badge/PyTorch-2.2%2B-red.svg)](https://pytorch.org/)
[![CUDA](https://img.shields.io/badge/CUDA-12.1-green.svg)](https://developer.nvidia.com/cuda-toolkit)
[![SAE-lens](https://img.shields.io/badge/SAE--lens-0.4%2B-orange.svg)](https://github.com/jbloomAus/SAELens)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
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

| Method | DPG (T3) | DPG (T4) | EOG (T4) | MedQA (%) | HIV Acc (%) |
|--------|----------|----------|----------|-----------|-------------|
| Vanilla | 0.71+/-.03 | 0.19+/-.02 | 0.21+/-.03 | 62.3 | 71.8 |
| Zero-ablation | 0.67+/-.03 | 0.17+/-.02 | 0.19+/-.03 | 58.7 | 66.9 |
| Prompting | 0.48+/-.04 | 0.12+/-.02 | 0.14+/-.03 | 62.1 | 71.2 |
| Linear ablation | 0.31+/-.03 | 0.08+/-.02 | 0.10+/-.02 | 60.2 | 68.5 |
| **CAE (ours)** | **0.19+/-.02** | **0.04+/-.01** | **0.05+/-.02** | **61.4** | **70.1** |

DPG: demographic parity gap (lower is fairer). EOG: equalized odds gap. +/-: bootstrap 95% CI over 1,000 resamples. MedQA and HIV Acc are point estimates (seed sensitivity: SD = 0.012 for DPG).

---

## Installation

```bash
git clone https://github.com/anonymous/biasscope.git
cd biasscope
conda create -n biasscope python=3.10 -y
conda activate biasscope
pip install -r requirements.txt
```

Verify:

```bash
python -c "import torch; print(f'PyTorch {torch.__version__}, CUDA {torch.cuda.is_available()}')"
python -c "import sae_lens; print(f'SAE-lens {sae_lens.__version__}')"
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
|-- data/templates/          # 20 base clinical templates
|-- src/
|   |-- extraction/          # SAE activation extraction + max-aggregation
|   |-- probing/             # L1 logistic probe + 5-fold CV
|   |-- cofiring/            # Jaccard co-firing + stigma set S construction
|   |-- steering/            # Latent steering (Eq. 7)
|   |-- cae/                 # Stigma subspace projection (Eq. 9) + CAE editing (Eq. 10)
|   |-- evaluation/          # DPG, EOG, bootstrap CI, MedQA accuracy
|   `-- utils/               # Model/SAE loading, config parsing
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

## Benchmark

**2,004 counterfactual clinical vignettes** in a 2x2 factorial design:

|  | Black | White |
|--|-------|-------|
| **HIV+** | 501 | 501 |
| **HIV-** | 501 | 501 |

**6 clinical scenarios** across 20 templates:

| Scenario | Templates | Example |
|----------|-----------|---------|
| Neurocognitive complaint | 1-3 | Memory, concentration, executive function |
| Substance use screening | 4-7 | Alcohol, opioid, cannabis, stimulant |
| Pain management | 8-10 | Chronic, neuropathic, post-surgical |
| Psychiatric evaluation | 11-13 | Depression, anxiety, PTSD |
| Medication adherence | 14-17 | Missed doses, refill gaps, side effects |
| Routine follow-up | 18-20 | Chronic conditions, wellness |

**4 probe tasks:**

| Task | Format | Evaluation Metric |
|------|--------|-------------------|
| T1 Diagnosis | Free text | Qualitative |
| T2 Treatment | Free text | Qualitative |
| T3 Risk | 1-5 Likert score | DPG (gap in mean Likert score) |
| T4 Referral | Yes/No | DPG (gap in referral rate), EOG |

---

## Quick Start

### Full pipeline

```bash
# Step 1: Generate benchmark (requires OpenAI API key for GPT-4)
python scripts/01_generate_vignettes.py --config configs/default.yaml

# Step 2-4: Extract activations, train probe, co-firing analysis
python scripts/02_extract_activations.py --config configs/default.yaml
python scripts/03_train_probe.py --config configs/default.yaml
python scripts/04_cofiring_analysis.py --config configs/default.yaml

# Step 5-6: Factorial ANOVA and steering experiments
python scripts/05_factorial_anova.py --config configs/default.yaml
python scripts/06_steering.py --config configs/default.yaml

# Step 7-9: CAE projection, inference, evaluation
python scripts/07_cae_project.py --config configs/default.yaml
python scripts/08_cae_inference.py --config configs/default.yaml
python scripts/09_evaluate.py --config configs/default.yaml
```

### Reproduce Table 5 (all baselines + CAE)

```bash
bash scripts/run_all_baselines.sh
# Outputs: results/evaluation/main_results.csv
```

### Reproduce Table 6 (ablation grid)

```bash
python scripts/10_ablation_grid.py --config configs/default.yaml
# ~28h on 4xA100
```

---

## Method: Contrastive Activation Editing

CAE decomposes the race decoder direction **d_r** into stigma-coupled and clinical components:

**Step 1: Stigma subspace projection (precomputed once)**

```
d_r^stigma = D_S (D_S^T D_S)^{-1} D_S^T d_r
```

where D_S is the matrix of decoder directions for the stigma-associated latent set S (|S| = 47 latents identified via Jaccard co-firing at the 95th percentile threshold).

**Step 2: Inference-time editing (per token)**

```
h' = h - alpha * f_r^t * d_r^stigma
```

**Key properties:**

- **Conditional**: when f_r^t = 0 (Black latent inactive), h' = h (no intervention)
- **Targeted**: only the stigma-coupled component is removed; clinical information in directions orthogonal to D_S is preserved
- **Efficient**: projection precomputed; per-token overhead is +1.1 ms (13%)

---

## Configuration

All hyperparameters in `configs/default.yaml`:

```yaml
model:
  name: google/gemma-2-9b-it
  dtype: bfloat16
sae:
  suite: gemma-scope-9b-pt-res-canonical
  layer: 20           # Best DPG (Table 6)
  width: 16384
probe:
  regularization: 0.1 # L1 penalty
cofiring:
  metric: jaccard
  threshold_percentile: 95  # yields |S| = 47
steering:
  alpha: 1.0
  perplexity_threshold: 0.15  # 15% above baseline
cae:
  alpha: 1.0
  pseudoinverse_threshold: 1.0e-4
evaluation:
  bootstrap_n: 1000
  seeds: [42, 123, 456]
```

**Selected configuration** (bold in Table 6; SD over 3 seeds):
- Layer 20: DPG = 0.19 +/- .01, MedQA = 61.4 +/- .3
- Width 16,384 (wider SAEs offer diminishing returns)
- |S| = 47 (95th percentile threshold)

---

## Computational Requirements

| Stage | Time | GPUs |
|-------|------|------|
| Vignette generation (GPT-4 API) | 3.2 h | 0 |
| SAE activation extraction | 4.5 h | 4 |
| Probe + co-firing + ANOVA | ~10 min | 0 |
| Steering (500 vignettes) | 1.8 h | 4 |
| CAE inference (2,004 vignettes) | 3.6 h | 4 |
| Full ablation grid | 28 h | 4 |
| **Total (without ablation)** | **~13 h** | |
| **Total (with ablation)** | **~41 h** | |

Hardware: 4x NVIDIA A100 80GB, AMD EPYC 7763 64-core, 512 GB RAM.

Estimated carbon footprint: ~25 kg CO2 total (~8 kg for main experiments).

---

## Environment

| Component | Version |
|-----------|---------|
| Python | 3.10.12 |
| PyTorch | 2.2.1+cu121 |
| Transformers | 4.42.0 |
| SAE-lens | 0.4.0 |
| scikit-learn | 1.4.0 |
| NumPy | 1.26.3 |
| SciPy | 1.12.0 |

---

## License

MIT License with Responsible Use clause. See [LICENSE](LICENSE).

The benchmark and code are intended for **bias auditing and mitigation research**. Use of the activation editing techniques to amplify bias or cause harm is explicitly prohibited.
