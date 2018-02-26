from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
import requests
import re
import time

header = {
    'User-Agent':'Dalvik/2.1.0 (Linux; U; Android 7.1.1; MI 6 MIUI/V9.0.6.0.NCACNEI) VideoArticle/6.3.1 okhttp/3.7.0.6',
    'zpw':'62353214550',
    'accept-encoding':'gzip',
}

session = requests.Session()
datas = ''
chrome_options = Options()
chrome_options.add_argument('--load--images=false')
browser = webdriver.Chrome(chrome_options = chrome_options)
browser.get('https://www.baidu.com/s?&wd=123')
wait = WebDriverWait(browser, 10)
def query():
    global datas
    try:
        # 不完整
        url = 'https://api-spe-ttl.ixigua.com/cdn/h/1/heartbeat/..........&_rticket={time}'
        times = round(time.time() * 1000)
        response = session.get(url.format(time = times), headers = header)
        response.encoding = 'utf-8'
        text = response.text
        reg_data = re.compile(r'\*(.*?)\？', re.S)
        data = re.findall(reg_data,text)
        if data and not data == datas:
            question = data[0][1:]
            baidu(question)
            datas = data
            print(question)
    except ConnectionError:
        print('error')

def baidu(question):
    try:
        input_ = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '#kw'))
        )
        submit = wait.until(
            EC.element_to_be_clickable(((By.CSS_SELECTOR, '#su')))
        )
        input_.clear()
        input_.send_keys(question)
        submit.click()
        time.sleep(10)
    except TimeoutException:
        print('ka')

def main():
    query()


if __name__ == '__main__':
    while True:
        main()
        time.sleep(1)
