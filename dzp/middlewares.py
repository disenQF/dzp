# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html
import time
from scrapy import signals
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


class DzSpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


# 登录的中间件
class LoginMiddleware(object):
    def __init__(self):
        self.options = Options()
        # self.options.add_argument('--headless')
        self.driver = webdriver.Chrome(chrome_options=self.options)

    def process_request(self, request, spider):
        # 判断当前的请求url是否为login_url
        if request.url.startswith(spider.login_url):
            spider.logger.info('--开始模拟登录---')
            self.driver.get(request.url)  # 打开登录页面

            # 查找iframe, 并切换到frame中
            # 查找iframe中切换账号登录图标，并点击
            # 再点击账号和密码登录
            # 点击登录， 注意：登录的间隔时不要太短，不然会出验证码
            iframe = self.driver.find_element_by_xpath('//iframe')
            self.driver.switch_to.frame(iframe)
            time.sleep(1)
            qrcode = self.driver.find_element_by_xpath('//div[@class="icon-qrcode"]')
            qrcode.click()
            time.sleep(1)

            self.driver.find_element_by_xpath('//a[@id="tab-account"]').click()
            self.driver.find_element_by_xpath('//*[@id="account-textbox"]').send_keys('15035455735')
            self.driver.find_element_by_xpath('//*[@id="password-textbox"]').send_keys('fan427329')
            self.driver.find_element_by_xpath('//*[@id="login-button-account"]').click()

            time.sleep(2)

            self.driver.switch_to.default_content()

            user_info = self.driver.find_element_by_xpath('//*[@class="userinfo-container"]')
            if user_info:
                print('--登录成功--')
                # selenum_cookies => scrapy_cookie
                """
                {'_lxsdk_s': '167f7d9e6c5-327-beb-05d%7C%7C41',
                 '_hc.v': '407eb6f6-3ec1-2cd5-adff-6613a81c148e.1546051513',
                  '_lxsdk': '167f7d9e6c332-04ee97d7507144-10326653-75300-167f7d9e6c4c8', 
                  '_lxsdk_cuid': '167f7d9e6c332-04ee97d7507144-10326653-75300-167f7d9e6c4c8',
                   's_ViewType': '10',
                    'lgtoken': '09af88558-d1f5-4f4b-beb2-714f12c10188'}

                """
                cookie = {item["name"]: item["value"] for item in self.driver.get_cookies()}

        else:
            spider.logger.info('---非登录请求----')


class DzpDownloaderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)
