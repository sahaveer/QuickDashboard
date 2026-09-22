import tkinter as tk
from actions.screenshot import open_in_explorer, get_default_screenshots_dir

class TitlePromptDialog:
    """
    Executive Snapshot Dialog:
    - Choose between Full Screen vs Area Snippet
    - Enter optional Title / Tag
    - Direct button to Open Screenshots Folder in Windows File Explorer
    """
    def __init__(self, parent, on_full_screen, on_area_snippet):
        self.parent = parent
        self.on_full_screen = on_full_screen
        self.on_area_snippet = on_area_snippet

        self.win = tk.Toplevel(parent)
        self.win.title("Executive Snapshot & Snipping Tool")
        self.win.geometry("450x240")
        self.win.attributes("-topmost", True)
        self.win.config(bg="#1E1F24")

        # Center on screen
        self.win.update_idletasks()
        sw = self.win.winfo_screenwidth()
        sh = self.win.winfo_screenheight()
        self.win.geometry(f"450x240+{(sw - 450)//2}+{(sh - 240)//2}")

        self._build_ui()

    def _build_ui(self):
        # Header
        hdr = tk.Frame(self.win, bg="#141518", padx=16, pady=10)
        hdr.pack(fill="x")

        tk.Label(hdr, text="📸 Executive Snapshot & Snipping Tool", font=("Segoe UI", 11, "bold"), fg="#D4AF37", bg="#141518").pack(anchor="w")

        body = tk.Frame(self.win, bg="#1E1F24", padx=20, pady=12)
        body.pack(fill="both", expand=True)

        tk.Label(body, text="Snapshot Title / Tag (Optional):", font=("Segoe UI", 9, "bold"), fg="#FFFFFF", bg="#1E1F24").pack(anchor="w")
        tk.Label(body, text="E.g. 'Budget_Review' (or leave blank to use timestamp):", font=("Segoe UI", 8), fg="#9E9E9E", bg="#1E1F24").pack(anchor="w")

        self.title_var = tk.StringVar()
        self.entry = tk.Entry(body, textvariable=self.title_var, font=("Segoe UI", 10), bg="#2B2D35", fg="#FFF", insertbackground="#D4AF37", bd=1)
        self.entry.pack(fill="x", pady=(6, 12))
        self.entry.focus_set()
        self.entry.bind("<Return>", lambda e: self._choose_full())
        self.entry.bind("<Escape>", lambda e: self.win.destroy())

        # Buttons: Choice between Full Screen vs Select Area
        btn_box = tk.Frame(body, bg="#1E1F24")
        btn_box.pack(fill="x", pady=(2, 8))

        btn_area = tk.Button(
            btn_box,
            text="✂️  Select Area (Snippet)",
            font=("Segoe UI", 9, "bold"),
            bg="#2E303A",
            fg="#D4AF37",
            activebackground="#D4AF37",
            activeforeground="#121212",
            bd=1,
            relief="solid",
            padx=12,
            pady=7,
            cursor="hand2",
            command=self._choose_area
        )
        btn_area.pack(side="left", fill="x", expand=True, padx=(0, 6))

        btn_full = tk.Button(
            btn_box,
            text="🖥️  Full Screen Capture",
            font=("Segoe UI", 9, "bold"),
            bg="#D4AF37",
            fg="#121212",
            activebackground="#FFD700",
            activeforeground="#121212",
            bd=0,
            padx=12,
            pady=7,
            cursor="hand2",
            command=self._choose_full
        )
        btn_full.pack(side="right", fill="x", expand=True, padx=(6, 0))

        # Bottom Bar: Folder link & Cancel
        bbar = tk.Frame(self.win, bg="#141518", padx=16, pady=8)
        bbar.pack(fill="x", side="bottom")

        btn_folder = tk.Button(
            bbar,
            text="📂 Open Screenshots Folder",
            font=("Segoe UI", 8),
            bg="#141518",
            fg="#4ECA5D",
            activebackground="#141518",
            activeforeground="#81C784",
            bd=0,
            cursor="hand2",
            command=lambda: open_in_explorer()
        )
        btn_folder.pack(side="left")

        btn_cancel = tk.Button(
            bbar,
            text="Cancel",
            font=("Segoe UI", 8),
            bg="#33353D",
            fg="#FFF",
            bd=0,
            padx=12,
            pady=3,
            cursor="hand2",
            command=self.win.destroy
        )
        btn_cancel.pack(side="right")

    def _choose_full(self):
        title = self.title_var.get().strip()
        self.win.destroy()
        if self.on_full_screen:
            self.on_full_screen(title)

    def _choose_area(self):
        title = self.title_var.get().strip()
        self.win.destroy()
        if self.on_area_snippet:
            self.on_area_snippet(title)
