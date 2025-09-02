import json, os

class State:
    def __init__(self, path: str):
        self.path = path
        if not os.path.exists(path):
            with open(path, "w") as f:
                f.write("{}")

    def get(self, key, default=None):
        try:
            with open(self.path, "r") as f:
                data = json.load(f)
        except Exception:
            data = {}
        return data.get(key, default)

    def set(self, key, value):
        try:
            with open(self.path, "r") as f:
                data = json.load(f)
        except Exception:
            data = {}
        data[key] = value
        with open(self.path, "w") as f:
            json.dump(data, f)
