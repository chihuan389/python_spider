import redis
from setting import REDIS_HOST,REDIS_KEY,REDIS_PORT
from setting import INITIAL_SCORE,MAX_SCORE,MIN_SCORE
import re
from random import choice
from error import PoolEmptyError

pool = redis.ConnectionPool(host = REDIS_HOST,port = REDIS_PORT,decode_responses = True)

class RedisClient(object):
    def __init__(self):
        self.db = redis.StrictRedis(connection_pool=pool)

    def add(self,proxy,score = INITIAL_SCORE):
        if not re.match(r'\d+\.\d+\.\d+\.\d+\:\d+',proxy):
            print('代理不规范',proxy)
            return
        if not self.db.zscore(REDIS_KEY,proxy):
            return self.db.zadd(REDIS_KEY,score,proxy)

    def radom(self):
        result = self.db.zrevrangebyscore(REDIS_KEY,MAX_SCORE,MAX_SCORE)
        if len(result):
            return choice(result)
        else:
            result = self.db.zrevrange(REDIS_KEY, 0 , 100)
            if len(result):
                return choice(result)
            else:
                raise PoolEmptyError

    def exists(self,proxy):
        if self.db.zscore(REDIS_KEY,proxy):
            return True
        else:
            return False
        # return not self.db.zscore(REDIS_KEY,proxy) == None
    def max(self,proxy):
        print('代理',proxy,'可用，设置为',MAX_SCORE)
        return self.db.zadd(REDIS_KEY, MAX_SCORE, proxy)

    def count(self):
        return self.db.zcard(REDIS_KEY)

    def all(self):
        return self.db.zrangebyscore(REDIS_KEY, MIN_SCORE, MAX_SCORE)

    def decrease(self,proxy):
        score = self.db.zscore(REDIS_KEY,proxy)
        if score and score > MIN_SCORE:
            print('代理', proxy, '当前分数', score, '减10')
            return self.db.zincrby(REDIS_KEY, proxy, -10)
        else:
            print('代理', proxy, '当前分数', score, '移除')
            return self.db.zrem(REDIS_KEY, proxy)

    def batch(self, start, stop):
        return self.db.zrevrange(REDIS_KEY, start, stop - 1)









