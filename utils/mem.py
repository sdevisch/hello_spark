import os
import platform
import subprocess
from typing import Optional


def _read_proc_meminfo_total_kb() -> Optional[int]:
    try:
        with open("/proc/meminfo", "r", encoding="utf-8") as f:
            for line in f:
                if line.startswith("MemTotal:"):
                    parts = line.split()
                    # Example: MemTotal:       32777268 kB
                    return int(parts[1])  # already in kB
    except Exception:
        return None
    return None


def _sysctl_mem_bytes() -> Optional[int]:
    try:
        out = subprocess.check_output(["sysctl", "-n", "hw.memsize"], text=True).strip()
        return int(out)
    except Exception:
        return None


def get_total_memory_gb(default_gb: float = 8.0) -> float:
    """Return total system memory in GB without requiring psutil.

    Tries, in order: psutil (if available), /proc/meminfo (Linux), sysctl (macOS),
    then falls back to a conservative default.
    """
    # Try psutil if present
    try:
        import psutil  # type: ignore

        return float(psutil.virtual_memory().total) / (1024**3)
    except Exception:
        pass

    if platform.system() == "Linux":
        kb = _read_proc_meminfo_total_kb()
        if kb is not None:
            return float(kb) / (1024**2)

    if platform.system() == "Darwin":
        bytes_total = _sysctl_mem_bytes()
        if bytes_total is not None:
            return float(bytes_total) / (1024**3)

    # Windows or unknown
    try:
        import ctypes

        class MEMORYSTATUSEX(ctypes.Structure):
            _fields_ = [
                ("dwLength", ctypes.c_ulong),
                ("dwMemoryLoad", ctypes.c_ulong),
                ("ullTotalPhys", ctypes.c_ulonglong),
                ("ullAvailPhys", ctypes.c_ulonglong),
                ("ullTotalPageFile", ctypes.c_ulonglong),
                ("ullAvailPageFile", ctypes.c_ulonglong),
                ("ullTotalVirtual", ctypes.c_ulonglong),
                ("ullAvailVirtual", ctypes.c_ulonglong),
                ("sullAvailExtendedVirtual", ctypes.c_ulonglong),
            ]

        stat = MEMORYSTATUSEX()
        stat.dwLength = ctypes.sizeof(MEMORYSTATUSEX)
        if ctypes.windll.kernel32.GlobalMemoryStatusEx(ctypes.byref(stat)):
            return float(stat.ullTotalPhys) / (1024**3)
    except Exception:
        pass

    return default_gb


def get_process_memory_gb() -> float:
    """Return current process RSS in GB without requiring psutil.

    Tries psutil if present, otherwise uses resource.getrusage.
    """
    # Try psutil
    try:
        import psutil  # type: ignore

        return float(psutil.Process(os.getpid()).memory_info().rss) / (1024**3)
    except Exception:
        pass

    # resource fallback
    try:
        import resource

        usage = resource.getrusage(resource.RUSAGE_SELF)
        rss = usage.ru_maxrss
        # On Linux ru_maxrss is in kilobytes; on macOS it's in bytes
        if platform.system() == "Darwin":
            bytes_rss = float(rss)
        else:
            bytes_rss = float(rss) * 1024.0
        return bytes_rss / (1024**3)
    except Exception:
        return 0.0


def get_process_memory_mb() -> float:
    return get_process_memory_gb() * 1024.0


def get_cpu_count(default_count: int = 4) -> int:
    try:
        # Try psutil if present for consistency
        import psutil  # type: ignore

        count = psutil.cpu_count(logical=True)
        if isinstance(count, int) and count > 0:
            return count
    except Exception:
        pass
    try:
        count2 = os.cpu_count()
        if isinstance(count2, int) and count2 is not None and count2 > 0:
            return count2
    except Exception:
        pass
    return default_count


