"""Double Control method orchestration: Statistical (L1) + Physical (L2) checks."""

import numpy as np
import pandas as pd
from .statistical import statistical_control
from .physical import physical_control


def double_control_full(signal_raw, signal_reconstructed, df_metrics=None, **kwargs):
    """
    Complete Double Control method:
    Level 1 (Statistical Control): reconstruction error, ML anomalies
    Level 2 (Physical Control): balance, gradients, correlations
    
    Returns final report with both L1 and L2 decisions.
    """
    
    # Level 1: Statistical Control
    l1_scores, l1_flags, l1_details = statistical_control(
        signal_raw, 
        signal_reconstructed,
        stat_threshold=kwargs.get("stat_threshold", 0.6)
    )
    
    # Level 2: Physical Control
    if df_metrics is not None:
        l2_scores, l2_flags, l2_details = physical_control(
            df_metrics,
            max_gradient=kwargs.get("max_gradient", 2.0),
            phys_threshold=kwargs.get("phys_threshold", 0.7)
        )
    else:
        l2_scores = np.zeros_like(l1_scores)
        l2_flags = np.zeros_like(l1_flags)
        l2_details = {"status": "no_metrics"}
    
    # Final Decision: Both must agree (AND) or weighted combination
    final_mode = kwargs.get("final_mode", "weighted")  # or "strict"
    
    if final_mode == "strict":
        # Both L1 and L2 must flag as anomaly
        final_flags = (l1_flags & l2_flags).astype(int)
    else:
        # Weighted combination
        w_l1 = kwargs.get("w_l1", 0.55)
        w_l2 = kwargs.get("w_l2", 0.45)
        final_scores = w_l1 * l1_scores + w_l2 * l2_scores
        final_threshold = kwargs.get("final_threshold", 0.65)
        final_flags = (final_scores > final_threshold).astype(int)
    
    # Build report
    report = {
        "L1_Statistical": {
            "scores": l1_scores,
            "flags": l1_flags,
            "anomaly_count": l1_flags.sum(),
            "details": l1_details
        },
        "L2_Physical": {
            "scores": l2_scores,
            "flags": l2_flags,
            "anomaly_count": l2_flags.sum(),
            "details": l2_details
        },
        "Final_Decision": {
            "flags": final_flags,
            "anomaly_count": final_flags.sum(),
            "mode": final_mode,
            "verdict": "ANOMALY DETECTED" if final_flags.sum() > 0 else "NORMAL"
        },
        "Summary": {
            "total_points": len(final_flags),
            "anomaly_percentage": 100.0 * final_flags.sum() / len(final_flags) if len(final_flags) > 0 else 0,
            "l1_agreement": 100.0 * (l1_flags == final_flags).sum() / len(final_flags) if len(final_flags) > 0 else 0,
        }
    }
    
    return report
