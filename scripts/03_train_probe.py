"""Step 03: Train L1 logistic probe for race prediction

Usage:
    python scripts/03_train_probe.py --config configs/default.yaml
"""
import argparse, yaml, sys
sys.path.insert(0, ".")

def main(cfg):
    """Train L1 logistic probe for race prediction"""
    raise NotImplementedError(
        "This is a scaffold. Full implementation requires model weights and API keys. "
        "See README.md for usage instructions."
    )

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Train L1 logistic probe for race prediction")
    parser.add_argument("--config", default="configs/default.yaml")
    args = parser.parse_args()
    with open(args.config) as f: cfg = yaml.safe_load(f)
    main(cfg)
