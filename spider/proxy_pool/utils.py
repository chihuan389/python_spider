import requests
from requests.exceptions import ConnectionError

base_header = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36',
    'Accept-Encoding': 'gzip, deflate, sdch',
    'Accept-Language': 'zh-CN,zh;q=0.8'
}

def get_page(url,options = {}):
    headers =dict(base_header,**options)
    print('正在抓取',url)
    try:
        response = requests.get(url,headers = headers)
        if response.status_code ==200:
            print('抓取成功',url)
            return response
        else:
            print('抓取失败',url,response.status_code)
            return None
    except ConnectionError:
        print('抓取失败',url)
        return None

def proxy_port(port_code):
    dict_code = {'A': '1', 'B': '2', 'C': '3', 'D': '4', 'E': '5', 'F': '6', 'G': '7', 'H': '8', 'I': '9', 'Z': '0'}
    port_len = len(port_code)
    extra = -int('1' * port_len)
    for k, v in dict_code.items():
        port_code = port_code.replace(k, v)
    number_z = 0
    if '0' in port_code:
        for x in port_code:
            if x == '0':
                number_z += 1
        for i in range(0, number_z):
            index_z = port_code.index('0')
            extra += 10 ** (port_len - index_z)
    port_code = (int(port_code) + extra) / 8
    return str(int(port_code))

