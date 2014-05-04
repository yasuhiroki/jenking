import logging
import requests
import json
import sys
from lxml import etree
from html.parser import HTMLParser 
from html.entities import name2codepoint 
from datetime import date
from stats import PluginStats 


class PluginStatsCreator():

    def __init__(self, id):
        self.id = id
        self.plugin_stats_list = []
        self.thread_finish = False

    def create_plugin_stats(self, plugin_names):
        cnt = 0
        sum_plugins = len(plugin_names)
        for plugin_json in plugin_names:
            cnt += 1
            print("[Thread {0:4}] Create plugin datas [{1}/{2}]".format(self.id, str(cnt), str(sum_plugins)))
            if plugin_json is None:
                continue
            stats_file_url = "http://stats.jenkins-ci.org/plugin-installation-trend/" + plugin_json
            print("[Thread {0:4}] Get data: [{1}]".format(self.id, stats_file_url))
            try:
                r = requests.get(stats_file_url, timeout=5.0)
                stats = PluginStats(r.text)
            except:
                logging.warn(sys.exc_info())
                continue

            plugin_search_url = (
                "https://wiki.jenkins-ci.org/dosearchsite.action?queryString=" + 
                plugin_json[0:plugin_json.find(".stats.json")]
                )
            print("[Thread {0:4}] Get data: [{1}]".format(self.id, plugin_search_url))
            try:
                r = requests.get(plugin_search_url, timeout=10.0)
                tree = etree.HTML(r.text)
                first_link = tree.find(".//h3/a")
                stats.plugin_info_url = "https://wiki.jenkins-ci.org" + first_link.attrib["href"]
            except:
                logging.warn(sys.exc_info())
                continue
            self.plugin_stats_list.append(stats)
        self.thread_finish = True
        print("[Thread {0:4}] Finish".format(self.id))

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
        merged_data = self._merge_stats()
        merged_data["Modify_date"] = str(date.today())
        json_str = json.dumps(merged_data, sort_keys=True, indent=4)
        f = open(file_name,  'w')
        f.write(json_str)
        f.close()

    def _merge_stats(self):
        rtn = {"plugins":[]}
        for _stats in self.plugin_stats_list:
            rtn["plugins"].append(_stats.get_json())
        return rtn

    def _sort_total_installation(self, stats_list):
        import operator
        stats_list.sort(key=operator.attrgetter('total_installation'), reverse=True)
        return stats_list
