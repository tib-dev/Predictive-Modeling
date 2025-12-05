"""
project_root.py
----------------
Utility to compute and expose the project root directory.

Ensures that scripts or notebooks can consistently reference the
top-level project folder without repeating path logic.

Usage:
    from insurance_analytics.utils.project_root import get_project_root
    root = get_project_root()
"""

from pathlib import Path


def get_project_root() -> Path:
    """
    Returns the absolute path to the project root directory.

    Assumes this file lives inside `utils/project_root.py` and that
    the project root is two levels up.

    Returns
    -------
    Path
        Path object pointing to the project root.

    Raises
    ------
    RuntimeError
        If the root cannot be determined.
    """
    try:
        return Path(__file__).resolve().parent.parent
    except Exception as e:
        raise RuntimeError(f"Could not determine project root: {e}")
