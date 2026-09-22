import os
import time
import logging
from PyQt6 import QtWidgets, QtCore, QtGui
from actions.screenshot import open_in_explorer, get_default_screenshots_dir

class PyQtSnapshotDialog(QtWidgets.QDialog):
    """
    Executive Snapshot Dialog in PyQt6:
    - Choose between Full Screen Snapshot vs Area Snippet
    - Enter optional Title / Tag
    - Direct button to Open Screenshots Folder in Windows File Explorer
    """
    def __init__(self, parent, on_full_screen, on_area_snippet):
        super().__init__(parent)
        self.on_full_screen = on_full_screen
        self.on_area_snippet = on_area_snippet

        self.setWindowTitle("📸 Executive Snapshot & Snipping Tool")
        self.setFixedSize(500, 260)
        self.setWindowFlags(QtCore.Qt.WindowType.Dialog | QtCore.Qt.WindowType.WindowStaysOnTopHint)
        self.setStyleSheet("""
            QDialog {
                background-color: #17181D;
                color: #FFFFFF;
                font-family: 'Segoe UI';
                border: 2px solid #8C7026;
                border-radius: 10px;
            }
            QLabel {
                color: #E0E0E0;
            }
            QLineEdit {
                background-color: #242630;
                color: #FFFFFF;
                border: 1px solid #3B3E4F;
                border-radius: 6px;
                padding: 8px 12px;
                font-size: 13px;
            }
            QLineEdit:focus {
                border: 1px solid #D4AF37;
            }
        """)

        self._build_ui()
        self._center()

    def _center(self):
        screen = QtWidgets.QApplication.screenAt(QtGui.QCursor.pos()) or QtWidgets.QApplication.primaryScreen()
        if screen:
            geom = screen.availableGeometry()
            x = geom.x() + (geom.width() - self.width()) // 2
            y = geom.y() + (geom.height() - self.height()) // 2
            self.move(x, y)

    def _build_ui(self):
        layout = QtWidgets.QVBoxLayout(self)
        layout.setContentsMargins(20, 18, 20, 18)
        layout.setSpacing(12)

        # Header
        hdr = QtWidgets.QHBoxLayout()
        lbl_h = QtWidgets.QLabel("📸  Executive Snapshot & Snipping Tool")
        lbl_h.setStyleSheet("font-size: 14px; font-weight: bold; color: #D4AF37; border: none;")
        hdr.addWidget(lbl_h)
        hdr.addStretch()
        layout.addLayout(hdr)

        # Title prompt
        lbl_sub = QtWidgets.QLabel("Enter optional title/tag (or leave blank for timestamp):")
        lbl_sub.setStyleSheet("font-size: 11px; color: #A0A3B0; border: none;")
        layout.addWidget(lbl_sub)

        self.e_title = QtWidgets.QLineEdit()
        self.e_title.setPlaceholderText("e.g. Budget_Briefing, Contract_Page1, Audit_Report")
        self.e_title.returnPressed.connect(self._choose_full)
        layout.addWidget(self.e_title)

        # Choice Buttons
        btn_box = QtWidgets.QHBoxLayout()
        btn_box.setSpacing(10)

        btn_area = QtWidgets.QPushButton("✂️  Select Area (Snippet)")
        btn_area.setCursor(QtCore.Qt.CursorShape.PointingHandCursor)
        btn_area.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #2C2E3A, stop:1 #20222A);
                color: #D4AF37;
                font-size: 11px;
                font-weight: bold;
                border: 1px solid #8C7026;
                border-radius: 6px;
                padding: 10px 14px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #3A3C4C, stop:1 #2C2E3A);
                border: 1px solid #F3CF65;
                color: #FFFFFF;
            }
        """)
        btn_area.clicked.connect(self._choose_area)
        btn_box.addWidget(btn_area, 1)

        btn_full = QtWidgets.QPushButton("📸  Full Screen Capture")
        btn_full.setCursor(QtCore.Qt.CursorShape.PointingHandCursor)
        btn_full.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #B89327, stop:1 #8C7026);
                color: #121212;
                font-size: 11px;
                font-weight: bold;
                border: none;
                border-radius: 6px;
                padding: 10px 14px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #D4AF37, stop:1 #A88620);
                color: #000000;
            }
        """)
        btn_full.clicked.connect(self._choose_full)
        btn_box.addWidget(btn_full, 1)
        layout.addLayout(btn_box)

        # Bottom Bar: Folder & Cancel
        bot_bar = QtWidgets.QHBoxLayout()
        btn_folder = QtWidgets.QPushButton("📂 Open Screenshots Folder")
        btn_folder.setCursor(QtCore.Qt.CursorShape.PointingHandCursor)
        btn_folder.setStyleSheet("background: transparent; color: #4ECA5D; font-size: 10px; font-weight: bold; border: none;")
        btn_folder.clicked.connect(lambda: open_in_explorer())
        bot_bar.addWidget(btn_folder)

        bot_bar.addStretch()

        btn_cancel = QtWidgets.QPushButton("Cancel (Esc)")
        btn_cancel.setCursor(QtCore.Qt.CursorShape.PointingHandCursor)
        btn_cancel.setStyleSheet("background: transparent; color: #8A8D98; font-size: 10px; border: none;")
        btn_cancel.clicked.connect(self.reject)
        bot_bar.addWidget(btn_cancel)

        layout.addLayout(bot_bar)

    def _choose_full(self):
        title = self.e_title.text().strip()
        self.accept()
        if self.on_full_screen:
            self.on_full_screen(title)

    def _choose_area(self):
        title = self.e_title.text().strip()
        self.accept()
        if self.on_area_snippet:
            self.on_area_snippet(title)


class PyQtSnipperOverlay(QtWidgets.QWidget):
    """
    Interactive fullscreen snipping overlay in PyQt6.
    Allows user to click and drag to select any rectangular region on the screen.
    """
    def __init__(self, on_complete, on_cancel=None):
        super().__init__()
        self.on_complete = on_complete
        self.on_cancel = on_cancel

        self.start_pt = None
        self.current_pt = None
        self.is_drawing = False

        self.setWindowFlags(
            QtCore.Qt.WindowType.FramelessWindowHint
            | QtCore.Qt.WindowType.WindowStaysOnTopHint
            | QtCore.Qt.WindowType.Tool
        )
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setCursor(QtCore.Qt.CursorShape.CrossCursor)

        # Cover the entire virtual desktop
        screen = QtWidgets.QApplication.primaryScreen()
        virtual_geom = screen.virtualGeometry() if screen else QtCore.QRect(0, 0, 1920, 1080)
        self.setGeometry(virtual_geom)
        self.show()

    def paintEvent(self, event: QtGui.QPaintEvent):
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)

        # 1. Dark semi-transparent dimming across screen
        painter.fillRect(self.rect(), QtGui.QColor(0, 0, 0, 90))

        # 2. Top Instructions Banner
        banner_w, banner_h = 360, 38
        banner_x = (self.width() - banner_w) // 2
        banner_y = 20
        banner_rect = QtCore.QRect(banner_x, banner_y, banner_w, banner_h)

        painter.setPen(QtGui.QPen(QtGui.QColor("#D4AF37"), 1.5))
        painter.setBrush(QtGui.QBrush(QtGui.QColor(24, 25, 30, 230)))
        painter.drawRoundedRect(banner_rect, 6, 6)

        painter.setPen(QtGui.QColor("#FFFFFF"))
        painter.setFont(QtGui.QFont("Segoe UI", 10, QtGui.QFont.Weight.Bold))
        painter.drawText(banner_rect, QtCore.Qt.AlignmentFlag.AlignCenter, "✂️ Click & drag to snip  •  ESC to cancel")

        # 3. Selected Snippet Rectangle
        if self.is_drawing and self.start_pt and self.current_pt:
            rect = QtCore.QRect(self.start_pt, self.current_pt).normalized()

            # Clear hole for selection
            painter.setCompositionMode(QtGui.QPainter.CompositionMode.CompositionMode_Clear)
            painter.fillRect(rect, QtGui.QColor(0, 0, 0, 0))

            # Draw gold border around selection
            painter.setCompositionMode(QtGui.QPainter.CompositionMode.CompositionMode_SourceOver)
            pen = QtGui.QPen(QtGui.QColor("#FFD700"), 2, QtCore.Qt.PenStyle.DashLine)
            painter.setPen(pen)
            painter.setBrush(QtCore.Qt.BrushStyle.NoBrush)
            painter.drawRect(rect)

            # Dimensions tooltip
            dim_text = f"{rect.width()} × {rect.height()}"
            painter.setPen(QtGui.QColor("#FFFFFF"))
            painter.setFont(QtGui.QFont("Segoe UI", 9, QtGui.QFont.Weight.Bold))
            painter.fillRect(rect.left(), max(0, rect.top() - 20), 80, 18, QtGui.QColor(18, 19, 23, 210))
            painter.drawText(rect.left() + 6, max(14, rect.top() - 6), dim_text)

    def mousePressEvent(self, event: QtGui.QMouseEvent):
        if event.button() == QtCore.Qt.MouseButton.LeftButton:
            self.start_pt = event.pos()
            self.current_pt = event.pos()
            self.is_drawing = True
            self.update()

    def mouseMoveEvent(self, event: QtGui.QMouseEvent):
        if self.is_drawing:
            self.current_pt = event.pos()
            self.update()

    def mouseReleaseEvent(self, event: QtGui.QMouseEvent):
        if event.button() == QtCore.Qt.MouseButton.LeftButton and self.is_drawing:
            self.is_drawing = False
            if self.start_pt and self.current_pt:
                rect = QtCore.QRect(self.start_pt, self.current_pt).normalized()
                if rect.width() > 15 and rect.height() > 15:
                    self.close()
                    # Convert to screen coordinates (left, top, right, bottom)
                    bbox = (rect.left(), rect.top(), rect.right(), rect.bottom())
                    if self.on_complete:
                        self.on_complete(bbox)
                    return
            self._cancel()

    def keyPressEvent(self, event: QtGui.QKeyEvent):
        if event.key() == QtCore.Qt.Key.Key_Escape:
            self._cancel()

    def _cancel(self):
        self.close()
        if self.on_cancel:
            self.on_cancel()
