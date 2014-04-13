import json


class PluginStats:

    json = None
    name = None
    json_url = None
    total_installation = 0

    def __init__(self, json_data):
        self.create_plugin_data_from_json(json_data)

    def create_plugin_data_from_json(self, json_data):
        json_d = json.loads(json_data)
        self.json = json_d
        self.name = json_d["name"]
        self.total_installation = json_d["installations"][str(max(map(int, json_d["installations"].keys())))]
