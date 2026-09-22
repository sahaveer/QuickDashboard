import time
import ctypes
import logging

VK_MAP = {
    "win": 0x5B, "lwin": 0x5B, "rwin": 0x5C,
    "ctrl": 0x11, "control": 0x11,
    "alt": 0x12, "menu": 0x12,
    "shift": 0x10,
    "esc": 0x1B, "escape": 0x1B,
    "tab": 0x09, "enter": 0x0D, "space": 0x20,
    "backspace": 0x08, "delete": 0x2E,
    "up": 0x26, "down": 0x28, "left": 0x25, "right": 0x27,
    "prtscn": 0x2C, "printscreen": 0x2C,
    "period": 0xBE, ".": 0xBE,
    "comma": 0xBC, ",": 0xBC,
    "semicolon": 0xBA, ";": 0xBA,
    "plus": 0xBB, "=": 0xBB,
    "minus": 0xBD, "-": 0xBD,
    "0": 0x30, "1": 0x31, "2": 0x32, "3": 0x33, "4": 0x34,
    "5": 0x35, "6": 0x36, "7": 0x37, "8": 0x38, "9": 0x39
}

TOP_50_SHORTCUTS = [
    # 1 - 10: Screen Capture, Clipboard & Core Navigation
    {
        "id": "win_shift_s",
        "keys": "win+shift+s",
        "title": "SNIP TOOL",
        "subtitle": "Snipping Tool Snapshot",
        "icon": "✂️",
        "badge": "Win+Shift+S",
        "desc": "Windows Snipping Tool (Area / Window capture)"
    },
    {
        "id": "win_v",
        "keys": "win+v",
        "title": "CLIPBOARD",
        "subtitle": "Clipboard History Panel",
        "icon": "📋",
        "badge": "Win+V",
        "desc": "Open Clipboard History (View past copied texts & images)"
    },
    {
        "id": "win_d",
        "keys": "win+d",
        "title": "DESKTOP",
        "subtitle": "Show / Hide Desktop",
        "icon": "🖥️",
        "badge": "Win+D",
        "desc": "Minimize all windows to desktop (Boss Key)"
    },
    {
        "id": "win_l",
        "keys": "win+l",
        "title": "LOCK PC",
        "subtitle": "Lock Workstation Screen",
        "icon": "🔒",
        "badge": "Win+L",
        "desc": "Instantly lock your computer screen"
    },
    {
        "id": "ctrl_shift_esc",
        "keys": "ctrl+shift+esc",
        "title": "TASK MGR",
        "subtitle": "Open Windows Task Manager",
        "icon": "⚡",
        "badge": "Ctrl+Shift+Esc",
        "desc": "Open Task Manager directly to kill frozen programs"
    },
    {
        "id": "win_e",
        "keys": "win+e",
        "title": "EXPLORER",
        "subtitle": "Open File Explorer",
        "icon": "📁",
        "badge": "Win+E",
        "desc": "Open Windows File Explorer"
    },
    {
        "id": "win_period",
        "keys": "win+.",
        "title": "EMOJIS",
        "subtitle": "Emoji & Symbol Selector",
        "icon": "😀",
        "badge": "Win+.",
        "desc": "Open Windows Emoji, Symbol & Math Character Panel"
    },
    {
        "id": "win_h",
        "keys": "win+h",
        "title": "DICTATION",
        "subtitle": "Voice Typing & Speech",
        "icon": "🎙️",
        "badge": "Win+H",
        "desc": "Windows Voice Typing (Dictate speech into any text field)"
    },
    {
        "id": "alt_tab",
        "keys": "alt+tab",
        "title": "SWITCH APP",
        "subtitle": "Switch Between Apps",
        "icon": "🔄",
        "badge": "Alt+Tab",
        "desc": "Switch between open windows and apps"
    },
    {
        "id": "win_tab",
        "keys": "win+tab",
        "title": "TASK VIEW",
        "subtitle": "Task View & Desktops",
        "icon": "🗂️",
        "badge": "Win+Tab",
        "desc": "Open Task View and Virtual Desktops"
    },

    # 11 - 20: Window Snapping & System Tools
    {
        "id": "win_i",
        "keys": "win+i",
        "title": "SETTINGS",
        "subtitle": "Windows Settings Panel",
        "icon": "⚙️",
        "badge": "Win+I",
        "desc": "Open Windows System Settings"
    },
    {
        "id": "win_r",
        "keys": "win+r",
        "title": "RUN DIALOG",
        "subtitle": "Run Command Prompt",
        "icon": "🏃",
        "badge": "Win+R",
        "desc": "Open the Windows Run dialog box"
    },
    {
        "id": "win_x",
        "keys": "win+x",
        "title": "POWER MENU",
        "subtitle": "Quick Link Admin Menu",
        "icon": "⚡",
        "badge": "Win+X",
        "desc": "Open Windows Quick Link / Admin Menu"
    },
    {
        "id": "win_a",
        "keys": "win+a",
        "title": "QUICK ACTION",
        "subtitle": "Action Center / Wi-Fi",
        "icon": "📶",
        "badge": "Win+A",
        "desc": "Open Quick Settings (Wi-Fi, Bluetooth, Audio)"
    },
    {
        "id": "win_n",
        "keys": "win+n",
        "title": "NOTIFY & CAL",
        "subtitle": "Notification & Calendar",
        "icon": "📅",
        "badge": "Win+N",
        "desc": "Open Notification Center and Calendar"
    },
    {
        "id": "win_z",
        "keys": "win+z",
        "title": "SNAP LAYOUT",
        "subtitle": "Snap Window Grid",
        "icon": "📐",
        "badge": "Win+Z",
        "desc": "Open Windows Snap Layouts grid"
    },
    {
        "id": "win_left",
        "keys": "win+left",
        "title": "SNAP LEFT",
        "subtitle": "Snap Window Left Half",
        "icon": "◀️",
        "badge": "Win+Left",
        "desc": "Snap active window to the left half of screen"
    },
    {
        "id": "win_right",
        "keys": "win+right",
        "title": "SNAP RIGHT",
        "subtitle": "Snap Window Right Half",
        "icon": "▶️",
        "badge": "Win+Right",
        "desc": "Snap active window to the right half of screen"
    },
    {
        "id": "win_up",
        "keys": "win+up",
        "title": "MAXIMIZE",
        "subtitle": "Maximize Active Window",
        "icon": "🔼",
        "badge": "Win+Up",
        "desc": "Maximize the active window"
    },
    {
        "id": "win_down",
        "keys": "win+down",
        "title": "MINIMIZE",
        "subtitle": "Minimize Active Window",
        "icon": "🔽",
        "badge": "Win+Down",
        "desc": "Minimize the active window"
    },

    # 21 - 30: Document, Edit & Office Actions
    {
        "id": "win_prtscn",
        "keys": "win+prtscn",
        "title": "FULL SNAP",
        "subtitle": "Auto-Save Full Screen",
        "icon": "📸",
        "badge": "Win+PrtScn",
        "desc": "Take full screenshot and auto-save directly to Pictures"
    },
    {
        "id": "alt_f4",
        "keys": "alt+f4",
        "title": "CLOSE APP",
        "subtitle": "Exit Current Program",
        "icon": "❌",
        "badge": "Alt+F4",
        "desc": "Close the active application or window"
    },
    {
        "id": "ctrl_z",
        "keys": "ctrl+z",
        "title": "UNDO",
        "subtitle": "Undo Last Change",
        "icon": "↩️",
        "badge": "Ctrl+Z",
        "desc": "Undo last edit or action"
    },
    {
        "id": "ctrl_y",
        "keys": "ctrl+y",
        "title": "REDO",
        "subtitle": "Redo Last Action",
        "icon": "↪️",
        "badge": "Ctrl+Y",
        "desc": "Redo undone action"
    },
    {
        "id": "ctrl_a",
        "keys": "ctrl+a",
        "title": "SELECT ALL",
        "subtitle": "Select All Text / Files",
        "icon": "☑️",
        "badge": "Ctrl+A",
        "desc": "Select all items, text, or files in view"
    },
    {
        "id": "ctrl_c",
        "keys": "ctrl+c",
        "title": "COPY",
        "subtitle": "Copy Selected to Clip",
        "icon": "📄",
        "badge": "Ctrl+C",
        "desc": "Copy selected item to clipboard"
    },
    {
        "id": "ctrl_v",
        "keys": "ctrl+v",
        "title": "PASTE",
        "subtitle": "Paste from Clipboard",
        "icon": "📥",
        "badge": "Ctrl+V",
        "desc": "Paste content from clipboard"
    },
    {
        "id": "ctrl_x",
        "keys": "ctrl+x",
        "title": "CUT",
        "subtitle": "Cut Selected Item",
        "icon": "✂️",
        "badge": "Ctrl+X",
        "desc": "Cut selected content"
    },
    {
        "id": "ctrl_f",
        "keys": "ctrl+f",
        "title": "FIND",
        "subtitle": "Search in Page / Doc",
        "icon": "🔍",
        "badge": "Ctrl+F",
        "desc": "Search for word or phrase in active document/webpage"
    },
    {
        "id": "ctrl_h",
        "keys": "ctrl+h",
        "title": "REPLACE",
        "subtitle": "Find and Replace",
        "icon": "🔄",
        "badge": "Ctrl+H",
        "desc": "Open Find & Replace in Word/Excel or Browser History"
    },

    # 31 - 40: Browser, Tabs & Navigation
    {
        "id": "ctrl_s",
        "keys": "ctrl+s",
        "title": "SAVE FILE",
        "subtitle": "Save Document / Sheet",
        "icon": "💾",
        "badge": "Ctrl+S",
        "desc": "Save current file or spreadsheet"
    },
    {
        "id": "ctrl_p",
        "keys": "ctrl+p",
        "title": "PRINT / PDF",
        "subtitle": "Print or Export PDF",
        "icon": "🖨️",
        "badge": "Ctrl+P",
        "desc": "Print document or save as PDF"
    },
    {
        "id": "ctrl_w",
        "keys": "ctrl+w",
        "title": "CLOSE TAB",
        "subtitle": "Close Active Tab",
        "icon": "⏹️",
        "badge": "Ctrl+W",
        "desc": "Close current browser tab or document"
    },
    {
        "id": "ctrl_t",
        "keys": "ctrl+t",
        "title": "NEW TAB",
        "subtitle": "Open Fresh Browser Tab",
        "icon": "➕",
        "badge": "Ctrl+T",
        "desc": "Open a new web browser tab"
    },
    {
        "id": "ctrl_shift_t",
        "keys": "ctrl+shift+t",
        "title": "REOPEN TAB",
        "subtitle": "Restore Closed Tab",
        "icon": "🔄",
        "badge": "Ctrl+Shift+T",
        "desc": "Reopen the last closed browser tab"
    },
    {
        "id": "ctrl_n",
        "keys": "ctrl+n",
        "title": "NEW WINDOW",
        "subtitle": "New Window / Doc",
        "icon": "🪟",
        "badge": "Ctrl+N",
        "desc": "Open a new application window or blank file"
    },
    {
        "id": "ctrl_shift_n",
        "keys": "ctrl+shift+n",
        "title": "INCOGNITO",
        "subtitle": "Private Browsing Tab",
        "icon": "🕵️",
        "badge": "Ctrl+Shift+N",
        "desc": "Open Private / Incognito browser window"
    },
    {
        "id": "ctrl_l",
        "keys": "ctrl+l",
        "title": "URL BAR",
        "subtitle": "Focus Web Address Bar",
        "icon": "🌐",
        "badge": "Ctrl+L",
        "desc": "Jump focus directly to the browser URL address bar"
    },
    {
        "id": "ctrl_plus",
        "keys": "ctrl+plus",
        "title": "ZOOM IN",
        "subtitle": "Magnify Text & View",
        "icon": "🔎",
        "badge": "Ctrl+Plus",
        "desc": "Zoom in / enlarge view"
    },
    {
        "id": "ctrl_minus",
        "keys": "ctrl+minus",
        "title": "ZOOM OUT",
        "subtitle": "Shrink Zoom View",
        "icon": "🔍",
        "badge": "Ctrl+Minus",
        "desc": "Zoom out to see more data"
    },

    # 41 - 50: Advanced Display, Media & Productivity
    {
        "id": "ctrl_0",
        "keys": "ctrl+0",
        "title": "RESET ZOOM",
        "subtitle": "Reset Zoom to 100%",
        "icon": "🎯",
        "badge": "Ctrl+0",
        "desc": "Reset display zoom to default 100%"
    },
    {
        "id": "f5",
        "keys": "f5",
        "title": "REFRESH",
        "subtitle": "Reload Webpage / Sheet",
        "icon": "🔄",
        "badge": "F5",
        "desc": "Refresh active webpage or data connection"
    },
    {
        "id": "f11",
        "keys": "f11",
        "title": "FULLSCREEN",
        "subtitle": "Toggle Full Screen Mode",
        "icon": "⛶",
        "badge": "F11",
        "desc": "Toggle fullscreen distraction-free view"
    },
    {
        "id": "win_m",
        "keys": "win+m",
        "title": "MIN ALL",
        "subtitle": "Minimize All Windows",
        "icon": "🗕",
        "badge": "Win+M",
        "desc": "Minimize all windows to taskbar"
    },
    {
        "id": "win_shift_m",
        "keys": "win+shift+m",
        "title": "RESTORE ALL",
        "subtitle": "Restore Minimized",
        "icon": "🗖",
        "badge": "Win+Shift+M",
        "desc": "Restore all minimized windows back to screen"
    },
    {
        "id": "win_p",
        "keys": "win+p",
        "title": "PROJECT",
        "subtitle": "Presentation / Dual Mon",
        "icon": "📽️",
        "badge": "Win+P",
        "desc": "Open presentation / dual-monitor projection sidebar"
    },
    {
        "id": "win_k",
        "keys": "win+k",
        "title": "CAST DISPLAY",
        "subtitle": "Connect Wireless Screen",
        "icon": "📺",
        "badge": "Win+K",
        "desc": "Cast display to conference TV or wireless screen"
    },
    {
        "id": "win_g",
        "keys": "win+g",
        "title": "GAME BAR",
        "subtitle": "Screen Recorder & Audio",
        "icon": "🎮",
        "badge": "Win+G",
        "desc": "Open Game Bar for quick video capture and audio mixer"
    },
    {
        "id": "win_1",
        "keys": "win+1",
        "title": "PINNED APP 1",
        "subtitle": "Launch 1st Taskbar App",
        "icon": "1️⃣",
        "badge": "Win+1",
        "desc": "Quick-launch the 1st pinned app on your Windows Taskbar"
    },
    {
        "id": "win_2",
        "keys": "win+2",
        "title": "PINNED APP 2",
        "subtitle": "Launch 2nd Taskbar App",
        "icon": "2️⃣",
        "badge": "Win+2",
        "desc": "Quick-launch the 2nd pinned app on your Windows Taskbar"
    }
]

def parse_shortcut_keys(shortcut_str: str):
    """Parses a shortcut string into a list of virtual key codes."""
    parts = [p.strip().lower() for p in shortcut_str.split("+")]
    codes = []
    for p in parts:
        if p in VK_MAP:
            codes.append(VK_MAP[p])
        elif len(p) == 1 and p.isalnum():
            codes.append(ord(p.upper()))
        elif p.startswith("f") and p[1:].isdigit():
            f_num = int(p[1:])
            if 1 <= f_num <= 24:
                codes.append(0x6F + f_num)
    return codes

def execute_shortcut(shortcut_str: str):
    """
    Simulates a Windows shortcut key combination using keybd_event.
    Handles special cases like win+l (LockWorkStation).
    """
    clean_str = shortcut_str.strip().lower()

    # Special case: Lock workstation
    if clean_str in ("win+l", "lock"):
        try:
            ctypes.windll.user32.LockWorkStation()
            return {"success": True, "summary": "Workstation Locked"}
        except Exception as e:
            return {"success": False, "summary": f"Failed to lock: {e}"}

    codes = parse_shortcut_keys(clean_str)
    if not codes:
        return {"success": False, "summary": f"Unrecognized shortcut: {shortcut_str}"}

    KEYEVENTF_KEYUP = 0x0002
    try:
        # Give a split-second pause so window focus transfers to target app
        time.sleep(0.08)

        # Press keys down in order
        for vk in codes:
            ctypes.windll.user32.keybd_event(vk, 0, 0, 0)
            time.sleep(0.01)

        # Release keys in reverse order
        for vk in reversed(codes):
            ctypes.windll.user32.keybd_event(vk, 0, KEYEVENTF_KEYUP, 0)
            time.sleep(0.01)

        return {"success": True, "summary": f"Executed shortcut: {shortcut_str.upper()}"}
    except Exception as e:
        logging.error(f"Error simulating shortcut {shortcut_str}: {e}")
        return {"success": False, "summary": f"Error: {e}"}
