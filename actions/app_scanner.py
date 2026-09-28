import os
import sys
import winreg
import subprocess
import json
import logging
from typing import List, Dict, Optional

# Cache to avoid re-scanning filesystem every time dialog opens
_CACHED_APPS: Optional[List[Dict[str, str]]] = None

SYSTEM_UTILITIES = [
    ("Calculator", "calc.exe", "🧮", "System Utility", "calculator calc math sum numbers"),
    ("Notepad", "notepad.exe", "📝", "System Utility", "notepad text editor notes txt"),
    ("Snipping Tool", "snippingtool.exe", "✂️", "System Utility", "snipping tool snip screenshot screen capture"),
    ("Paint", "mspaint.exe", "🎨", "System Utility", "paint drawing mspaint image edit graphics"),
    ("File Explorer", "explorer.exe", "📁", "System Utility", "explorer files folders drive my computer"),
    ("Task Manager", "taskmgr.exe", "📊", "System Utility", "task manager taskmgr kill processes performance cpu ram"),
    ("Command Prompt", "cmd.exe", "💻", "System Utility", "cmd command prompt terminal dos shell cli"),
    ("PowerShell", "powershell.exe", "⚡", "System Utility", "powershell terminal windows scripting shell"),
    ("Windows Settings", "ms-settings:", "⚙️", "System Utility", "settings preferences configuration control"),
    ("Control Panel", "control.exe", "🎛️", "System Utility", "control panel settings system administrative"),
    ("Device Manager", "devmgmt.msc", "🖥️", "System Utility", "device manager drivers hardware usb display"),
    ("Sound Control Panel", "mmsys.cpl", "🔊", "System Utility", "sound audio volume speakers microphone headphones"),
    ("Disk Management", "diskmgmt.msc", "💾", "System Utility", "disk management partitions storage drives"),
    ("Registry Editor", "regedit.exe", "🔧", "System Utility", "registry editor regedit system settings"),
]

IGNORE_KEYWORDS = [
    'uninstall', 'help', 'readme', 'documentation', 'release notes', 
    'website', 'remove', 'license', 'manual', 'modify', 'setup wizard',
    'support center', 'online help', 'diagnostic', 'troubleshoot'
]

def pick_icon_for_app(app_name: str) -> str:
    n = app_name.lower()
    if any(w in n for w in ['chrome', 'edge', 'firefox', 'brave', 'browser', 'opera', 'safari', 'internet', 'tor']):
        return '🌐'
    if any(w in n for w in ['code', 'pycharm', 'studio', 'visual studio', 'sublime', 'terminal', 'git', 'intellij', 'antigravity', 'anythingllm', 'ide', 'compiler']):
        return '💻'
    if any(w in n for w in ['excel', 'sheet', 'calc', 'finance', 'broker', 'quote', 'stock', 'trading']):
        return '📊'
    if any(w in n for w in ['word', 'writer', 'document', 'pdf', 'acrobat', 'reader', 'onenote', 'notes', 'obsidian']):
        return '📄'
    if any(w in n for w in ['powerpoint', 'slide', 'present', 'keynote']):
        return '📽️'
    if any(w in n for w in ['spotify', 'music', 'audio', 'sound', 'itunes', 'fl studio']):
        return '🎵'
    if any(w in n for w in ['vlc', 'video', 'player', 'media', 'bandicam', 'capcut', 'premiere', 'davinci', 'blackmagic', 'stream']):
        return '🎬'
    if any(w in n for w in ['discord', 'slack', 'teams', 'zoom', 'telegram', 'whatsapp', 'skype', 'signal', 'messenger', 'outlook', 'mail']):
        return '💬'
    if any(w in n for w in ['steam', 'game', 'epic', 'xbox', 'play', 'riot', 'battle.net', 'asphalt']):
        return '🎮'
    if any(w in n for w in ['photoshop', 'illustrator', 'paint', 'blender', 'design', 'cad', 'fusion', 'bambu', '3d', 'render']):
        return '🎨'
    if any(w in n for w in ['cleaner', 'ccleaner', 'purge', 'antivirus', 'security', 'defender', 'protect']):
        return '🛡️'
    if any(w in n for w in ['cloud', 'drive', 'dropbox', 'onedrive', 'backup']):
        return '☁️'
    return '🚀'

def scan_installed_apps(force_refresh: bool = False, include_store_apps: bool = True) -> List[Dict[str, str]]:
    """
    Fast discovery of installed applications across Windows.
    Combines:
      1. Essential System Utilities (Instant)
      2. Start Menu Shortcuts (.lnk from All Users and Current User)
      3. Registry App Paths (HKLM & HKCU)
      4. Windows Store / Modern UWP Apps (via PowerShell Get-StartApps)
    Returns sorted list of app dictionaries:
      {'name': str, 'target': str, 'icon': str, 'category': str, 'keywords': str}
    """
    global _CACHED_APPS
    if _CACHED_APPS is not None and not force_refresh:
        return _CACHED_APPS

    apps: List[Dict[str, str]] = []
    seen_names = set()

    # 1. System Utilities
    for name, cmd, ico, cat, kw in SYSTEM_UTILITIES:
        apps.append({
            "name": name,
            "target": cmd,
            "icon": ico,
            "category": cat,
            "keywords": f"{name} {kw}".lower()
        })
        seen_names.add(name.lower())

    # 2. Start Menu Shortcuts (.lnk)
    start_dirs = [
        os.path.join(os.environ.get('ProgramData', r'C:\ProgramData'), r'Microsoft\Windows\Start Menu\Programs'),
        os.path.join(os.environ.get('APPDATA', ''), r'Microsoft\Windows\Start Menu\Programs')
    ]
    for d in start_dirs:
        if not os.path.exists(d):
            continue
        for root, _, files in os.walk(d):
            for f in files:
                if f.lower().endswith('.lnk'):
                    raw_name = os.path.splitext(f)[0].strip()
                    if any(k in raw_name.lower() for k in IGNORE_KEYWORDS):
                        continue
                    clean_lower = raw_name.lower()
                    if clean_lower in seen_names:
                        continue
                    seen_names.add(clean_lower)

                    full_path = os.path.join(root, f)
                    ico = pick_icon_for_app(raw_name)
                    apps.append({
                        "name": raw_name,
                        "target": full_path,
                        "icon": ico,
                        "category": "Desktop Application",
                        "keywords": f"{raw_name} {raw_name.replace(' ', '')}".lower()
                    })

    # 3. Registry App Paths
    for root_k in (winreg.HKEY_LOCAL_MACHINE, winreg.HKEY_CURRENT_USER):
        try:
            with winreg.OpenKey(root_k, r"SOFTWARE\Microsoft\Windows\CurrentVersion\App Paths") as key:
                num_subkeys = winreg.QueryInfoKey(key)[0]
                for i in range(num_subkeys):
                    try:
                        sk = winreg.EnumKey(key, i)
                        with winreg.OpenKey(key, sk) as subk:
                            val, _ = winreg.QueryValueEx(subk, "")
                            val_c = val.strip('"')
                            if val_c.lower().endswith('.exe') and os.path.exists(val_c):
                                app_name = os.path.splitext(sk)[0].replace('_', ' ').replace('-', ' ').title()
                                if app_name.lower() not in seen_names and not any(k in app_name.lower() for k in IGNORE_KEYWORDS):
                                    seen_names.add(app_name.lower())
                                    ico = pick_icon_for_app(app_name)
                                    apps.append({
                                        "name": app_name,
                                        "target": val_c,
                                        "icon": ico,
                                        "category": "Desktop Application",
                                        "keywords": f"{app_name} {sk}".lower()
                                    })
                    except Exception:
                        pass
        except Exception:
            pass

    # 4. Windows Store / UWP Apps via Get-StartApps
    if include_store_apps:
        try:
            cmd = ["powershell", "-NoProfile", "-NonInteractive", "-Command", "Get-StartApps | ConvertTo-Json -Compress"]
            proc = subprocess.run(cmd, capture_output=True, text=True, timeout=2)
            if proc.returncode == 0 and proc.stdout.strip():
                data = json.loads(proc.stdout)
                if isinstance(data, dict):
                    data = [data]
                for item in data:
                    name = item.get("Name", "").strip()
                    app_id = item.get("AppID", "").strip()
                    if not name or not app_id:
                        continue
                    if any(k in name.lower() for k in IGNORE_KEYWORDS):
                        continue
                    if name.lower() in seen_names:
                        continue
                    
                    # If it's a UWP app id (contains '!' or doesn't look like a direct path)
                    target = f"shell:AppsFolder\\{app_id}" if ("!" in app_id or not os.path.exists(app_id)) else app_id
                    seen_names.add(name.lower())
                    ico = pick_icon_for_app(name)
                    apps.append({
                        "name": name,
                        "target": target,
                        "icon": ico,
                        "category": "Windows Store App" if "!" in app_id else "Desktop Application",
                        "keywords": f"{name} {app_id}".lower()
                    })
        except Exception as e:
            logging.debug(f"Fast UWP discovery skipped: {e}")

    # Sort alphabetically with System Utilities at the top
    def sort_key(item):
        is_sys = 0 if item["category"] == "System Utility" else 1
        return (is_sys, item["name"].lower())

    apps.sort(key=sort_key)
    _CACHED_APPS = apps
    return apps
