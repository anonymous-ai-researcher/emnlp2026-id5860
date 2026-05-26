"""Contrastive Activation Editing: projection and editing (Eq. 9-10)."""
import torch

def compute_stigma_projection(sae, race_idx, stigma_set, pinv_thr=1e-4):
    """d_r^stigma = D_S (D_S^T D_S)^{-1} D_S^T d_r"""
    W_dec = sae.W_dec.data
    d_r = W_dec[race_idx]
    D_S = W_dec[stigma_set].T
    U, S, Vh = torch.linalg.svd(D_S, full_matrices=False)
    S_inv = torch.where(S > pinv_thr * S[0], 1.0 / S, torch.zeros_like(S))
    D_S_pinv = Vh.T @ torch.diag(S_inv) @ U.T
    d_stigma = D_S @ (D_S_pinv @ d_r)
    return d_stigma, d_r - d_stigma

def cae_edit(h, f_r, d_stigma, alpha=1.0):
    """h' = h - alpha * f_r^t * d_r^stigma"""
    return h - alpha * f_r.unsqueeze(-1) * d_stigma
