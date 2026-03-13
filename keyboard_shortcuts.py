import tkinter as tk

class KeyboardShortcuts:
    def __init__(self, root, timer_app):
        self.root = root
        self.timer_app = timer_app
        self.setup_shortcuts()

    def setup_shortcuts(self):
        """Setup keyboard shortcuts for the application."""
        # Timer controls
        self.root.bind('<space>', lambda e: self.toggle_timer())  # Spacebar to start/pause
        self.root.bind('<Return>', lambda e: self.toggle_timer())  # Enter to start/pause
        self.root.bind('<KeyPress-r>', lambda e: self.reset_timer())  # R to reset
        self.root.bind('<KeyPress-R>', lambda e: self.reset_timer())  # Shift+R to reset

        # Preset shortcuts
        self.root.bind('<KeyPress-1>', lambda e: self.load_preset_by_index(0))
        self.root.bind('<KeyPress-2>', lambda e: self.load_preset_by_index(1))
        self.root.bind('<KeyPress-3>', lambda e: self.load_preset_by_index(2))
        self.root.bind('<KeyPress-4>', lambda e: self.load_preset_by_index(3))
        self.root.bind('<KeyPress-5>', lambda e: self.load_preset_by_index(4))

        # Music controls
        self.root.bind('<KeyPress-p>', lambda e: self.toggle_music())
        self.root.bind('<KeyPress-P>', lambda e: self.toggle_music())
        self.root.bind('<KeyPress-n>', lambda e: self.next_track())
        self.root.bind('<KeyPress-N>', lambda e: self.next_track())
        self.root.bind('<KeyPress-b>', lambda e: self.prev_track())
        self.root.bind('<KeyPress-B>', lambda e: self.prev_track())

        # Volume controls
        self.root.bind('<KeyPress-plus>', lambda e: self.volume_up())
        self.root.bind('<KeyPress-equal>', lambda e: self.volume_up())  # = is same as +
        self.root.bind('<KeyPress-minus>', lambda e: self.volume_down())
        self.root.bind('<KeyPress-underscore>', lambda e: self.volume_down())  # Shift+-

        # Settings adjustment (when not running)
        self.root.bind('<KeyPress-w>', lambda e: self.adjust_work_time(1))   # W to increase work time
        self.root.bind('<KeyPress-W>', lambda e: self.adjust_work_time(-1))  # Shift+W to decrease
        self.root.bind('<KeyPress-t>', lambda e: self.adjust_rest_time(1))   # T to increase rest time
        self.root.bind('<KeyPress-T>', lambda e: self.adjust_rest_time(-1))  # Shift+T to decrease
        self.root.bind('<KeyPress-u>', lambda e: self.adjust_rounds(1))      # U to increase rounds
        self.root.bind('<KeyPress-U>', lambda e: self.adjust_rounds(-1))     # Shift+U to decrease

        # Fullscreen toggle (already handled in main app)
        # F11 and Escape are handled in the main timer class

    def toggle_timer(self):
        """Toggle timer start/pause."""
        if self.timer_app.state == "IDLE":
            self.timer_app.toggle_timer()
        elif self.timer_app.state in ["WORK", "REST", "PREPARE"]:
            self.timer_app.toggle_pause()

    def reset_timer(self):
        """Reset the timer."""
        if self.timer_app.state != "IDLE":
            self.timer_app.reset_timer()

    def load_preset_by_index(self, index):
        """Load preset by index (0-4)."""
        if self.timer_app.state == "IDLE":
            presets = list(self.timer_app.presets.keys())
            if 0 <= index < len(presets):
                self.timer_app.load_preset(presets[index])

    def toggle_music(self):
        """Toggle music playback."""
        self.timer_app.toggle_music()

    def next_track(self):
        """Go to next track."""
        self.timer_app.next_track()

    def prev_track(self):
        """Go to previous track."""
        self.timer_app.prev_track()

    def volume_up(self):
        """Increase volume."""
        current_volume = self.timer_app.volume_slider.get()
        new_volume = min(100, current_volume + 10)
        self.timer_app.volume_slider.set(new_volume)
        self.timer_app.change_volume(str(new_volume))

    def volume_down(self):
        """Decrease volume."""
        current_volume = self.timer_app.volume_slider.get()
        new_volume = max(0, current_volume - 10)
        self.timer_app.volume_slider.set(new_volume)
        self.timer_app.change_volume(str(new_volume))

    def adjust_work_time(self, direction):
        """Adjust work time (+1 or -1 minute)."""
        if self.timer_app.state == "IDLE":
            if direction > 0:
                self.timer_app.increase_work()
            else:
                self.timer_app.decrease_work()

    def adjust_rest_time(self, direction):
        """Adjust rest time (+1 or -1 minute)."""
        if self.timer_app.state == "IDLE":
            if direction > 0:
                self.timer_app.increase_rest()
            else:
                self.timer_app.decrease_rest()

    def adjust_rounds(self, direction):
        """Adjust number of rounds (+1 or -1)."""
        if self.timer_app.state == "IDLE":
            if direction > 0:
                self.timer_app.increase_rounds()
            else:
                self.timer_app.decrease_rounds()

    @staticmethod
    def get_shortcuts_help():
        """Return a string with all available keyboard shortcuts."""
        return """
=== KEYBOARD SHORTCUTS ===

TIMER CONTROLS:
  Space/Enter  - Start timer or toggle pause
  R           - Reset timer

PRESETS (when idle):
  1-5         - Load preset 1-5

MUSIC CONTROLS:
  P           - Play/Pause music
  N           - Next track
  B           - Previous track
  +/-         - Volume up/down

SETTINGS (when idle):
  W/Shift+W   - Increase/Decrease work time
  T/Shift+T   - Increase/Decrease rest time
  U/Shift+U   - Increase/Decrease rounds

OTHER:
  F11         - Toggle fullscreen
  Escape      - Exit fullscreen

=== END SHORTCUTS ===
        """.strip()