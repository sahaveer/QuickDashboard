import ctypes
import time
import logging

def minimize_all_windows():
    """Minimizes all windows to desktop using Windows Shell automation."""
    try:
        # Simulate Win + D keypress
        VK_LWIN = 0x5B
        VK_D = 0x44
        KEYEVENTF_KEYUP = 0x0002

        ctypes.windll.user32.keybd_event(VK_LWIN, 0, 0, 0)
        ctypes.windll.user32.keybd_event(VK_D, 0, 0, 0)
        time.sleep(0.05)
        ctypes.windll.user32.keybd_event(VK_D, 0, KEYEVENTF_KEYUP, 0)
        ctypes.windll.user32.keybd_event(VK_LWIN, 0, KEYEVENTF_KEYUP, 0)
        return True
    except Exception as e:
        logging.error(f"Failed to minimize windows: {e}")
        return False

def mute_system_audio():
    """Toggles master volume mute using VK_VOLUME_MUTE."""
    try:
        VK_VOLUME_MUTE = 0xAD
        KEYEVENTF_KEYUP = 0x0002
        ctypes.windll.user32.keybd_event(VK_VOLUME_MUTE, 0, 0, 0)
        ctypes.windll.user32.keybd_event(VK_VOLUME_MUTE, 0, KEYEVENTF_KEYUP, 0)
        return True
    except Exception as e:
        logging.error(f"Failed to mute audio: {e}")
        return False

def lock_workstation():
    """Instantly locks the Windows workstation."""
    try:
        return ctypes.windll.user32.LockWorkStation() != 0
    except Exception as e:
        logging.error(f"Failed to lock workstation: {e}")
        return False

def activate_privacy_shield(lock_screen=False):
    """
    Executes Executive Privacy Shield:
    1. Minimizes all open desktop windows
    2. Mutes system audio
    3. Locks workstation if requested
    """
    min_ok = minimize_all_windows()
    mute_ok = mute_system_audio()
    if lock_screen:
        lock_workstation()
        return "Workstation Locked & Audio Muted"

    return "Privacy Shield Active: Windows Minimized & Audio Muted"
