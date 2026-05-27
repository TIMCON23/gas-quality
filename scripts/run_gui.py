"""Entry point for SCADA GUI application."""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.gas_quality.gui import launch_gui

if __name__ == "__main__":
    launch_gui()
