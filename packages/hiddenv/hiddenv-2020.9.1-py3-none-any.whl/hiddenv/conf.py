import importlib
import os
from typing import Dict


class Settings:
    settings: Dict
    configured: bool

    def __init__(self):
        self.reset()

    def __getattr__(self, name):
        # ToDo keys can be lowercase and can start with _
        if not name.isupper():
            return self.__dict__[name]
        return self.settings[name]

    def configure(self):
        if self.configured:
            raise ValueError("Already configured.")

        module = os.environ.get("SETTINGS_MODULE")
        if not module:
            raise KeyError("Environment variable 'SETTINGS_MODULE' not set.")

        settings_module = importlib.import_module(module)
        for setting in dir(settings_module):
            if setting.isupper():
                self.settings[setting] = getattr(settings_module, setting)
        self.configured = True

    def reset(self):
        self.settings = {}
        self.configured = False

    def load(self, klass):
        # ToDo validate annotations
        return klass(
            **{
                key: self.settings[key.upper()]
                for key in klass.__annotations__
                if key.upper() in self.settings
            }
        )


settings = Settings()
