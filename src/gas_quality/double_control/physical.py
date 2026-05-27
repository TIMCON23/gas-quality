import pandas as pd
import numpy as np


def physical_control(df, **kwargs):
    """Level 2: Physical Control
    
    Checks:
    - Balance error (mass conservation)
    - Flow gradient (maximum rate of change constraints)
    - Pressure-flow correlations
    
    Returns (scores, flags, details).
    """
    
    # 1. Balance Check (if columns exist)
    balance_err = None
    if all(c in df.columns for c in ["Qin", "Qout", "Qcons", "Qacc"]):
        balance_err = df["Qin"] - (df["Qout"] + df["Qcons"] + df["Qacc"])
        balance_err = np.abs(balance_err.values)
    elif "flow_m3h" in df.columns:
        # Fallback: gradient-based
        balance_err = np.abs(np.gradient(df["flow_m3h"].values))
    else:
        return np.zeros(len(df)), np.zeros(len(df)), {"status": "insufficient_columns"}
    
    # 2. Flow gradient (rate of change constraint)
    flow_col = None
    for col in ["flow_m3h", "flow", "Q"]:
        if col in df.columns:
            flow_col = col
            break
    
    gradient_score = np.zeros(len(df))
    max_gradient_allowed = kwargs.get("max_gradient", 2.0)  # m³/h per minute
    
    if flow_col:
        flow = df[flow_col].values
        gradient = np.abs(np.gradient(flow))
        gradient_score = np.minimum(gradient / max_gradient_allowed, 1.0)
    
    # 3. Pressure correlation (if available)
    pressure_score = np.zeros(len(df))
    if "pressure_kpa" in df.columns:
        # Pressure should not vary wildly with small flow changes
        pressure = df["pressure_kpa"].values
        pres_grad = np.abs(np.gradient(pressure))
        pressure_score = np.minimum(pres_grad / 5.0, 1.0)  # max 5 kPa/min allowed
    
    # 4. Temperature anomaly (if available)
    temp_score = np.zeros(len(df))
    if "temp_c" in df.columns:
        temp = df["temp_c"].values
        temp_grad = np.abs(np.gradient(temp))
        temp_score = np.minimum(temp_grad / 2.0, 1.0)  # max 2 °C/min
    
    # 5. Combine physical scores
    w_balance = 0.4
    w_gradient = 0.3
    w_pressure = 0.2
    w_temp = 0.1
    
    balance_norm = (balance_err - balance_err.min()) / (balance_err.max() - balance_err.min() + 1e-6)
    
    combined_score = (w_balance * balance_norm + 
                     w_gradient * gradient_score + 
                     w_pressure * pressure_score + 
                     w_temp * temp_score)
    
    threshold = kwargs.get("phys_threshold", 0.7)
    flags = (combined_score > threshold).astype(int)
    
    details = {
        "balance_error": balance_err,
        "gradient_score": gradient_score,
        "pressure_score": pressure_score,
        "temp_score": temp_score,
        "combined_score": combined_score,
        "threshold": threshold,
        "anomaly_count": flags.sum()
    }
    
    return combined_score, flags, details
