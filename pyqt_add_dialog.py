import os
from PyQt6 import QtWidgets, QtCore, QtGui
import win32clipboard
from actions.shortcuts import TOP_50_SHORTCUTS
from actions.app_scanner import scan_installed_apps, pick_icon_for_app

NOTES_PALETTE = [
    (60, "C4"), (62, "D4"), (64, "E4"), (65, "F4"),
    (67, "G4"), (69, "A4"), (71, "B4"), (72, "C5"),
    (74, "D5"), (76, "E5"), (77, "F5"), (79, "G5")
]


class InstalledAppsPickerDialog(QtWidgets.QDialog):
    """
    Modal search & pick dialog for all installed Windows applications.
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        self.selected_app = None
        self.setWindowTitle("📦 Select Installed Application")
        self.setFixedSize(580, 520)
        self.setWindowFlags(QtCore.Qt.WindowType.Dialog | QtCore.Qt.WindowType.WindowStaysOnTopHint)
        self.setStyleSheet("""
            QDialog {
                background-color: #17181D;
                color: #FFFFFF;
                font-family: 'Segoe UI';
            }
            QLabel { color: #E0E0E0; }
            QLineEdit, QComboBox {
                background-color: #242630;
                color: #FFFFFF;
                border: 1px solid #3B3E4F;
                border-radius: 6px;
                padding: 6px 10px;
                font-size: 12px;
            }
            QLineEdit:focus, QComboBox:focus { border: 1px solid #D4AF37; }
        """)
        self._build_ui()

    def _build_ui(self):
        layout = QtWidgets.QVBoxLayout(self)
        layout.setContentsMargins(18, 16, 18, 16)
        layout.setSpacing(10)

        lbl_head = QtWidgets.QLabel("📦 Choose Application to Launch")
        lbl_head.setStyleSheet("font-size: 14px; font-weight: bold; color: #D4AF37;")
        layout.addWidget(lbl_head)

        # Filter bar
        filter_box = QtWidgets.QHBoxLayout()
        self.e_search = QtWidgets.QLineEdit()
        self.e_search.setPlaceholderText("🔍 Filter (e.g. Chrome, Excel, VS Code, Calculator)...")
        self.e_search.textChanged.connect(self._filter_apps)
        filter_box.addWidget(self.e_search, 1)

        self.cbo_cat = QtWidgets.QComboBox()
        self.cbo_cat.addItem("All Categories", "all")
        self.cbo_cat.addItem("🖥️ System Utilities", "System Utility")
        self.cbo_cat.addItem("🚀 Desktop Apps", "Desktop Application")
        self.cbo_cat.addItem("📱 Store Apps", "Windows Store App")
        self.cbo_cat.currentIndexChanged.connect(lambda: self._filter_apps(self.e_search.text()))
        filter_box.addWidget(self.cbo_cat)
        layout.addLayout(filter_box)

        # List
        self.list_apps = QtWidgets.QListWidget()
        self.list_apps.setStyleSheet("""
            QListWidget {
                background-color: #1A1C24;
                border: 1px solid #2F3240;
                border-radius: 6px;
                padding: 4px;
            }
            QListWidget::item {
                background-color: #222430;
                border-radius: 4px;
                padding: 7px 10px;
                margin-bottom: 2px;
                color: #E8E8E8;
            }
            QListWidget::item:hover { background-color: #2D3040; }
            QListWidget::item:selected {
                background-color: #3A3521;
                border: 1px solid #D4AF37;
                color: #FFFFFF;
            }
        """)
        self.list_apps.itemDoubleClicked.connect(self._on_double_click)
        layout.addWidget(self.list_apps, 1)

        # Buttons
        btn_bar = QtWidgets.QHBoxLayout()
        btn_cancel = QtWidgets.QPushButton("Cancel")
        btn_cancel.setCursor(QtCore.Qt.CursorShape.PointingHandCursor)
        btn_cancel.setStyleSheet("""
            QPushButton {
                background-color: #2A2D3A;
                color: #CCCCCC;
                border-radius: 5px;
                padding: 7px 18px;
                border: none;
            }
            QPushButton:hover { background-color: #383C4E; }
        """)
        btn_cancel.clicked.connect(self.reject)
        btn_bar.addWidget(btn_cancel)
        btn_bar.addStretch()

        btn_select = QtWidgets.QPushButton("Select Application")
        btn_select.setCursor(QtCore.Qt.CursorShape.PointingHandCursor)
        btn_select.setStyleSheet("""
            QPushButton {
                background-color: #D4AF37;
                color: #121212;
                font-weight: bold;
                border-radius: 5px;
                padding: 7px 22px;
                border: none;
            }
            QPushButton:hover { background-color: #F3CF65; }
        """)
        btn_select.clicked.connect(self._on_select)
        btn_bar.addWidget(btn_select)
        layout.addLayout(btn_bar)

        self._populate_apps()

    def _populate_apps(self, query=""):
        self.list_apps.clear()
        q = query.lower().strip()
        selected_cat = self.cbo_cat.currentData() if hasattr(self, 'cbo_cat') else "all"

        apps = scan_installed_apps()
        for app in apps:
            if selected_cat != "all" and app["category"] != selected_cat:
                continue
            if q and (q not in app["keywords"] and q not in app["name"].lower()):
                continue

            text = f"{app['icon']}  {app['name']}   [{app['category']}]"
            item = QtWidgets.QListWidgetItem(text)
            item.setData(QtCore.Qt.ItemDataRole.UserRole, app)
            item.setToolTip(f"Target: {app['target']}")
            self.list_apps.addItem(item)

    def _filter_apps(self, text):
        self._populate_apps(text)

    def _on_double_click(self, item):
        self.selected_app = item.data(QtCore.Qt.ItemDataRole.UserRole)
        self.accept()

    def _on_select(self):
        items = self.list_apps.selectedItems()
        if items:
            self.selected_app = items[0].data(QtCore.Qt.ItemDataRole.UserRole)
            self.accept()
        else:
            QtWidgets.QMessageBox.warning(self, "Selection", "Please select an application from the list.")


class PyQtAddKeyDialog(QtWidgets.QDialog):
    """
    Modern PyQt6 Piano Key Builder Dialog.
    Ordered by priority:
      1. 📋 Copied Text (Snippets, fast paste)
      2. 📦 Installed Applications (200+ detected apps & tools)
      3. 🛠️ Custom Action / Script (.bat, .exe, URLs, rescue actions)
      4. ⚡ Top 50 Most Used Shortcuts (Win+Shift+S, Win+V, etc.)
    """
    def __init__(self, parent, on_save, existing_key=None, key_index=None):
        super().__init__(parent)
        self.on_save = on_save
        self.existing_key = existing_key
        self.key_index = key_index

        self.setWindowTitle("🎹 Piano Key Builder — Executive Deck")
        screen = QtWidgets.QApplication.screenAt(QtGui.QCursor.pos()) or QtWidgets.QApplication.primaryScreen()
        sh = screen.availableGeometry().height() if screen else 720
        dialog_h = min(600, sh - 50)
        self.setFixedSize(680, dialog_h)
        self.setWindowFlags(QtCore.Qt.WindowType.Dialog | QtCore.Qt.WindowType.WindowStaysOnTopHint)
        self.setStyleSheet("""
            QDialog {
                background-color: #17181D;
                color: #FFFFFF;
                font-family: 'Segoe UI';
            }
            QLabel {
                color: #E0E0E0;
            }
            QLineEdit, QTextEdit, QComboBox {
                background-color: #242630;
                color: #FFFFFF;
                border: 1px solid #3B3E4F;
                border-radius: 6px;
                padding: 6px 10px;
                font-size: 12px;
            }
            QLineEdit:focus, QTextEdit:focus, QComboBox:focus {
                border: 1px solid #D4AF37;
            }
            QTabWidget::pane {
                border: 1px solid #2F3240;
                background-color: #1C1E26;
                border-radius: 8px;
                top: -1px;
            }
            QTabBar::tab {
                background-color: #242630;
                color: #B0B3C0;
                font-weight: bold;
                font-size: 11px;
                padding: 10px 14px;
                border-top-left-radius: 6px;
                border-top-right-radius: 6px;
                margin-right: 3px;
            }
            QTabBar::tab:selected {
                background-color: #1C1E26;
                color: #D4AF37;
                border-bottom: 2px solid #D4AF37;
            }
            QCheckBox {
                color: #CCCCCC;
                font-size: 11px;
            }
            QCheckBox::indicator {
                width: 16px;
                height: 16px;
                border-radius: 4px;
                background-color: #242630;
                border: 1px solid #3B3E4F;
            }
            QCheckBox::indicator:checked {
                background-color: #D4AF37;
            }
        """)

        self._build_ui()

    def _build_ui(self):
        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.setContentsMargins(20, 16, 20, 16)
        main_layout.setSpacing(12)

        # Header
        hdr = QtWidgets.QHBoxLayout()
        lbl_head = QtWidgets.QLabel("🎹 Piano Key Builder")
        lbl_head.setStyleSheet("font-size: 16px; font-weight: bold; color: #D4AF37;")
        hdr.addWidget(lbl_head)
        hdr.addStretch()
        main_layout.addLayout(hdr)

        lbl_desc = QtWidgets.QLabel("Configure your 1-click piano button from installed apps, snippets, or custom actions:")
        lbl_desc.setStyleSheet("font-size: 11px; color: #9E9E9E;")
        main_layout.addWidget(lbl_desc)

        # Top Shared Fields: Key Title & Icon
        f_top = QtWidgets.QFrame()
        f_top.setStyleSheet("background-color: #1F212A; border-radius: 8px; padding: 6px;")
        top_layout = QtWidgets.QGridLayout(f_top)
        top_layout.setContentsMargins(12, 10, 12, 10)
        top_layout.setSpacing(8)

        lbl_t = QtWidgets.QLabel("PIANO KEY TITLE (Shows Bold on Key):")
        lbl_t.setStyleSheet("font-size: 10px; font-weight: bold; color: #D4AF37; border: none;")
        top_layout.addWidget(lbl_t, 0, 0)

        lbl_i = QtWidgets.QLabel("ICON:")
        lbl_i.setStyleSheet("font-size: 10px; font-weight: bold; color: #D4AF37; border: none;")
        top_layout.addWidget(lbl_i, 0, 1)

        init_title = self.existing_key.get("title", "OFFICER APPROVAL") if self.existing_key else "OFFICER APPROVAL"
        self.e_title = QtWidgets.QLineEdit(init_title)
        self.e_title.setStyleSheet("font-size: 13px; font-weight: bold; color: #FFFFFF;")
        top_layout.addWidget(self.e_title, 1, 0)

        init_icon = self.existing_key.get("icon", "📋") if self.existing_key else "📋"
        self.e_icon = QtWidgets.QLineEdit(init_icon)
        self.e_icon.setFixedWidth(65)
        self.e_icon.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.e_icon.setStyleSheet("font-size: 15px;")
        top_layout.addWidget(self.e_icon, 1, 1)

        top_layout.setColumnStretch(0, 4)
        top_layout.setColumnStretch(1, 1)
        main_layout.addWidget(f_top)

        # Tabs for Mode Selection:
        # Tab 0: Copied Content
        # Tab 1: Installed Applications
        # Tab 2: Custom Made Key
        # Tab 3: Top 50 Shortcuts
        self.tabs = QtWidgets.QTabWidget()

        self.tab_copied = QtWidgets.QWidget()
        self._build_copied_tab()
        self.tabs.addTab(self.tab_copied, "1. 📋 Copied Text")

        self.tab_installed_apps = QtWidgets.QWidget()
        self._build_installed_apps_tab()
        self.tabs.addTab(self.tab_installed_apps, "2. 📦 Installed Apps")

        self.tab_custom = QtWidgets.QWidget()
        self._build_custom_tab()
        self.tabs.addTab(self.tab_custom, "3. 🛠️ Custom Action")

        self.tab_shortcuts = QtWidgets.QWidget()
        self._build_shortcuts_tab()
        self.tabs.addTab(self.tab_shortcuts, "4. ⚡ Shortcuts")

        main_layout.addWidget(self.tabs, 1)

        # Select initial tab
        if self.existing_key:
            act = self.existing_key.get("action", "")
            if act == "paste_text":
                self.tabs.setCurrentIndex(0)
            elif act == "launch_app":
                target = self.existing_key.get("text", "")
                if target.lower().endswith(('.bat', '.cmd', '.ps1')):
                    self.tabs.setCurrentIndex(2)  # Custom script tab
                else:
                    self.tabs.setCurrentIndex(1)  # Installed Apps tab
            elif act == "shortcut":
                self.tabs.setCurrentIndex(3)
            else:
                self.tabs.setCurrentIndex(2)
        else:
            self.tabs.setCurrentIndex(0)

        # Bottom Buttons
        btn_bar = QtWidgets.QHBoxLayout()
        btn_cancel = QtWidgets.QPushButton("Cancel")
        btn_cancel.setCursor(QtCore.Qt.CursorShape.PointingHandCursor)
        btn_cancel.setStyleSheet("""
            QPushButton {
                background-color: #2F3240;
                color: #FFFFFF;
                border-radius: 6px;
                padding: 9px 20px;
                font-size: 12px;
                border: none;
            }
            QPushButton:hover {
                background-color: #3D4154;
            }
        """)
        btn_cancel.clicked.connect(self.reject)
        btn_bar.addWidget(btn_cancel)
        btn_bar.addStretch()

        btn_save = QtWidgets.QPushButton("Save Piano Key")
        btn_save.setCursor(QtCore.Qt.CursorShape.PointingHandCursor)
        btn_save.setStyleSheet("""
            QPushButton {
                background-color: #D4AF37;
                color: #121212;
                font-weight: bold;
                font-size: 13px;
                border-radius: 6px;
                padding: 9px 26px;
                border: none;
            }
            QPushButton:hover {
                background-color: #F3CF65;
            }
        """)
        btn_save.clicked.connect(self._save_key)
        btn_bar.addWidget(btn_save)

        main_layout.addLayout(btn_bar)

    def _build_copied_tab(self):
        layout = QtWidgets.QVBoxLayout(self.tab_copied)
        layout.setContentsMargins(16, 14, 16, 14)
        layout.setSpacing(10)

        top_row = QtWidgets.QHBoxLayout()
        lbl = QtWidgets.QLabel("Copied Text Bar / Snippet Content:")
        lbl.setStyleSheet("font-size: 11px; font-weight: bold; color: #D4AF37;")
        top_row.addWidget(lbl)
        top_row.addStretch()

        btn_paste = QtWidgets.QPushButton("📋 Paste from Clipboard")
        btn_paste.setCursor(QtCore.Qt.CursorShape.PointingHandCursor)
        btn_paste.setStyleSheet("""
            QPushButton {
                background-color: #282A36;
                color: #D4AF37;
                font-weight: bold;
                font-size: 11px;
                border-radius: 4px;
                padding: 5px 12px;
                border: 1px solid #D4AF37;
            }
            QPushButton:hover {
                background-color: #D4AF37;
                color: #121212;
            }
        """)
        btn_paste.clicked.connect(self._paste_from_clipboard)
        top_row.addWidget(btn_paste)
        layout.addLayout(top_row)

        init_text = self.existing_key.get("text", "Approved. Please process as per official policy and record in the minutes.") if self.existing_key else "Approved. Please process as per official policy and record in the minutes."
        self.txt_copied = QtWidgets.QTextEdit()
        self.txt_copied.setPlainText(init_text)
        self.txt_copied.setStyleSheet("font-family: 'Consolas'; font-size: 12px; line-height: 1.4;")
        layout.addWidget(self.txt_copied, 1)

        self.chk_auto_paste = QtWidgets.QCheckBox("Simulate Auto-Paste (Ctrl+V) directly into active document/email on press")
        self.chk_auto_paste.setChecked(self.existing_key.get("auto_paste", True) if self.existing_key else True)
        layout.addWidget(self.chk_auto_paste)

        lbl_hint = QtWidgets.QLabel("💡 Tip: Enter any frequent text (approval note, memo, email signature, bank details, zoom link).")
        lbl_hint.setStyleSheet("font-size: 10px; font-style: italic; color: #888888;")
        layout.addWidget(lbl_hint)

    def _build_installed_apps_tab(self):
        layout = QtWidgets.QVBoxLayout(self.tab_installed_apps)
        layout.setContentsMargins(14, 12, 14, 12)
        layout.setSpacing(8)

        # Filter bar
        filter_box = QtWidgets.QHBoxLayout()
        lbl_s = QtWidgets.QLabel("🔍 Search Apps:")
        lbl_s.setStyleSheet("font-size: 11px; font-weight: bold; color: #D4AF37;")
        filter_box.addWidget(lbl_s)

        self.e_app_search = QtWidgets.QLineEdit()
        self.e_app_search.setPlaceholderText("Filter apps (e.g. Chrome, Excel, VS Code, Calculator, PyCharm)...")
        self.e_app_search.textChanged.connect(self._filter_installed_apps)
        filter_box.addWidget(self.e_app_search, 1)

        self.cbo_app_cat = QtWidgets.QComboBox()
        self.cbo_app_cat.addItem("All Categories", "all")
        self.cbo_app_cat.addItem("🖥️ System Utilities", "System Utility")
        self.cbo_app_cat.addItem("🚀 Desktop Apps", "Desktop Application")
        self.cbo_app_cat.addItem("📱 Store Apps", "Windows Store App")
        self.cbo_app_cat.currentIndexChanged.connect(lambda: self._filter_installed_apps(self.e_app_search.text()))
        filter_box.addWidget(self.cbo_app_cat)

        btn_refresh = QtWidgets.QPushButton("🔄 Refresh")
        btn_refresh.setCursor(QtCore.Qt.CursorShape.PointingHandCursor)
        btn_refresh.setStyleSheet("""
            QPushButton {
                background-color: #2D303E;
                color: #B0B3C0;
                font-size: 11px;
                border-radius: 4px;
                padding: 6px 10px;
                border: 1px solid #3B3E4F;
            }
            QPushButton:hover {
                background-color: #3B3F52;
                color: #FFFFFF;
            }
        """)
        btn_refresh.clicked.connect(self._refresh_apps)
        filter_box.addWidget(btn_refresh)
        layout.addLayout(filter_box)

        # List Widget
        self.list_installed_apps = QtWidgets.QListWidget()
        self.list_installed_apps.setStyleSheet("""
            QListWidget {
                background-color: #17181F;
                border: 1px solid #2F3240;
                border-radius: 6px;
                padding: 4px;
            }
            QListWidget::item {
                background-color: #21232D;
                border-radius: 4px;
                padding: 8px 10px;
                margin-bottom: 3px;
                color: #E8E8E8;
            }
            QListWidget::item:hover {
                background-color: #2C2F3D;
            }
            QListWidget::item:selected {
                background-color: #3A3521;
                border: 1px solid #D4AF37;
                color: #FFFFFF;
            }
        """)
        self.list_installed_apps.itemClicked.connect(self._on_app_selected)
        self.list_installed_apps.itemDoubleClicked.connect(self._on_app_double_clicked)
        layout.addWidget(self.list_installed_apps, 1)

        lbl_hint = QtWidgets.QLabel("💡 Tip: Click any app to preview title/icon, or double-click to immediately save it to your piano deck.")
        lbl_hint.setStyleSheet("font-size: 10px; font-style: italic; color: #888888;")
        layout.addWidget(lbl_hint)

        self._populate_installed_apps()

    def _populate_installed_apps(self, query=""):
        self.list_installed_apps.clear()
        q = query.lower().strip()
        selected_cat = self.cbo_app_cat.currentData() if hasattr(self, 'cbo_app_cat') else "all"

        apps = scan_installed_apps()
        for app in apps:
            if selected_cat != "all" and app["category"] != selected_cat:
                continue
            if q and (q not in app["keywords"] and q not in app["name"].lower()):
                continue

            text = f"{app['icon']}  {app['name']}   [{app['category']}]"
            item = QtWidgets.QListWidgetItem(text)
            item.setData(QtCore.Qt.ItemDataRole.UserRole, app)
            item.setToolTip(f"Target: {app['target']}")
            self.list_installed_apps.addItem(item)

    def _filter_installed_apps(self, text):
        self._populate_installed_apps(text)

    def _refresh_apps(self):
        scan_installed_apps(force_refresh=True)
        self._populate_installed_apps(self.e_app_search.text())

    def _on_app_selected(self, item):
        app = item.data(QtCore.Qt.ItemDataRole.UserRole)
        if app:
            clean_name = app["name"].replace("_", " ").replace("-", " ").strip()
            self.e_title.setText(clean_name.upper())
            self.e_icon.setText(app["icon"])

    def _on_app_double_clicked(self, item):
        self._on_app_selected(item)
        self._save_key()

    def _build_custom_tab(self):
        layout = QtWidgets.QVBoxLayout(self.tab_custom)
        layout.setContentsMargins(16, 14, 16, 14)
        layout.setSpacing(10)

        lbl = QtWidgets.QLabel("Select Custom Action Type:")
        lbl.setStyleSheet("font-size: 11px; font-weight: bold; color: #D4AF37;")
        layout.addWidget(lbl)

        self.cbo_custom_type = QtWidgets.QComboBox()
        self.custom_actions = [
            ("launch_app", "🚀 Launch App / Run Script (.bat, .exe, .cmd)"),
            ("custom_url", "🌐 Open Website / URL in Browser"),
            ("kill_tasks", "⚡ Kill Hung Processes (Excel, Chrome)"),
            ("clean_system", "🧹 Purge Recycle Bin & Cache"),
            ("privacy_shield", "🛡️ Privacy Shield (Boss Key & Mute)"),
            ("toggle_music", "🎵 Background Ambient Focus Music")
        ]
        for act, name in self.custom_actions:
            self.cbo_custom_type.addItem(name, act)
        self.cbo_custom_type.currentIndexChanged.connect(self._on_custom_type_changed)
        layout.addWidget(self.cbo_custom_type)

        self.lbl_param = QtWidgets.QLabel("Target Application Path, Batch File (.bat), or URL:")
        self.lbl_param.setStyleSheet("font-size: 11px; font-weight: bold; color: #CCCCCC; margin-top: 6px;")
        layout.addWidget(self.lbl_param)

        param_row = QtWidgets.QHBoxLayout()
        init_param = self.existing_key.get("text", "") if self.existing_key else ""
        self.e_custom_param = QtWidgets.QLineEdit(init_param)
        self.e_custom_param.setPlaceholderText("e.g. C:\\Scripts\\deploy.bat, calc.exe, or https://portal.company.com")
        self.e_custom_param.setStyleSheet("font-family: 'Consolas'; font-size: 12px;")
        param_row.addWidget(self.e_custom_param, 1)

        self.btn_pick_app = QtWidgets.QPushButton("📦 Installed Apps...")
        self.btn_pick_app.setCursor(QtCore.Qt.CursorShape.PointingHandCursor)
        self.btn_pick_app.setStyleSheet("""
            QPushButton {
                background-color: #2D303E;
                color: #D4AF37;
                font-weight: bold;
                font-size: 11px;
                border-radius: 5px;
                padding: 6px 12px;
                border: 1px solid #7D6522;
            }
            QPushButton:hover {
                background-color: #3B3F52;
                border-color: #D4AF37;
            }
        """)
        self.btn_pick_app.clicked.connect(self._pick_installed_app_for_custom)
        param_row.addWidget(self.btn_pick_app)

        self.btn_browse = QtWidgets.QPushButton("📁 Browse File...")
        self.btn_browse.setCursor(QtCore.Qt.CursorShape.PointingHandCursor)
        self.btn_browse.setStyleSheet("""
            QPushButton {
                background-color: #2D303E;
                color: #D4AF37;
                font-weight: bold;
                font-size: 11px;
                border-radius: 5px;
                padding: 6px 12px;
                border: 1px solid #7D6522;
            }
            QPushButton:hover {
                background-color: #3B3F52;
                border-color: #D4AF37;
            }
        """)
        self.btn_browse.clicked.connect(self._browse_custom_target)
        param_row.addWidget(self.btn_browse)
        layout.addLayout(param_row)

        # Set initial combo selection if editing existing key
        if self.existing_key:
            existing_act = self.existing_key.get("action", "")
            idx = self.cbo_custom_type.findData(existing_act)
            if idx >= 0:
                self.cbo_custom_type.setCurrentIndex(idx)
            elif existing_act == "custom_url" and init_param.lower().endswith(('.bat', '.cmd', '.exe', '.lnk')):
                self.cbo_custom_type.setCurrentIndex(0)

        layout.addStretch()

    def _on_custom_type_changed(self, index):
        act = self.cbo_custom_type.itemData(index)
        if act == "launch_app":
            self.lbl_param.setText("Target Application, Batch Script (.bat), or Executable:")
            self.e_custom_param.setPlaceholderText("e.g. C:\\Scripts\\run_api.bat, notepad.exe, calc")
            self.e_custom_param.setEnabled(True)
            self.btn_pick_app.setVisible(True)
            self.btn_browse.setVisible(True)
        elif act == "custom_url":
            self.lbl_param.setText("Website URL to open in default browser:")
            self.e_custom_param.setPlaceholderText("e.g. https://finance.yahoo.com or portal.company.com")
            self.e_custom_param.setEnabled(True)
            self.btn_pick_app.setVisible(False)
            self.btn_browse.setVisible(False)
        elif act == "kill_tasks":
            self.lbl_param.setText("Process Name to Terminate (e.g. excel.exe, chrome.exe):")
            self.e_custom_param.setPlaceholderText("e.g. excel.exe, acrobat.exe")
            self.e_custom_param.setEnabled(True)
            self.btn_pick_app.setVisible(False)
            self.btn_browse.setVisible(False)
        else:
            self.lbl_param.setText("No parameters needed for this built-in action.")
            self.e_custom_param.setEnabled(False)
            self.btn_pick_app.setVisible(False)
            self.btn_browse.setVisible(False)

    def _pick_installed_app_for_custom(self):
        dlg = InstalledAppsPickerDialog(self)
        if dlg.exec() == QtWidgets.QDialog.DialogCode.Accepted and dlg.selected_app:
            app = dlg.selected_app
            self.e_custom_param.setText(app["target"])
            idx = self.cbo_custom_type.findData("launch_app")
            if idx >= 0:
                self.cbo_custom_type.setCurrentIndex(idx)

            cur_title = self.e_title.text().strip()
            if not cur_title or cur_title in ("OFFICER APPROVAL", "NEW KEY", "MY ACTION"):
                clean_name = app["name"].replace("_", " ").replace("-", " ").strip()
                self.e_title.setText(clean_name.upper())

            self.e_icon.setText(app["icon"])

    def _browse_custom_target(self):
        filePath, _ = QtWidgets.QFileDialog.getOpenFileName(
            self,
            "Select Application, Batch File, or Script to Launch",
            "",
            "Executables & Scripts (*.bat *.cmd *.exe *.lnk *.ps1 *.py *.vbs);;All Files (*.*)"
        )
        if filePath:
            norm_path = os.path.normpath(filePath)
            self.e_custom_param.setText(norm_path)
            idx = self.cbo_custom_type.findData("launch_app")
            if idx >= 0:
                self.cbo_custom_type.setCurrentIndex(idx)

            # Auto-suggest Title if currently default/blank
            cur_title = self.e_title.text().strip()
            if not cur_title or cur_title in ("OFFICER APPROVAL", "NEW KEY", "MY ACTION"):
                base_name = os.path.splitext(os.path.basename(norm_path))[0]
                clean_title = base_name.replace("_", " ").replace("-", " ").upper()
                self.e_title.setText(clean_title)

            # Auto-suggest icon based on extension
            ext = os.path.splitext(norm_path)[1].lower()
            if ext in ('.bat', '.cmd', '.ps1'):
                self.e_icon.setText("⚙️")
            elif ext in ('.exe', '.lnk'):
                self.e_icon.setText("🚀")
            elif ext in ('.py', '.vbs'):
                self.e_icon.setText("📜")

    def _build_shortcuts_tab(self):
        layout = QtWidgets.QVBoxLayout(self.tab_shortcuts)
        layout.setContentsMargins(14, 12, 14, 12)
        layout.setSpacing(8)

        # Search / Filter bar
        search_box = QtWidgets.QHBoxLayout()
        lbl_s = QtWidgets.QLabel("🔍 Search Shortcuts:")
        lbl_s.setStyleSheet("font-size: 11px; font-weight: bold; color: #D4AF37;")
        search_box.addWidget(lbl_s)

        self.e_search = QtWidgets.QLineEdit()
        self.e_search.setPlaceholderText("Type e.g. 'snip', 'desktop', 'lock', 'copy'...")
        self.e_search.textChanged.connect(self._filter_shortcuts)
        search_box.addWidget(self.e_search)
        layout.addLayout(search_box)

        # List Widget of Shortcuts
        self.list_shortcuts = QtWidgets.QListWidget()
        self.list_shortcuts.setStyleSheet("""
            QListWidget {
                background-color: #17181F;
                border: 1px solid #2F3240;
                border-radius: 6px;
                padding: 4px;
            }
            QListWidget::item {
                background-color: #21232D;
                border-radius: 4px;
                padding: 8px 10px;
                margin-bottom: 3px;
            }
            QListWidget::item:hover {
                background-color: #2C2F3D;
            }
            QListWidget::item:selected {
                background-color: #3A3521;
                border: 1px solid #D4AF37;
                color: #FFFFFF;
            }
        """)
        self._populate_shortcuts()
        self.list_shortcuts.itemClicked.connect(self._on_shortcut_selected)
        layout.addWidget(self.list_shortcuts, 1)

    def _populate_shortcuts(self, query=""):
        self.list_shortcuts.clear()
        q = query.lower().strip()
        for sc in TOP_50_SHORTCUTS:
            text = f"{sc['icon']}  [{sc['badge']}]  {sc['title']} — {sc['desc']}"
            if not q or q in text.lower() or q in sc['keys'].lower():
                item = QtWidgets.QListWidgetItem(text)
                item.setData(QtCore.Qt.ItemDataRole.UserRole, sc)
                self.list_shortcuts.addItem(item)

    def _filter_shortcuts(self, text):
        self._populate_shortcuts(text)

    def _on_shortcut_selected(self, item):
        sc = item.data(QtCore.Qt.ItemDataRole.UserRole)
        if sc:
            self.e_title.setText(sc["title"])
            self.e_icon.setText(sc["icon"])

    def _paste_from_clipboard(self):
        try:
            win32clipboard.OpenClipboard()
            data = win32clipboard.GetClipboardData(win32clipboard.CF_UNICODETEXT)
            win32clipboard.CloseClipboard()
            if data:
                self.txt_copied.setPlainText(data)
        except Exception:
            pass

    def _save_key(self):
        title = self.e_title.text().strip()
        if not title:
            QtWidgets.QMessageBox.warning(self, "Validation", "Please enter a Title for this key.")
            return

        icon = self.e_icon.text().strip() or "🎹"
        current_tab_idx = self.tabs.currentIndex()

        idx = self.key_index if self.key_index is not None else 0
        n_num, n_name = NOTES_PALETTE[idx % len(NOTES_PALETTE)]

        if current_tab_idx == 0:
            # 1. Copied Content
            act_type = "paste_text"
            text_val = self.txt_copied.toPlainText().strip()
            subtitle = "Text Snippet"
            badge = "Snippet"
            auto_paste = self.chk_auto_paste.isChecked()
        elif current_tab_idx == 1:
            # 2. Installed Applications
            selected_items = self.list_installed_apps.selectedItems()
            if not selected_items:
                QtWidgets.QMessageBox.warning(self, "Validation", "Please select an installed application from the list.")
                return
            app_info = selected_items[0].data(QtCore.Qt.ItemDataRole.UserRole)
            act_type = "launch_app"
            text_val = app_info["target"]
            subtitle = "Launch App"
            badge = "App"
            auto_paste = False
            # ensure title/icon are set
            if not self.e_title.text().strip() or self.e_title.text().strip() in ("OFFICER APPROVAL", "NEW KEY", "MY ACTION"):
                clean_name = app_info["name"].replace("_", " ").replace("-", " ").strip()
                title = clean_name.upper()
                self.e_title.setText(title)
            if not self.e_icon.text().strip() or self.e_icon.text().strip() == "📋":
                icon = app_info["icon"]
                self.e_icon.setText(icon)
        elif current_tab_idx == 2:
            # 3. Custom Action
            act_type = self.cbo_custom_type.currentData()
            text_val = self.e_custom_param.text().strip()
            clean_t = text_val.strip('"').strip("'")
            is_script_or_app = (
                clean_t.lower().endswith(('.bat', '.cmd', '.exe', '.lnk', '.ps1', '.py', '.vbs', '.msi'))
                or os.path.exists(clean_t)
                or (len(clean_t) > 2 and clean_t[1] == ':' and '\\' in clean_t)
                or clean_t.lower().startswith(('shell:', 'ms-settings:'))
            )
            if act_type == "launch_app" or (act_type == "custom_url" and is_script_or_app):
                act_type = "launch_app"
                if clean_t.lower().endswith(('.bat', '.cmd', '.ps1', '.py', '.vbs')):
                    subtitle = "Run Script"
                    badge = "Script"
                else:
                    subtitle = "Launch App"
                    badge = "App"
            elif act_type == "custom_url":
                subtitle = "Web Portal"
                badge = "URL"
            elif act_type == "kill_tasks":
                subtitle = "Kill Task"
                badge = "Rescue"
            elif act_type == "clean_system":
                subtitle = "Recycle & Cache"
                badge = "Purge"
            elif act_type == "privacy_shield":
                subtitle = "Boss Key"
                badge = "Privacy"
            elif act_type == "toggle_music":
                subtitle = "Focus Audio"
                badge = "Music"
            else:
                subtitle = "Custom Action"
                badge = "Custom"
            auto_paste = False
        else:
            # 4. Top 50 Shortcut
            selected_items = self.list_shortcuts.selectedItems()
            if not selected_items:
                QtWidgets.QMessageBox.warning(self, "Validation", "Please select a shortcut from the list.")
                return
            sc = selected_items[0].data(QtCore.Qt.ItemDataRole.UserRole)
            act_type = "shortcut"
            text_val = sc["keys"]
            subtitle = sc["subtitle"]
            badge = sc["badge"]
            auto_paste = False

        key_data = {
            "id": self.existing_key.get("id") if self.existing_key else f"key_{title.lower().replace(' ', '_')}",
            "note": n_num,
            "note_name": n_name,
            "title": title.upper(),
            "subtitle": subtitle,
            "icon": icon,
            "action": act_type,
            "badge": badge,
            "text": text_val,
            "auto_paste": auto_paste
        }

        self.on_save(key_data, self.key_index)
        self.accept()
