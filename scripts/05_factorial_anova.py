"""Step 05: Two-way ANOVA for Race x HIV-Status interaction

Usage:
    python scripts/05_factorial_anova.py --config configs/default.yaml
"""
import argparse, yaml, sys
sys.path.insert(0, ".")

def main(cfg):
    """Two-way ANOVA for Race x HIV-Status interaction"""
    raise NotImplementedError(
        "This is a scaffold. Full implementation requires model weights and API keys. "
        "See README.md for usage instructions."
    )

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Two-way ANOVA for Race x HIV-Status interaction")
    parser.add_argument("--config", default="configs/default.yaml")
    args = parser.parse_args()
    with open(args.config) as f: cfg = yaml.safe_load(f)
    main(cfg)
