import os
import webbrowser
import logging
import ctypes

class MusicPlayer:
    """
    Ambient Focus Audio Manager for Senior Officers.
    Manages executive background streams and ambient audio.
    """
    def __init__(self, stations=None, active_index=0):
        self.stations = stations or [
            {"title": "Executive Focus Lofi", "url": "https://www.youtube.com/watch?v=jfKfPfyJRdk"},
            {"title": "Classical Piano (Chopin & Mozart)", "url": "https://www.youtube.com/watch?v=4Tr0ovkx_-8"},
            {"title": "Deep Work Ambient Flow", "url": "https://www.youtube.com/watch?v=WPni755-Krg"},
            {"title": "Gentle Nature & Rain Meditation", "url": "https://www.youtube.com/watch?v=mPZkdNFkNps"}
        ]
        self.active_index = active_index % len(self.stations) if self.stations else 0
        self.is_playing = False
        self._winmm = ctypes.windll.winmm

    def toggle(self):
        """Toggles play/pause state. Returns (is_playing, current_title, summary_msg)."""
        if not self.stations:
            return (False, "No Station", "No music stations configured")

        station = self.stations[self.active_index]
        if not self.is_playing:
            # Start playing
            self.is_playing = True
            try:
                webbrowser.open_new_tab(station["url"])
                summary = f"Playing: {station['title']}"
            except Exception as e:
                logging.error(f"Failed to play music: {e}")
                summary = f"Error launching audio: {e}"
        else:
            # Toggle to next station or pause
            self.is_playing = False
            summary = f"Focus Audio Paused"

        return (self.is_playing, station["title"], summary)

    def next_station(self):
        """Advances to next ambient music station."""
        if not self.stations:
            return "No stations"
        self.active_index = (self.active_index + 1) % len(self.stations)
        station = self.stations[self.active_index]
        self.is_playing = True
        try:
            webbrowser.open_new_tab(station["url"])
        except Exception:
            pass
        return f"Now Playing: {station['title']}"

    def get_current_info(self):
        if not self.stations:
            return "Idle"
        station = self.stations[self.active_index]
        state = "Playing" if self.is_playing else "Paused"
        return f"{state}: {station['title']}"
