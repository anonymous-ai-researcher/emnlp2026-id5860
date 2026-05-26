"""L1-regularized logistic probe for race prediction from SAE latents."""
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score, accuracy_score, f1_score
from sklearn.model_selection import StratifiedKFold

def train_probe(z, labels, C=0.1):
    probe = LogisticRegression(penalty="l1", C=C, solver="saga", max_iter=5000, random_state=42)
    probe.fit(z, labels)
    top_latents = np.argsort(np.abs(probe.coef_[0]))[::-1]
    return probe, top_latents

def evaluate(probe, z, labels):
    probs = probe.predict_proba(z)[:, 1]
    return {"auroc": roc_auc_score(labels, probs), "accuracy": accuracy_score(labels, probe.predict(z)),
            "f1": f1_score(labels, probe.predict(z))}

def cross_validate(z, labels, C=0.1, n_folds=5):
    skf = StratifiedKFold(n_splits=n_folds, shuffle=True, random_state=42)
    scores = []
    for train_idx, val_idx in skf.split(z, labels):
        probe = LogisticRegression(penalty="l1", C=C, solver="saga", max_iter=5000)
        probe.fit(z[train_idx], labels[train_idx])
        scores.append(roc_auc_score(labels[val_idx], probe.predict_proba(z[val_idx])[:, 1]))
    return {"mean": np.mean(scores), "std": np.std(scores), "folds": scores}
