# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
import logging
import requests
import time

base_header = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36',
    'Accept-Encoding': 'gzip, deflate, sdch',
    'Accept-Language': 'zh-CN,zh;q=0.8'
}
proxxyy = ''

class ZhihuSpiderMiddleware(object):
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

class ProxyMiddleware(object):

    logger = logging.getLogger(__name__)

    def get_proxy(self):
        proxy = requests.get('http://192.168.99.1:5555/random').text
        if isinstance(proxy, bytes):
            proxy = proxy.decode('utf-8')
        proxy = 'http://' + proxy
        proxies = {
            'http':proxy
        }
        code_list = [200, 302]
        if requests.get('https://baidu.com',headers = base_header, proxies = proxies,allow_redirects=False,timeout = 5).status_code in code_list:
            return proxy
        else:
            self.get_proxy()

    def process_response(self, request, response, spider):
        global proxxyy
        if response.status == 403:
            proxxyy = self.get_proxy()
            return request
        else:
            return response

    def process_request(self, request, spider):
        self.logger.debug('Using Proxy')
        request.meta['proxy'] = proxxyy
        return None








