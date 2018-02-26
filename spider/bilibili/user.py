from fake_useragent import UserAgent
import time
import requests
import re
import json
from multiprocessing import Pool,Process
from bloomfilter import BloomFilter
import pymongo
bf = BloomFilter()
# ua = UserAgent()
header = {
    'Referer':'https://www.bilibili.com/',
    'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
}
session = requests.Session()
session.get('https://www.bilibili.com/',headers = header)
conn = pymongo.MongoClient('localhost',27017)
db = conn['bilibili']
coll = db['user']

def cycle(func):
    def wrapper(*args, **kwargs):
        while True:
            func(*args, **kwargs)
    return wrapper

@cycle
def get_followings(mid = None, pn = '1'):
    url = 'https://api.bilibili.com/x/relation/followings?vmid={mid}&pn={pn}&ps=50&order=desc&jsonp=jsonp&callback=__jp35'
    if not mid:
        mid = bf.queue_pop('followings')
    urls = url.format(pn = pn,mid = mid)
    if not bf.isContains(urls):
        bf.insert(urls)
        try:
            response = session.get(urls,headers = header)
            reg_follow = re.compile(r'__jp35\((.*)\)')
            text = re.findall(reg_follow,response.text)[0]
            text = json.loads(text)
            count = 0
            if 'data' in text.keys():
                for data in text['data']['list']:
                    bf.queue_push('user', data['mid'])
                    print(count, data['mid'])
                    count += 1
                for x in range(2,9999):
                    if count == 50:
                        get_followings(mid, str(x))
                    else:
                        return None
        except Exception:
            print('get_followings error')

@cycle
def get_followers(mid = None, pn = '1'):
    url = 'https://api.bilibili.com/x/relation/followers?vmid={mid}&pn={pn}&ps=50&order=desc&jsonp=jsonp&callback=__jp35'
    urls = url.format(pn = pn,mid = mid)
    if not mid:
        mid = bf.queue_pop('followers')
    if not bf.isContains(urls):
        bf.insert(urls)
        try:
            response = session.get(urls,headers = header)
            reg_follow = re.compile(r'__jp35\((.*)\)')
            text = re.findall(reg_follow,response.text)[0]
            text = json.loads(text)
            count = 0
            if 'data' in text.keys():
                for data in text['data']['list']:
                    bf.queue_push('user', data['mid'])
                    print(count, data['mid'],'s')
                    count += 1
                for x in range(2,9999):
                    if count == 50:
                        get_followers(mid, str(x))
                    else:
                        return None
        except Exception:
            print('get_followers error')

@cycle
def get_user():
    url = 'https://api.bilibili.com/cardrich?callback=jQuery17207544474408437294_1514799183798&mid={mid}&type=jsonp'
    mid = bf.queue_pop('user')
    urls = url.format(mid = mid)
    if not bf.isContains(urls):
        bf.insert(urls)
        try:
            response = session.get(urls,headers = header)
            reg_follow = re.compile(r'37294_1514799183798\((.*)\)')
            text = re.findall(reg_follow, response.text)[0]
            text = json.loads(text)
            if 'data' in text.keys():
                text = text['data']['card']
                dict = {
                    'level':text['level_info']['current_level'],
                    'mid':text['mid'],
                    'regtime':text['regtime'],
                    'name':text['name'],
                    'face':text['face'],
                    'attention':text['attention'],
                    'fans':text['fans'],
                    'birthday':text['birthday'],
                    'sex':text['sex'],
                    'sign':text['sign'],
                    'place':text['place'],
                }
                coll.insert(dict)
                if not dict['fans'] == 0:
                    bf.queue_push('followers', mid)
                if not dict['attention'] == 0:
                    bf.queue_push('followings', mid)
        except Exception:
            print('get_user error')

def main():
    bf.queue_push('user', '777536')
    Process(target = get_user).start()
    time.sleep(3)
    Process(target = get_followings).start()
    Process(target = get_followers).start()


if __name__ == '__main__':
    main()
