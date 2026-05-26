"""Step 06: Steering experiments with Black latent

Usage:
    python scripts/06_steering.py --config configs/default.yaml
"""
import argparse, yaml, sys
sys.path.insert(0, ".")

def main(cfg):
    """Steering experiments with Black latent"""
    raise NotImplementedError(
        "This is a scaffold. Full implementation requires model weights and API keys. "
        "See README.md for usage instructions."
    )

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Steering experiments with Black latent")
    parser.add_argument("--config", default="configs/default.yaml")
    args = parser.parse_args()
    with open(args.config) as f: cfg = yaml.safe_load(f)
    main(cfg)
