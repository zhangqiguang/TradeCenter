# -*- coding: utf-8 -*-
import urllib
from urllib.parse import urlparse

class DataFormatPipeline(object):

    def process_item(self, item, spider):
        if spider.name == "szse":
            self.format_szse_data(item)
        return item

    def format_szse_data(self, item):
        item["ruledate"] = str(item["ruledate"]).replace('[', '').replace(']', '')
        if "file_urls" in item.keys():
            path = urlparse(item["file_urls"][0]).path
            path = urllib.parse.unquote(path)
            item["filepath"] = [path]
        else:
            item["file_urls"] = ""
            item["filename"] = ""
            item["filepath"] = ""
