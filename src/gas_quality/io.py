import pandas as pd
from .config import RAW_DIR, RESULTS_DIR, PLOTS_DIR
from pathlib import Path


def ensure_dirs():
    for p in (RAW_DIR, RESULTS_DIR, PLOTS_DIR):
        Path(p).mkdir(parents=True, exist_ok=True)


def read_raw_csv(name):
    p = RAW_DIR / name
    return pd.read_csv(p)


def save_results(df, name):
    p = RESULTS_DIR / name
    df.to_csv(p, index=False)


def save_plot(fig, name):
    p = PLOTS_DIR / name
    fig.savefig(p, dpi=300)
