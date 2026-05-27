"""High-level pipeline orchestration."""

from .io import ensure_dirs, save_results
from .benchmark import build_benchmark_from_rec
from .config import DEFAULTS
import argparse


def run_pipeline(mode="cli"):
    """Run pipeline in CLI or GUI mode."""
    
    if mode == "gui":
        from .gui import launch_gui
        launch_gui()
    else:
        ensure_dirs()
        print("=" * 60)
        print("Double Control Gas Quality Analysis Pipeline")
        print("=" * 60)
        print("\nBuilding benchmark from reconstruction data...")
        
        try:
            results = build_benchmark_from_rec()
            print("\nResults:")
            print(results)
            print("\n✓ Analysis complete. Results saved to:")
            print(f"  - {DEFAULTS['benchmark_dataset']}")
            print(f"  - {DEFAULTS['model_comparison']}")
        except Exception as e:
            print(f"\n✗ Error: {e}")
            raise


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Gas Quality Double Control Pipeline")
    parser.add_argument("--gui", action="store_true", help="Launch GUI interface")
    args = parser.parse_args()
    
    mode = "gui" if args.gui else "cli"
    run_pipeline(mode=mode)

