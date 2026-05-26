#!/bin/bash
# Run all baseline methods + CAE for Table 5 comparison
set -e

echo "=== Step 1: Vanilla (no intervention) ==="
python scripts/08_cae_inference.py --config configs/default.yaml --method vanilla

echo "=== Step 2: Zero-ablation ==="
python scripts/08_cae_inference.py --config configs/default.yaml --method zero_ablation

echo "=== Step 3: Anti-bias prompting ==="
python scripts/08_cae_inference.py --config configs/default.yaml --method prompting

echo "=== Step 4: Linear direction ablation ==="
python scripts/08_cae_inference.py --config configs/default.yaml --method linear_ablation

echo "=== Step 5: CAE (ours) ==="
python scripts/07_cae_project.py --config configs/default.yaml
python scripts/08_cae_inference.py --config configs/default.yaml --method cae

echo "=== Step 6: Evaluate all ==="
python scripts/09_evaluate.py --config configs/default.yaml

echo "Done. Results in results/evaluation/"
