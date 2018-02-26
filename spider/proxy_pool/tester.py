import asyncio
import aiohttp
import time
from db import RedisClient
from setting import *
from utils import base_header

class Tester(object):
    def __init__(self):
        self.redis = RedisClient()

    async def test_single_proxy(self, proxy):
        conn = aiohttp.TCPConnector(verify_ssl=False)
        async with aiohttp.ClientSession(connector=conn) as session:
            try:
                if isinstance(proxy,bytes):
                    proxy = proxy.decode('utf-8')
                real_proxy = 'http://' + proxy
                print('正在测试', proxy)
                async with session.get(TEST_URL, headers = base_header, proxy=real_proxy, timeout=3, allow_redirects=False) as response:
                    if response.status in VALID_STATUS_CODES:
                        self.redis.max(proxy)
                        print('代理可用',proxy)
                    else:
                        self.redis.decrease(proxy)
                        print('请求错误',response.status,proxy)
            except (asyncio.TimeoutError,aiohttp.client_exceptions.ClientProxyConnectionError,aiohttp.ClientError):
                self.redis.decrease(proxy)
                print('代理请求失败',proxy)

    def run(self):
        print('测试器开始运行')
        try:
            count = self.redis.count()
            print('当前剩下代理数量:',count)
            for i in range(0, count, BATCH_TEST_SIZE):
                start = i
                stop = min(i + BATCH_TEST_SIZE ,count)
                print('正在测试第', start + 1, '-', stop, '的代理')
                test_proxies = self.redis.batch(start,stop)
                loop = asyncio.get_event_loop()
                tasks = [self.test_single_proxy(proxy) for proxy in test_proxies]
                loop.run_until_complete(asyncio.wait(tasks))
                time.sleep(5)
        except Exception as e:
            print('测试器发生错误', e.args)

