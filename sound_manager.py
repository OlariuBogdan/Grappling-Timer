import os
import winsound
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class SoundManager:
    def __init__(self, root_path):
        self.sounds_dir = os.path.join(root_path, 'sounds')
        self.pygame_available = False
        self.audio_tracks = {}

        # Enhanced sound mapping with better organization
        self.sound_mapping = {
            'prepare': 'pregatire.mp3',     # Preparation countdown start
            'work': 'start 2.mp3',          # Work round start
            'rest': 'final.mp3',            # Rest period start
            'warning': 'start.wav',         # 10-second warning
            'finished': 'final 2.mp3',      # Training completion
            'button': None,                 # UI button feedback (beep only)
            'error': None                   # Error feedback (beep only)
        }

        # Fallback frequencies for different events (Windows beep)
        self.fallback_frequencies = {
            'prepare': (800, 800),    # freq, duration
            'work': (1200, 200),
            'rest': (800, 300),
            'warning': (1000, 150),
            'finished': (1500, 500),
            'button': (600, 50),
            'error': (400, 200)
        }

        self.initialize_pygame()

    def initialize_pygame(self):
        """Initialize pygame mixer with error handling."""
        try:
            import pygame
            pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=512)
            self.pygame_available = True
            logging.info("Pygame initialized successfully")
            self.load_all_sounds()
        except ImportError:
            logging.warning("Pygame not available. Using system beeps only.")
            self.pygame_available = False
        except Exception as e:
            logging.error(f"Failed to initialize pygame: {e}. Using system beeps.")
            self.pygame_available = False

    def load_all_sounds(self):
        """Load all sound files into memory for instant playback."""
        if not self.pygame_available:
            return

        import pygame

        loaded_count = 0
        for event, filename in self.sound_mapping.items():
            if filename is None:
                continue  # Skip events that only use beeps

            path = os.path.join(self.sounds_dir, filename)
            if os.path.exists(path):
                try:
                    self.audio_tracks[event] = pygame.mixer.Sound(path)
                    loaded_count += 1
                    logging.debug(f"Loaded sound: {filename}")
                except pygame.error as e:
                    logging.error(f"Failed to load {filename}: {e}")
                except Exception as e:
                    logging.error(f"Unexpected error loading {filename}: {e}")
            else:
                logging.warning(f"Sound file not found: {filename}")

        logging.info(f"Loaded {loaded_count} sound files")

    def play(self, event_name, fallback_freq=None, fallback_duration=None):
        """
        Play a sound event.

        Args:
            event_name (str): The event to play ('prepare', 'work', 'rest', etc.)
            fallback_freq (int, optional): Custom fallback frequency
            fallback_duration (int, optional): Custom fallback duration
        """
        # Try pygame first
        if self.pygame_available and event_name in self.audio_tracks:
            try:
                sound = self.audio_tracks[event_name]
                sound.stop()  # Stop if already playing
                sound.play()
                return True
            except Exception as e:
                logging.error(f"Error playing {event_name} with pygame: {e}")

        # Fallback to system beep
        if event_name in self.fallback_frequencies:
            freq, duration = self.fallback_frequencies[event_name]
            if fallback_freq is not None:
                freq = fallback_freq
            if fallback_duration is not None:
                duration = fallback_duration

            try:
                winsound.Beep(freq, duration)
                return True
            except Exception as e:
                logging.error(f"Error playing system beep for {event_name}: {e}")

        return False

    def set_volume(self, volume):
        """Set master volume for all sounds (0.0 to 1.0)."""
        if not self.pygame_available:
            return

        try:
            import pygame
            for sound in self.audio_tracks.values():
                sound.set_volume(volume)
        except Exception as e:
            logging.error(f"Error setting volume: {e}")

    def get_available_sounds(self):
        """Return list of events that have audio files loaded."""
        return list(self.audio_tracks.keys())

    def test_sound(self, event_name):
        """Test play a specific sound event."""
        return self.play(event_name)