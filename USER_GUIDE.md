# 🎹 Piano Deck — Senior Officers Executive Dashboard
## Complete User Guide: Use Cases, Installation & Operations

> **An ultra-luxury, tactile automation dashboard styled after Steinway & Sons Grand Piano keys, docked above the Windows taskbar for Senior Officers, C-Suite Executives, and Enterprise Teams.**

---

## 📑 Table of Contents
1. [Overview & Philosophy](#-1-overview--philosophy)
2. [Executive Use Cases by Role](#-2-executive-use-cases-by-role)
   - [Senior Officers & C-Suite](#senior-officers--c-suite-chief-executive)
   - [Executive Assistants & Secretariats](#executive-assistants--secretariats)
   - [Finance & Accounts Officers](#finance--accounts-officers)
   - [Legal & Compliance Counsel](#legal--compliance-counsel)
   - [Shared Workstations & Shift Offices](#shared-workstations--shift-offices)
3. [Step-by-Step Installation Guide](#-3-step-by-step-installation-guide)
   - [System Prerequisites](#system-prerequisites)
   - [Option A: Git Clone (Recommended)](#option-a-git-clone-recommended)
   - [Option B: Direct ZIP Download](#option-b-direct-zip-download)
   - [Installing Python Dependencies](#installing-python-dependencies)
   - [Launching the Dashboard](#launching-the-dashboard)
   - [Configuring Windows Auto-Start](#configuring-windows-auto-start-optional)
4. [How to Use the Dashboard](#-4-how-to-use-the-dashboard)
   - [The Piano Deck Interface](#the-piano-deck-interface)
   - [Moving & Folding the Dock](#moving--folding-the-dock)
   - [Acoustic Grand Piano Sound Feedback](#acoustic-grand-piano-sound-feedback)
   - [Multi-User Profiles System](#multi-user-profiles-system)
   - [Default Out-of-the-Box Keys](#default-out-of-the-box-keys)
   - [Adding New Piano Keys (Key Builder)](#adding-new-piano-keys-key-builder)
   - [Editing & Deleting Keys](#editing--deleting-keys)
   - [Smart Snapshot & Self-Closing Window](#smart-snapshot--self-closing-window)
5. [Architecture & Configuration Files](#-5-architecture--configuration-files)
6. [Troubleshooting & FAQ](#-6-troubleshooting--faq)

---

## 🏛️ 1. Overview & Philosophy

Senior officers, directors, and executives handle high volumes of critical tasks daily: approving memos, reviewing financial sheets, capturing snippets of reports, switching between corporate portals, and clearing sensitive workstation caches. 

Traditional desktop shortcuts are cluttered, easy to misclick, and lack tactile clarity. **Piano Deck** re-imagines desktop productivity by turning mundane workflows into **large, tactile Grand Piano keys**:
- **Large Ergonomic Targets**: Piano keys provide expansive click areas docked right above your Windows taskbar.
- **Physical Cognitive Mapping**: Musical note associations (C4, D4, E4, F4) create intuitive subconscious reflexes for each action.
- **Steinway Ivory Aesthetic**: Specular gradients, 3D mechanical press depression, metallic gold trim, and ClearType typography deliver an interface worthy of executive offices.
- **Native Windows Synthesis**: Uses the native Windows Multimedia synthesizer (`winmm.dll`) to produce authentic Acoustic Grand Piano chords with **zero external audio files or sound lag**.
- **Multi-Profile Isolation**: Different officers sharing the same desktop maintain independent layouts, text snippets, and automations.

---

## 💼 2. Executive Use Cases by Role

### Senior Officers & C-Suite (Chief / Executive)
- **1-Click Official Approval Snippet**: Instantly copies and auto-pastes standardized clearance text into official emails, WhatsApp Web messages, or Word documents:
  > *"Approved. Please process as per official policy and record in the minutes."*
- **Purge & Clean**: 1-click cleanup that empties the Windows Recycle Bin, clears `%TEMP%` and system caches, and flushes DNS cache after confidential sessions.
- **Privacy Shield ("Boss Key")**: An immediate single-click panic key that minimizes all open windows to desktop and mutes master system audio if confidential data needs immediate obscuring.
- **Smart Snapshot**: Captures clean documentation of briefings and automatically timestamps them into `Pictures/Screenshots`.

---

### Executive Assistants & Secretariats
- **Standardized Agenda Headers**: Injects recurrent meeting agendas, standardized follow-up templates, and signature blocks in a fraction of a second.
- **Fast Media Dispatch**: Captures briefing slides or notices and dispatches them straight to a Telegram channel/group or opens WhatsApp Web with the image already copied to the clipboard.
- **Quick Clipboard History Access (`Win+V`)**: Instant 1-click access to the Windows multi-item clipboard history to retrieve previous cut/copied references.
- **System De-Clutter**: Rapid cache cleaner between shift handovers.

---

### Finance & Accounts Officers
- **Emergency Unfreeze (Kill Frozen Excel)**: Heavy spreadsheets and pivot tables frequently lock up or hang during payroll and quarter-end close. A single key terminates hung background Excel processes without needing to open Task Manager.
- **Snip Audit / Financial Clauses**: Uses the interactive gold crosshair region selector to snip financial tables, balance sheets, or discrepancy lines and immediately places raw bitmap data in the clipboard for pasting into audit notes.
- **Payment Approved Memo**: Auto-pastes recurring voucher approval statements:
  > *"Invoice calculations and supporting vouchers verified. Approved for disbursement."*
- **1-Click ERP / Banking Launch**: Launches the enterprise SAP/Oracle or corporate banking portal in a designated browser window.

---

### Legal & Compliance Counsel
- **Confidentiality Vetting Clause**: Pastes binding confidentiality clauses, disclaimers, or NDA footnotes into contracts with a single touch:
  > *"Subject to legal vetting. Privileged and confidential communication."*
- **Instant Workstation Security (`Win+L`)**: A single piano key immediately locks the Windows workstation when stepping away from the desk for hearings or conferences.
- **Contract Clause Snip**: Quickly cuts specific legal clauses and generates timestamped audit records.

---

### Shared Workstations & Shift Offices
- Multiple officers or duty managers can share a single desktop PC without overwriting each other's custom shortcuts.
- Selecting your profile from the top-left dropdown (`[ 👤 Senior Officer ▼ ]`, `[ 💼 Finance & Accounts ▼ ]`, `[ ➕ Add New Profile ]`) instantly re-maps the entire piano board to your personal suite.

---

## 💻 3. Step-by-Step Installation Guide

### System Prerequisites
- **Operating System**: Windows 10 or Windows 11 (64-bit)
- **Python**: Python 3.10, 3.11, 3.12, 3.13, or 3.14
- **Hardware**: Compatible with standard 1080p displays, multi-monitor setups, and 4K Ultra-HD displays (supports 100% to 300% DPI scaling).

---

### Option A: Git Clone (Recommended)

1. Open **PowerShell** or **Command Prompt** (`Win + R` → type `powershell` → Enter).
2. Clone the repository to your desired folder:
   ```powershell
   git clone https://github.com/your-username/piano-deck-dashboard.git
   cd "piano-deck-dashboard"
   ```

---

### Option B: Direct ZIP Download

1. Download the ZIP file from the GitHub repository (`Code` → `Download ZIP`).
2. Extract the archive into a permanent folder (e.g., `C:\Apps\PianoDeck\`).
3. Open PowerShell inside that folder.

---

### Installing Python Dependencies

Piano Deck requires PyQt6 for hardware-accelerated graphics and pywin32 for native Windows clipboard/audio integration.

Run:
```powershell
pip install -r requirements.txt
```

> **Manual pip install (if not using requirements.txt):**
> ```powershell
> pip install PyQt6 pillow pywin32 requests
> ```

---

### Launching the Dashboard

You can start the dashboard in either of two ways:

#### Method 1: Double-Click the Launcher
Simply double-click the included batch file:
```
run_piano_deck.bat
```
This launches the application smoothly in the background without keeping an open terminal window.

#### Method 2: Command Line
```powershell
python main.py
```

---

### Configuring Windows Auto-Start (Optional)
If you want Piano Deck to launch automatically whenever you log into Windows:
1. Press `Win + R`, type `shell:startup`, and press **Enter**.
2. Right-click inside the Startup folder → **New** → **Shortcut**.
3. In the location box, enter:
   ```cmd
   pythonw "C:\Path\To\Your\Project\main.py"
   ```
   *(Replace with your actual folder path)*.
4. Name the shortcut **Piano Deck** and click **Finish**.

---

## 🎹 4. How to Use the Dashboard

```
+-----------------------------------------------------------------------------------+
|  🎹 EXECUTIVE PIANO DECK  | Profile: [ Senior Officer v ]  [+ New]  | 🔊 Sound ON |
+-----------------------------------------------------------------------------------+
|   [ C4: PURGE ]    [ D4: SNAPSHOT ]    [ E4: APPROVAL ]    [ F4: PRIVACY ]    [ + ]
+-----------------------------------------------------------------------------------+
```

### The Piano Deck Interface
When started, the Piano Deck docks at the bottom center of your primary screen, resting **4 pixels directly above your Windows taskbar**.
- **Steinway Ivory Keys**: The lower portion displays large, ivory piano keys. Left-clicking depresses the key mechanically, triggers an Acoustic Grand Piano note, and executes its assigned automation.
- **Mahogany Fallboard (Top Rail)**: Contains profile switching, volume toggle, quick screenshot directory launcher, fold button, and close button.

### Moving & Folding the Dock
- **Drag Repositioning**: Click and drag anywhere on the dark mahogany top rail to position the deck anywhere on your screen or move it to a secondary monitor.
- **Fold / Expand**: Click **`▼ Fold`** on the top rail to collapse the deck into an ultra-thin 38-pixel bar when full screen space is required. Click **`▲ Expand`** to restore the full piano keys.

### Acoustic Grand Piano Sound Feedback
- Every key press plays an authentic Acoustic Grand Piano note (from C4 to G5) using Windows' internal General MIDI synthesizer (`winmm.dll`).
- Cleaning and batch automations trigger celebratory C-Major chords.
- To mute or re-enable audio feedback at any time, click **`🔊 Sound ON`** / **`🔇 Sound OFF`** in the top rail.

---

### Multi-User Profiles System
1. Click the **Profile Dropdown** (`[ 👤 Senior Officer ▼ ]`) on the top rail.
2. Select any role:
   - **👤 Senior Officer**: Chief executive actions.
   - **💼 Finance & Accounts**: Accounting, spreadsheet unfreeze & audit tools.
   - **👔 Executive Assistant**: PA meeting memos & rapid dispatch.
   - **⚖️ Legal & Compliance**: Contract vetting clauses & security locks.
3. **Adding a New Profile**:
   - Click **`[ ➕ New ]`** next to the dropdown.
   - Enter the Officer's name (e.g., *"Director Verma"*, *"Chief Medical Officer"*).
   - A fresh, fully customizable profile is immediately provisioned and saved in `profiles.json`.

---

### Default Out-of-the-Box Keys

| Key Note | Title | Default Action | Technical Behavior |
| :---: | :--- | :--- | :--- |
| **C4** | 🧹 **PURGE & CLEAN** | Recycle Bin & Cache Purge | Empties Recycle Bin (`SHEmptyRecycleBinW`), purges `%TEMP%` and Windows Temp, flushes DNS (`ipconfig /flushdns`), and announces freed MB. |
| **D4** | 📸 **SNAPSHOT** | Executive Screen Capture | Prompts for optional title and lets you pick Full Screen or Area Snipping. Saves to `Pictures/Screenshots` and copies bitmap to Clipboard. |
| **E4** | 📋 **OFFICER APPROVAL** | Official Memo Macro | Copies the official approval statement to clipboard and simulates `Ctrl + V` to insert it into your active document. |
| **F4** | 🛡️ **PRIVACY SHIELD** | Executive "Boss Key" | Minimizes all open application windows to desktop (`Win + D`) and mutes system master volume. |
| **+** | ➕ **ADD KEY** | Key Builder | Launches the 3-Tier Piano Key Builder dialog. |

---

### Adding New Piano Keys (Key Builder)
Click the black-and-gold **`[ + ]` Piano Key** on the far right of the rack to open the **Piano Key Builder**.

The dialog presents 3 options:

#### Option 1: 📋 Copied Content / Snippet Macro (Default & Most Used)
Use this for recurring text (email templates, disclaimers, signatures, URLs):
1. **Piano Key Title**: Type the text you want displayed bold on the piano key (e.g. `MY SIGNATURE`, `ZOOM LINK`, `PAYMENT OK`).
2. **Icon**: Select an emoji or icon (e.g. 📋, 🖋️, 📑).
3. **Copied Content Text Bar**: Paste your recurring text into the box.
   - *Pro-Tip*: Click **`[ 📋 Paste from Clipboard ]`** to automatically dump whatever text you currently have copied into the bar.
4. **Auto-Paste (`Ctrl+V`) Toggle**: Check this box if you want the piano key to automatically type/paste the text directly into whichever application window is currently active.
5. Click **`Save Piano Key`**.

#### Option 2: 🛠️ Custom Made Key
1. Select action type:
   - **Open Web Link**: Enter any URL (e.g., `https://portal.company.com` or `https://finance.yahoo.com`).
   - **Launch App**: Enter program name or path (e.g., `calc.exe`, `notepad.exe`, `excel.exe`).
   - **Kill Hung Tasks**: Enter process name (e.g., `excel.exe`, `acrobat.exe`).
2. Give it a title and click **`Save Piano Key`**.

#### Option 3: ⚡ Top 50 Most Used Windows Shortcuts
Select from a searchable catalog of the most productive shortcuts:
- `Win + Shift + S`: Windows Snipping Tool
- `Win + V`: Windows Clipboard History
- `Win + D`: Show / Hide Desktop
- `Ctrl + Shift + Esc`: Windows Task Manager
- `Win + E`: Windows File Explorer
- `Win + L`: Lock Workstation
- `Alt + Tab`: Task Switcher
- `Win + ← / → / ↑`: Window Snapping

Use the **Live Search Bar** to filter by typing any keyword (e.g., `"clip"`, `"task"`, `"lock"`). Select the shortcut, and click **`Save Piano Key`**.

---

### Editing & Deleting Keys
- **Right-Click** on any piano key to open its context menu:
  - **✏️ Edit Key / Text Snippet**: Modifies title, text content, or action.
  - **🗑️ Delete Key**: Removes the key immediately. The remaining keys will automatically slide over and recalculate dock width without flickering or closing the app.
  - **➕ Add Another Key**: Opens the key builder.

---

### Smart Snapshot & Self-Closing Window
When pressing **SNAPSHOT** (or any snapshot action key):
1. The Piano Deck automatically conceals itself so it does not appear in your screenshot.
2. An executive dialog lets you choose between:
   - **📸 Full Screen Capture**
   - **✂️ Select Area Snippet**: Dimmed screen with a glowing gold crosshair rubber-band selector.
3. The image is saved to:
   ```
   C:\Users\<YourUsername>\Pictures\Screenshots\
   ```
4. Raw bitmap data is copied to the Windows Clipboard (`CF_DIB`) so you can immediately paste it into emails, WhatsApp, or Word (`Ctrl + V`).
5. A **Self-Closing Notification Window** appears on the bottom-right corner:
   - Shows the exact file path and thumbnail preview.
   - Counts down from **6 seconds** before self-dismissing.
   - **Hover Pause**: Moving your mouse over the popup pauses the countdown timer.
   - **📂 Open in File Explorer**: 1-click button to jump directly to the saved image in Windows Explorer.

---

## 📁 5. Architecture & Configuration Files

```
DASHBOARD for Senior Officers/
├── main.py                     # High-DPI application bootstrap
├── pyqt_deck.py                # Flagship PyQt6 Steinway Piano Deck widget
├── pyqt_add_dialog.py          # 3-Tier Key Builder (Snippet, Custom, Shortcuts)
├── pyqt_saved_popup.py         # Self-closing snapshot popup with 6s timer
├── pyqt_snipper.py             # Native PyQt6 snapshot modal & snipping overlay
├── profile_manager.py          # Multi-user profile engine
├── profiles.json               # JSON store for isolated user profiles and keys
├── config_manager.py           # Configuration manager
├── config.json                 # Global configuration settings
├── audio_engine.py             # Windows Multimedia native MIDI synth (winmm.dll)
├── test_suite.py               # 8-point automated regression test suite
├── requirements.txt            # Dependency specification
├── run_piano_deck.bat          # 1-Click double-clickable batch launcher
├── README.md                   # Repository overview
├── USER_GUIDE.md               # Complete user & installation guide
├── index.html                  # GitHub Pages public showcase site
└── actions/
    ├── cleaner.py              # Recycle Bin & multi-cache deep purge
    ├── screenshot.py           # High-resolution screen & area capture
    ├── snippet.py              # Clipboard text injection & auto-paste engine
    ├── shortcuts.py            # Top 50 Windows shortcuts registry & simulator
    ├── process_killer.py       # Hung process termination engine
    └── dispatcher.py           # WhatsApp Web & Telegram Bot API dispatch
```

---

## ❓ 6. Troubleshooting & FAQ

#### Q1: Nothing appeared when launching the dashboard!
- **Resolution**: Check if you have an Ultra-HD (4K) monitor at high DPI scaling (e.g. 300%). The latest version auto-detects `QtWidgets.QApplication.primaryScreen().availableGeometry()` and docks directly above the taskbar. Also check your Windows taskbar for the **Executive Piano Deck** icon. Click it to bring the deck to the foreground.

#### Q2: Can I use Piano Deck on a dual-monitor or multi-monitor setup?
- **Yes**: Simply click and drag the dark mahogany top rail of the deck to any of your monitors. It will anchor and remember its placement.

#### Q3: Does the audio require external speakers or sound files?
- **No**: Piano Deck uses Windows' built-in General MIDI synthesizer (`winmm.dll` device 0). It routes through your default Windows audio output (headphones, monitor speakers, or laptop speakers) with zero latency and zero downloaded audio files.

#### Q4: How do I backup my custom piano keys and profiles?
- All custom profiles, buttons, and snippets are saved as clean human-readable JSON in `profiles.json`. Simply back up or copy `profiles.json` to preserve your layout across computers.

#### Q5: Can I paste long multi-line paragraphs or disclaimers?
- **Yes**: The Copied Content text bar in the Key Builder supports multi-line text, line breaks, bullet points, and unicode characters.

---

*Executive Piano Deck — Engineered for Precision, Speed, and Executive Elegance.*
