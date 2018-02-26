import requests
import json
import re
from pyquery import PyQuery as PQ
from setting import *
from verify import Yundama
import time
from smsreminder import send_message

session = requests.Session()
ydm = Yundama(YDM_USERNAME, YDM_PASSWORD, YDM_ID, YDM_KEY)

def query():
    print('query')
    header = {
        'Referer': 'http://www.rahos.gov.cn/wsyy/Step1.aspx?type=1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.62 Safari/537.36',
    }
    url = 'http://www.rahos.gov.cn/wsyy/Step2.aspx'
    data = {
        'toclient': '1',
        'hid_ysdm': YSDM,
        'hid_ksdm': KSDM,
        'hid_lch': 'invalid'
    }
    response = session.post(url, headers = header, data = data)
    text = response.text.replace('xmlns','another_attr')
    # print(text)
    doc = PQ(text)
    hid_rq_xq6 = doc('#hid_rq_xq6').attr['value']
    hid_rq_xq7 = doc('#hid_rq_xq7').attr['value']
    datas = doc('#DoctorTable a')
    reg_data = re.compile(r'\(\'(.*?)\'\,\'(.*?)\'\,\'(.*?)\'\,\'(.*?)\'\,\'(.*?)\'')
    for x in datas.items():
        text = x.text()
        href = re.findall(reg_data,str(x))[0]
        dict = {
            'doctor':href[0],
            'week':href[1],
            'time':href[2],
            'date':href[3],
            'code':href[4],
            'number': text,
            'hid_rq_xq6':hid_rq_xq6,
            'hid_rq_xq7':hid_rq_xq7

        }
        current_number = dict['number'].split(r'/')[0]
        max_number = dict['number'].split(r'/')[1]
        if int(current_number) < int(max_number) and dict['date'] == '2018/1/18':
            print(dict)
            return dict

def submitInfo(dict):
    header = {
        'Referer': 'http://www.rahos.gov.cn/wsyy/Step2.aspx',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.62 Safari/537.36',
    }
    url = 'http://www.rahos.gov.cn/wsyy/Step3.aspx'
    data = {
        'hid_ysdm':dict['doctor'],
        'hid_xqj':dict['week'],
        'hid_sxw':dict['time'],
        'hid_rq':dict['date'],
        'hid_jym':dict['code'],
        'hid_rq_xq6': dict['hid_rq_xq6'],
        'hid_rq_xq7': dict['hid_rq_xq7'],
    }
    response = session.post(url, headers = header, data = data)
    text = response.text.replace('xmlns', 'another_attr')
    doc = PQ(text)
    EVENTVALIDATION = doc('#__EVENTVALIDATION').attr['value']
    VIEWSTATE = doc('#__VIEWSTATE').attr['value']
    toclient = doc('#toclient').attr['value']
    hid_zjpb = doc('#hid_zjpb').attr['value']
    hid_zjfy = doc('#hid_zjfy').attr['value']
    dicts = {
        'eventvalidation':EVENTVALIDATION,
        'viewstate':VIEWSTATE,
        'toclient':toclient,
        'hid_zjpb':hid_zjpb,
        'hid_zjfy':hid_zjfy,
    }
    print(dicts)
    return dicts

def get_data(dict, code):
    header = {
        'Referer': 'http://www.rahos.gov.cn/wsyy/Step3.aspx',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.62 Safari/537.36',
    }
    url = 'http://www.rahos.gov.cn/wsyy/Step3.aspx'
    data = {
        '__VIEWSTATE':dict['viewstate'],
        '__EVENTVALIDATION':dict['eventvalidation'],
        'ibrkh':IDCARD,
        'sbtn_read':'读取',
        'idnum':'',
        'idname':NAME,
        'idsex':IDSEX,
        'iddate':'',
        'idphone':'',
        'idadderess':'',
        'txt_yzm':'',
        'toclient':dict['toclient'],
        'toserverjzxh':'',
        'toserverjzsj':'',
        'hid_brid':'',
        'hid_zjpb':dict['hid_zjpb'],
        'hid_zjfy':dict['hid_zjfy'],
    }
    response = session.post(url, headers = header, data = data)
    text = response.text.replace('xmlns', 'another_attr')
    print(data)
    doc = PQ(text)
    idnum = doc('#idnum').attr['value']
    iddate = doc('#iddate').attr['value']
    idphone = doc('#idphone').attr['value']
    idadderess = doc('#idadderess').attr['value']
    # txt_yzm = doc('#txt_yzm').attr['value']
    submit = '提交预约信息'
    hid_brid = doc('#hid_brid').attr['value']
    count = len(dict['toclient']) - len(dict['toclient'].replace('|',''))
    if count == 1:
        reg_count = re.compile(r'(.*?)\|(.*?)#')
        a = re.findall(reg_count, dict['toclient'])[0]
        toserverjzsj = a[1]
        toserverjzxh = a[0]
    else:
        for x in dict['toclient'].split('|'):
            y = x.split('#')
            if len(y) >= 2:
                toserverjzxh = y[1]
                toserverjzsj = y[0]
                break
    datas = {
        '__VIEWSTATE': dict['viewstate'],
        '__EVENTVALIDATION': dict['eventvalidation'],
        'ibrkh': IDCARD,
        'submit':submit,
        'idnum': idnum,
        'idname': NAME,
        'idsex': IDSEX,
        'iddate': iddate,
        'idphone': idphone,
        'idadderess': idadderess,
        'txt_yzm': code,
        'toclient': dict['toclient'],
        'toserverjzxh': toserverjzxh,
        'toserverjzsj': toserverjzsj,
        'hid_brid': hid_brid,
        'hid_zjpb': dict['hid_zjpb'],
        'hid_zjfy': dict['hid_zjfy'],
    }
    urls = 'http://www.rahos.gov.cn/wsyy/Step3.aspx'
    response = session.post(urls, headers = header, data = datas)
    print(datas)


def download_pic(retry = 0):
    url = 'http://www.rahos.gov.cn/wsyy/imageCode.aspx'
    header = {
        'Referer': 'http://www.rahos.gov.cn/wsyy/Step2.aspx',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.62 Safari/537.36',
    }
    response = session.get(url, headers =header)
    res = response.content
    with open('code.png','wb') as fn:
        fn.write(res)
    code = ydm.identify(file = FILE)
    if retry >= 3:
        return None
    elif not code and retry < 3:
        return download_pic(retry + 1)
    else:
        return code

def main(cycle):
    while True:
        dict = query()
        if dict:
            dicts = submitInfo(dict)
            code = download_pic()
            if code:
                get_data(dicts, code)
                send_message('你好')
                break
        time.sleep(cycle)

if __name__ == '__main__':
    main(3)