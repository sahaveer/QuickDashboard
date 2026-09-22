import os
import tkinter as tk
from actions.screenshot import open_in_explorer
from actions.snippet import set_clipboard_text

class SavedNotificationWindow:
    """
    Luxury, self-closing executive notification window.
    Clearly displays where the screenshot was saved, provides 1-click
    Explorer and Copy Path buttons, and auto-closes after a visible countdown.
    """
    _current_instance = None

    @classmethod
    def show(cls, parent, filepath: str, is_snippet: bool = False, timeout_seconds: int = 6):
        if cls._current_instance and cls._current_instance.win.winfo_exists():
            try:
                cls._current_instance.win.destroy()
            except Exception:
                pass

        cls._current_instance = cls(parent, filepath, is_snippet=is_snippet, timeout_seconds=timeout_seconds)

    def __init__(self, parent, filepath: str, is_snippet: bool = False, timeout_seconds: int = 6):
        self.parent = parent
        self.filepath = os.path.abspath(filepath)
        self.filename = os.path.basename(self.filepath)
        self.folder = os.path.dirname(self.filepath)
        self.is_snippet = is_snippet
        self.remaining = timeout_seconds
        self.is_paused = False

        self.win = tk.Toplevel(parent)
        self.win.title("Snapshot Saved")
        self.win.overrideredirect(True)
        self.win.attributes("-topmost", True)
        self.win.attributes("-alpha", 0.97)
        self.win.config(bg="#1E1F24")

        # Outer Gold Border
        outer = tk.Frame(self.win, bg="#D4AF37", bd=2)
        outer.pack(fill="both", expand=True)

        body = tk.Frame(outer, bg="#18191E", padx=18, pady=14)
        body.pack(fill="both", expand=True)

        # Header with icon
        hdr = tk.Frame(body, bg="#18191E")
        hdr.pack(fill="x", pady=(0, 10))

        icon_char = "✂️" if is_snippet else "📸"
        lbl_icon = tk.Label(hdr, text=icon_char, font=("Segoe UI Emoji", 20), bg="#18191E", fg="#D4AF37")
        lbl_icon.pack(side="left", padx=(0, 10))

        title_text = "Area Snippet Saved & Copied!" if is_snippet else "Full Snapshot Saved & Copied!"
        lbl_title = tk.Label(hdr, text=title_text, font=("Segoe UI", 11, "bold"), fg="#FFFFFF", bg="#18191E")
        lbl_title.pack(side="left", anchor="w")

        btn_close = tk.Label(hdr, text="✕", font=("Segoe UI", 10, "bold"), fg="#8E9099", bg="#18191E", cursor="hand2")
        btn_close.pack(side="right")
        btn_close.bind("<Button-1>", lambda e: self.win.destroy())

        # Badges (Saved + Clipboard)
        badge_frame = tk.Frame(body, bg="#18191E")
        badge_frame.pack(fill="x", pady=(0, 10))

        b1 = tk.Label(badge_frame, text="✅ SAVED TO DISK", font=("Segoe UI", 7, "bold"), bg="#1B382B", fg="#4ECA5D", padx=6, pady=2)
        b1.pack(side="left", padx=(0, 8))

        b2 = tk.Label(badge_frame, text="📋 COPIED TO CLIPBOARD (Ready for Ctrl+V)", font=("Segoe UI", 7, "bold"), bg="#1E324A", fg="#42A5F5", padx=6, pady=2)
        b2.pack(side="left")

        # Exact Path Info Box
        info_box = tk.Frame(body, bg="#23252E", padx=12, pady=10, bd=1, relief="solid")
        info_box.pack(fill="x", pady=(0, 12))

        # File Name
        f_row = tk.Frame(info_box, bg="#23252E")
        f_row.pack(fill="x", pady=(0, 4))
        tk.Label(f_row, text="File Name:", font=("Segoe UI", 8, "bold"), fg="#D4AF37", bg="#23252E", width=10, anchor="w").pack(side="left")
        lbl_fn = tk.Label(f_row, text=self.filename, font=("Consolas", 9, "bold"), fg="#FFFFFF", bg="#23252E", anchor="w")
        lbl_fn.pack(side="left", fill="x", expand=True)

        # Folder Path
        p_row = tk.Frame(info_box, bg="#23252E")
        p_row.pack(fill="x")
        tk.Label(p_row, text="Location:", font=("Segoe UI", 8, "bold"), fg="#D4AF37", bg="#23252E", width=10, anchor="w").pack(side="left")
        lbl_fp = tk.Label(p_row, text=self.folder, font=("Consolas", 8), fg="#90CAF9", bg="#23252E", anchor="w", wraplength=380, justify="left")
        lbl_fp.pack(side="left", fill="x", expand=True)

        # Action Buttons
        btn_bar = tk.Frame(body, bg="#18191E")
        btn_bar.pack(fill="x", pady=(0, 8))

        btn_open = tk.Button(
            btn_bar,
            text="📂  Open in File Explorer",
            font=("Segoe UI", 9, "bold"),
            bg="#D4AF37",
            fg="#121212",
            activebackground="#F3CF65",
            activeforeground="#121212",
            bd=0,
            padx=14,
            pady=6,
            cursor="hand2",
            command=self._open_explorer
        )
        btn_open.pack(side="left", padx=(0, 8))

        btn_copy_path = tk.Button(
            btn_bar,
            text="📋 Copy Path",
            font=("Segoe UI", 8),
            bg="#2E303A",
            fg="#E0E0E0",
            activebackground="#3E4250",
            activeforeground="#FFFFFF",
            bd=0,
            padx=10,
            pady=6,
            cursor="hand2",
            command=self._copy_path
        )
        btn_copy_path.pack(side="left")

        # Countdown label at bottom
        self.lbl_timer = tk.Label(
            body,
            text=f"Auto-closing in {self.remaining}s... (hover to pause)",
            font=("Segoe UI", 8, "italic"),
            fg="#7E808A",
            bg="#18191E",
            anchor="e"
        )
        self.lbl_timer.pack(side="bottom", fill="x")

        # Position dialog gracefully on screen (lower right, right above taskbar)
        self.win.update_idletasks()
        w = 520
        h = self.win.winfo_reqheight()
        sw = self.win.winfo_screenwidth()
        sh = self.win.winfo_screenheight()

        x = sw - w - 25
        y = sh - h - 75
        self.win.geometry(f"{w}x{h}+{x}+{y}")

        # Pause countdown on mouse hover so user can read / click peacefully
        self.win.bind("<Enter>", lambda e: self._set_paused(True))
        self.win.bind("<Leave>", lambda e: self._set_paused(False))
        self.win.bind("<Escape>", lambda e: self.win.destroy())

        # Start countdown
        self.win.after(1000, self._tick)

    def _open_explorer(self):
        open_in_explorer(self.filepath)
        self.win.destroy()

    def _copy_path(self):
        set_clipboard_text(self.filepath)
        self.lbl_timer.config(text="✓ Full path copied to clipboard!", fg="#4ECA5D")

    def _set_paused(self, paused: bool):
        self.is_paused = paused
        if paused:
            self.lbl_timer.config(text="Timer paused • Click to open or dismiss", fg="#D4AF37")
        else:
            self.lbl_timer.config(text=f"Auto-closing in {self.remaining}s...", fg="#7E808A")

    def _tick(self):
        if not self.win.winfo_exists():
            return

        if not self.is_paused:
            self.remaining -= 1
            if self.remaining <= 0:
                self._fade_out()
                return
            self.lbl_timer.config(text=f"Auto-closing in {self.remaining}s... (hover to pause)", fg="#7E808A")

        self.win.after(1000, self._tick)

    def _fade_out(self):
        if not self.win.winfo_exists():
            return
        try:
            cur_alpha = self.win.attributes("-alpha")
            if cur_alpha > 0.15:
                self.win.attributes("-alpha", cur_alpha - 0.2)
                self.win.after(35, self._fade_out)
            else:
                self.win.destroy()
        except Exception:
            pass
