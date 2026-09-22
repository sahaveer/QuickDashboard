import ctypes
import time
import threading
import logging

class AudioEngine:
    """
    Windows Native MIDI Synthesizer Engine.
    Uses winmm.dll to output real Acoustic Grand Piano notes with zero external audio assets.
    """
    def __init__(self, enabled=True):
        self.enabled = enabled
        self._hmidi = None
        self._winmm = None
        self._lock = threading.Lock()
        self._init_midi()

    def _init_midi(self):
        try:
            self._winmm = ctypes.windll.winmm
            hmidi = ctypes.c_void_p()
            # Device -1 selects MIDI_MAPPER (Microsoft GS Wavetable Synth)
            res = self._winmm.midiOutOpen(ctypes.byref(hmidi), -1, 0, 0, 0)
            if res == 0:
                self._hmidi = hmidi
                # Program change to Instrument 0 (Acoustic Grand Piano) on Channel 0
                # 0x0000C0 = Program Change, Channel 0, Program 0
                self._winmm.midiOutShortMsg(self._hmidi, 0x0000C0)
            else:
                logging.warning(f"Could not open Windows MIDI Mapper, error code {res}")
        except Exception as e:
            logging.error(f"Failed to initialize MIDI device: {e}")

    def play_note(self, note=60, velocity=95, duration=0.3):
        """
        Plays a MIDI note on the Grand Piano.
        note: MIDI note number (60 = C4 Middle C, 62 = D4, etc.)
        velocity: Strike strength (0-127)
        duration: Duration in seconds before Note Off
        """
        if not self.enabled or not self._hmidi:
            return

        def _worker():
            with self._lock:
                if not self._hmidi:
                    return
                # Note On: 0x90 | Channel 0, Note, Velocity -> (velocity << 16) | (note << 8) | 0x90
                msg_on = (int(velocity) << 16) | (int(note) << 8) | 0x90
                self._winmm.midiOutShortMsg(self._hmidi, msg_on)

            time.sleep(duration)

            with self._lock:
                if not self._hmidi:
                    return
                # Note Off: 0x80 | Channel 0, Note, 0 -> (0 << 16) | (note << 8) | 0x80
                msg_off = (int(note) << 8) | 0x80
                self._winmm.midiOutShortMsg(self._hmidi, msg_off)

        threading.Thread(target=_worker, daemon=True).start()

    def play_chord(self, notes=[60, 64, 67, 72], velocity=90, duration=0.4):
        """Plays an executive harmonious chord (e.g. on clean completion)."""
        if not self.enabled:
            return
        for n in notes:
            self.play_note(note=n, velocity=velocity, duration=duration)
            time.sleep(0.04)

    def close(self):
        with self._lock:
            if self._hmidi and self._winmm:
                try:
                    self._winmm.midiOutClose(self._hmidi)
                except Exception:
                    pass
                self._hmidi = None
