import os
import shutil
import ctypes
import subprocess
import logging

def empty_recycle_bin():
    """Empties the Windows Recycle Bin silently."""
    try:
        # SHERB_NOCONFIRMATION (0x1) | SHERB_NOPROGRESSUI (0x2) | SHERB_NOSOUND (0x4) = 7
        res = ctypes.windll.shell32.SHEmptyRecycleBinW(None, None, 7)
        return res == 0
    except Exception as e:
        logging.warning(f"Error emptying recycle bin: {e}")
        return False

def flush_dns():
    """Flushes the Windows DNS Resolver Cache."""
    try:
        subprocess.run(["ipconfig", "/flushdns"], capture_output=True, text=True, check=False, creationflags=subprocess.CREATE_NO_WINDOW)
        return True
    except Exception as e:
        logging.warning(f"Error flushing DNS: {e}")
        return False

def clean_directory(dir_path, max_files=1000):
    """
    Cleans temporary files and folders in dir_path efficiently.
    Returns (files_removed, bytes_freed).
    """
    files_removed = 0
    bytes_freed = 0

    if not os.path.exists(dir_path):
        return (0, 0)

    try:
        with os.scandir(dir_path) as entries:
            for entry in entries:
                if files_removed >= max_files:
                    break
                try:
                    if entry.is_file(follow_symlinks=False):
                        size = entry.stat().st_size
                        os.remove(entry.path)
                        files_removed += 1
                        bytes_freed += size
                    elif entry.is_dir(follow_symlinks=False):
                        shutil.rmtree(entry.path, ignore_errors=True)
                        files_removed += 1
                except Exception:
                    pass
    except Exception:
        pass

    return (files_removed, bytes_freed)

def run_system_cleanup():
    """
    Executes a comprehensive, safe executive clean:
    1. Windows Recycle Bin
    2. User %TEMP%
    3. Windows Temp (if permitted)
    4. INetCache (Internet temporary files)
    5. Windows DNS flush
    Returns a result dict.
    """
    total_files = 0
    total_bytes = 0

    # 1. User Temp
    user_temp = os.environ.get("TEMP", "")
    if user_temp and os.path.exists(user_temp):
        f_cnt, b_cnt = clean_directory(user_temp)
        total_files += f_cnt
        total_bytes += b_cnt

    # 2. System Temp
    sys_temp = r"C:\Windows\Temp"
    if os.path.exists(sys_temp):
        f_cnt, b_cnt = clean_directory(sys_temp)
        total_files += f_cnt
        total_bytes += b_cnt

    # 3. Internet cache
    local_app_data = os.environ.get("LOCALAPPDATA", "")
    if local_app_data:
        inet_cache = os.path.join(local_app_data, "Microsoft", "Windows", "INetCache")
        if os.path.exists(inet_cache):
            f_cnt, b_cnt = clean_directory(inet_cache)
            total_files += f_cnt
            total_bytes += b_cnt

    # 4. Recycle Bin
    bin_status = empty_recycle_bin()

    # 5. Flush DNS
    dns_status = flush_dns()

    # Format freed size
    if total_bytes >= 1024 * 1024 * 1024:
        size_str = f"{total_bytes / (1024 * 1024 * 1024):.2f} GB"
    elif total_bytes >= 1024 * 1024:
        size_str = f"{total_bytes / (1024 * 1024):.1f} MB"
    else:
        size_str = f"{total_bytes / 1024:.0f} KB"

    summary = f"Cleared {total_files} files ({size_str}) • Recycle Bin Emptied"
    if dns_status:
        summary += " • DNS Flushed"

    return {
        "success": True,
        "files_removed": total_files,
        "bytes_freed": total_bytes,
        "size_str": size_str,
        "recycle_bin_emptied": bin_status,
        "dns_flushed": dns_status,
        "summary": summary
    }

if __name__ == "__main__":
    res = run_system_cleanup()
    print(res["summary"])
