import os
import time
import webbrowser
import threading
import logging
import win32clipboard

def set_clipboard_text(text: str):
    """Places text onto Windows Clipboard."""
    try:
        win32clipboard.OpenClipboard()
        win32clipboard.EmptyClipboard()
        win32clipboard.SetClipboardText(text, win32clipboard.CF_UNICODETEXT)
        win32clipboard.CloseClipboard()
        return True
    except Exception as e:
        logging.error(f"Failed to copy text to clipboard: {e}")
        return False

def open_and_autofill(url: str, username: str = "", password: str = "", use_selenium: bool = False, callback=None):
    """
    Launches the configured portal.
    If use_selenium is True and selenium is available, attempts automated login.
    Otherwise, opens default browser and copies password to clipboard for 1-click paste.
    """
    def _worker():
        if not url:
            if callback:
                callback({"success": False, "summary": "Portal URL is not configured. Set in Settings."})
            return

        target_url = url.strip()
        if not target_url.startswith("http://") and not target_url.startswith("https://"):
            target_url = "https://" + target_url

        if use_selenium:
            try:
                from selenium import webdriver
                from selenium.webdriver.common.by import By
                from selenium.webdriver.support.ui import WebDriverWait
                from selenium.webdriver.support import expected_conditions as EC

                driver = webdriver.Chrome()
                driver.get(target_url)

                # Attempt to find common username / email inputs
                user_selectors = ["input[type='email']", "input[type='text']", "#username", "#user", "#email", "[name='username']", "[name='email']"]
                pass_selectors = ["input[type='password']", "#password", "#pass", "[name='password']"]

                # Wait briefly for page to load
                wait = WebDriverWait(driver, 5)
                for sel in user_selectors:
                    try:
                        elem = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, sel)))
                        if elem and username:
                            elem.clear()
                            elem.send_keys(username)
                            break
                    except Exception:
                        pass

                for sel in pass_selectors:
                    try:
                        elem = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, sel)))
                        if elem and password:
                            elem.clear()
                            elem.send_keys(password)
                            break
                    except Exception:
                        pass

                summary = f"Automated portal launched: {target_url}"
                if callback:
                    callback({"success": True, "summary": summary})
                return
            except Exception as e:
                logging.warning(f"Selenium autofill encountered issue ({e}), falling back to native browser launch.")

        # Native launch mode
        try:
            webbrowser.open_new_tab(target_url)
            # If password provided, copy to clipboard for convenience
            if password:
                set_clipboard_text(password)
                summary = f"Opened {target_url} • Password copied to clipboard"
            elif username:
                set_clipboard_text(username)
                summary = f"Opened {target_url} • Username copied to clipboard"
            else:
                summary = f"Opened {target_url}"

            if callback:
                callback({"success": True, "summary": summary})
        except Exception as e:
            logging.error(f"Failed to open portal: {e}")
            if callback:
                callback({"success": False, "summary": f"Failed to open portal: {e}"})

    t = threading.Thread(target=_worker, daemon=True)
    t.start()
    return t
