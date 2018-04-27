from scrapy.pipelines.files import FilesPipeline
from urllib.parse import urlparse
from os.path import basename, dirname, join
import urllib

class FileDownloadPipeline(FilesPipeline):

    def file_path(self, request, response=None, info=None):
        if self.spiderinfo.spider.name == "szse":
            path = urlparse(request.url).path
            return urllib.parse.unquote(path)
        return None
        # return join(basename(dirname(path)), basename(path))