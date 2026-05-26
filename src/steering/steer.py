"""Latent steering: amplify Black latent during generation (Eq. 7)."""
import torch

def steer_latent(f, race_idx, alpha=1.0):
    """f_r^t <- f_r^t + alpha * max_i(f_i^t)"""
    f_max = f.max(dim=-1, keepdim=True).values
    f_steered = f.clone()
    f_steered[..., race_idx] += alpha * f_max.squeeze(-1)
    return f_steered
