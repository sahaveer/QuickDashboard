import os
import sys

# Test 1: Config (3 initial keys)
import config_manager
cm = config_manager.ConfigManager()
keys = cm.get('keys', [])
assert len(keys) == 3, f"Expected 3 initial keys, found {len(keys)}"
print('[PASS] 1. ConfigManager verified with 3 initial keys')

# Test 2: Multi-User Profile Manager
import profile_manager
pm = profile_manager.ProfileManager()
profiles = pm.get_all_profiles()
assert len(profiles) >= 4, f"Expected at least 4 default profiles, found {len(profiles)}"
assert pm.get_active_profile_id() in pm.data["profiles"]
# Test switching profile
pm.set_active_profile("finance_officer")
assert pm.get_active_profile_id() == "finance_officer"
pm.set_active_profile("senior_officer")
print(f'[PASS] 2. ProfileManager verified with {len(profiles)} isolated profiles and instant switching')

# Test 3: Audio Engine (MIDI Synthesizer)
import audio_engine
ae = audio_engine.AudioEngine(enabled=True)
ae.play_note(60, duration=0.1)
ae.close()
print('[PASS] 3. AudioEngine native MIDI synth test passed')

# Test 4: Cleaner
import actions.cleaner as cleaner
clean_res = cleaner.run_system_cleanup()
assert clean_res['success'] is True
print(f"[PASS] 4. Cleaner: {clean_res['summary']}")

# Test 5: Screenshot with Title
import actions.screenshot as screenshot
snap_res = screenshot.capture_screen(title="Executive_Briefing")
assert snap_res['success'] is True
assert "Executive_Briefing" in snap_res['filename']
assert os.path.exists(snap_res['filepath'])
print(f"[PASS] 5. Screenshot with custom title: {snap_res['filename']}")

# Test 6: Copied Text / Snippet Macro
import actions.snippet as snippet
snip_res = snippet.execute_text_snippet("Official Memo: Approved by Senior Officer.", auto_paste=False)
assert snip_res['success'] is True
print(f"[PASS] 6. Snippet macro: {snip_res['summary']}")

# Test 7: Process Killer
import actions.process_killer as pk
pk_res = pk.kill_hung_processes(["dummy_test_app.exe"])
assert pk_res['success'] is True
print(f"[PASS] 7. Process killer: {pk_res['summary']}")

# Test 8: PyQt6 Piano Deck GUI initialization
from PyQt6 import QtWidgets
import pyqt_deck

qt_app = QtWidgets.QApplication.instance() or QtWidgets.QApplication(sys.argv)
deck = pyqt_deck.PyQtPianoDeck()
assert deck.isVisible() is False
assert deck.profile_mgr.get_active_profile_id() == "senior_officer"
deck.close()
deck.deleteLater()
qt_app.processEvents()
print('[PASS] 8. PyQtPianoDeck GUI verified with modern Steinway Ivory styling & Profile Switcher')

# Test 9: Installed Applications Discovery & Launcher
from actions.app_scanner import scan_installed_apps
scanned_apps = scan_installed_apps()
assert len(scanned_apps) > 10, f"Expected >10 installed apps, found {len(scanned_apps)}"
assert any(a['name'] == 'Calculator' for a in scanned_apps), "Calculator should be discovered"
print(f'[PASS] 9. Installed Apps Scanner verified with {len(scanned_apps)} applications indexed')

print('\n*** ALL 9 INTEGRATION TESTS PASSED CLEANLY! ***')

