import os
import json
import logging

PROFILES_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "profiles.json")

DEFAULT_PROFILES = {
    "active_profile_id": "senior_officer",
    "profiles": {
        "senior_officer": {
            "name": "Senior Officer",
            "icon": "👤",
            "role": "Chief / Executive",
            "keys": [
                {
                    "id": "key_clean",
                    "note": 60,
                    "note_name": "C4",
                    "title": "PURGE & CLEAN",
                    "subtitle": "Recycle Bin & Cache",
                    "icon": "🧹",
                    "action": "clean_system",
                    "badge": "1-Click"
                },
                {
                    "id": "key_snap",
                    "note": 62,
                    "note_name": "D4",
                    "title": "SNAPSHOT",
                    "subtitle": "Smart Snip & Save",
                    "icon": "📸",
                    "action": "screenshot_titled",
                    "badge": "Smart Snap"
                },
                {
                    "id": "key_approval",
                    "note": 64,
                    "note_name": "E4",
                    "title": "OFFICER APPROVAL",
                    "subtitle": "Official Memo",
                    "icon": "📋",
                    "action": "paste_text",
                    "badge": "Snippet",
                    "text": "Approved. Please process as per official policy and record in the minutes.",
                    "auto_paste": True
                },
                {
                    "id": "key_privacy",
                    "note": 65,
                    "note_name": "F4",
                    "title": "PRIVACY SHIELD",
                    "subtitle": "Boss Key & Mute",
                    "icon": "🛡️",
                    "action": "privacy_shield",
                    "badge": "Boss Key"
                }
            ]
        },
        "finance_officer": {
            "name": "Finance & Accounts",
            "icon": "💼",
            "role": "Financial Management",
            "keys": [
                {
                    "id": "key_excel_kill",
                    "note": 60,
                    "note_name": "C4",
                    "title": "KILL EXCEL",
                    "subtitle": "Unfreeze Spreadsheets",
                    "icon": "⚡",
                    "action": "kill_tasks",
                    "badge": "Rescue",
                    "text": "excel.exe"
                },
                {
                    "id": "key_snip_fin",
                    "note": 62,
                    "note_name": "D4",
                    "title": "SNIP AUDIT",
                    "subtitle": "Area Snipping Tool",
                    "icon": "✂️",
                    "action": "screenshot_titled",
                    "badge": "Area Snip"
                },
                {
                    "id": "key_payment_approved",
                    "note": 64,
                    "note_name": "E4",
                    "title": "PAYMENT OK",
                    "subtitle": "Disbursement Memo",
                    "icon": "💰",
                    "action": "paste_text",
                    "badge": "Snippet",
                    "text": "Invoice calculations and supporting vouchers verified. Approved for disbursement.",
                    "auto_paste": True
                },
                {
                    "id": "key_portal",
                    "note": 65,
                    "note_name": "F4",
                    "title": "ERP PORTAL",
                    "subtitle": "Finance Dashboard",
                    "icon": "🌐",
                    "action": "custom_url",
                    "badge": "Web Link",
                    "text": "https://finance.yahoo.com"
                }
            ]
        },
        "executive_assistant": {
            "name": "Executive Assistant",
            "icon": "👔",
            "role": "Secretariat / PA",
            "keys": [
                {
                    "id": "key_agenda",
                    "note": 60,
                    "note_name": "C4",
                    "title": "MEETING AGENDA",
                    "subtitle": "Insert Meeting Header",
                    "icon": "📅",
                    "action": "paste_text",
                    "badge": "Snippet",
                    "text": "MEETING DOSSIER\nDate: [Date]\nAttendees: [Names]\nAgenda: 1. Review 2. Decisions 3. Next Steps",
                    "auto_paste": True
                },
                {
                    "id": "key_dispatch",
                    "note": 62,
                    "note_name": "D4",
                    "title": "DISPATCH",
                    "subtitle": "WhatsApp / TG Share",
                    "icon": "📤",
                    "action": "dispatch_screenshot",
                    "badge": "Direct Share"
                },
                {
                    "id": "key_clip_hist",
                    "note": 64,
                    "note_name": "E4",
                    "title": "CLIPBOARD HIST",
                    "subtitle": "View Past Copies",
                    "icon": "📋",
                    "action": "shortcut",
                    "badge": "Win+V",
                    "text": "win+v"
                },
                {
                    "id": "key_clean",
                    "note": 65,
                    "note_name": "F4",
                    "title": "PURGE CACHE",
                    "subtitle": "Clean Temp Files",
                    "icon": "🧹",
                    "action": "clean_system",
                    "badge": "1-Click"
                }
            ]
        },
        "legal_compliance": {
            "name": "Legal & Compliance",
            "icon": "⚖️",
            "role": "Legal Advisory",
            "keys": [
                {
                    "id": "key_legal_vetted",
                    "note": 60,
                    "note_name": "C4",
                    "title": "LEGAL VETTING",
                    "subtitle": "Compliance Clause",
                    "icon": "⚖️",
                    "action": "paste_text",
                    "badge": "Snippet",
                    "text": "Reviewed and legally vetted. In full compliance with regulatory statutory mandates.",
                    "auto_paste": True
                },
                {
                    "id": "key_lock",
                    "note": 62,
                    "note_name": "D4",
                    "title": "LOCK PC",
                    "subtitle": "Confidentiality Lock",
                    "icon": "🔒",
                    "action": "shortcut",
                    "badge": "Win+L",
                    "text": "win+l"
                },
                {
                    "id": "key_snip",
                    "note": 64,
                    "note_name": "E4",
                    "title": "SNIP CLAUSE",
                    "subtitle": "Capture Contract Text",
                    "icon": "✂️",
                    "action": "screenshot_titled",
                    "badge": "Area Snip"
                }
            ]
        }
    }
}

class ProfileManager:
    """Manages multi-user profiles, independent button configurations, and switching."""
    def __init__(self, file_path=PROFILES_FILE):
        self.file_path = file_path
        self.data = self.load()

    def load(self):
        if not os.path.exists(self.file_path):
            self.save(DEFAULT_PROFILES)
            return DEFAULT_PROFILES.copy()
        try:
            with open(self.file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                if "profiles" not in data or not data["profiles"]:
                    return DEFAULT_PROFILES.copy()
                return data
        except Exception as e:
            logging.error(f"Error loading profiles: {e}")
            return DEFAULT_PROFILES.copy()

    def save(self, data=None):
        if data is not None:
            self.data = data
        try:
            with open(self.file_path, "w", encoding="utf-8") as f:
                json.dump(self.data, f, indent=4, ensure_ascii=False)
            return True
        except Exception as e:
            logging.error(f"Error saving profiles: {e}")
            return False

    def get_active_profile_id(self):
        return self.data.get("active_profile_id", "senior_officer")

    def get_active_profile(self):
        p_id = self.get_active_profile_id()
        profiles = self.data.get("profiles", {})
        if p_id in profiles:
            return profiles[p_id]
        first_id = next(iter(profiles))
        self.data["active_profile_id"] = first_id
        return profiles[first_id]

    def set_active_profile(self, profile_id):
        if profile_id in self.data.get("profiles", {}):
            self.data["active_profile_id"] = profile_id
            self.save()
            return True
        return False

    def get_all_profiles(self):
        """Returns list of (profile_id, profile_dict)."""
        return list(self.data.get("profiles", {}).items())

    def add_profile(self, name: str, icon: str = "👤", copy_from_id: str = None):
        """Creates a new profile with custom name."""
        clean_id = name.lower().replace(" ", "_").replace("&", "and")
        base_id = clean_id
        counter = 1
        while clean_id in self.data["profiles"]:
            clean_id = f"{base_id}_{counter}"
            counter += 1

        if copy_from_id and copy_from_id in self.data["profiles"]:
            keys = [dict(k) for k in self.data["profiles"][copy_from_id]["keys"]]
        else:
            keys = [
                {
                    "id": "key_clean",
                    "note": 60,
                    "note_name": "C4",
                    "title": "PURGE & CLEAN",
                    "subtitle": "Recycle Bin & Cache",
                    "icon": "🧹",
                    "action": "clean_system",
                    "badge": "1-Click"
                },
                {
                    "id": "key_snap",
                    "note": 62,
                    "note_name": "D4",
                    "title": "SNAPSHOT",
                    "subtitle": "Smart Snip & Save",
                    "icon": "📸",
                    "action": "screenshot_titled",
                    "badge": "Smart Snap"
                },
                {
                    "id": "key_snip",
                    "note": 64,
                    "note_name": "E4",
                    "title": f"{name.upper()} NOTE",
                    "subtitle": "Quick Text Snippet",
                    "icon": "📋",
                    "action": "paste_text",
                    "badge": "Snippet",
                    "text": f"Approved by {name}.",
                    "auto_paste": True
                }
            ]

        self.data["profiles"][clean_id] = {
            "name": name,
            "icon": icon,
            "role": "Custom Profile",
            "keys": keys
        }
        self.data["active_profile_id"] = clean_id
        self.save()
        return clean_id

    def delete_profile(self, profile_id):
        if len(self.data.get("profiles", {})) <= 1:
            return False  # Do not delete the last remaining profile
        if profile_id in self.data["profiles"]:
            del self.data["profiles"][profile_id]
            if self.data["active_profile_id"] == profile_id:
                self.data["active_profile_id"] = next(iter(self.data["profiles"]))
            self.save()
            return True
        return False

    def update_keys_for_active_profile(self, keys_list):
        p_id = self.get_active_profile_id()
        if p_id in self.data["profiles"]:
            self.data["profiles"][p_id]["keys"] = keys_list
            self.save()
            return True
        return False
