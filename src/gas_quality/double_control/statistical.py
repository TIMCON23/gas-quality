import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import IsolationForest


def statistical_control(signal_raw, signal_reconstructed, **kwargs):
    """Level 1: Statistical Control
    
    Analyzes reconstruction error, rolling statistics, and ML anomaly scores.
    Returns (scores, flags, details).
    """
    
    # 1. Reconstruction Error
    min_len = min(len(signal_raw), len(signal_reconstructed))

    # Trim to common length to avoid broadcasting errors
    signal_raw = np.asarray(signal_raw)[:min_len]
    signal_reconstructed = np.asarray(signal_reconstructed)[:min_len]

    recon_err = np.abs(signal_reconstructed - signal_raw)
    
    # 2. Rolling statistics (z-score detection)
    df = pd.DataFrame({"signal": signal_reconstructed})
    rolling_mean = df["signal"].rolling(window=15, center=True).mean()
    rolling_std = df["signal"].rolling(window=15, center=True).std()
    rolling_mean = rolling_mean.bfill().ffill()
    rolling_std = rolling_std.bfill().ffill()
    
    stat_score = np.abs((signal_reconstructed - rolling_mean.values) / (rolling_std.values + 1e-6))
    stat_score = np.minimum(stat_score, 10)
    
    # 3. Isolation Forest
    X = signal_reconstructed.reshape(-1, 1)
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    iso_forest = IsolationForest(contamination=0.1, random_state=42)
    iso_forest.fit(X_scaled)
    iso_scores = -iso_forest.decision_function(X_scaled)
    iso_scores = (iso_scores - iso_scores.min()) / (iso_scores.max() - iso_scores.min() + 1e-6)
    
    # 4. Combine scores
    w_recon, w_stat, w_iso = 0.3, 0.4, 0.3
    recon_norm = (recon_err - recon_err.min()) / (recon_err.max() - recon_err.min() + 1e-6)
    stat_norm = (stat_score - stat_score.min()) / (stat_score.max() - stat_score.min() + 1e-6)
    
    combined_score = w_recon * recon_norm + w_stat * stat_norm + w_iso * iso_scores
    combined_score = (combined_score - combined_score.min()) / (combined_score.max() - combined_score.min() + 1e-6)
    
    threshold = kwargs.get("stat_threshold", 0.6)
    flags = (combined_score > threshold).astype(int)
    
    details = {
        "recon_error": recon_err,
        "stat_score": stat_score,
        "iso_score": iso_scores,
        "combined_score": combined_score,
        "threshold": threshold,
        "anomaly_count": flags.sum()
    }
    
    return combined_score, flags, details
