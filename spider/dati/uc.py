
import requests
import re
import time
import json
from baiwang import baidu
session = requests.Session()
header = {
    'Referer':'https://qmdt.uc.cn/sm/index?uc_param_str=dsdnfrpfbivesscpgimibtbmnijblauputogpintnwkt&entry=weathertest&uc_biz_str=S%3Acustom%7CC%3Atitlebar_hover_2',
    'User-Agent':'Mozilla/5.0 (Linux; U; Android 7.1.1; zh-CN; MI 6 Build/NMF26X) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/57.0.2987.108 UCBrowser/11.8.3.963 Mobile Safari/537.36',
}
data = ''

def query():
    global data
    try:
        t = round(time.time()*1000)
        # 不完整
        url = 'https://qmdt.uc.cn/sm/queryQuestion?................&__t={time}&currentTime={current_time}'
        response = session.post(url.format(time = t,current_time = round(time.time()*1000), headers = header))
        print(response.text)
        text = json.loads(response.text)
        if text['success'] == True:
            code = text['question']['code']
            question = text['question']['question']
            if question and not data == question:
                data = question
                baidu(data)
                print(code, question)
    except ConnectionError:
        print('error')


def main():
    query()

if __name__ == '__main__':
    while True:
        main()
        time.sleep(1)