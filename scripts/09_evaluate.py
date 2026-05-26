"""Step 09: Compute DPG, EOG, MedQA accuracy, bootstrap CI

Usage:
    python scripts/09_evaluate.py --config configs/default.yaml
"""
import argparse, yaml, sys
sys.path.insert(0, ".")

def main(cfg):
    """Compute DPG, EOG, MedQA accuracy, bootstrap CI"""
    raise NotImplementedError(
        "This is a scaffold. Full implementation requires model weights and API keys. "
        "See README.md for usage instructions."
    )

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Compute DPG, EOG, MedQA accuracy, bootstrap CI")
    parser.add_argument("--config", default="configs/default.yaml")
    args = parser.parse_args()
    with open(args.config) as f: cfg = yaml.safe_load(f)
    main(cfg)
