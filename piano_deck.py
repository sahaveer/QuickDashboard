import os
import ctypes
from ctypes import wintypes
import tkinter as tk
from tkinter import font as tkfont, messagebox
import threading
import logging
import webbrowser

from config_manager import ConfigManager
from audio_engine import AudioEngine
from ui.toast import ToastManager
from ui.settings_dialog import SettingsDialog
from ui.add_key_dialog import AddKeyDialog
from ui.title_prompt import TitlePromptDialog
from ui.snipper import SnippingOverlay
from ui.saved_popup import SavedNotificationWindow

# Action imports
from actions.cleaner import run_system_cleanup
from actions.screenshot import capture_screen, open_in_explorer
from actions.dispatcher import execute_snap_and_dispatch
from actions.workspace import launch_workspace_bundle
from actions.autologin import open_and_autofill
from actions.music_player import MusicPlayer
from actions.privacy import activate_privacy_shield
from actions.snippet import execute_text_snippet
from actions.process_killer import kill_hung_processes
from actions.shortcuts import execute_shortcut

class PianoKey(tk.Canvas):
    """
    Realistic Grand Piano Ivory Key with 3D tactile action,
    hover highlights, mechanical depression, right-click context menu,
    and gold typography.
    """
    def __init__(self, parent, key_config, on_press=None, width=135, height=135, is_add_key=False, key_index=None):
        super().__init__(parent, width=width, height=height, bg="#121316", highlightthickness=0, cursor="hand2")
        self.cfg = key_config
        self.on_press = on_press
        self.is_add_key = is_add_key
        self.key_index = key_index
        self.w = width
        self.h = height
        self.is_pressed = False
        self.is_hovered = False

        self.bind("<Enter>", self._on_enter)
        self.bind("<Leave>", self._on_leave)
        self.bind("<Button-1>", self._on_button_down)
        self.bind("<ButtonRelease-1>", self._on_button_up)
        self.bind("<Button-3>", self._on_right_click)
        self.bind("<Configure>", self._on_resize)

        self.draw_key()

    def _on_resize(self, event):
        if event.width > 30 and event.height > 30:
            if event.width != self.w or event.height != self.h:
                self.w = event.width
                self.h = event.height
                self.draw_key()

    def _on_right_click(self, event):
        top = self.winfo_toplevel()
        if self.is_add_key:
            if hasattr(top, "open_add_key_dialog"):
                top.open_add_key_dialog()
            return

        # Context Menu for configuring / editing / deleting the key
        menu = tk.Menu(self, tearoff=0, bg="#202126", fg="#FFFFFF", activebackground="#D4AF37", activeforeground="#121212", font=("Segoe UI", 9))
        menu.add_command(label="✏️  Edit Key / Text Snippet", command=lambda: top.open_edit_key_dialog(self.key_index))
        menu.add_command(label="🗑️  Delete This Key", command=lambda: top.delete_key(self.key_index))
        menu.add_separator()
        menu.add_command(label="➕  Add New Key", command=lambda: top.open_add_key_dialog())
        menu.add_command(label="⚙️  Executive Settings", command=lambda: top.open_settings())

        try:
            menu.tk_popup(event.x_root, event.y_root)
        finally:
            menu.grab_release()

    def draw_key(self):
        self.delete("all")
        y_offset = 4 if self.is_pressed else 0

        if self.is_add_key:
            # Styled Add Key (Ebony / Brass accents)
            if self.is_pressed:
                fill_top = "#32353E"
                fill_bottom = "#22242B"
                border_color = "#E5C158"
                accent_gold = "#E5C158"
                title_color = "#FFF"
                sub_color = "#C5C7D0"
            elif self.is_hovered:
                fill_top = "#2A2C34"
                fill_bottom = "#1E2026"
                border_color = "#D4AF37"
                accent_gold = "#D4AF37"
                title_color = "#FFFFFF"
                sub_color = "#AAAAAA"
            else:
                fill_top = "#222329"
                fill_bottom = "#1A1B20"
                border_color = "#7A6321"
                accent_gold = "#D4AF37"
                title_color = "#E0E0E0"
                sub_color = "#8A8D98"
        else:
            # Classic Ivory Key
            if self.is_pressed:
                fill_top = "#E2D8C3"
                fill_bottom = "#C5BAA3"
                border_color = "#B58E29"
                accent_gold = "#8C6D1F"
                title_color = "#111111"
                sub_color = "#333333"
            elif self.is_hovered:
                fill_top = "#FFFFFF"
                fill_bottom = "#F6F4EB"
                border_color = "#E5C158"
                accent_gold = "#B58E29"
                title_color = "#181818"
                sub_color = "#444444"
            else:
                fill_top = "#FCFAF2"
                fill_bottom = "#EFECE1"
                border_color = "#D6CEB8"
                accent_gold = "#A38020"
                title_color = "#202124"
                sub_color = "#5F6368"

        # 3D Drop shadow under the key
        self.create_rectangle(3, 4 + y_offset, self.w - 3, self.h - 1, fill="#0B0B0D", outline="")

        # Main Key Body
        r = 5
        x1, y1, x2, y2 = 4, 2 + y_offset, self.w - 4, self.h - 5 + y_offset

        self._round_rect(x1, y1, x2, y2, radius=r, fill=fill_bottom, outline=border_color, width=1)
        self.create_rectangle(x1 + 1, y1 + 1, x2 - 1, y1 + (self.h * 0.45), fill=fill_top, outline="")

        # Top Note marker
        note_text = self.cfg.get("note_name", "")
        self.create_text(x1 + 10, y1 + 12, text=note_text, font=("Georgia", 8, "bold"), fill=accent_gold, anchor="w")

        # Top brass hinge line
        self.create_line(x1 + 30, y1 + 12, x2 - 8, y1 + 12, fill="#735C1D" if self.is_add_key else "#E6D3A3", width=1)

        # Action Icon
        icon_text = self.cfg.get("icon", "🎹")
        icon_font_size = 22 if self.is_add_key else 20
        self.create_text(self.w / 2, y1 + 42, text=icon_text, font=("Segoe UI Emoji", icon_font_size), anchor="center")

        # Action Title
        title_text = self.cfg.get("title", "")
        self.create_text(self.w / 2, y1 + 72, text=title_text, font=("Segoe UI", 9, "bold"), fill=title_color, anchor="center")

        # Action Subtitle
        sub_text = self.cfg.get("subtitle", "")
        if len(sub_text) > 22:
            sub_text = sub_text[:20] + ".."
        self.create_text(self.w / 2, y1 + 90, text=sub_text, font=("Segoe UI", 7), fill=sub_color, anchor="center")

        # Bottom Badge
        badge_text = self.cfg.get("badge", "")
        if self.is_add_key:
            badge_bg = "#2E303A" if not self.is_pressed else "#D4AF37"
            badge_fg = "#D4AF37" if not self.is_pressed else "#121212"
            badge_border = "#7A6321"
        else:
            badge_bg = "#E0D7BE" if not self.is_pressed else "#D4AF37"
            badge_fg = "#5A4913" if not self.is_pressed else "#FFFFFF"
            badge_border = "#C4B89A"

        bx1, by1 = self.w / 2 - 42, y1 + 104
        bx2, by2 = self.w / 2 + 42, y1 + 120
        self._round_rect(bx1, by1, bx2, by2, radius=4, fill=badge_bg, outline=badge_border, width=1)
        self.create_text(self.w / 2, (by1 + by2) / 2, text=badge_text, font=("Segoe UI", 7, "bold"), fill=badge_fg, anchor="center")

    def _round_rect(self, x1, y1, x2, y2, radius=6, **kwargs):
        points = [
            x1 + radius, y1,
            x2 - radius, y1,
            x2, y1,
            x2, y1 + radius,
            x2, y2 - radius,
            x2, y2,
            x2 - radius, y2,
            x1 + radius, y2,
            x1, y2,
            x1, y2 - radius,
            x1, y1 + radius,
            x1, y1
        ]
        return self.create_polygon(points, smooth=True, **kwargs)

    def _on_enter(self, event):
        self.is_hovered = True
        self.draw_key()

    def _on_leave(self, event):
        self.is_hovered = False
        self.is_pressed = False
        self.draw_key()

    def _on_button_down(self, event):
        self.is_pressed = True
        self.draw_key()

    def _on_button_up(self, event):
        if self.is_pressed:
            self.is_pressed = False
            self.draw_key()
            if self.on_press:
                self.on_press(self.cfg)


class PianoDeckBar(tk.Tk):
    """
    Main Executive Dashboard Window.
    Docks above Windows Taskbar with full Grand Piano Deck aesthetics.
    """
    def __init__(self):
        super().__init__()
        self.cfg_mgr = ConfigManager()
        self.config = self.cfg_mgr.config
        self.audio = AudioEngine(enabled=self.config.get("app", {}).get("sound_enabled", True))
        self.music = MusicPlayer(stations=self.config.get("music", {}).get("stations", []))

        self.title("Senior Officers Executive Dashboard")
        self.overrideredirect(True)
        self.attributes("-topmost", self.config.get("app", {}).get("always_on_top", True))
        self.config_window()

        self.is_collapsed = False
        self._drag_start_x = 0
        self._drag_start_y = 0

        self._build_deck()
        self._dock_to_bottom()

    def config_window(self):
        self.configure(bg="#141518")
        try:
            ctypes.windll.shcore.SetProcessDpiAwareness(1)
        except Exception:
            pass

    def _get_workarea(self):
        rect = wintypes.RECT()
        ctypes.windll.user32.SystemParametersInfoW(0x0030, 0, ctypes.byref(rect), 0)
        return rect.left, rect.top, rect.right, rect.bottom

    def _dock_to_bottom(self):
        left, top, right, bottom = self._get_workarea()
        screen_w = right - left

        # Dynamic dock width based on key count
        key_count = len(self.config.get("keys", [])) + 1  # user keys + 1 add button
        desired_w = max(580, min(1280, key_count * 155 + 40))
        dock_w = min(desired_w, screen_w - 20)
        dock_h = 175 if not self.is_collapsed else 38

        x = left + (screen_w - dock_w) // 2
        y = bottom - dock_h

        self.geometry(f"{dock_w}x{dock_h}+{x}+{y}")

    def _build_deck(self):
        for widget in self.winfo_children():
            widget.destroy()

        self.outer_frame = tk.Frame(self, bg="#735C1D", bd=1)
        self.outer_frame.pack(fill="both", expand=True)

        self.deck_container = tk.Frame(self.outer_frame, bg="#16171B")
        self.deck_container.pack(fill="both", expand=True, padx=1, pady=1)

        # Top rail (Fallboard)
        self.rail = tk.Frame(self.deck_container, bg="#202126", height=32)
        self.rail.pack(fill="x", side="top")
        self.rail.pack_propagate(False)

        lbl_brand = tk.Label(self.rail, text="🎹  EXECUTIVE PIANO DECK", font=("Segoe UI", 9, "bold"), fg="#D4AF37", bg="#202126", cursor="fleur")
        lbl_brand.pack(side="left", padx=(14, 8))

        lbl_desc = tk.Label(self.rail, text="• Senior Officers Rapid Automation Suite", font=("Segoe UI", 8), fg="#8A8C94", bg="#202126", cursor="fleur")
        lbl_desc.pack(side="left")

        for w in (self.rail, lbl_brand, lbl_desc):
            w.bind("<Button-1>", self._start_drag)
            w.bind("<B1-Motion>", self._on_drag)

        btn_close = tk.Label(self.rail, text="✕", font=("Segoe UI", 9, "bold"), fg="#8E9099", bg="#202126", cursor="hand2", padx=10)
        btn_close.pack(side="right")
        btn_close.bind("<Button-1>", lambda e: self.quit_app())
        btn_close.bind("<Enter>", lambda e: btn_close.config(fg="#FF5252"))
        btn_close.bind("<Leave>", lambda e: btn_close.config(fg="#8E9099"))

        collapse_char = "▼ Fold" if not self.is_collapsed else "▲ Expand Piano"
        self.btn_fold = tk.Label(self.rail, text=collapse_char, font=("Segoe UI", 8, "bold"), fg="#D4AF37", bg="#202126", cursor="hand2", padx=8)
        self.btn_fold.pack(side="right", padx=6)
        self.btn_fold.bind("<Button-1>", lambda e: self.toggle_collapse())

        sound_icon = "🔊 Sound ON" if self.audio.enabled else "🔇 Sound OFF"
        self.btn_sound = tk.Label(self.rail, text=sound_icon, font=("Segoe UI", 8), fg="#BDBDBD", bg="#202126", cursor="hand2", padx=8)
        self.btn_sound.pack(side="right", padx=6)
        self.btn_sound.bind("<Button-1>", lambda e: self.toggle_sound())

        btn_add = tk.Label(self.rail, text="➕ Add Key", font=("Segoe UI", 8, "bold"), fg="#D4AF37", bg="#202126", cursor="hand2", padx=8)
        btn_add.pack(side="right", padx=6)
        btn_add.bind("<Button-1>", lambda e: self.open_add_key_dialog())

        btn_folder = tk.Label(self.rail, text="📂 Screenshots", font=("Segoe UI", 8), fg="#4ECA5D", bg="#202126", cursor="hand2", padx=6)
        btn_folder.pack(side="right", padx=4)
        btn_folder.bind("<Button-1>", lambda e: open_in_explorer())

        btn_cfg = tk.Label(self.rail, text="⚙ Settings", font=("Segoe UI", 8), fg="#BDBDBD", bg="#202126", cursor="hand2", padx=8)
        btn_cfg.pack(side="right", padx=6)
        btn_cfg.bind("<Button-1>", lambda e: self.open_settings())

        sep = tk.Frame(self.deck_container, bg="#A88B32", height=1)
        sep.pack(fill="x", side="top")

        if not self.is_collapsed:
            self.keys_rack = tk.Frame(self.deck_container, bg="#0E0F12", pady=4)
            self.keys_rack.pack(fill="both", expand=True)

            keys_data = self.config.get("keys", [])
            for idx, key_cfg in enumerate(keys_data):
                pkey = PianoKey(self.keys_rack, key_cfg, on_press=self.handle_key_press, width=140, height=132, key_index=idx)
                pkey.pack(side="left", fill="both", expand=True, padx=2)

            # Plus Piano Key Button on far right
            add_cfg = {
                "id": "key_add_btn",
                "note": 72,
                "note_name": "+",
                "title": "ADD KEY",
                "subtitle": "New Action / Text",
                "icon": "➕",
                "badge": "+ Add Key",
                "action": "open_add_dialog"
            }
            btn_add_key = PianoKey(self.keys_rack, add_cfg, on_press=lambda cfg: self.open_add_key_dialog(), width=130, height=132, is_add_key=True)
            btn_add_key.pack(side="left", fill="both", expand=True, padx=2)

    def _start_drag(self, event):
        self._drag_start_x = event.x
        self._drag_start_y = event.y

    def _on_drag(self, event):
        x = self.winfo_x() + (event.x - self._drag_start_x)
        y = self.winfo_y() + (event.y - self._drag_start_y)
        self.geometry(f"+{x}+{y}")

    def toggle_collapse(self):
        self.is_collapsed = not self.is_collapsed
        self._build_deck()
        self._dock_to_bottom()

    def toggle_sound(self):
        self.audio.enabled = not self.audio.enabled
        self.config["app"]["sound_enabled"] = self.audio.enabled
        self.cfg_mgr.save()
        sound_icon = "🔊 Sound ON" if self.audio.enabled else "🔇 Sound OFF"
        self.btn_sound.config(text=sound_icon)
        ToastManager.show(self, "Audio Synthesizer", f"Piano Acoustic Sound {'Enabled' if self.audio.enabled else 'Muted'}", icon="🎵")

    def open_settings(self):
        SettingsDialog(self, self.cfg_mgr, audio_engine=self.audio, on_saved=self._on_settings_saved)

    def _on_settings_saved(self):
        self.config = self.cfg_mgr.config
        self.attributes("-topmost", self.config.get("app", {}).get("always_on_top", True))
        self.audio.enabled = self.config.get("app", {}).get("sound_enabled", True)
        self.music.stations = self.config.get("music", {}).get("stations", [])
        self._build_deck()
        self._dock_to_bottom()
        ToastManager.show(self, "Settings Saved", "Executive Preferences updated successfully!", icon="✅")

    def open_add_key_dialog(self):
        next_idx = len(self.config.get("keys", []))
        AddKeyDialog(self, on_save=self._on_key_saved, key_index=next_idx)

    def open_edit_key_dialog(self, key_index):
        keys = self.config.get("keys", [])
        if 0 <= key_index < len(keys):
            AddKeyDialog(self, on_save=self._on_key_saved, existing_key=keys[key_index], key_index=key_index)

    def delete_key(self, key_index):
        keys = self.config.get("keys", [])
        if 0 <= key_index < len(keys):
            deleted = keys.pop(key_index)
            self.cfg_mgr.save(self.config)
            self._build_deck()
            self._dock_to_bottom()
            ToastManager.show(self, "Key Deleted", f"Removed key '{deleted.get('title')}'", icon="🗑️")

    def _on_key_saved(self, key_data, key_index):
        keys = self.config.get("keys", [])
        if key_index is not None and key_index < len(keys):
            keys[key_index] = key_data
            action_desc = "Updated"
        else:
            keys.append(key_data)
            action_desc = "Added"

        self.cfg_mgr.save(self.config)
        self._build_deck()
        self._dock_to_bottom()
        self.audio.play_chord([60, 64, 67, 72])
        ToastManager.show(self, f"Key {action_desc}", f"Piano Key '{key_data['title']}' is ready to use!", icon="🎹")

    def handle_key_press(self, key_cfg):
        note = key_cfg.get("note", 60)
        self.audio.play_note(note=note, velocity=105, duration=0.35)

        action = key_cfg.get("action", "")
        title = key_cfg.get("title", "")

        if action == "clean_system":
            self._action_clean()
        elif action in ("take_screenshot", "screenshot_instant", "screenshot_titled"):
            TitlePromptDialog(
                self,
                on_full_screen=lambda t: self._action_screenshot(title=t),
                on_area_snippet=lambda t: self._action_snippet_area(title=t)
            )
        elif action == "paste_text":
            self._action_snippet(key_cfg)
        elif action == "dispatch_screenshot":
            self._action_dispatch()
        elif action == "launch_workspace":
            self._action_workspace()
        elif action == "portal_login":
            self._action_autologin()
        elif action == "kill_tasks":
            self._action_kill_tasks(key_cfg)
        elif action == "custom_url":
            self._action_custom_url(key_cfg)
        elif action == "toggle_music":
            self._action_music()
        elif action == "privacy_shield":
            self._action_privacy()
        elif action == "shortcut":
            self._action_shortcut(key_cfg)
        elif action == "open_settings":
            self.open_settings()
        elif action == "open_add_dialog":
            self.open_add_key_dialog()
        else:
            ToastManager.show(self, title, f"Action '{action}' triggered.", icon="🎹")

    # ==================== ACTIONS ====================

    def _action_shortcut(self, key_cfg):
        sc_keys = key_cfg.get("text", "")
        title = key_cfg.get("title", "SHORTCUT")

        def _worker():
            # If shortcut involves screen snapping, minimizing, or screenshot, hide deck briefly
            lower_sc = sc_keys.lower()
            needs_hide = any(k in lower_sc for k in ("win+shift+s", "win+d", "prtscn", "win+l"))
            if needs_hide:
                self.withdraw()
                time.sleep(0.18)

            res = execute_shortcut(sc_keys)

            if needs_hide and "win+l" not in lower_sc:
                time.sleep(0.2)
                self.after(0, self.deiconify)

            ToastManager.show(self, title, res["summary"], icon="⚡")

        threading.Thread(target=_worker, daemon=True).start()

    def _action_snippet(self, key_cfg):
        text = key_cfg.get("text", "")
        auto_paste = key_cfg.get("auto_paste", True)

        def _worker():
            res = execute_text_snippet(text, auto_paste=auto_paste)
            ToastManager.show(self, "Text Snippet", res["summary"], icon="📋")

        threading.Thread(target=_worker, daemon=True).start()

    def _action_clean(self):
        def _worker():
            res = run_system_cleanup()
            self.audio.play_chord([60, 64, 67, 72])
            ToastManager.show(self, "Deep Clean Complete", res["summary"], icon="🧹")

        threading.Thread(target=_worker, daemon=True).start()

    def _action_screenshot(self, title="", bbox=None):
        # Hide on main thread so piano deck does not obstruct the screenshot
        self.withdraw()

        def _worker():
            try:
                time.sleep(0.18)  # Allow desktop to repaint cleanly without the dashboard
                res = capture_screen(title=title, bbox=bbox)
            finally:
                # Restore piano deck safely on main GUI thread
                self.after(0, self.deiconify)

            if res.get("success"):
                self.after(0, lambda: SavedNotificationWindow.show(
                    self,
                    filepath=res["filepath"],
                    is_snippet=bool(bbox),
                    timeout_seconds=6
                ))
            else:
                ToastManager.show(self, "Capture Error", "Could not capture display.", icon="⚠️")

        threading.Thread(target=_worker, daemon=True).start()

    def _action_snippet_area(self, title=""):
        self.withdraw()
        self.after(180, lambda: self._launch_snipping_overlay(title))

    def _launch_snipping_overlay(self, title):
        def _on_region(bbox):
            self._action_screenshot(title=title, bbox=bbox)

        def _on_cancel():
            self.deiconify()

        SnippingOverlay(self, on_complete=_on_region, on_cancel=_on_cancel)

    def _action_dispatch(self):
        self.withdraw()

        def _worker():
            try:
                time.sleep(0.18)
                res = execute_snap_and_dispatch(self.config)
            finally:
                self.after(0, self.deiconify)

            ToastManager.show(self, "Dispatch Result", res["message"], icon="📤")

        threading.Thread(target=_worker, daemon=True).start()

    def _action_workspace(self):
        urls = self.config.get("workspace", {}).get("urls", [])
        apps = self.config.get("workspace", {}).get("apps", [])

        def _cb(res):
            ToastManager.show(self, "Workspace Launched", res["summary"], icon="💼")

        launch_workspace_bundle(urls, apps, callback=_cb)

    def _action_autologin(self):
        auto_cfg = self.config.get("autologin", {})
        url = auto_cfg.get("url", "")
        username = auto_cfg.get("username", "")
        password = auto_cfg.get("password", "") if auto_cfg.get("auto_copy_password") else ""

        def _cb(res):
            ToastManager.show(self, "Portal Login", res["summary"], icon="🔐")

        open_and_autofill(url, username, password, callback=_cb)

    def _action_kill_tasks(self, key_cfg):
        def _worker():
            targets = key_cfg.get("text", "")
            res = kill_hung_processes(targets)
            ToastManager.show(self, "Task Rescue", res["summary"], icon="⚡")

        threading.Thread(target=_worker, daemon=True).start()

    def _action_custom_url(self, key_cfg):
        url = key_cfg.get("text", "").strip()
        if url:
            if not url.startswith("http://") and not url.startswith("https://"):
                url = "https://" + url
            webbrowser.open_new_tab(url)
            ToastManager.show(self, "Web Link", f"Opened {url}", icon="🌐")

    def _action_music(self):
        is_playing, title, summary = self.music.toggle()
        icon = "🎵" if is_playing else "⏸️"
        ToastManager.show(self, "Ambient Focus Audio", summary, icon=icon)

    def _action_privacy(self):
        msg = activate_privacy_shield(lock_screen=False)
        ToastManager.show(self, "Privacy Shield", msg, icon="🛡️")

    def quit_app(self):
        self.audio.close()
        self.destroy()

if __name__ == "__main__":
    app = PianoDeckBar()
    app.mainloop()
