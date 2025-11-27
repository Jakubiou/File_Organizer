import os
import sys

class ConfigLoader:
    @staticmethod
    def get_config_path():
        external_config = os.path.join(os.path.dirname(os.path.abspath(sys.argv[0])), "config.json")
        if os.path.exists(external_config):
            return external_config

        if getattr(sys, 'frozen', False):
            return os.path.join(sys._MEIPASS, "config.json")

        return os.path.join(os.path.dirname(__file__), "config.json")
