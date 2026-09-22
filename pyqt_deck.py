import os
import sys
import ctypes
from ctypes import wintypes
import threading
import time
import webbrowser

from PyQt6 import QtWidgets, QtCore, QtGui

from profile_manager import ProfileManager
from config_manager import ConfigManager
from audio_engine import AudioEngine
from pyqt_add_dialog import PyQtAddKeyDialog
from pyqt_saved_popup import PyQtSavedPopup

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
from pyqt_snipper import PyQtSnapshotDialog, PyQtSnipperOverlay

class PianoKeyWidget(QtWidgets.QFrame):
    """
    Luxury Grand Piano Ivory Key with 3D tactile action,
    specular gradients, gold accents, and mechanical press depression.
    """
    clicked = QtCore.pyqtSignal(dict)
    rightClicked = QtCore.pyqtSignal(dict, int)

    def __init__(self, key_cfg: dict, key_index: int = 0, is_add_key: bool = False):
        super().__init__()
        self.cfg = key_cfg
        self.key_index = key_index
        self.is_add_key = is_add_key

        self.setCursor(QtCore.Qt.CursorShape.PointingHandCursor)
        self.setMinimumSize(130, 135)
        self._setup_style()
        self._build_ui()

    def _setup_style(self):
        if self.is_add_key:
            # Obsidian & Gold Add Button Key
            self.setStyleSheet("""
                QFrame#PianoKey {
                    background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #282A34, stop:0.5 #1E2028, stop:1 #15161C);
                    border: 1px solid #7D6522;
                    border-bottom: 3px solid #5A4716;
                    border-radius: 8px;
                    margin-top: 0px;
                }
                QFrame#PianoKey:hover {
                    background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #323542, stop:0.5 #262832, stop:1 #1A1C24);
                    border: 1px solid #D4AF37;
                    border-bottom: 3px solid #A88620;
                }
            """)
        else:
            # Genuine Steinway Ivory Key with 3D drop depth
            self.setStyleSheet("""
                QFrame#PianoKey {
                    background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #FFFFFF, stop:0.45 #FAF8F2, stop:1 #ECE6D8);
                    border: 1px solid #CFC7B4;
                    border-bottom: 4px solid #9C937E;
                    border-radius: 7px;
                    margin-top: 0px;
                }
                QFrame#PianoKey:hover {
                    background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #FFFFFF, stop:0.4 #FFFDF8, stop:1 #F5EFE0);
                    border: 1px solid #D4AF37;
                    border-bottom: 4px solid #B89327;
                }
            """)
        self.setObjectName("PianoKey")

    def _build_ui(self):
        layout = QtWidgets.QVBoxLayout(self)
        layout.setContentsMargins(10, 8, 10, 8)
        layout.setSpacing(3)

        # Top row: Note name (e.g. C4, D4) + brass hinge accent
        top_row = QtWidgets.QHBoxLayout()
        note_name = self.cfg.get("note_name", "C4")
        lbl_note = QtWidgets.QLabel(note_name)
        note_color = "#D4AF37" if self.is_add_key else "#8F6E1C"
        lbl_note.setStyleSheet(f"font-size: 10px; font-weight: bold; color: {note_color}; font-family: 'Georgia'; border: none; background: transparent;")
        top_row.addWidget(lbl_note)

        line = QtWidgets.QFrame()
        line.setFrameShape(QtWidgets.QFrame.Shape.HLine)
        line_color = "#4D3E14" if self.is_add_key else "#E8DAC0"
        line.setStyleSheet(f"background-color: {line_color}; max-height: 1px; border: none;")
        top_row.addWidget(line, 1)
        layout.addLayout(top_row)

        # Icon
        icon_str = self.cfg.get("icon", "🎹")
        lbl_icon = QtWidgets.QLabel(icon_str)
        icon_size = 26 if self.is_add_key else 24
        lbl_icon.setStyleSheet(f"font-size: {icon_size}px; border: none; background: transparent;")
        lbl_icon.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(lbl_icon)

        # Title
        title_str = self.cfg.get("title", "")
        lbl_title = QtWidgets.QLabel(title_str)
        t_color = "#E0E0E0" if self.is_add_key else "#18191E"
        lbl_title.setStyleSheet(f"font-size: 11px; font-weight: bold; color: {t_color}; font-family: 'Segoe UI'; border: none; background: transparent;")
        lbl_title.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(lbl_title)

        # Subtitle
        sub_str = self.cfg.get("subtitle", "")
        if len(sub_str) > 20:
            sub_str = sub_str[:18] + ".."
        lbl_sub = QtWidgets.QLabel(sub_str)
        s_color = "#8A8D98" if self.is_add_key else "#5E626E"
        lbl_sub.setStyleSheet(f"font-size: 9px; color: {s_color}; border: none; background: transparent;")
        lbl_sub.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(lbl_sub)

        # Bottom Badge
        badge_str = self.cfg.get("badge", "")
        if badge_str:
            badge_box = QtWidgets.QHBoxLayout()
            lbl_badge = QtWidgets.QLabel(badge_str)
            if self.is_add_key:
                lbl_badge.setStyleSheet("background-color: #2D303B; color: #D4AF37; font-size: 9px; font-weight: bold; border-radius: 4px; padding: 2px 6px; border: 1px solid #7D6522;")
            else:
                lbl_badge.setStyleSheet("background-color: #DFD7C2; color: #4F431B; font-size: 9px; font-weight: bold; border-radius: 4px; padding: 2px 6px; border: 1px solid #C4BA9F;")
            badge_box.addStretch()
            badge_box.addWidget(lbl_badge)
            badge_box.addStretch()
            layout.addLayout(badge_box)

    def mousePressEvent(self, event: QtGui.QMouseEvent):
        if event.button() == QtCore.Qt.MouseButton.LeftButton:
            # Tactile visual depression
            if self.is_add_key:
                self.setStyleSheet("""
                    QFrame#PianoKey {
                        background-color: #121317;
                        border: 1px solid #FFD700;
                        border-top: 3px solid #08080A;
                        border-radius: 8px;
                        margin-top: 4px;
                    }
                """)
            else:
                self.setStyleSheet("""
                    QFrame#PianoKey {
                        background-color: #DCD3BF;
                        border: 1px solid #A88620;
                        border-top: 4px solid #827863;
                        border-radius: 7px;
                        margin-top: 4px;
                    }
                """)
        elif event.button() == QtCore.Qt.MouseButton.RightButton:
            self.rightClicked.emit(self.cfg, self.key_index)
        super().mousePressEvent(event)

    def mouseReleaseEvent(self, event: QtGui.QMouseEvent):
        if event.button() == QtCore.Qt.MouseButton.LeftButton:
            self._setup_style()
            self.clicked.emit(self.cfg)
        super().mouseReleaseEvent(event)


class PyQtPianoDeck(QtWidgets.QWidget):
    """
    World-class Grand Piano Executive Dashboard Window in PyQt6.
    Docks above taskbar with multi-profile switching, acoustic MIDI synth,
    ivory keys, and rich executive automations.
    """
    def __init__(self):
        super().__init__()
        self.profile_mgr = ProfileManager()
        self.cfg_mgr = ConfigManager()
        self.audio = AudioEngine(enabled=self.cfg_mgr.config.get("app", {}).get("sound_enabled", True))
        self.music = MusicPlayer(stations=self.cfg_mgr.config.get("music", {}).get("stations", []))

        self.is_collapsed = False
        self._drag_pos = None

        self.setWindowTitle("Executive Piano Deck — Senior Officers Dashboard")
        self.setWindowFlags(QtCore.Qt.WindowType.FramelessWindowHint | QtCore.Qt.WindowType.WindowStaysOnTopHint)
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground)

        self._build_main_ui()
        self._dock_to_bottom()

    def _dock_to_bottom(self):
        screen = QtWidgets.QApplication.screenAt(QtGui.QCursor.pos()) or QtWidgets.QApplication.primaryScreen()
        if not screen:
            return
        geom = screen.availableGeometry()
        screen_w = geom.width()
        screen_h = geom.height()

        active_prof = self.profile_mgr.get_active_profile()
        keys_count = len(active_prof.get("keys", [])) + 1
        desired_w = max(680, min(1360, keys_count * 155 + 50))
        dock_w = min(desired_w, screen_w - 20)
        dock_h = 205 if not self.is_collapsed else 48

        x = geom.x() + (screen_w - dock_w) // 2
        y = geom.y() + screen_h - dock_h - 4

        self.setGeometry(x, y, dock_w, dock_h)

    def _build_main_ui(self):
        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.setContentsMargins(6, 6, 6, 6)

        # Outer Grand Piano Frame with Gold Rim
        self.outer_frame = QtWidgets.QFrame(self)
        self.outer_frame.setStyleSheet("""
            QFrame#OuterFrame {
                background-color: #121317;
                border: 2px solid #8C7026;
                border-radius: 12px;
            }
        """)
        self.outer_frame.setObjectName("OuterFrame")

        # Drop shadow
        shadow = QtWidgets.QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(20)
        shadow.setColor(QtGui.QColor(0, 0, 0, 190))
        shadow.setOffset(0, 4)
        self.outer_frame.setGraphicsEffect(shadow)

        outer_layout = QtWidgets.QVBoxLayout(self.outer_frame)
        outer_layout.setContentsMargins(1, 1, 1, 1)
        outer_layout.setSpacing(0)

        # Fallboard (Mahogany / Ebony Top Rail)
        self.fallboard = QtWidgets.QFrame()
        self.fallboard.setFixedHeight(36)
        self.fallboard.setStyleSheet("""
            QFrame {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #25262F, stop:1 #18191E);
                border-top-left-radius: 10px;
                border-top-right-radius: 10px;
                border-bottom: 1px solid #8C7026;
            }
        """)

        rail_layout = QtWidgets.QHBoxLayout(self.fallboard)
        rail_layout.setContentsMargins(14, 0, 10, 0)
        rail_layout.setSpacing(10)

        # Brand Title
        lbl_brand = QtWidgets.QLabel("🎹  EXECUTIVE PIANO DECK")
        lbl_brand.setStyleSheet("font-size: 11px; font-weight: bold; color: #D4AF37; font-family: 'Segoe UI'; border: none; background: transparent;")
        rail_layout.addWidget(lbl_brand)

        # Profile Switcher Pill
        lbl_p = QtWidgets.QLabel("Profile:")
        lbl_p.setStyleSheet("font-size: 10px; color: #A0A3B0; border: none; background: transparent;")
        rail_layout.addWidget(lbl_p)

        self.cbo_profiles = QtWidgets.QComboBox()
        self.cbo_profiles.setCursor(QtCore.Qt.CursorShape.PointingHandCursor)
        self.cbo_profiles.setStyleSheet("""
            QComboBox {
                background-color: #2B2D38;
                color: #FFFFFF;
                border: 1px solid #484B5C;
                border-radius: 5px;
                padding: 2px 10px 2px 8px;
                font-size: 11px;
                font-weight: bold;
            }
            QComboBox:hover {
                border: 1px solid #D4AF37;
            }
            QComboBox::drop-down {
                border: none;
            }
            QComboBox QAbstractItemView {
                background-color: #21232C;
                color: #FFFFFF;
                selection-background-color: #D4AF37;
                selection-color: #121212;
                border: 1px solid #484B5C;
                padding: 4px;
            }
        """)
        self._populate_profiles()
        self.cbo_profiles.currentIndexChanged.connect(self._on_profile_switched)
        rail_layout.addWidget(self.cbo_profiles)

        btn_new_prof = QtWidgets.QPushButton("➕ New")
        btn_new_prof.setCursor(QtCore.Qt.CursorShape.PointingHandCursor)
        btn_new_prof.setStyleSheet("""
            QPushButton {
                background-color: #22242D;
                color: #D4AF37;
                font-size: 10px;
                font-weight: bold;
                border: 1px solid #635222;
                border-radius: 4px;
                padding: 3px 8px;
            }
            QPushButton:hover {
                background-color: #D4AF37;
                color: #121212;
            }
        """)
        btn_new_prof.clicked.connect(self._create_new_profile_dialog)
        rail_layout.addWidget(btn_new_prof)

        rail_layout.addStretch()

        # Top Rail Action Buttons
        btn_folder = QtWidgets.QPushButton("📂 Screenshots")
        btn_folder.setCursor(QtCore.Qt.CursorShape.PointingHandCursor)
        btn_folder.setStyleSheet("""
            QPushButton {
                background: transparent;
                color: #4ECA5D;
                font-size: 10px;
                font-weight: bold;
                border: none;
                padding: 4px 8px;
            }
            QPushButton:hover {
                color: #81C784;
            }
        """)
        btn_folder.clicked.connect(lambda: open_in_explorer())
        rail_layout.addWidget(btn_folder)

        sound_text = "🔊 Sound ON" if self.audio.enabled else "🔇 Sound OFF"
        self.btn_sound = QtWidgets.QPushButton(sound_text)
        self.btn_sound.setCursor(QtCore.Qt.CursorShape.PointingHandCursor)
        self.btn_sound.setStyleSheet("""
            QPushButton {
                background: transparent;
                color: #C5C7D0;
                font-size: 10px;
                border: none;
                padding: 4px 8px;
            }
            QPushButton:hover {
                color: #FFFFFF;
            }
        """)
        self.btn_sound.clicked.connect(self._toggle_sound)
        rail_layout.addWidget(self.btn_sound)

        btn_add = QtWidgets.QPushButton("➕ Add Key")
        btn_add.setCursor(QtCore.Qt.CursorShape.PointingHandCursor)
        btn_add.setStyleSheet("""
            QPushButton {
                background: transparent;
                color: #D4AF37;
                font-size: 10px;
                font-weight: bold;
                border: none;
                padding: 4px 8px;
            }
            QPushButton:hover {
                color: #F3CF65;
            }
        """)
        btn_add.clicked.connect(self._open_add_key_dialog)
        rail_layout.addWidget(btn_add)

        fold_text = "▼ Fold" if not self.is_collapsed else "▲ Expand"
        self.btn_fold = QtWidgets.QPushButton(fold_text)
        self.btn_fold.setCursor(QtCore.Qt.CursorShape.PointingHandCursor)
        self.btn_fold.setStyleSheet("""
            QPushButton {
                background: transparent;
                color: #D4AF37;
                font-size: 10px;
                font-weight: bold;
                border: none;
                padding: 4px 8px;
            }
        """)
        self.btn_fold.clicked.connect(self._toggle_collapse)
        rail_layout.addWidget(self.btn_fold)

        btn_close = QtWidgets.QPushButton("✕")
        btn_close.setCursor(QtCore.Qt.CursorShape.PointingHandCursor)
        btn_close.setStyleSheet("""
            QPushButton {
                background: transparent;
                color: #8E9099;
                font-size: 12px;
                font-weight: bold;
                border: none;
                padding: 4px 8px;
            }
            QPushButton:hover {
                color: #FF5252;
            }
        """)
        btn_close.clicked.connect(self.close)
        rail_layout.addWidget(btn_close)

        outer_layout.addWidget(self.fallboard)

        # Piano Keys Rack
        self.rack = QtWidgets.QFrame()
        self.rack.setStyleSheet("background-color: #0E0F13; border-bottom-left-radius: 10px; border-bottom-right-radius: 10px;")
        self.rack_layout = QtWidgets.QHBoxLayout(self.rack)
        self.rack_layout.setContentsMargins(8, 6, 8, 8)
        self.rack_layout.setSpacing(6)
        outer_layout.addWidget(self.rack, 1)

        main_layout.addWidget(self.outer_frame)

        self._populate_profiles()
        self._populate_keys()

    def _populate_keys(self):
        # Clear existing keys in rack
        while self.rack_layout.count():
            item = self.rack_layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.setParent(None)
                widget.deleteLater()

        active_prof = self.profile_mgr.get_active_profile()
        keys_list = active_prof.get("keys", [])

        for idx, k_cfg in enumerate(keys_list):
            key_widget = PianoKeyWidget(k_cfg, key_index=idx)
            key_widget.clicked.connect(self.handle_key_press)
            key_widget.rightClicked.connect(self._show_key_context_menu)
            self.rack_layout.addWidget(key_widget, 1)

        # Plus Piano Key on far right
        add_cfg = {
            "id": "add_btn",
            "note": 72,
            "note_name": "+",
            "title": "ADD KEY",
            "subtitle": "New Action / Snippet",
            "icon": "➕",
            "badge": "+ Add Key"
        }
        btn_add_key = PianoKeyWidget(add_cfg, is_add_key=True)
        btn_add_key.clicked.connect(lambda cfg: self._open_add_key_dialog())
        self.rack_layout.addWidget(btn_add_key, 1)

        self._dock_to_bottom()

    def _populate_profiles(self):
        self.cbo_profiles.blockSignals(True)
        self.cbo_profiles.clear()
        active_id = self.profile_mgr.get_active_profile_id()
        selected_index = 0
        for idx, (p_id, p_data) in enumerate(self.profile_mgr.get_all_profiles()):
            display_text = f"{p_data.get('icon', '👤')} {p_data.get('name', p_id)}"
            self.cbo_profiles.addItem(display_text, p_id)
            if p_id == active_id:
                selected_index = idx
        self.cbo_profiles.setCurrentIndex(selected_index)
        self.cbo_profiles.blockSignals(False)

    def _on_profile_switched(self, index):
        p_id = self.cbo_profiles.itemData(index)
        if p_id:
            self.profile_mgr.set_active_profile(p_id)
            self._populate_keys()
            self.audio.play_chord([60, 64, 67, 72])

    def _create_new_profile_dialog(self):
        name, ok = QtWidgets.QInputDialog.getText(
            self,
            "Create New Profile",
            "Enter Profile / Officer Name:\n(e.g. Director Sharma, CFO, Legal Team)"
        )
        if ok and name.strip():
            new_id = self.profile_mgr.add_profile(name.strip())
            self._populate_profiles()
            self._populate_keys()
            self.audio.play_chord([60, 64, 67, 72])

    def _toggle_sound(self):
        self.audio.enabled = not self.audio.enabled
        self.cfg_mgr.config["app"]["sound_enabled"] = self.audio.enabled
        self.cfg_mgr.save()
        sound_text = "🔊 Sound ON" if self.audio.enabled else "🔇 Sound OFF"
        self.btn_sound.setText(sound_text)

    def _toggle_collapse(self):
        self.is_collapsed = not self.is_collapsed
        if self.is_collapsed:
            self.rack.hide()
            self.btn_fold.setText("▲ Expand")
        else:
            self.rack.show()
            self.btn_fold.setText("▼ Fold")
        self._dock_to_bottom()

    def _open_add_key_dialog(self, existing_key=None, key_index=None):
        dlg = PyQtAddKeyDialog(self, on_save=self._on_key_saved, existing_key=existing_key, key_index=key_index)
        dlg.exec()

    def _on_key_saved(self, key_data, key_index):
        active_prof = self.profile_mgr.get_active_profile()
        keys_list = active_prof.get("keys", [])

        if key_index is not None and key_index < len(keys_list):
            keys_list[key_index] = key_data
        else:
            keys_list.append(key_data)

        self.profile_mgr.update_keys_for_active_profile(keys_list)
        self._populate_keys()
        self.audio.play_chord([60, 64, 67, 72])

    def _show_key_context_menu(self, key_cfg, key_index):
        menu = QtWidgets.QMenu(self)
        menu.setStyleSheet("""
            QMenu {
                background-color: #21232C;
                color: #FFFFFF;
                border: 1px solid #D4AF37;
                padding: 4px;
            }
            QMenu::item {
                padding: 6px 18px;
            }
            QMenu::item:selected {
                background-color: #D4AF37;
                color: #121212;
            }
        """)
        act_edit = menu.addAction("✏️  Edit Key / Text Snippet")
        act_del = menu.addAction("🗑️  Delete Key")
        menu.addSeparator()
        act_add = menu.addAction("➕  Add Another Key")

        action = menu.exec(QtGui.QCursor.pos())
        if action == act_edit:
            self._open_add_key_dialog(existing_key=key_cfg, key_index=key_index)
        elif action == act_del:
            active_prof = self.profile_mgr.get_active_profile()
            keys_list = active_prof.get("keys", [])
            if 0 <= key_index < len(keys_list):
                keys_list.pop(key_index)
                self.profile_mgr.update_keys_for_active_profile(keys_list)
                self._populate_keys()
        elif action == act_add:
            self._open_add_key_dialog()

    def handle_key_press(self, key_cfg):
        # 1. Play Acoustic Grand Piano Note
        note = key_cfg.get("note", 60)
        self.audio.play_note(note=note, velocity=105, duration=0.35)

        action = key_cfg.get("action", "")
        title = key_cfg.get("title", "")

        # 2. Dispatch Action
        if action == "clean_system":
            self._action_clean()
        elif action in ("take_screenshot", "screenshot_instant", "screenshot_titled"):
            self._prompt_screenshot()
        elif action == "paste_text":
            self._action_snippet(key_cfg)
        elif action == "shortcut":
            self._action_shortcut(key_cfg)
        elif action == "dispatch_screenshot":
            self._action_dispatch()
        elif action == "kill_tasks":
            self._action_kill_tasks(key_cfg)
        elif action == "custom_url":
            self._action_custom_url(key_cfg)
        elif action == "toggle_music":
            self._action_music()
        elif action == "privacy_shield":
            self._action_privacy()

    # ==================== ACTION WORKERS ====================

    def _prompt_screenshot(self):
        dlg = PyQtSnapshotDialog(
            self,
            on_full_screen=lambda t: self._action_screenshot(title=t),
            on_area_snippet=lambda t: self._action_snippet_area(title=t)
        )
        dlg.exec()

    def _action_screenshot(self, title="", bbox=None):
        self.hide()

        def _worker():
            try:
                time.sleep(0.18)
                res = capture_screen(title=title, bbox=bbox)
            finally:
                QtCore.QMetaObject.invokeMethod(self, "show", QtCore.Qt.ConnectionType.QueuedConnection)

            if res.get("success"):
                QtCore.QMetaObject.invokeMethod(
                    self,
                    "_show_saved_popup",
                    QtCore.Qt.ConnectionType.QueuedConnection,
                    QtCore.Q_ARG(str, res["filepath"]),
                    QtCore.Q_ARG(bool, bool(bbox))
                )

        threading.Thread(target=_worker, daemon=True).start()

    @QtCore.pyqtSlot(str, bool)
    def _show_saved_popup(self, filepath, is_snippet):
        PyQtSavedPopup.show_popup(filepath, is_snippet=is_snippet, timeout_seconds=6)

    def _action_snippet_area(self, title=""):
        self.hide()
        QtCore.QTimer.singleShot(180, lambda: self._start_snipper(title))

    def _start_snipper(self, title):
        def _on_region(bbox):
            self._action_screenshot(title=title, bbox=bbox)

        def _on_cancel():
            self.show()

        self._snipper = PyQtSnipperOverlay(on_complete=_on_region, on_cancel=_on_cancel)

    def _action_snippet(self, key_cfg):
        text = key_cfg.get("text", "")
        auto_paste = key_cfg.get("auto_paste", True)

        def _worker():
            execute_text_snippet(text, auto_paste=auto_paste)

        threading.Thread(target=_worker, daemon=True).start()

    def _action_shortcut(self, key_cfg):
        sc_keys = key_cfg.get("text", "")
        def _worker():
            lower_sc = sc_keys.lower()
            needs_hide = any(k in lower_sc for k in ("win+shift+s", "win+d", "prtscn", "win+l"))
            if needs_hide:
                QtCore.QMetaObject.invokeMethod(self, "hide", QtCore.Qt.ConnectionType.QueuedConnection)
                time.sleep(0.18)

            execute_shortcut(sc_keys)

            if needs_hide and "win+l" not in lower_sc:
                time.sleep(0.2)
                QtCore.QMetaObject.invokeMethod(self, "show", QtCore.Qt.ConnectionType.QueuedConnection)

        threading.Thread(target=_worker, daemon=True).start()

    def _action_clean(self):
        def _worker():
            res = run_system_cleanup()
            self.audio.play_chord([60, 64, 67, 72])

        threading.Thread(target=_worker, daemon=True).start()

    def _action_dispatch(self):
        self.hide()
        def _worker():
            try:
                time.sleep(0.18)
                execute_snap_and_dispatch(self.cfg_mgr.config)
            finally:
                QtCore.QMetaObject.invokeMethod(self, "show", QtCore.Qt.ConnectionType.QueuedConnection)

        threading.Thread(target=_worker, daemon=True).start()

    def _action_kill_tasks(self, key_cfg):
        targets = key_cfg.get("text", "")
        threading.Thread(target=lambda: kill_hung_processes(targets), daemon=True).start()

    def _action_custom_url(self, key_cfg):
        url = key_cfg.get("text", "").strip()
        if url:
            if not url.startswith("http://") and not url.startswith("https://"):
                url = "https://" + url
            webbrowser.open_new_tab(url)

    def _action_music(self):
        self.music.toggle()

    def _action_privacy(self):
        activate_privacy_shield(lock_screen=False)

    # Window Dragging from Fallboard
    def mousePressEvent(self, event: QtGui.QMouseEvent):
        if event.button() == QtCore.Qt.MouseButton.LeftButton:
            self._drag_pos = event.globalPosition().toPoint() - self.frameGeometry().topLeft()
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event: QtGui.QMouseEvent):
        if self._drag_pos is not None and event.buttons() == QtCore.Qt.MouseButton.LeftButton:
            self.move(event.globalPosition().toPoint() - self._drag_pos)
        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event: QtGui.QMouseEvent):
        self._drag_pos = None
        super().mouseReleaseEvent(event)
