from json import load, dump

class SettingsManager:
    def __init__(self, settings_file='settings'):
        self.settings_file = settings_file

    def load_settings(self):
        try:
            with open(self.settings_file, "r") as f:
                return load(f)
        except FileNotFoundError:
            return {}

    def save_settings(self, data):
        settings = self.load_settings()
        settings.update(data)
        with open(self.settings_file, 'w') as f:
            dump(settings, f, indent=4)