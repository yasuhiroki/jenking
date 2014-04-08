import requests
import json
from html.parser import HTMLParser 
from html.entities import name2codepoint 
from stats import PluginStats 


class PluginStatsCreator():

    def __init__(self, id):
        self.id = id
        self.plugin_stats_list = []
        self.thread_finish = False

    def create_plugin_stats(self, plugin_names):
        print("[Thread] ", self.id, " Create plugin datas")
        for plugin_json_url in plugin_names:
            if plugin_json_url is None:
                continue
            print("[Thraed ", self.id, "] Get data: ", plugin_json_url)
            try:
                r = requests.get("http://stats.jenkins-ci.org/plugin-installation-trend/" + plugin_json_url, timeout=5.0)
            except:
                continue
            self.plugin_stats_list.append(PluginStats(r.text))
        self.thread_finish = True
        print("[Thread] Finish")

    def create_plugin_data(self, plugin_datas):
        return False


class StatsHtmlParser(HTMLParser):

    json_list = []

    def handle_starttag(self, tag, attrs):
        if tag == "a":
            for attr in attrs:
                print("  attr:", attr)
                print("  attr[0]:", attr[0])
                print("  attr[1]:", attr[1])
                if (attr[0] == "href"
                    and attr[1].count("stats.json") > 0):
                    self.json_list.append(attr[1])
    """
    def handle_endtag(self, tag):
        print("End tag    :", tag)

    def handle_data(self, data):
        print("Data       :", str(data))

    def handle_comment(self, data):
        print("Comment    :", data)
    """


class PluginStatsFormatter():
    
    import sys, os
    default_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../js/stats.json')

    def __init__(self):
        plugin_stats_list = []

    def set_plugin_stats_list(self, plugin_stats_list):
        self.plugin_stats_list = plugin_stats_list

    def dump(self, file_name=""):
        if file_name == "":
            file_name = self.default_file_path
        self.plugin_stats_list = self._sort_total_installation(self.plugin_stats_list)
        json_str = json.dumps(self._merge_stats(), sort_keys=True, indent=4)
        print(json_str) 
        f = open(file_name,  'w')
        f.write(json_str)
        f.close()

    def _merge_stats(self):
        rtn = {"plugins":[]}
        for _stats in self.plugin_stats_list:
            rtn["plugins"].append(_stats.json)
            rtn["plugins"][len(rtn["plugins"]) - 1]['total_installation'] = str(_stats.total_installation)
        return rtn

    def _sort_total_installation(self, stats_list):
        import operator
        stats_list.sort(key=operator.attrgetter('total_installation'), reverse=True)
        return stats_list
