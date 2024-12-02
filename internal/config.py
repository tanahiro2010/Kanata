import json

class Config(object):
    def __init__(self, config_path: str):
        self.config_path = config_path
        return

    def load_config(self):
        return json.loads(open(file=self.config_path, mode="w").read())

    def save_config(self, data: json):
        return open(file=self.config_path, mode="w").write(json.dumps(data, indent=4))

