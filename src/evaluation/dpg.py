"""Demographic Parity Gap, Equalized Odds Gap, and bootstrap CI."""
import numpy as np

def dpg(preds_a, preds_b):
    return abs(preds_a.mean() - preds_b.mean())

def eog(preds_a, labels_a, preds_b, labels_b):
    def rates(p, l):
        tpr = ((p==1)&(l==1)).sum() / max((l==1).sum(), 1)
        fpr = ((p==1)&(l==0)).sum() / max((l==0).sum(), 1)
        return tpr, fpr
    tpr_a, fpr_a = rates(preds_a, labels_a)
    tpr_b, fpr_b = rates(preds_b, labels_b)
    return max(abs(tpr_a - tpr_b), abs(fpr_a - fpr_b))

def bootstrap_ci(fn, args, n=1000, ci=0.95, seed=42):
    rng = np.random.RandomState(seed)
    N = len(args[0])
    vals = [fn(*[a[rng.choice(N, N, replace=True)] for a in args]) for _ in range(n)]
    lo, hi = np.percentile(vals, [(1-ci)/2*100, (1+ci)/2*100])
    return {"mean": np.mean(vals), "ci": (lo, hi), "std": np.std(vals)}
