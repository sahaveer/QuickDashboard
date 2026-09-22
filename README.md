# 🎹 Piano Deck — Senior Officers Executive Dashboard (PyQt6 Edition)

An ultra-luxury rapid-automation dashboard docked directly above the Windows taskbar, redesigned with **PyQt6 hardware-accelerated Steinway Ivory piano keys**, **Multi-User Profile Switching**, and **Acoustic Grand Piano MIDI audio chords & notes** (`winmm.dll`).

[![Documentation](https://img.shields.io/badge/User%20Guide-USER__GUIDE.md-D4AF37?style=for-the-badge&logo=markdown)](USER_GUIDE.md)
[![Live Showcase](https://img.shields.io/badge/Web%20Simulator-GitHub%20Pages-4ECA5D?style=for-the-badge&logo=github)](index.html)
[![Windows Compatible](https://img.shields.io/badge/Platform-Windows%2010%20%7C%2011-0078D6?style=for-the-badge&logo=windows)](USER_GUIDE.md)

> 📖 **Looking for full installation instructions, role use cases, and shortcut catalogs? Read the [Complete User Guide (USER_GUIDE.md)](USER_GUIDE.md).**
>
> 🌐 **Want to try the keys in your browser? Open [index.html](index.html) for the interactive web simulator.**

---

## 👤 Multi-User Profile Switcher

Different officers and staff can share the same computer while maintaining their own **completely isolated sets of buttons, text snippets, and shortcuts**:

- **👤 Senior Officer (Default)**: Purge & Clean, Smart Snapshot, Officer Approval Snippet, Privacy Shield.
- **💼 Finance & Accounts**: Kill Frozen Excel, Snip Financial Statements, Payment Approved Memo, ERP Portal.
- **👔 Executive Assistant / PA**: Meeting Agenda Header, Dispatch Snapshot (WhatsApp/Telegram), Clipboard History (`Win+V`), Purge Cache.
- **⚖️ Legal & Compliance**: Legal Vetting Clause, Lock PC (`Win+L`), Snip Clause.
- **➕ Add New Profile**: Add any officer name (e.g. *"Director Sharma"*, *"CFO"*, *"Personal"*) with 1 click.

Switching profiles from the dropdown immediately updates the piano deck in real time!

---

## 🎹 Piano Key Controls & Builder

The dashboard features **large, tactile Steinway Ivory keys** with 3D drop depth and mechanical press depression:

| Key | Musical Note | Action | Description |
| :--- | :---: | :--- | :--- |
| **Key 1** | **C4** | 🧹 **PURGE & CLEAN** | Empties Windows Recycle Bin, clears `%TEMP%`, Windows temp cache, and flushes DNS cache. Plays a celebratory C-Major chord and reports space freed. |
| **Key 2** | **D4** | 📸 **SNAPSHOT** | Captures display with choice of **Full Screen** or **Area Snippet (Snipping Tool)**, saves PNG to `Pictures/Screenshots`, copies bitmap to Clipboard (`CF_DIB`), and shows a **self-closing confirmation window**. |
| **Key 3** | **E4** | 📋 **OFFICER APPROVAL** | **Copied Text / Snippet Macro**: Copies pre-configured official text and auto-pastes it directly into your active document, email, or chat! |
| **Right Key**| **+** | ➕ **ADD PIANO KEY** | Opens the **Piano Key Builder** to add custom actions, text snippets, or choose from the Top 50 Shortcuts. |

---

## 📋 Adding Copied Content (Primary Key Option)
When you click **➕ Add Key**:
1. **Option 1 (Default)**: **📋 Copied Content**
   - **Key Title**: Input what text shows bold on the piano key (e.g., `OFFICER APPROVAL`, `MY SIGNATURE`, `ZOOM LINK`).
   - **Copied Content Text Bar**: Enter your text, or click **`[ 📋 Paste from Clipboard ]`** to insert your current clipboard text with 1 click.
   - **Auto-Paste Toggle**: Choose whether pressing the key simulates `Ctrl+V` to paste immediately into your active window.
2. **Option 2**: **🛠️ Custom Made Key** (Web link, app launcher, process killer, privacy shield).
3. **Option 3 to 52**: **⚡ Top 50 Most Used Shortcuts** with instant search/filter bar (`Win+Shift+S`, `Win+V`, `Win+D`, `Ctrl+Shift+Esc`, etc.).

---

## 🚀 Quick Start

### Launching the Dashboard
Run the following command from the project root:
```bash
python main.py
```

### Dock Controls (Top Rail)
- **Drag Handle**: Click and drag the dark mahogany top rail to position the deck anywhere on your monitors.
- **▼ Fold / ▲ Expand**: Minimizes the piano into a compact 38px executive floating bar when you need maximum screen area.
- **🔊 Sound ON / 🔇 Sound OFF**: Instantly toggles the Acoustic Grand Piano MIDI audio synthesizer.
- **⚙ Settings**: Opens the preferences modal to configure phone numbers, bot tokens, and URLs.
- **✕ Exit**: Closes the application gracefully.

---

## ⚙️ Configuration & Customization

Settings are persisted in `config.json` and can be edited either in the UI (`⚙ Settings` key) or directly in `config.json`.

### 1. WhatsApp & Telegram Dispatch
- **WhatsApp**: Enter recipient's phone number with country code (e.g. `+919876543210`). When you press **DISPATCH**, WhatsApp opens the chat and your screenshot is already copied to your clipboard—simply press `Ctrl + V` and Enter!
- **Telegram**: Enter your Bot Token (from `@BotFather`) and Target Chat ID (from `@userinfobot` or your group ID). The dashboard will upload and send the screenshot directly through the Telegram Bot API.

### 2. Morning Work Suite (Portals & Apps)
Add any number of URLs or desktop programs to launch with a single press of **Key 4**:
```json
"workspace": {
    "urls": [
        "https://finance.yahoo.com",
        "https://news.google.com"
    ],
    "apps": [
        "calc.exe",
        "notepad.exe"
    ]
}
```

---

## 🛠️ Architecture

```
DASHBOARD for Senior Officers/
├── main.py                     # Application entry point & logging
├── piano_deck.py               # Grand piano GUI with ivory keys, 3D press, and docking
├── config_manager.py           # Configuration loader & validator
├── config.json                 # Persistent configuration
├── audio_engine.py             # Windows native MIDI synthesizer (winmm.dll)
├── actions/
│   ├── cleaner.py              # Recycle Bin & multi-tier cache purge
│   ├── screenshot.py           # High-resolution screenshot & CF_DIB clipboard
│   ├── dispatcher.py           # WhatsApp Web & Telegram Bot API dispatch
│   ├── workspace.py            # Staggered portal and app launcher
│   ├── autologin.py            # Web portal auto-login & credential helper
│   ├── music_player.py         # Ambient focus audio manager
│   └── privacy.py              # Instant window minimization & master audio mute
├── ui/
│   ├── toast.py                # Luxury floating notification banners
│   └── settings_dialog.py      # Executive preferences modal
└── Screenshots/                # Auto-saved screenshot directory
```
