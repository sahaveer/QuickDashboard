import os
from PyQt6 import QtWidgets, QtCore, QtGui
from actions.screenshot import open_in_explorer
from actions.snippet import set_clipboard_text

class PyQtSavedPopup(QtWidgets.QWidget):
    """
    Ultra-modern self-closing screenshot notification popup in PyQt6.
    Displays file location, badges, explorer button, and auto-closing countdown.
    """
    _current_instance = None

    @classmethod
    def show_popup(cls, filepath: str, is_snippet: bool = False, timeout_seconds: int = 6):
        if cls._current_instance is not None:
            try:
                cls._current_instance.close()
            except Exception:
                pass
        cls._current_instance = cls(filepath, is_snippet=is_snippet, timeout_seconds=timeout_seconds)
        cls._current_instance.show()

    def __init__(self, filepath: str, is_snippet: bool = False, timeout_seconds: int = 6):
        super().__init__()
        self.filepath = os.path.abspath(filepath)
        self.filename = os.path.basename(self.filepath)
        self.folder = os.path.dirname(self.filepath)
        self.is_snippet = is_snippet
        self.remaining = timeout_seconds
        self.is_paused = False

        self.setWindowFlags(QtCore.Qt.WindowType.FramelessWindowHint | QtCore.Qt.WindowType.WindowStaysOnTopHint | QtCore.Qt.WindowType.Tool)
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground)

        self._build_ui()
        self._position_on_screen()

        # Timer
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self._tick)
        self.timer.start(1000)

    def _build_ui(self):
        layout = QtWidgets.QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)

        # Outer Card with luxury gold border & dark glass
        self.card = QtWidgets.QFrame(self)
        self.card.setStyleSheet("""
            QFrame {
                background-color: #18191F;
                border: 2px solid #D4AF37;
                border-radius: 12px;
            }
        """)

        # Soft drop shadow
        shadow = QtWidgets.QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(24)
        shadow.setColor(QtGui.QColor(0, 0, 0, 180))
        shadow.setOffset(0, 6)
        self.card.setGraphicsEffect(shadow)

        card_layout = QtWidgets.QVBoxLayout(self.card)
        card_layout.setContentsMargins(18, 16, 18, 14)
        card_layout.setSpacing(10)

        # Top Header row
        top_row = QtWidgets.QHBoxLayout()
        icon_str = "✂️" if self.is_snippet else "📸"
        lbl_icon = QtWidgets.QLabel(icon_str)
        lbl_icon.setStyleSheet("font-size: 22px; border: none;")
        top_row.addWidget(lbl_icon)

        title_str = "Area Snippet Saved & Copied!" if self.is_snippet else "Full Snapshot Saved & Copied!"
        lbl_title = QtWidgets.QLabel(title_str)
        lbl_title.setStyleSheet("font-size: 15px; font-weight: bold; color: #FFFFFF; font-family: 'Segoe UI'; border: none;")
        top_row.addWidget(lbl_title, 1)

        btn_close = QtWidgets.QPushButton("✕")
        btn_close.setCursor(QtCore.Qt.CursorShape.PointingHandCursor)
        btn_close.setStyleSheet("""
            QPushButton {
                background: transparent;
                color: #8E9099;
                font-size: 14px;
                font-weight: bold;
                border: none;
                padding: 4px;
            }
            QPushButton:hover {
                color: #FF5252;
            }
        """)
        btn_close.clicked.connect(self.close)
        top_row.addWidget(btn_close)
        card_layout.addLayout(top_row)

        # Badges row
        badge_row = QtWidgets.QHBoxLayout()
        b1 = QtWidgets.QLabel("✅ SAVED TO DISK")
        b1.setStyleSheet("background-color: #1B382B; color: #4ECA5D; font-size: 10px; font-weight: bold; border-radius: 4px; padding: 3px 8px; border: 1px solid #285A3C;")
        badge_row.addWidget(b1)

        b2 = QtWidgets.QLabel("📋 IN CLIPBOARD (Ready for Ctrl+V)")
        b2.setStyleSheet("background-color: #1E324A; color: #42A5F5; font-size: 10px; font-weight: bold; border-radius: 4px; padding: 3px 8px; border: 1px solid #28527A;")
        badge_row.addWidget(b2)
        badge_row.addStretch()
        card_layout.addLayout(badge_row)

        # Location box
        loc_box = QtWidgets.QFrame()
        loc_box.setStyleSheet("""
            QFrame {
                background-color: #23252E;
                border: 1px solid #333644;
                border-radius: 8px;
                padding: 8px;
            }
        """)
        loc_layout = QtWidgets.QVBoxLayout(loc_box)
        loc_layout.setContentsMargins(10, 8, 10, 8)
        loc_layout.setSpacing(4)

        lbl_fn_title = QtWidgets.QLabel("FILE NAME:")
        lbl_fn_title.setStyleSheet("font-size: 9px; font-weight: bold; color: #D4AF37; border: none;")
        loc_layout.addWidget(lbl_fn_title)

        lbl_fn = QtWidgets.QLabel(self.filename)
        lbl_fn.setStyleSheet("font-size: 12px; font-weight: bold; color: #FFFFFF; font-family: 'Consolas'; border: none;")
        loc_layout.addWidget(lbl_fn)

        lbl_dir_title = QtWidgets.QLabel("SAVED IN FOLDER:")
        lbl_dir_title.setStyleSheet("font-size: 9px; font-weight: bold; color: #D4AF37; border: none; margin-top: 4px;")
        loc_layout.addWidget(lbl_dir_title)

        lbl_fp = QtWidgets.QLabel(self.folder)
        lbl_fp.setStyleSheet("font-size: 11px; color: #90CAF9; font-family: 'Consolas'; border: none;")
        lbl_fp.setWordWrap(True)
        loc_layout.addWidget(lbl_fp)

        card_layout.addWidget(loc_box)

        # Action Buttons
        btn_row = QtWidgets.QHBoxLayout()
        btn_open = QtWidgets.QPushButton("📂  Open in File Explorer")
        btn_open.setCursor(QtCore.Qt.CursorShape.PointingHandCursor)
        btn_open.setStyleSheet("""
            QPushButton {
                background-color: #D4AF37;
                color: #121212;
                font-weight: bold;
                font-size: 12px;
                border-radius: 6px;
                padding: 7px 16px;
                border: none;
            }
            QPushButton:hover {
                background-color: #F3CF65;
            }
        """)
        btn_open.clicked.connect(self._open_explorer)
        btn_row.addWidget(btn_open)

        btn_copy = QtWidgets.QPushButton("📋  Copy Path")
        btn_copy.setCursor(QtCore.Qt.CursorShape.PointingHandCursor)
        btn_copy.setStyleSheet("""
            QPushButton {
                background-color: #2E303A;
                color: #E0E0E0;
                font-size: 11px;
                border-radius: 6px;
                padding: 7px 12px;
                border: 1px solid #434654;
            }
            QPushButton:hover {
                background-color: #3E4250;
                color: #FFFFFF;
            }
        """)
        btn_copy.clicked.connect(self._copy_path)
        btn_row.addWidget(btn_copy)
        btn_row.addStretch()
        card_layout.addLayout(btn_row)

        # Countdown label
        self.lbl_timer = QtWidgets.QLabel(f"Auto-closing in {self.remaining}s... (hover mouse to pause)")
        self.lbl_timer.setStyleSheet("font-size: 10px; font-style: italic; color: #7E808A; border: none;")
        self.lbl_timer.setAlignment(QtCore.Qt.AlignmentFlag.AlignRight)
        card_layout.addWidget(self.lbl_timer)

        layout.addWidget(self.card)
        self.setFixedWidth(520)

    def _position_on_screen(self):
        screen = QtWidgets.QApplication.primaryScreen().availableGeometry()
        w = 520
        h = self.sizeHint().height() or 220
        x = screen.right() - w - 24
        y = screen.bottom() - h - 30
        self.setGeometry(x, y, w, h)

    def enterEvent(self, event):
        self.is_paused = True
        self.lbl_timer.setText("Timer paused • Click to open or dismiss")
        self.lbl_timer.setStyleSheet("font-size: 10px; font-weight: bold; color: #D4AF37; border: none;")
        super().enterEvent(event)

    def leaveEvent(self, event):
        self.is_paused = False
        self.lbl_timer.setText(f"Auto-closing in {self.remaining}s...")
        self.lbl_timer.setStyleSheet("font-size: 10px; font-style: italic; color: #7E808A; border: none;")
        super().leaveEvent(event)

    def _open_explorer(self):
        open_in_explorer(self.filepath)
        self.close()

    def _copy_path(self):
        set_clipboard_text(self.filepath)
        self.lbl_timer.setText("✓ Full path copied to clipboard!")
        self.lbl_timer.setStyleSheet("font-size: 10px; font-weight: bold; color: #4ECA5D; border: none;")

    def _tick(self):
        if not self.is_paused:
            self.remaining -= 1
            if self.remaining <= 0:
                self.close()
                return
            self.lbl_timer.setText(f"Auto-closing in {self.remaining}s... (hover to pause)")
