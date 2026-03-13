import json
import os

class ConfigManager:
    def __init__(self, config_file="config.json"):
        self.config_file = config_file
        self.default_config = {
            "last_preset": "Training",
            "work_time": 300,  # 5 minutes
            "rest_time": 60,   # 1 minute
            "total_rounds": 5,
            "prep_time": 12,
            "volume": 50,
            "fullscreen": True,
            "music_folder": "",
            "window_width": 1920,
            "window_height": 1080
        }
        self.config = self.load_config()

    def load_config(self):
        """Load configuration from file, or create default if doesn't exist."""
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    loaded_config = json.load(f)
                    # Merge with defaults to handle new config options
                    config = self.default_config.copy()
                    config.update(loaded_config)
                    return config
            except (json.JSONDecodeError, IOError) as e:
                print(f"Error loading config: {e}. Using defaults.")
                return self.default_config.copy()
        else:
            return self.default_config.copy()

    def save_config(self):
        """Save current configuration to file."""
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=4, ensure_ascii=False)
        except IOError as e:
            print(f"Error saving config: {e}")

    def get(self, key, default=None):
        """Get a configuration value."""
        return self.config.get(key, default if default is not None else self.default_config.get(key))

    def set(self, key, value):
        """Set a configuration value."""
        self.config[key] = value
        self.save_config()

    def reset_to_defaults(self):
        """Reset configuration to default values."""
        self.config = self.default_config.copy()
        self.save_config()