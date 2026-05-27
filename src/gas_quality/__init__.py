"""gas_quality package
Minimal package initializer for the gas quality project.
"""
__version__ = "0.1.0"

from .pipeline import run_pipeline  # convenient shortcut
from .orchestration import MASHost

__all__ = ["run_pipeline", "MASHost"]
