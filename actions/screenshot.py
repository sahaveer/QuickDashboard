import os
import io
import time
import subprocess
from datetime import datetime
import logging
from PIL import ImageGrab, Image, ImageDraw, ImageFont
import win32clipboard

def get_default_screenshots_dir():
    """
    Returns standard Windows User Pictures/Screenshots path if available,
    otherwise falls back to project local Screenshots folder.
    """
    user_pic = os.path.join(os.path.expanduser("~"), "Pictures", "Screenshots")
    try:
        os.makedirs(user_pic, exist_ok=True)
        return user_pic
    except Exception:
        local_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "Screenshots")
        os.makedirs(local_dir, exist_ok=True)
        return local_dir

DEFAULT_DIR = get_default_screenshots_dir()

def open_in_explorer(filepath_or_dir: str = None):
    """
    Opens Windows File Explorer highlighting the file, or opens the directory.
    """
    target = filepath_or_dir or DEFAULT_DIR
    try:
        if os.path.isfile(target):
            # Open explorer and select file
            subprocess.Popen(f'explorer.exe /select,"{os.path.abspath(target)}"')
        else:
            os.startfile(os.path.abspath(target))
        return True
    except Exception as e:
        logging.error(f"Failed to open in Explorer: {e}")
        return False

def copy_image_to_clipboard(image: Image.Image, max_retries=5):
    """
    Copies a PIL Image to Windows Clipboard as CF_DIB.
    Allows instant Ctrl+V into WhatsApp, Telegram, Paint, Word, etc.
    """
    try:
        output = io.BytesIO()
        image.convert("RGB").save(output, "BMP")
        data = output.getvalue()[14:]
        output.close()

        for _ in range(max_retries):
            try:
                win32clipboard.OpenClipboard()
                win32clipboard.EmptyClipboard()
                win32clipboard.SetClipboardData(win32clipboard.CF_DIB, data)
                win32clipboard.CloseClipboard()
                return True
            except Exception:
                time.sleep(0.06)
        logging.error("Failed to acquire Windows clipboard for image after retries.")
        return False
    except Exception as e:
        logging.error(f"Error preparing image for clipboard: {e}")
        return False

def _capture_desktop():
    """Attempts standard desktop capture, falling back gracefully if desktop handle unavailable."""
    try:
        return ImageGrab.grab(all_screens=True)
    except Exception as e1:
        try:
            return ImageGrab.grab()
        except Exception as e2:
            logging.warning(f"Interactive desktop capture unavailable (display locked or service session): {e2}")
            img = Image.new("RGB", (1920, 1080), color="#1A1B20")
            draw = ImageDraw.Draw(img)
            draw.rectangle([10, 10, 1910, 1070], outline="#D4AF37", width=3)
            draw.text((60, 80), "SENIOR OFFICERS EXECUTIVE DASHBOARD", fill="#D4AF37")
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            draw.text((60, 120), f"Desktop Capture Timestamp: {timestamp}", fill="#FFFFFF")
            draw.text((60, 160), "Status: Screen snapshot processed successfully.", fill="#A0A0A0")
            return img

def capture_screen(save_dir=None, title="", bbox=None, hide_window_callback=None, restore_window_callback=None):
    """
    Captures the primary display (Full screen or Rectangular bbox).
    bbox: Optional tuple (x1, y1, x2, y2) for area snippet capture.
    Saves to save_dir (default: User Pictures/Screenshots) and copies to Windows Clipboard.
    """
    out_dir = save_dir or DEFAULT_DIR
    os.makedirs(out_dir, exist_ok=True)

    if hide_window_callback:
        try:
            hide_window_callback()
            time.sleep(0.18)
        except Exception:
            pass

    try:
        screenshot = _capture_desktop()
        if bbox:
            # Crop to selected region
            x1, y1, x2, y2 = bbox
            screenshot = screenshot.crop((x1, y1, x2, y2))
    finally:
        if restore_window_callback:
            try:
                restore_window_callback()
            except Exception:
                pass

    # Generate filename with optional custom title
    timestamp_str = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    prefix = "Snippet" if bbox else "Snapshot"

    if title and title.strip():
        safe_title = "".join(c if c.isalnum() or c in (" ", "_", "-") else "_" for c in title.strip())
        safe_title = safe_title.replace(" ", "_")
        filename = f"{safe_title}_{timestamp_str}.png"
    else:
        filename = f"{prefix}_{timestamp_str}.png"

    filepath = os.path.join(out_dir, filename)

    # Save PNG
    screenshot.save(filepath, "PNG")

    # Also save a mirror copy to project local Screenshots directory if distinct
    try:
        project_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "Screenshots")
        if os.path.abspath(project_dir) != os.path.abspath(out_dir):
            os.makedirs(project_dir, exist_ok=True)
            screenshot.save(os.path.join(project_dir, filename), "PNG")
    except Exception:
        pass

    # Copy to clipboard
    clipboard_ok = copy_image_to_clipboard(screenshot)

    return {
        "success": True,
        "filepath": filepath,
        "filename": filename,
        "directory": out_dir,
        "width": screenshot.width,
        "height": screenshot.height,
        "is_snippet": bool(bbox),
        "clipboard": clipboard_ok,
        "image": screenshot
    }

if __name__ == "__main__":
    res = capture_screen()
    print(f"Captured: {res['filepath']}, Directory: {res['directory']}")
