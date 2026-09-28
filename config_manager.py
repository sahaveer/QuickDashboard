import os
import sys
import json
import logging

def get_base_dir():
    if getattr(sys, 'frozen', False):
        return os.path.dirname(sys.executable)
    return os.path.dirname(os.path.abspath(__file__))

CONFIG_FILE = os.path.join(get_base_dir(), "config.json")

DEFAULT_CONFIG = {
    "app": {
        "title": "Piano Deck - Senior Officers Dashboard",
        "always_on_top": True,
        "sound_enabled": True,
        "sound_volume": 100,
        "dock_height": 165,
        "is_collapsed": False,
        "theme": "executive_gold"
    },
    "telegram": {
        "bot_token": "",
        "chat_id": "",
        "auto_send": True
    },
    "whatsapp": {
        "default_phone": "",
        "default_message": "Snapshot shared from Senior Officer Dashboard"
    },
    "workspace": {
        "urls": [
            "https://finance.yahoo.com",
            "https://news.google.com"
        ],
        "apps": [
            "calc.exe",
            "notepad.exe"
        ]
    },
    "autologin": {
        "portal_name": "Executive Portal",
        "url": "https://google.com",
        "username": "executive.officer@domain.com",
        "password": "",
        "auto_copy_password": True
    },
    "music": {
        "active_index": 0,
        "stations": [
            {
                "title": "Executive Focus Lofi",
                "type": "web",
                "url": "https://www.youtube.com/watch?v=jfKfPfyJRdk"
            },
            {
                "title": "Classical Masterpieces (Chopin & Mozart)",
                "type": "web",
                "url": "https://www.youtube.com/watch?v=4Tr0ovkx_-8"
            },
            {
                "title": "Deep Work Ambient Flow",
                "type": "web",
                "url": "https://www.youtube.com/watch?v=WPni755-Krg"
            },
            {
                "title": "Gentle Nature & Rain Meditation",
                "type": "web",
                "url": "https://www.youtube.com/watch?v=mPZkdNFkNps"
            }
        ]
    },
    "keys": [
        {
            "id": "key_clean",
            "note": 60,
            "note_name": "C4",
            "title": "PURGE & CLEAN",
            "subtitle": "Recycle Bin & Temp Cache",
            "icon": "🧹",
            "action": "clean_system",
            "badge": "1-Click"
        },
        {
            "id": "key_snap",
            "note": 62,
            "note_name": "D4",
            "title": "SNAPSHOT",
            "subtitle": "Save Image & Copy to Clip",
            "icon": "📸",
            "action": "screenshot_titled",
            "badge": "Smart Snap"
        },
        {
            "id": "key_approval",
            "note": 64,
            "note_name": "E4",
            "title": "OFFICER APPROVAL",
            "subtitle": "Copy / Paste Official Memo",
            "icon": "📋",
            "action": "paste_text",
            "badge": "Snippet",
            "text": "Approved. Please process as per official policy and record in the minutes.",
            "auto_paste": True
        }
    ]
}

class ConfigManager:
    """Manages application configuration, reading and writing to config.json."""
    def __init__(self, file_path=CONFIG_FILE):
        self.file_path = file_path
        self.config = self.load()

    def load(self):
        if not os.path.exists(self.file_path):
            self.save(DEFAULT_CONFIG)
            return DEFAULT_CONFIG.copy()
        try:
            with open(self.file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                # Merge missing keys from DEFAULT_CONFIG
                for k, v in DEFAULT_CONFIG.items():
                    if k not in data:
                        data[k] = v
                    elif isinstance(v, dict) and isinstance(data[k], dict):
                        for sub_k, sub_v in v.items():
                            if sub_k not in data[k]:
                                data[k][sub_k] = sub_v
                return data
        except Exception as e:
            logging.error(f"Error loading config: {e}. Reverting to defaults.")
            return DEFAULT_CONFIG.copy()

    def save(self, data=None):
        if data is not None:
            self.config = data
        try:
            with open(self.file_path, "w", encoding="utf-8") as f:
                json.dump(self.config, f, indent=4, ensure_ascii=False)
            return True
        except Exception as e:
            logging.error(f"Error saving config: {e}")
            return False

    def get(self, key, default=None):
        return self.config.get(key, default)

    def set(self, key, value):
        self.config[key] = value
        self.save()
