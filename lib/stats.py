import json


class PluginStats:

    def __init__(self, json_data):
        self.json = None
        self.name = None
        self.json_url = None
        self.total_installation = 0
        self.plugin_info_url = None

        self.create_plugin_data_from_json(json_data)

    def create_plugin_data_from_json(self, json_data):
        json_d = json.loads(json_data)
        self.json = json_d
        self.name = json_d["name"]
        self.total_installation = json_d["installations"][str(max(map(int, json_d["installations"].keys())))]

    def get_json(self):
        self.json['total_installation'] = str(self.total_installation)
        self.json['plugin_info_url'] = str(self.plugin_info_url)
        return self.json
