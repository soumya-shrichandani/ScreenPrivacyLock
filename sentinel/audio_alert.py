# ==============================================================================
# PROJECT SMART SENTINEL — AI ANTI-SHOULDER SURFER & PRIVACY SHIELD
# AUTHOR / CREATOR: Soumya Shrichandani
# COPYRIGHT (C) 2026 SOUMYA SHRICHANDANI. ALL RIGHTS RESERVED.
# ==============================================================================

import threading
import time
from sentinel import config

try:
    import winsound
    HAS_WINSOUND = True
except ImportError:
    HAS_WINSOUND = False


class SoundSynthesizer:
    """
    Asynchronous synthesized audio alerts for Sentinel threat notifications.
    Non-blocking: executes via background daemon threads.
    """
    def __init__(self):
        self.last_alert_time = 0.0

    def _play_pattern(self, freq_durations):
        if not HAS_WINSOUND or not config.AUDIO_ALERTS_ENABLED:
            return
        try:
            for freq, dur_ms in freq_durations:
                winsound.Beep(int(freq), int(dur_ms))
        except Exception:
            pass

    def alert_intruder(self):
        """High-urgency two-tone security breach alert."""
        now = time.time()
        if now - self.last_alert_time < 3.0:
            return
        self.last_alert_time = now

        pattern = [(1600, 120), (1200, 100), (2000, 180)]
        threading.Thread(target=self._play_pattern, args=(pattern,), daemon=True).start()

    def alert_absence_warning(self):
        """Soft pulsing warning before workstation auto-locks."""
        pattern = [(750, 80), (750, 80)]
        threading.Thread(target=self._play_pattern, args=(pattern,), daemon=True).start()

    def chime_secured(self):
        """Friendly ascending chime indicating area re-secured."""
        pattern = [(650, 80), (950, 100), (1300, 140)]
        threading.Thread(target=self._play_pattern, args=(pattern,), daemon=True).start()
