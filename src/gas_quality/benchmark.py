"""Benchmark builder: orchestration of reconstruction, injection, detection, evaluation."""
import os
import numpy as np
import pandas as pd

from .reconstruction import reconstruct_signal
from .anomalies.injection import inject_anomalies
from .anomalies.detectors import isolation_forest_score, dbscan_score, autoencoder_score
from .evaluation import compute_metrics
from .config import DEFAULTS


def build_benchmark_from_rec(rec_filepath=None, save_results=True):
    rec_filepath = rec_filepath or DEFAULTS["rec_file"]
    df = pd.read_csv(rec_filepath)
    # align and sort
    time = df["time"].values.astype(float)
    signal = df["black"].values.astype(float)
    time_dense, recon = reconstruct_signal(time, signal)

    # inject anomalies
    signal_anom, labels = inject_anomalies(recon)

    X = signal_anom.reshape(-1, 1)

    # detectors
    scores_if, pred_if = isolation_forest_score(X)
    scores_db, pred_db = dbscan_score(X)
    scores_ae, pred_ae = autoencoder_score(X)

    # simple dc score
    grad = np.abs(np.gradient(signal_anom))
    dc_score = np.abs((np.abs(recon - signal_anom)) + 0.7 * grad)
    pred_dc = (dc_score > np.percentile(dc_score, 85)).astype(int)

    # collect model rows similar to original generation
    rows = []
    models = [
        ("IsolationForest", scores_if, pred_if),
        ("DBSCAN", scores_db, pred_db),
        ("Autoencoder", scores_ae, pred_ae),
        ("DoubleControl", dc_score, pred_dc),
    ]
    for name, scores, preds in models:
        # compute metrics
        m = compute_metrics(labels, preds, scores)
        rows.append({"model": name, "ROC_AUC": m["ROC_AUC"], "Precision": m["Precision"], "Recall": m["Recall"], "F1": m["F1"]})

    results_df = pd.DataFrame(rows)

    if save_results:
        os.makedirs(DEFAULTS["benchmark_dataset"].parent, exist_ok=True)
        # dataset
        dataset_df = pd.DataFrame({"time": time_dense, "signal_normal": recon, "signal_anomaly": signal_anom, "label": labels})
        dataset_df.to_csv(DEFAULTS["benchmark_dataset"], index=False)
        results_df.to_csv(DEFAULTS["model_comparison"], index=False)

    return results_df


if __name__ == "__main__":
    print("Building benchmark from rec_date...")
    res = build_benchmark_from_rec()
    print(res)
