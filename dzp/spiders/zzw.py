# -*- coding: utf-8 -*-
import scrapy


class ZzwSpider(scrapy.Spider):
    name = 'zzw'
    allowed_domains = ['www.dianping.com']
    start_urls = ['http://www.dianping.com/']

    def parse(self, response):
        pass
