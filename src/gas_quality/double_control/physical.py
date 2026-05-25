import pandas as pd
import numpy as np


def physical_control(df, qin_col="Qin", qout_col="Qout", qcons_col="Qcons", qacc_col="Qacc"):
    # compute balance error if columns present
    if all(c in df.columns for c in [qin_col, qout_col, qcons_col, qacc_col]):
        be = df[qin_col] - (df[qout_col] + df[qcons_col] + df[qacc_col])
        return np.abs(be.values)
    else:
        # fallback: use gradient of flow if available
        if "flow_m3h" in df.columns:
            grad = np.abs(np.gradient(df["flow_m3h"].values))
            return grad
    return np.zeros(len(df))
