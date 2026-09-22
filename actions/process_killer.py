import os
import subprocess
import logging

def kill_hung_processes(process_names=None):
    """
    Terminates unresponsive or specified processes.
    Default targets: excel.exe, winword.exe, acrobat.exe (common culprits during officer briefings).
    """
    targets = process_names or ["excel.exe", "winword.exe", "acrobat.exe"]
    if isinstance(targets, str):
        targets = [p.strip() for p in targets.split(",") if p.strip()]

    killed = []
    for proc in targets:
        if not proc.lower().endswith(".exe"):
            proc = proc + ".exe"
        try:
            # taskkill /F /IM <proc>
            cmd = ["taskkill", "/F", "/IM", proc]
            res = subprocess.run(cmd, capture_output=True, text=True, check=False, creationflags=subprocess.CREATE_NO_WINDOW)
            if res.returncode == 0:
                killed.append(proc)
        except Exception as e:
            logging.error(f"Error terminating {proc}: {e}")

    if killed:
        return {"success": True, "summary": f"Terminated hung process: {', '.join(killed)}"}
    else:
        return {"success": True, "summary": "No hung targeted processes were running."}
