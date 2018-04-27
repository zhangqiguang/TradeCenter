# -*- coding: utf-8 -*-
import json

class JsonStorePipeline(object):
    def __init__(self):
        self.filename = None

    def process_item(self, item, spider):
        if spider.name == "szse":
            if self.filename == None:
                self.filename = open("szse.json", "wb+")
            text = json.dumps(dict(item), ensure_ascii = False) + ",\n"
            self.filename.write(text.encode("utf-8"))
        if spider.name == "position":
            if self.filename == None:
                self.filename = open("position.json", "wb+")
            text = json.dumps(dict(item), ensure_ascii = False) + ",\n"
            self.filename.write(text.encode("utf-8"))
        if spider.name == "tencent":
            if self.filename == None:
                self.filename = open("tencent.json", "wb+")
            text = json.dumps(dict(item), ensure_ascii = False) + ",\n"
            self.filename.write(text.encode("utf-8"))
        return item

    def close_spider(self, spider):
        if self.filename:
            self.filename.close()