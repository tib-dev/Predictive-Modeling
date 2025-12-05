"""
project_root.py
----------------
Utility to compute and expose the project root directory.

This helps notebooks or scripts consistently reference the top-level
project folder without repeating the same Path logic.

Usage:
    from utils.project_root import get_project_root
    root = get_project_root()
"""

from pathlib import Path


def get_project_root() -> Path:
    """
    Returns the absolute path to the project root directory.
    The function assumes that this file lives inside:
     utils/project_root.py

    Returns:
        Path: Path object pointing to the project root.
    """
    try:
        # utils/ -> go up one level
        return Path(__file__).resolve().parent.parent
    except Exception as e:
        raise RuntimeError(f"Could not determine project root: {e}")
