import json
import os

class UserSettings:
    def __init__(self):
        self.settings_file = "user_settings.json"
        self.settings = self.load_settings()

    def load_settings(self):
        if os.path.exists(self.settings_file):
            with open(self.settings_file, "r") as f:
                return json.load(f)
        return {}

    def save_settings(self):
        with open(self.settings_file, "w") as f:
            json.dump(self.settings, f)

    def get_setting(self, key, default=None):
        return self.settings.get(key, default)

    def set_setting(self, key, value):
        self.settings[key] = value
        self.save_settings()

    def clear_settings(self):
        self.settings = {}
        self.save_settings()