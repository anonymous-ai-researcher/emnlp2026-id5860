"""Model and SAE loading utilities."""
import torch, yaml
from transformers import AutoTokenizer, AutoModelForCausalLM
from sae_lens import SAE

def load_config(path="configs/default.yaml"):
    with open(path) as f: return yaml.safe_load(f)

def load_model(cfg):
    tok = AutoTokenizer.from_pretrained(cfg["model"]["name"])
    model = AutoModelForCausalLM.from_pretrained(
        cfg["model"]["name"], torch_dtype=getattr(torch, cfg["model"]["dtype"]), device_map="auto")
    return model, tok

def load_sae(cfg):
    return SAE.from_pretrained(
        release=cfg["sae"]["suite"],
        sae_id=f"layer_{cfg['sae']['layer']}/width_{cfg['sae']['width']//1000}k/canonical")
