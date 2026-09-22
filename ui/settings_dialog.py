import tkinter as tk
from tkinter import ttk, messagebox
import requests

class SettingsDialog:
    """Executive Settings Modal for Senior Officers Dashboard."""
    def __init__(self, parent, config_manager, audio_engine=None, on_saved=None):
        self.parent = parent
        self.cfg_mgr = config_manager
        self.config = self.cfg_mgr.config
        self.audio_engine = audio_engine
        self.on_saved = on_saved

        self.win = tk.Toplevel(parent)
        self.win.title("Senior Officers Dashboard — Executive Settings")
        self.win.geometry("640x580")
        self.win.minsize(560, 500)
        self.win.attributes("-topmost", True)
        self.win.config(bg="#1E1F24")

        # Center on screen
        self.win.update_idletasks()
        sw = self.win.winfo_screenwidth()
        sh = self.win.winfo_screenheight()
        self.win.geometry(f"640x580+{(sw - 640)//2}+{(sh - 580)//2}")

        self._build_ui()

    def _build_ui(self):
        # Header banner
        hdr = tk.Frame(self.win, bg="#141518", padx=20, pady=16)
        hdr.pack(fill="x")

        lbl_title = tk.Label(hdr, text="⚙️ Executive Dashboard Preferences", font=("Segoe UI", 13, "bold"), fg="#D4AF37", bg="#141518")
        lbl_title.pack(anchor="w")

        lbl_sub = tk.Label(hdr, text="Configure 1-Click Keys, WhatsApp/Telegram dispatch, Morning bundles, and Credentials.", font=("Segoe UI", 9), fg="#9E9E9E", bg="#141518")
        lbl_sub.pack(anchor="w", pady=(2, 0))

        # Notebook / Tabs
        style = ttk.Style()
        style.theme_use("default")
        style.configure("TNotebook", background="#1E1F24", borderwidth=0)
        style.configure("TNotebook.Tab", background="#292A30", foreground="#E0E0E0", padding=[14, 6], font=("Segoe UI", 9, "bold"))
        style.map("TNotebook.Tab", background=[("selected", "#D4AF37")], foreground=[("selected", "#121212")])

        nb = ttk.Notebook(self.win)
        nb.pack(fill="both", expand=True, padx=20, pady=12)

        # Tab 1: Dispatch (WhatsApp & Telegram)
        tab_dispatch = tk.Frame(nb, bg="#1E1F24", padx=16, pady=16)
        nb.add(tab_dispatch, text="📤 Dispatch (WA & TG)")
        self._build_dispatch_tab(tab_dispatch)

        # Tab 2: Workspace Suite
        tab_workspace = tk.Frame(nb, bg="#1E1F24", padx=16, pady=16)
        nb.add(tab_workspace, text="💼 Morning Suite")
        self._build_workspace_tab(tab_workspace)

        # Tab 3: Auto-Login Portal
        tab_login = tk.Frame(nb, bg="#1E1F24", padx=16, pady=16)
        nb.add(tab_login, text="🔐 Portal Auto-Login")
        self._build_login_tab(tab_login)

        # Tab 4: Sound & System
        tab_system = tk.Frame(nb, bg="#1E1F24", padx=16, pady=16)
        nb.add(tab_system, text="🎵 Piano Sound & Deck")
        self._build_system_tab(tab_system)

        # Bottom Action Bar
        btn_bar = tk.Frame(self.win, bg="#141518", padx=20, pady=12)
        btn_bar.pack(fill="x", side="bottom")

        btn_cancel = tk.Button(btn_bar, text="Cancel", font=("Segoe UI", 9), bg="#33353D", fg="#FFF", bd=0, padx=16, pady=6, cursor="hand2", command=self.win.destroy)
        btn_cancel.pack(side="right", padx=(8, 0))

        btn_save = tk.Button(btn_bar, text="Save Preferences", font=("Segoe UI", 9, "bold"), bg="#D4AF37", fg="#121212", bd=0, padx=20, pady=6, cursor="hand2", command=self._save_all)
        btn_save.pack(side="right")

    def _build_dispatch_tab(self, parent):
        # WhatsApp Section
        wa_frame = tk.LabelFrame(parent, text=" WhatsApp Dispatch Settings ", font=("Segoe UI", 9, "bold"), bg="#1E1F24", fg="#4ECA5D", padx=12, pady=10)
        wa_frame.pack(fill="x", pady=(0, 14))

        tk.Label(wa_frame, text="Default Phone Number (with Country Code, e.g. +919876543210):", font=("Segoe UI", 8), bg="#1E1F24", fg="#CCCCCC").pack(anchor="w")
        self.wa_phone_var = tk.StringVar(value=self.config.get("whatsapp", {}).get("default_phone", ""))
        e_wa_phone = tk.Entry(wa_frame, textvariable=self.wa_phone_var, font=("Segoe UI", 9), bg="#2B2D35", fg="#FFFFFF", insertbackground="#D4AF37", bd=1)
        e_wa_phone.pack(fill="x", pady=(2, 6))

        tk.Label(wa_frame, text="Default Dispatch Message:", font=("Segoe UI", 8), bg="#1E1F24", fg="#CCCCCC").pack(anchor="w")
        self.wa_msg_var = tk.StringVar(value=self.config.get("whatsapp", {}).get("default_message", "Snapshot from Senior Officer Dashboard"))
        e_wa_msg = tk.Entry(wa_frame, textvariable=self.wa_msg_var, font=("Segoe UI", 9), bg="#2B2D35", fg="#FFFFFF", insertbackground="#D4AF37", bd=1)
        e_wa_msg.pack(fill="x", pady=(2, 2))

        # Telegram Section
        tg_frame = tk.LabelFrame(parent, text=" Telegram Bot Direct Upload Settings ", font=("Segoe UI", 9, "bold"), bg="#1E1F24", fg="#29B6F6", padx=12, pady=10)
        tg_frame.pack(fill="x")

        tk.Label(tg_frame, text="Telegram Bot Token (from @BotFather):", font=("Segoe UI", 8), bg="#1E1F24", fg="#CCCCCC").pack(anchor="w")
        self.tg_token_var = tk.StringVar(value=self.config.get("telegram", {}).get("bot_token", ""))
        e_tg_token = tk.Entry(tg_frame, textvariable=self.tg_token_var, font=("Segoe UI", 9), bg="#2B2D35", fg="#FFFFFF", insertbackground="#D4AF37", bd=1, show="•")
        e_tg_token.pack(fill="x", pady=(2, 6))

        tk.Label(tg_frame, text="Target Chat ID / Group ID (e.g. 123456789 or -100123456789):", font=("Segoe UI", 8), bg="#1E1F24", fg="#CCCCCC").pack(anchor="w")
        self.tg_chat_var = tk.StringVar(value=self.config.get("telegram", {}).get("chat_id", ""))
        e_tg_chat = tk.Entry(tg_frame, textvariable=self.tg_chat_var, font=("Segoe UI", 9), bg="#2B2D35", fg="#FFFFFF", insertbackground="#D4AF37", bd=1)
        e_tg_chat.pack(fill="x", pady=(2, 6))

        btn_test_tg = tk.Button(tg_frame, text="Test Telegram Connection", font=("Segoe UI", 8), bg="#29B6F6", fg="#000", bd=0, padx=10, pady=4, cursor="hand2", command=self._test_telegram)
        btn_test_tg.pack(anchor="w")

    def _build_workspace_tab(self, parent):
        tk.Label(parent, text="Morning Portals / Websites (one per line):", font=("Segoe UI", 9, "bold"), bg="#1E1F24", fg="#FFFFFF").pack(anchor="w")
        self.txt_urls = tk.Text(parent, height=5, font=("Consolas", 9), bg="#2B2D35", fg="#FFFFFF", insertbackground="#D4AF37", bd=1)
        self.txt_urls.pack(fill="x", pady=(4, 12))
        urls = self.config.get("workspace", {}).get("urls", [])
        self.txt_urls.insert("1.0", "\n".join(urls))

        tk.Label(parent, text="Desktop Applications / Scripts (one per line, e.g. calc.exe, excel.exe):", font=("Segoe UI", 9, "bold"), bg="#1E1F24", fg="#FFFFFF").pack(anchor="w")
        self.txt_apps = tk.Text(parent, height=5, font=("Consolas", 9), bg="#2B2D35", fg="#FFFFFF", insertbackground="#D4AF37", bd=1)
        self.txt_apps.pack(fill="x", pady=(4, 6))
        apps = self.config.get("workspace", {}).get("apps", [])
        self.txt_apps.insert("1.0", "\n".join(apps))

    def _build_login_tab(self, parent):
        tk.Label(parent, text="Target Portal URL:", font=("Segoe UI", 8), bg="#1E1F24", fg="#CCCCCC").pack(anchor="w")
        self.portal_url_var = tk.StringVar(value=self.config.get("autologin", {}).get("url", ""))
        e_url = tk.Entry(parent, textvariable=self.portal_url_var, font=("Segoe UI", 9), bg="#2B2D35", fg="#FFFFFF", insertbackground="#D4AF37", bd=1)
        e_url.pack(fill="x", pady=(2, 10))

        tk.Label(parent, text="Username / Email:", font=("Segoe UI", 8), bg="#1E1F24", fg="#CCCCCC").pack(anchor="w")
        self.portal_user_var = tk.StringVar(value=self.config.get("autologin", {}).get("username", ""))
        e_user = tk.Entry(parent, textvariable=self.portal_user_var, font=("Segoe UI", 9), bg="#2B2D35", fg="#FFFFFF", insertbackground="#D4AF37", bd=1)
        e_user.pack(fill="x", pady=(2, 10))

        tk.Label(parent, text="Password / PIN:", font=("Segoe UI", 8), bg="#1E1F24", fg="#CCCCCC").pack(anchor="w")
        self.portal_pass_var = tk.StringVar(value=self.config.get("autologin", {}).get("password", ""))
        e_pass = tk.Entry(parent, textvariable=self.portal_pass_var, font=("Segoe UI", 9), bg="#2B2D35", fg="#FFFFFF", insertbackground="#D4AF37", bd=1, show="•")
        e_pass.pack(fill="x", pady=(2, 10))

        self.copy_pass_var = tk.BooleanVar(value=self.config.get("autologin", {}).get("auto_copy_password", True))
        chk_pass = tk.Checkbutton(parent, text="Copy password to clipboard on launch for instant paste", variable=self.copy_pass_var, bg="#1E1F24", fg="#FFFFFF", selectcolor="#2B2D35", activebackground="#1E1F24", activeforeground="#D4AF37")
        chk_pass.pack(anchor="w", pady=(4, 0))

    def _build_system_tab(self, parent):
        self.sound_var = tk.BooleanVar(value=self.config.get("app", {}).get("sound_enabled", True))
        chk_sound = tk.Checkbutton(parent, text="Enable Acoustic Grand Piano Audio Notes on Key Press", variable=self.sound_var, font=("Segoe UI", 9, "bold"), bg="#1E1F24", fg="#FFFFFF", selectcolor="#2B2D35", activebackground="#1E1F24", activeforeground="#D4AF37")
        chk_sound.pack(anchor="w", pady=(6, 12))

        btn_test_sound = tk.Button(parent, text="🎵 Test Piano Chord (C Major)", font=("Segoe UI", 8), bg="#D4AF37", fg="#000", bd=0, padx=12, pady=5, cursor="hand2", command=self._test_chord)
        btn_test_sound.pack(anchor="w", pady=(0, 20))

        self.topmost_var = tk.BooleanVar(value=self.config.get("app", {}).get("always_on_top", True))
        chk_top = tk.Checkbutton(parent, text="Keep Piano Deck Always on Top of Windows", variable=self.topmost_var, font=("Segoe UI", 9), bg="#1E1F24", fg="#FFFFFF", selectcolor="#2B2D35", activebackground="#1E1F24", activeforeground="#D4AF37")
        chk_top.pack(anchor="w", pady=(4, 10))

    def _test_chord(self):
        if self.audio_engine:
            self.audio_engine.play_chord([60, 64, 67, 72])

    def _test_telegram(self):
        tok = self.tg_token_var.get().strip()
        chat = self.tg_chat_var.get().strip()
        if not tok or not chat:
            messagebox.showwarning("Telegram Setup", "Please enter both Bot Token and Chat ID first.", parent=self.win)
            return
        try:
            url = f"https://api.telegram.org/bot{tok}/sendMessage"
            r = requests.post(url, json={"chat_id": chat, "text": "✅ Senior Officers Dashboard: Telegram Bot connected successfully!"}, timeout=8)
            if r.json().get("ok"):
                messagebox.showinfo("Telegram Success", "Connection verified! Test message sent to your Telegram chat.", parent=self.win)
            else:
                messagebox.showerror("Telegram Error", f"Telegram response: {r.json().get('description')}", parent=self.win)
        except Exception as e:
            messagebox.showerror("Error", f"Could not connect to Telegram: {e}", parent=self.win)

    def _save_all(self):
        # Update config object
        self.config["whatsapp"]["default_phone"] = self.wa_phone_var.get().strip()
        self.config["whatsapp"]["default_message"] = self.wa_msg_var.get().strip()

        self.config["telegram"]["bot_token"] = self.tg_token_var.get().strip()
        self.config["telegram"]["chat_id"] = self.tg_chat_var.get().strip()

        urls = [line.strip() for line in self.txt_urls.get("1.0", "end").split("\n") if line.strip()]
        apps = [line.strip() for line in self.txt_apps.get("1.0", "end").split("\n") if line.strip()]
        self.config["workspace"]["urls"] = urls
        self.config["workspace"]["apps"] = apps

        self.config["autologin"]["url"] = self.portal_url_var.get().strip()
        self.config["autologin"]["username"] = self.portal_user_var.get().strip()
        self.config["autologin"]["password"] = self.portal_pass_var.get().strip()
        self.config["autologin"]["auto_copy_password"] = self.copy_pass_var.get()

        self.config["app"]["sound_enabled"] = self.sound_var.get()
        self.config["app"]["always_on_top"] = self.topmost_var.get()

        self.cfg_mgr.save(self.config)

        if self.audio_engine:
            self.audio_engine.enabled = self.sound_var.get()

        if self.on_saved:
            self.on_saved()

        self.win.destroy()
