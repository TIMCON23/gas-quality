from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

DATA_DIR = ROOT / "data"
RAW_DIR = DATA_DIR / "raw"
PROCESSED_DIR = DATA_DIR / "processed"
PLOTS_DIR = DATA_DIR / "plots"
RESULTS_DIR = DATA_DIR / "results"

DEFAULTS = {
    "rec_file": RAW_DIR / "rec_date.csv",
    "metrological_file": RAW_DIR / "metrological_data.csv",
    "model_comparison": RESULTS_DIR / "model_comparison.csv",
    "benchmark_dataset": RESULTS_DIR / "benchmark_dataset.csv",
}
