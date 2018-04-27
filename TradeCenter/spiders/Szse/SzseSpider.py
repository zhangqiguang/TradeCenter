# -*- coding: utf-8 -*-
import scrapy
from TradeCenter.spiders.Szse import SzseItem
import re

class SzseSpider(scrapy.Spider):
    """
        功能：爬取深圳证券交易所法律/规则
        """
    # 爬虫名
    name = "szse"
    # 爬虫作用范围
    allowed_domains = ["szse.cn"]

    url = "http://www.szse.cn/main/rule/bsywgz/"

    offset = 0
    totalpage = 0
    # 起始url
    start_urls = [url + "index.shtml"]

    def parse(self, response):
        note = response.xpath("//td[@class='pd6']")
        for each in note.xpath(".//a"):
            # 初始化模型对象
            if self.totalpage == 0:
                pagetext = response.xpath("//td/text()").re('第\d+页/共\d+页')[0]
                totalpage = int(re.findall("\d+", pagetext)[1])
                # totalpage = 2
            item = SzseItem.SzseItem()
            item['rulelink'] = each.xpath("./@href").extract()[0]
            item['ruletitle'] = each.xpath("./text()").extract()[0]
            item['ruledate'] = each.xpath("../span/text()").extract()[0]

            link = str(item["rulelink"])
            b = link.index("/")
            idx_shtml = link.rfind(".shtml")
            idx_pdf = link.rfind(".pdf")
            idx_doc = link.rfind(".doc")
            e = 0
            if idx_shtml > 0:
                e = idx_shtml + 6
            elif idx_pdf > 0:
                e = idx_pdf + 4
            elif idx_doc > 0:
                e = idx_doc + 4
            item["rulelink"] = "http://www.szse.cn" + link[b:e]
            if idx_shtml > 0:
                request = scrapy.Request(url=item["rulelink"], callback=self.parse_content)
                request.meta['item'] = item
                yield request
            if idx_pdf > 0 or idx_doc > 0:
                item["file_urls"] = [item["rulelink"]]
                item["filename"] = item["ruletitle"]
                item["content"] = ""
                yield item

        if self.offset < totalpage - 1:
            self.offset += 1
        yield scrapy.Request(self.url + "index_" + str(self.offset) + ".shtml", callback=self.parse)

    def parse_content(self, response):
        item = response.meta['item']
        content = response.xpath("//div[@class='auto_height w_width']")
        item["content"] = content.extract()[0]
        a = content.xpath('.//a[re:test(@href, ".*.[doc|pdf]$")]')
        if a:
            item["file_urls"] = ["http://www.szse.cn" + a.xpath("./@href").extract()[0]]
            item["filename"] = a.xpath("./text()").extract()[0]
        yield item
