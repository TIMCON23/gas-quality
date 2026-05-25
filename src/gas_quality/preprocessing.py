import numpy as np
import pandas as pd


def align_and_dropna(df, required_cols):
    df = df.dropna()
    for c in required_cols:
        if c not in df.columns:
            raise ValueError(f"Missing column: {c}")
    return df


def resample_to_seconds(time, signal):
    # placeholder: user can replace with real resampling
    return time, signal
