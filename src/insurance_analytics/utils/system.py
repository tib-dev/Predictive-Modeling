"""
System resource utilities for CPU, memory, and process inspection.
"""

import psutil


def get_cpu_usage():
    """
    Get CPU usage as a percentage.

    Returns:
        float | None: CPU usage percentage, or None on failure.
    """
    try:
        return psutil.cpu_percent(interval=1)
    except Exception as e:
        print(f"[SYSTEM] CPU check failed: {e}")
        return None


def get_memory_usage():
    """
    Get memory usage statistics.

    Returns:
        dict | None: Memory info dictionary, or None on failure.
    """
    try:
        mem = psutil.virtual_memory()
        return {"total": mem.total, "used": mem.used, "percent": mem.percent}
    except Exception as e:
        print(f"[SYSTEM] Memory check failed: {e}")
        return None


def get_process_info():
    """
    Retrieve list of running processes.

    Returns:
        list: List of process dictionaries.
    """
    try:
        return [{"pid": p.pid, "name": p.name()} for p in psutil.process_iter()]
    except Exception as e:
        print(f"[SYSTEM] Process list failed: {e}")
        return []
