"""Step 02: Extract SAE activations for all vignettes

Usage:
    python scripts/02_extract_activations.py --config configs/default.yaml
"""
import argparse, yaml, sys
sys.path.insert(0, ".")

def main(cfg):
    """Extract SAE activations for all vignettes"""
    raise NotImplementedError(
        "This is a scaffold. Full implementation requires model weights and API keys. "
        "See README.md for usage instructions."
    )

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Extract SAE activations for all vignettes")
    parser.add_argument("--config", default="configs/default.yaml")
    args = parser.parse_args()
    with open(args.config) as f: cfg = yaml.safe_load(f)
    main(cfg)
