"""
Common statistical metrics used across analytics modules.
"""

import numpy as np


def safe_mean(values):
    """
    Compute mean safely with error handling.

    Args:
        values (list | array): Numerical values.

    Returns:
        float | None: Mean of values.
    """
    try:
        arr = np.array(values)
        return float(np.nanmean(arr))
    except Exception as e:
        print(f"[METRICS] Mean failed: {e}")
        return None


def safe_std(values):
    """
    Compute standard deviation safely.

    Args:
        values (list | array): Numerical values.

    Returns:
        float | None: Standard deviation.
    """
    try:
        arr = np.array(values)
        return float(np.nanstd(arr))
    except Exception as e:
        print(f"[METRICS] STD failed: {e}")
        return None


def calculate_throughput(count, time_sec):
    """
    Calculate throughput = items / time.

    Args:
        count (int): Number of processed items.
        time_sec (float): Time taken in seconds.

    Returns:
        float | None: Throughput result.
    """
    try:
        if time_sec == 0:
            return None
        return count / time_sec
    except Exception as e:
        print(f"[METRICS] Throughput calc failed: {e}")
        return None
