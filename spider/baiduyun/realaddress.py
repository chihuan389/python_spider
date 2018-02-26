import requests
import json
import re
import time
import execjs
import urllib.parse
from setting import *

header = {
    'Referer':'https://baidu.com',
    'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.62 Safari/537.36',
}
session = requests.Session()
phantom = execjs.get('PhantomJS')

with open('E:/spider/baiduyun/baiduyunpara.js','r',encoding='utf-8') as f:
    para = f.read()
    js_content = phantom.compile(para)

def cookies_string_to_dict(cookies):
    cookies_dict = {}
    for x in cookies.split(';'):
        y = x.split('=')
        if len(y) >= 2:
            cookies_dict[y[0].strip()] = y[1]
    return cookies_dict

def get_para(token):
    url = 'https://pan.baidu.com/s/{}'
    response = session.get(url.format(token), headers = header )
    return response.text

def parse_para(html):
    reg_yundata = re.compile(r'yunData\.setData\((.*?)\)\;')
    para = re.findall(reg_yundata,html)[0]
    para = json.loads(para)
    dict_para = {
        'uk' : para['uk'],
        'shareid' : para['shareid'],
        'sign' : para['sign'],
        'timestamp' : para['timestamp'],
        'fid_list' : [para['file_list']['list'][0]['fs_id']],
        }
    return dict_para

def get_address(para, bdclnd = ''):
    url = 'https://pan.baidu.com/api/sharedownload?sign={sign}&timestamp={timestamp}&bdstoken=null&channel=chunlei&clienttype=0&web=1&app_id=250528&logid={logid}'
    data = {
        'encrypt':'0',
        'product':'share',
        'uk':para['uk'],
        'primaryid':para['shareid'],
        'fid_list':str(para['fid_list']),
        'path_list':'',
        'type': 'batch',

    }
    if bdclnd:
        data['extra'] = str({'sekey':bdclnd}).replace(' ','')
        data['extra'] = urllib.parse.quote(str({'sekey':bdclnd})).replace('%27','%22').replace('/','%2F')
        data['extra'] = urllib.parse.unquote(data['extra'])
    print(data)
    print(para)
    baiduid = session.cookies['BAIDUID']
    logid = js_content.call('w',baiduid)
    response = session.post(url.format(sign = para['sign'],timestamp = para['timestamp'],logid = logid),headers = header,data = data)
    print(response.text)
    text = json.loads(response.text)
    print(text['dlink'])

def get_list(para, path):
    baiduid = session.cookies['BAIDUID']
    logid = js_content.call('w', baiduid)
    url ='https://pan.baidu.com/share/list?uk={uk}&shareid={shareid}&order=other&desc=1&showempty=0&web=1&page=1&num=100&dir={file}&t=0.1694852200076411&bdstoken=null&channel=chunlei&clienttype=0&web=1&app_id=250528&logid={logid}'
    response = session.get(url.format(logid = logid, uk = para ['uk'], shareid = para['shareid'], file = path), headers = header )
    print(response.text)
    text = json.loads(response.text)
    fid_list = []
    for x in text['list']:
        if x['isdir'] == 0:
            fid_list.append(x['fs_id'])
        if x['isdir'] == 1:
            path = x['path'].replace('/','%2F')
            print(path)
            c = get_list(para,path)
            if 'fid_list' in c:
                for y in c['fid_list']:
                    fid_list.append(y)
    para['fid_list'] = fid_list
    if fid_list:
        return para
    else:
        return None

def verify(token, code):
    url = 'https://pan.baidu.com/share/verify?surl={surl}&t={t}&bdstoken=null&channel=chunlei&clienttype=0&web=1&app_id=250528&logid={logid}'
    baiduid = session.cookies['BAIDUID']
    logid = js_content.call('w', baiduid)
    data = {
        'pwd':code,
        'vcode':'',
        'vcode_str':'',
    }
    response = session.post(url.format(surl = token[1:], t = round(time.time()*1000), logid = logid), headers = header, data = data)
    text = json.loads(response.text)
    if text['errno'] == 0:
        print('verify successful')
        bdclnd = session.cookies['BDCLND']
        return urllib.parse.unquote(bdclnd)
    else:
        print('verify failed,',text)

def main(token, code):
    session.get('https://baidu.com/', headers = header)
    if code:
        bdclnd = verify(token, code)
        html = get_para(token)
        para = parse_para(html)
        get_address(para,bdclnd)
    else:
        html = get_para(token)
        para = parse_para(html)
        get_address(para)

if __name__ == '__main__':
    # main('1qZErmBM','2ehd')
    main(ADDRESS, CODE)




