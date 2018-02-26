from db import RedisClient
from crawler import Crawler
from setting import *

class Getter():
    def __init__(self):
        self.redis = RedisClient()
        self.crawler = Crawler()

    def is_over_threshold(self):
        if self.redis.count() >= POOL_UPPER_THRESHOLD:
            return True
        else:
            return False

    def run(self):
        print('产生器开始执行')
        if not self.is_over_threshold():
            for x in range(0,self.crawler.__CrawlFuncCount__):
                callback = self.crawler.__CrawlFunc__[x]
                proxies = self.crawler.get_proxies(callback)
                for proxy in proxies:
                    self.redis.add(proxy)

