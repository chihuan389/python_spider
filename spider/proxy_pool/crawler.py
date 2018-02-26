import json
import requests
import re
from pyquery import PyQuery as pq
from utils import get_page,proxy_port

class ProxyMetaclass(type):
    def __new__(cls,name,bases,attrs):
        count = 0
        attrs['__CrawlFunc__'] = []
        for k,v in attrs.items():
            if 'crawl_' in k:
                attrs['__CrawlFunc__'].append(k)
                count += 1
        attrs['__CrawlFuncCount__'] = count
        return type.__new__(cls,name,bases,attrs)

class Crawler(object,metaclass=ProxyMetaclass):
    def get_proxies(self,callback):
        proxies = []
        for proxy in eval("self.{}()".format(callback)):
            print('成功获取代理',proxy)
            proxies.append(proxy)
        return proxies

    # def crawl_daxiang(self):
    #     url = 'http://vtp.daxiangdaili.com/ip/?tid=559363191592228&num=50&filter=on'
    #     html = get_page(url)
    #     if html:
    #         proxies = html.text.split('\n')
    #         for proxy in proxies:
    #             yield proxy

    def crawl_daili66(self,page_count=2):
        strat_url = 'http://www.66ip.cn/{page}.html'
        urls = [strat_url.format(page = page ) for page in range(1,page_count+1)]
        for url in urls:
            html = get_page(url)
            if html:
                doc = pq(html.content.decode('gb2312').replace('xmlns','other attr'))
                ip = doc('div.containerbox td:nth-child(1)').items()
                port =doc('td:nth-child(2)')
                count = 0
                for x in ip:
                    if count>=1:
                        proxy = ':'.join([x.text(),port.eq(count).text()])
                        yield proxy
                    count += 1

    def crawl_goubanjia(self):
        start_url = 'http://www.goubanjia.com/free/gngn/index{page}.shtml'
        for page in range(1,11):
            html = get_page(start_url.format(page = page))
            if html:
                doc = pq(html.text)
                tds  = doc('td.ip').items()
                for td in tds:
                    td.find('p').remove()
                    port_code = td.find('.port').attr['class'].replace('port ','')
                    port = proxy_port(port_code)
                    td.find('.port').remove()
                    ip = td.text().replace(' ','')
                    proxy = ip + port
                    yield proxy

    # def crawl_ip181(self):
    #     start_url = 'http://www.ip181.com/'
    #     html = get_page(start_url)
    #     if html:
    #         doc = pq(html.text)
    #         ip = doc('table.ctable td:nth-child(1)').items()
    #         port = doc('table.ctable td:nth-child(2)')
    #         count = 0
    #         for x in ip:
    #             if count >= 1:
    #                 proxy = ':'.join([x.text(), port.eq(count).text()])
    #                 yield proxy
    #             count += 1

    def crawl_ip3366(self):
        first_url = 'http://www.ip3366.net/free/?stype={num}&page=1'
        for num in range(1,3):
            html = get_page(first_url.format(num = num))
            if html:
                reg_last = re.compile(r'<a.*?page\=(\d+)\">尾页</a>')
                last = re.findall(reg_last, html.content.decode('gb2312'))[0]
                page_count = int(last)
                start_url = 'http://www.ip3366.net/free/?stype={num}&page={page}'
                for page in range(1,page_count + 1):
                    html = get_page(start_url.format(page = page,num = num))
                    if html:
                        doc = pq(html.text)
                        ip = doc('#list td:nth-child(1)').items()
                        port = doc('#list td:nth-child(2)')
                        count = 0
                        for x in ip:
                            if count >= 1:
                                proxy = ':'.join([x.text(), port.eq(count).text()])
                                yield proxy
                            count += 1

    def crawl_data5u(self):
        for i in ['gngn','gnpt']:
            start_url = 'http://www.data5u.com/free/{i}/index.shtml'.format(i = i)
            html = get_page(start_url,{'Host':'www.data5u.com',
            'Referer':'http://www.data5u.com/free/index.shtml'})
            if html:
                doc = pq(html.text)

                ip = doc(' ul > li:nth-child(2) span:nth-child(1) > li')
                port = doc(' ul > li:nth-child(2) span:nth-child(2) > li').items()
                count = 0
                for x in port:
                    if count >= 1:
                        port_code = x.attr['class'].replace('port ','')
                        porxy = ':'.join([ip.eq(count).text(),proxy_port(port_code)])
                        yield porxy
                    count += 1


    def crawl_kxdailli(self):
        first_url = 'http://www.kxdaili.com/ipList/1.html#ip'
        html = get_page(first_url)
        if html:
            reg_last = re.compile(r'ipList',re.S)
            last = re.findall(reg_last, html.text)
            page_count = len(last) + 1
            start_url = 'http://www.kxdaili.com/ipList/{page}.html#ip'
            for page in range(1, page_count + 1):
                html = get_page(start_url.format(page=page))
                if html:
                    doc = pq(html.text)
                    ip = doc('tbody >tr >td:nth-child(1)').items()
                    port = doc('tbody >tr td:nth-child(2)')
                    count = 0
                    for x in ip:
                            proxy = ':'.join([x.text(), port.eq(count).text()])
                            yield proxy
                            count += 1

    def crawl_xicidaili(self):
        start_url = 'http://www.xicidaili.com/{}/'
        for x in ['nn','nt']:
            html = get_page(start_url.format(x))
            if html:
                doc = pq(html.text)
                ip = doc('td:nth-child(2)').items()
                port = doc('td:nth-child(3)')
                count = 0
                for x in ip:
                    proxy = ':'.join([x.text(),port.eq(count).text()])
                    yield proxy
                    count += 1

    # def crawl_xdaili(self):
    #     start_url = 'http://www.xdaili.cn/freeproxy'
    #     html = get_page(start_url)
    #     if html:
    #         doc = pq(html.text)
    #         trs = doc('tr')
    #         print(trs)
    #         for tr in trs.items():
    #             ip = tr.find('td.el-table_1_column_1.is-center').text()
    #             port = tr.find('td.el-table_1_column_2.is-center').text()
    #             print( ':'.join([ip,port]))

    def crawl_xdaili(self):
        start_url = 'http://www.xdaili.cn/ipagent//freeip/getFreeIps?page=1&rows=10'
        html = get_page(start_url)
        if html:
            text = json.loads(html.text)
            for x in text['RESULT']['rows']:
                ip = x['ip']
                port = x['port']
                yield ':'.join([ip,port])




# a = Crawler()
# print(a.crawl_xdaili())
# for x in a.crawl_xdaili():
#     print(x)





























