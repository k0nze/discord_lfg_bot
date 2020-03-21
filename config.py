import json

class Config():
    def __init__(self, config_json_path):
        self.config_json_path = config_json_path

    def get(self, key):
        config = None
        with open(self.config_json_path) as config_json:
            config = json.load(config_json)

        return config[key]
