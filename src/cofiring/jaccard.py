"""Jaccard co-firing analysis between race latent and all other latents."""
import numpy as np

def compute_cofiring(z, race_idx, mask=None):
    """C(r,j) = |A_r & A_j| / |A_r | A_j| for all j."""
    if mask is not None: z = z[mask]
    active_r = z[:, race_idx] > 0
    M = z.shape[1]
    scores = np.zeros(M)
    for j in range(M):
        if j == race_idx: continue
        active_j = z[:, j] > 0
        inter = (active_r & active_j).sum()
        union = (active_r | active_j).sum()
        scores[j] = inter / union if union > 0 else 0
    return scores

def build_stigma_set(scores, percentile=95, race_idx=0):
    threshold = np.percentile(scores[scores > 0], percentile)
    S = [j for j in range(len(scores)) if scores[j] > threshold and j != race_idx]
    return S, threshold
