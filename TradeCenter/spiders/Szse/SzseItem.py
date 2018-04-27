# -*- coding: utf-8 -*-
import scrapy


class SzseItem(scrapy.Item):

    # 业务规则标题
    ruletitle = scrapy.Field()
    # 详情连接
    rulelink = scrapy.Field()
    # 发布日期
    ruledate = scrapy.Field()
    # 页面内容
    content = scrapy.Field()
    # 文件路径
    file_urls = scrapy.Field()
    # 文件标题
    filename = scrapy.Field()
    # 文件类型
    filepath = scrapy.Field()