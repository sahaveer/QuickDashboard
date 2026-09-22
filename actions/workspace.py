import os
import time
import subprocess
import webbrowser
import threading
import logging

def launch_workspace_bundle(urls: list, apps: list, callback=None):
    """
    Asynchronously launches a set of URLs and desktop applications.
    Calls optional callback(summary_dict) upon completion.
    """
    def _worker():
        opened_urls = 0
        opened_apps = 0
        errors = []

        # 1. Open Web Portals
        for url in urls:
            url_str = url.strip()
            if url_str:
                try:
                    if not url_str.startswith("http://") and not url_str.startswith("https://"):
                        url_str = "https://" + url_str
                    webbrowser.open_new_tab(url_str)
                    opened_urls += 1
                    time.sleep(0.2)
                except Exception as e:
                    logging.error(f"Failed to open URL {url_str}: {e}")
                    errors.append(f"URL: {url_str}")

        # 2. Launch Desktop Programs
        for app in apps:
            app_str = app.strip()
            if app_str:
                try:
                    # subprocess.Popen without blocking
                    subprocess.Popen(app_str, shell=True)
                    opened_apps += 1
                    time.sleep(0.3)
                except Exception as e:
                    logging.error(f"Failed to launch app {app_str}: {e}")
                    errors.append(f"App: {app_str}")

        summary = f"Opened {opened_urls} portal{'s' if opened_urls != 1 else ''} & {opened_apps} app{'s' if opened_apps != 1 else ''}"
        if errors:
            summary += f" ({len(errors)} failed)"

        res = {
            "success": True,
            "opened_urls": opened_urls,
            "opened_apps": opened_apps,
            "summary": summary
        }

        if callback:
            callback(res)
        return res

    t = threading.Thread(target=_worker, daemon=True)
    t.start()
    return t
