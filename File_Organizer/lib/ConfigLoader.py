import os
import sys
import json

class ConfigLoader:
    '''
    Class responsible for locating and loading the configuration file.
    '''
    def __init__(self):
        '''
         Initialize the ConfigLoader with an empty configuration.
        '''
        self.config = {}

    def get_config_path(self):
        '''
        Get the path to the configuration file.
        :return: Absolute path to the configuration file.
        '''
        external_config = os.path.join(os.path.dirname(os.path.abspath(sys.argv[0])), "config.json")
        if os.path.exists(external_config):
            return external_config

        if getattr(sys, 'frozen', False):
            return os.path.join(sys._MEIPASS, "config.json")

        return os.path.join(os.path.dirname(__file__), "config.json")

    def load_config(self):
        '''
        Load the configuration from the configuration file.
        :return: dict: Loaded configuration.
        '''
        config_path = self.get_config_path()
        if not os.path.exists(config_path):
            raise FileNotFoundError(f"Config file not found: {config_path}")

        with open(config_path, "r", encoding="utf-8") as f:
            try:
                raw_config = json.load(f)
            except json.JSONDecodeError as e:
                raise ValueError(f"Config file is not valid JSON: {e}")

        self.config = raw_config
        return self.config
