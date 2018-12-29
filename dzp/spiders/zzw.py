# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request

"""
https://github.com/disenQF/dzp.git
"""

class ZzwSpider(scrapy.Spider):
    name = 'zzw'
    allowed_domains = ['www.dianping.com',
                       'account.dianping.com']

    # def start_requests(self):
    #     self.login_url = 'https://account.dianping.com/login?'
    #     yield Request(self.login_url, callback=self.parse_zzw_home)

    start_urls = ['http://www.dianping.com/shop/6232395/review_all/p2']

    def parse(self, response):
        print(response.url, '---开始解析---')