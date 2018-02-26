from userlogin import userlogin,save_file
from pyquery import PyQuery as pq
from multiprocessing import Pool
import re
import requests
from setting import *

def parse_index(pagenumber, session):
    url_index = 'http://www.xunyingwang.com/movie/?page={page}'
    doc = pq(url_index.format(page = pagenumber))
    href = doc('.movie-item-in> a')
    for x in href.items():
        url_page = 'http://www.xunyingwang.com/videos/resList/{token}'
        reg_token = re.compile(r'(\d+)',re.S)
        token = re.findall(reg_token, x.attr['href'])[0]
        pasre_page(url_page.format(token = token), session)

def pasre_page(html,session):
    response = requests.get(html)
    reg_pan_surl = re.compile(r'\<a\smid.*?target\=\"_blank\"\shref=\"https://pan.baidu.com/s/(.*?)\"\>')
    reg_code = re.compile(r'密码：(.*?)\"\sis')
    if re.findall(reg_pan_surl, response.text):
        url_pan = re.findall(reg_pan_surl, response.text)[0]
        code = re.findall(reg_code, response.text)[0]
        print(url_pan, code)
        save_file(url_pan, code, session)

def main():
    pool = Pool(2)
    sessions = userlogin(USERNAME, PASSWORD)
    for x in range(1,10):
        pool.apply_async(parse_index, (x, sessions))
    pool.close()
    pool.join()

if __name__ =='__main__':
    main()