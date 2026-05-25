from .io import ensure_dirs, save_results
from .config import DEFAULTS

def run_pipeline():
    ensure_dirs()
    # placeholder orchestration
    print("Pipeline skeleton: directories ensured.")
    print(f"Defaults: {DEFAULTS}")

if __name__ == "__main__":
    run_pipeline()
