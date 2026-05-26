"""Step 01: Generate 2,004 counterfactual vignettes via GPT-4

Usage:
    python scripts/01_generate_vignettes.py --config configs/default.yaml
"""
import argparse, yaml, sys
sys.path.insert(0, ".")

def main(cfg):
    """Generate 2,004 counterfactual vignettes via GPT-4"""
    raise NotImplementedError(
        "This is a scaffold. Full implementation requires model weights and API keys. "
        "See README.md for usage instructions."
    )

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate 2,004 counterfactual vignettes via GPT-4")
    parser.add_argument("--config", default="configs/default.yaml")
    args = parser.parse_args()
    with open(args.config) as f: cfg = yaml.safe_load(f)
    main(cfg)
