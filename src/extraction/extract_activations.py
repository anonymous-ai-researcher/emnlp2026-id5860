"""Extract SAE latent activations from Gemma-2-9B-it via Gemma Scope."""
import torch, json, argparse
from pathlib import Path
from tqdm import tqdm
from transformers import AutoTokenizer, AutoModelForCausalLM
from sae_lens import SAE

def load_model_and_sae(model_name, sae_id, layer, width, dtype=torch.bfloat16):
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForCausalLM.from_pretrained(model_name, torch_dtype=dtype, device_map="auto")
    sae = SAE.from_pretrained(release=sae_id, sae_id=f"layer_{layer}/width_{width}k/canonical")
    return model, tokenizer, sae

def extract(model, tokenizer, sae, vignettes, layer, batch_size=8):
    activations = {}
    for i in tqdm(range(0, len(vignettes), batch_size)):
        batch = vignettes[i:i+batch_size]
        inputs = tokenizer([v["text"] for v in batch], return_tensors="pt", padding=True, truncation=True, max_length=512)
        inputs = {k: v.to(model.device) for k, v in inputs.items()}
        with torch.no_grad():
            hidden = model(**inputs, output_hidden_states=True).hidden_states[layer+1]
            for j, v in enumerate(batch):
                seq_len = inputs["attention_mask"][j].sum().item()
                f = sae.encode(hidden[j, :seq_len])
                activations[v["id"]] = f.max(dim=0).values.cpu()
    return activations

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", default="google/gemma-2-9b-it")
    parser.add_argument("--sae_id", default="gemma-scope-9b-pt-res-canonical")
    parser.add_argument("--layer", type=int, default=20)
    parser.add_argument("--width", type=int, default=16384)
    parser.add_argument("--vignettes", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    with open(args.vignettes) as f: vignettes = json.load(f)
    model, tok, sae = load_model_and_sae(args.model, args.sae_id, args.layer, args.width)
    acts = extract(model, tok, sae, vignettes, args.layer)
    Path(args.output).mkdir(parents=True, exist_ok=True)
    torch.save(acts, Path(args.output) / "activations.pt")
