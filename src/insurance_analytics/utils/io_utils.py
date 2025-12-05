"""
Utility functions for file input/output operations.
Handles CSV and text files with safe error-handling.
"""

import os
import pandas as pd


def read_csv(path):
    """
    Safely read a CSV file.

    Args:
        path (str): File path to read.

    Returns:
        DataFrame | None: Loaded pandas DataFrame, or None on error.
    """
    try:
        return pd.read_csv(path)
    except FileNotFoundError:
        print(f"[IO] File not found: {path}")
    except Exception as e:
        print(f"[IO] Failed to read CSV: {e}")
    return None


def write_csv(df, path):
    """
    Write a DataFrame to CSV safely.

    Args:
        df (DataFrame): The data to write.
        path (str): Destination path.
    """
    try:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        df.to_csv(path, index=False)
    except Exception as e:
        print(f"[IO] Failed to write CSV: {e}")


def read_text(path):
    """
    Read text from a file.

    Args:
        path (str): Path to the text file.

    Returns:
        str | None: File contents or None on error.
    """
    try:
        with open(path, "r") as f:
            return f.read()
    except Exception as e:
        print(f"[IO] Error reading text: {e}")
        return None


def write_text(path, content):
    """
    Write text to a file.

    Args:
        path (str): Destination path.
        content (str): Text to write.
    """
    try:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w") as f:
            f.write(content)
    except Exception as e:
        print(f"[IO] Error writing text: {e}")
