import tkinter as tk
from tkinter import ttk, messagebox
import win32clipboard

from actions.shortcuts import TOP_50_SHORTCUTS

NOTES_PALETTE = [
    (60, "C4"), (62, "D4"), (64, "E4"), (65, "F4"),
    (67, "G4"), (69, "A4"), (71, "B4"), (72, "C5"),
    (74, "D5"), (76, "E5"), (77, "F5"), (79, "G5")
]

class AddKeyDialog:
    """
    Executive Piano Key Builder Dialog.
    Ordered by priority:
      Option 1: 📋 Copied Content / Rapid Snippet (with paste bar & auto-paste)
      Option 2: 🛠️ Custom Made Key
      Option 3+: Top 50 Most Used Windows Shortcuts (Win+Shift+S, Win+V, etc.)
    """
    def __init__(self, parent, on_save, existing_key=None, key_index=None):
        self.parent = parent
        self.on_save = on_save
        self.existing_key = existing_key
        self.key_index = key_index

        self.win = tk.Toplevel(parent)
        title_text = "🎹 Add Piano Key" if not existing_key else "🎹 Edit Piano Key"
        self.win.title(title_text)
        self.win.geometry("620x680")
        self.win.attributes("-topmost", True)
        self.win.config(bg="#1A1B20")

        # Center on screen
        self.win.update_idletasks()
        sw = self.win.winfo_screenwidth()
        sh = self.win.winfo_screenheight()
        self.win.geometry(f"620x680+{(sw - 620)//2}+{(sh - 680)//2}")

        self._build_options_list()
        self._build_ui()

    def _build_options_list(self):
        # 1. First option: Copied Content
        # 2. Second option: Custom Made Key
        # 3. Third option onwards: Top 50 Shortcuts
        self.choices = [
            {
                "id": "copied_content",
                "label": "1. 📋 Copied Content (Paste Text / Snippet Macro)",
                "type": "paste_text"
            },
            {
                "id": "custom_made",
                "label": "2. 🛠️ Custom Made Key (Web Link, App Launcher, or Script)",
                "type": "custom"
            }
        ]

        # Add top 50 shortcuts
        for idx, sc in enumerate(TOP_50_SHORTCUTS, start=3):
            self.choices.append({
                "id": f"shortcut_{sc['id']}",
                "label": f"{idx}. {sc['icon']} {sc['badge']} — {sc['title']} ({sc['desc']})",
                "type": "shortcut",
                "data": sc
            })

    def _build_ui(self):
        # Header banner
        hdr = tk.Frame(self.win, bg="#141518", padx=20, pady=12)
        hdr.pack(fill="x")

        lbl_head = tk.Label(hdr, text="🎹 Piano Key Builder", font=("Segoe UI", 12, "bold"), fg="#D4AF37", bg="#141518")
        lbl_head.pack(anchor="w")

        lbl_sub = tk.Label(hdr, text="Create a 1-Click Copied Text Macro, Custom Action, or Top 50 Windows Shortcut.", font=("Segoe UI", 9), fg="#9E9E9E", bg="#141518")
        lbl_sub.pack(anchor="w", pady=(2, 0))

        # Main container
        body = tk.Frame(self.win, bg="#1A1B20", padx=20, pady=12)
        body.pack(fill="both", expand=True)

        # Category / Option Dropdown
        tk.Label(body, text="Select Key Category / Function:", font=("Segoe UI", 9, "bold"), bg="#1A1B20", fg="#D4AF37").pack(anchor="w")

        # Determine initial selection
        initial_label = self.choices[0]["label"]
        if self.existing_key:
            act = self.existing_key.get("action", "")
            if act == "paste_text":
                initial_label = self.choices[0]["label"]
            elif act == "shortcut":
                keys_val = self.existing_key.get("text", "").lower()
                for c in self.choices[2:]:
                    if c.get("data", {}).get("keys", "").lower() == keys_val:
                        initial_label = c["label"]
                        break
            else:
                initial_label = self.choices[1]["label"]

        self.selected_choice_var = tk.StringVar(value=initial_label)
        self.cbo_choice = ttk.Combobox(
            body,
            textvariable=self.selected_choice_var,
            values=[c["label"] for c in self.choices],
            state="readonly",
            font=("Segoe UI", 9)
        )
        self.cbo_choice.pack(fill="x", pady=(4, 14))
        self.cbo_choice.bind("<<ComboboxSelected>>", self._on_choice_changed)

        # Dynamic Section Frame
        self.content_frame = tk.Frame(body, bg="#1A1B20")
        self.content_frame.pack(fill="both", expand=True)

        # Shared fields: Title & Icon
        f_title_row = tk.Frame(self.content_frame, bg="#1A1B20")
        f_title_row.pack(fill="x", pady=(0, 10))

        # Title entry
        tk.Label(f_title_row, text="Key Title (Shows Bold on Piano Key):", font=("Segoe UI", 8, "bold"), bg="#1A1B20", fg="#FFFFFF").grid(row=0, column=0, sticky="w", padx=(0, 12))
        tk.Label(f_title_row, text="Icon:", font=("Segoe UI", 8, "bold"), bg="#1A1B20", fg="#FFFFFF").grid(row=0, column=1, sticky="w")

        init_title = self.existing_key.get("title", "OFFICER APPROVAL") if self.existing_key else "OFFICER APPROVAL"
        self.title_var = tk.StringVar(value=init_title)
        self.e_title = tk.Entry(f_title_row, textvariable=self.title_var, font=("Segoe UI", 10, "bold"), bg="#282930", fg="#FFFFFF", insertbackground="#D4AF37", bd=1)
        self.e_title.grid(row=1, column=0, sticky="ew", padx=(0, 12), pady=(3, 0))

        init_icon = self.existing_key.get("icon", "📋") if self.existing_key else "📋"
        self.icon_var = tk.StringVar(value=init_icon)
        self.e_icon = tk.Entry(f_title_row, textvariable=self.icon_var, font=("Segoe UI Emoji", 11), bg="#282930", fg="#FFFFFF", width=8, insertbackground="#D4AF37", bd=1)
        self.e_icon.grid(row=1, column=1, sticky="ew", pady=(3, 0))

        f_title_row.columnconfigure(0, weight=4)
        f_title_row.columnconfigure(1, weight=1)

        # Subtitle
        tk.Label(self.content_frame, text="Subtitle / Description:", font=("Segoe UI", 8), bg="#1A1B20", fg="#CCCCCC").pack(anchor="w")
        init_sub = self.existing_key.get("subtitle", "Copy Official Memo") if self.existing_key else "Copy Official Memo"
        self.sub_var = tk.StringVar(value=init_sub)
        self.e_sub = tk.Entry(self.content_frame, textvariable=self.sub_var, font=("Segoe UI", 9), bg="#282930", fg="#FFFFFF", insertbackground="#D4AF37", bd=1)
        self.e_sub.pack(fill="x", pady=(2, 12))

        # Specialized Section Container
        self.special_frame = tk.Frame(self.content_frame, bg="#1A1B20")
        self.special_frame.pack(fill="both", expand=True)

        self._render_special_ui()

        # Bottom Bar
        bbar = tk.Frame(self.win, bg="#141518", padx=20, pady=12)
        bbar.pack(fill="x", side="bottom")

        btn_cancel = tk.Button(bbar, text="Cancel", font=("Segoe UI", 9), bg="#33353D", fg="#FFF", bd=0, padx=14, pady=6, cursor="hand2", command=self.win.destroy)
        btn_cancel.pack(side="right", padx=(8, 0))

        btn_save = tk.Button(bbar, text="Save Piano Key", font=("Segoe UI", 9, "bold"), bg="#D4AF37", fg="#121212", bd=0, padx=20, pady=6, cursor="hand2", command=self._save_key)
        btn_save.pack(side="right")

    def _get_current_choice(self):
        sel_label = self.selected_choice_var.get()
        return next((c for c in self.choices if c["label"] == sel_label), self.choices[0])

    def _on_choice_changed(self, event=None):
        choice = self._get_current_choice()
        c_type = choice["type"]

        if c_type == "paste_text":
            self.title_var.set("OFFICER APPROVAL")
            self.icon_var.set("📋")
            self.sub_var.set("Copy Official Memo")
        elif c_type == "custom":
            self.title_var.set("EXECUTIVE ACTION")
            self.icon_var.set("🛠️")
            self.sub_var.set("Custom Action")
        elif c_type == "shortcut":
            sc = choice["data"]
            self.title_var.set(sc["title"])
            self.icon_var.set(sc["icon"])
            self.sub_var.set(sc["subtitle"])

        self._render_special_ui()

    def _render_special_ui(self):
        for w in self.special_frame.winfo_children():
            w.destroy()

        choice = self._get_current_choice()
        c_type = choice["type"]

        if c_type == "paste_text":
            # Option 1: Clean Copied Content Box
            box_hdr = tk.Frame(self.special_frame, bg="#1A1B20")
            box_hdr.pack(fill="x", pady=(0, 4))

            tk.Label(box_hdr, text="Copied Content / Text Bar:", font=("Segoe UI", 9, "bold"), bg="#1A1B20", fg="#D4AF37").pack(side="left")

            btn_paste_clip = tk.Button(
                box_hdr,
                text="📋 Paste from Clipboard",
                font=("Segoe UI", 8, "bold"),
                bg="#2E303A",
                fg="#D4AF37",
                activebackground="#D4AF37",
                activeforeground="#121212",
                bd=1,
                padx=8,
                pady=2,
                cursor="hand2",
                command=self._paste_clipboard_into_box
            )
            btn_paste_clip.pack(side="right")

            init_txt = self.existing_key.get("text", "Approved. Please process as per official policy and record in the minutes.") if self.existing_key else "Approved. Please process as per official policy and record in the minutes."
            self.txt_copied = tk.Text(self.special_frame, height=6, font=("Consolas", 10), bg="#24262E", fg="#FFFFFF", insertbackground="#D4AF37", bd=1)
            self.txt_copied.pack(fill="both", expand=True, pady=(2, 6))
            self.txt_copied.insert("1.0", init_txt)

            self.auto_paste_var = tk.BooleanVar(value=self.existing_key.get("auto_paste", True) if self.existing_key else True)
            chk_paste = tk.Checkbutton(
                self.special_frame,
                text="Simulate Auto-Paste (Ctrl+V) directly into active document/email on press",
                variable=self.auto_paste_var,
                font=("Segoe UI", 8),
                bg="#1A1B20",
                fg="#CCCCCC",
                selectcolor="#24262E",
                activebackground="#1A1B20"
            )
            chk_paste.pack(anchor="w", pady=(0, 4))

            lbl_hint = tk.Label(
                self.special_frame,
                text="💡 Tip: Enter any frequent text (approval note, memo, email signature, bank details, zoom link).",
                font=("Segoe UI", 8, "italic"),
                fg="#888888",
                bg="#1A1B20"
            )
            lbl_hint.pack(anchor="w")

        elif c_type == "custom":
            # Option 2: Custom Made Key
            tk.Label(self.special_frame, text="Custom Action Type:", font=("Segoe UI", 8, "bold"), bg="#1A1B20", fg="#D4AF37").pack(anchor="w")

            self.custom_type_var = tk.StringVar(value=self.existing_key.get("action", "custom_url") if self.existing_key else "custom_url")
            c_opts = [
                ("custom_url", "🌐 Open Website / URL"),
                ("kill_tasks", "⚡ Kill Hung Processes (Excel, Chrome)"),
                ("clean_system", "🧹 Purge Recycle Bin & Cache"),
                ("privacy_shield", "🛡️ Privacy Shield (Boss Key)"),
                ("toggle_music", "🎵 Background Ambient Focus Music")
            ]
            for val, txt in c_opts:
                tk.Radiobutton(
                    self.special_frame,
                    text=txt,
                    variable=self.custom_type_var,
                    value=val,
                    font=("Segoe UI", 8),
                    bg="#1A1B20",
                    fg="#FFFFFF",
                    selectcolor="#282930",
                    activebackground="#1A1B20"
                ).pack(anchor="w", pady=1)

            tk.Label(self.special_frame, text="Target URL or Process Name (if applicable):", font=("Segoe UI", 8, "bold"), bg="#1A1B20", fg="#CCCCCC").pack(anchor="w", pady=(8, 2))
            init_custom_txt = self.existing_key.get("text", "https://finance.yahoo.com") if self.existing_key else "https://finance.yahoo.com"
            self.e_custom_param = tk.Entry(self.special_frame, font=("Consolas", 9), bg="#282930", fg="#FFFFFF", insertbackground="#D4AF37", bd=1)
            self.e_custom_param.pack(fill="x", pady=(2, 6))
            self.e_custom_param.insert(0, init_custom_txt)

        elif c_type == "shortcut":
            # Option 3+: Top 50 Shortcuts
            sc = choice["data"]
            box = tk.Frame(self.special_frame, bg="#23252E", padx=14, pady=12, bd=1, relief="solid")
            box.pack(fill="x", pady=6)

            tk.Label(box, text=f"Keyboard Shortcut: {sc['badge']}", font=("Segoe UI", 11, "bold"), fg="#D4AF37", bg="#23252E").pack(anchor="w")
            tk.Label(box, text=sc["desc"], font=("Segoe UI", 9), fg="#FFFFFF", bg="#23252E", wraplength=480, justify="left").pack(anchor="w", pady=(4, 8))

            lbl_how = tk.Label(
                box,
                text="When you press this piano key, it will instantly simulate this key combination in Windows!",
                font=("Segoe UI", 8, "italic"),
                fg="#90CAF9",
                bg="#23252E"
            )
            lbl_how.pack(anchor="w")

    def _paste_clipboard_into_box(self):
        try:
            win32clipboard.OpenClipboard()
            clip_data = win32clipboard.GetClipboardData(win32clipboard.CF_UNICODETEXT)
            win32clipboard.CloseClipboard()
            if clip_data:
                self.txt_copied.delete("1.0", "end")
                self.txt_copied.insert("1.0", clip_data)
        except Exception:
            pass

    def _save_key(self):
        title = self.title_var.get().strip()
        if not title:
            messagebox.showwarning("Validation", "Please enter a Title for this key.", parent=self.win)
            return

        choice = self._get_current_choice()
        c_type = choice["type"]

        idx = self.key_index if self.key_index is not None else 0
        n_pair = NOTES_PALETTE[idx % len(NOTES_PALETTE)]
        note_num, note_name = n_pair

        if c_type == "paste_text":
            act_type = "paste_text"
            text_val = self.txt_copied.get("1.0", "end").strip()
            badge_val = "Snippet"
            auto_paste = self.auto_paste_var.get()
        elif c_type == "custom":
            act_type = self.custom_type_var.get()
            text_val = self.e_custom_param.get().strip()
            badge_val = "Custom"
            auto_paste = False
        elif c_type == "shortcut":
            sc = choice["data"]
            act_type = "shortcut"
            text_val = sc["keys"]
            badge_val = sc["badge"]
            auto_paste = False

        key_data = {
            "id": self.existing_key.get("id") if self.existing_key else f"key_{title.lower().replace(' ', '_')}",
            "note": note_num,
            "note_name": note_name,
            "title": title.upper(),
            "subtitle": self.sub_var.get().strip() or "Executive Action",
            "icon": self.icon_var.get().strip() or "🎹",
            "action": act_type,
            "badge": badge_val,
            "text": text_val,
            "auto_paste": auto_paste
        }

        self.on_save(key_data, self.key_index)
        self.win.destroy()
