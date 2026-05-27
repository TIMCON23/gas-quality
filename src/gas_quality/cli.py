"""Command-line interface for Double Control pipeline."""

import argparse
from .pipeline import run_pipeline


def main():
    parser = argparse.ArgumentParser(
        description="Double Control Gas Quality Analysis System",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python -m src.gas_quality.cli --cli          # Run CLI pipeline
  python -m src.gas_quality.cli --gui          # Launch SCADA GUI
  python scripts/run_gui.py                    # Alternative: direct GUI launch
        """
    )
    
    parser.add_argument("--gui", action="store_true", 
                       help="Launch interactive SCADA GUI interface")
    parser.add_argument("--cli", action="store_true", 
                       help="Run CLI pipeline (default if no flag)")
    
    args = parser.parse_args()
    
    # Default to CLI if no mode specified
    if not args.gui and not args.cli:
        args.cli = True
    
    if args.gui:
        run_pipeline(mode="gui")
    else:
        run_pipeline(mode="cli")


if __name__ == "__main__":
    main()

