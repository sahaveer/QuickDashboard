import time
import ctypes
import logging
import win32clipboard

def set_clipboard_text(text: str, max_retries=5):
    """Places text into Windows Clipboard with retry logic if clipboard is temporarily locked."""
    for _ in range(max_retries):
        try:
            win32clipboard.OpenClipboard()
            win32clipboard.EmptyClipboard()
            win32clipboard.SetClipboardText(text, win32clipboard.CF_UNICODETEXT)
            win32clipboard.CloseClipboard()
            return True
        except Exception:
            time.sleep(0.06)
    logging.error("Failed to acquire Windows clipboard after retries.")
    return False

def execute_text_snippet(text: str, auto_paste: bool = False):
    """
    Copies text to clipboard and optionally simulates Ctrl+V to paste
    directly into the currently active application (Word, Email, Browser, Chat).
    """
    if not text:
        return {"success": False, "summary": "No text configured for this key."}

    ok = set_clipboard_text(text)
    if not ok:
        return {"success": False, "summary": "Failed to set clipboard text."}

    preview = text if len(text) <= 30 else text[:27] + "..."

    if auto_paste:
        # Brief pause to allow active application focus
        time.sleep(0.08)
        try:
            VK_CONTROL = 0x11
            VK_V = 0x56
            KEYEVENTF_KEYUP = 0x0002

            ctypes.windll.user32.keybd_event(VK_CONTROL, 0, 0, 0)
            ctypes.windll.user32.keybd_event(VK_V, 0, 0, 0)
            ctypes.windll.user32.keybd_event(VK_V, 0, KEYEVENTF_KEYUP, 0)
            ctypes.windll.user32.keybd_event(VK_CONTROL, 0, KEYEVENTF_KEYUP, 0)
            return {"success": True, "summary": f"Pasted: \"{preview}\""}
        except Exception as e:
            logging.error(f"Auto-paste error: {e}")

    return {"success": True, "summary": f"Copied to clipboard: \"{preview}\""}
