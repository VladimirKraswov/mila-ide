import json
import os

class SettingsManager:
    def __init__(self, settings_file="settings.json"):
        self.settings_file = settings_file
        self.settings = {
            "font_size": 10  # Default font size
        }
        self.load_settings()

    def load_settings(self):
        """Load settings from the JSON file."""
        if os.path.exists(self.settings_file):
            with open(self.settings_file, "r") as file:
                self.settings.update(json.load(file))

    def save_settings(self):
        """Save current settings to the JSON file."""
        with open(self.settings_file, "w") as file:
            json.dump(self.settings, file, indent=4)

    def get_font_size(self):
        return self.settings.get("font_size", 10)

    def set_font_size(self, font_size):
        self.settings["font_size"] = font_size