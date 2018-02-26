from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from pyquery import PyQuery
from selenium.webdriver.chrome.options import Options
import re
import pymongo

chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--load--images=false')
browser = webdriver.Chrome(chrome_options=chrome_options)
wait = WebDriverWait(browser,10)
client = pymongo.MongoClient('localhost',27017,connect = False)
db = client['taobao']

def save_to_mongodb(result):
    table = db['taobaomeishi']
    try:
        if table.insert(result):
            print('save successful',result)
    except Exception:
        print('save failed')
    print(result)
def search():
    print('正在搜索')
    try:
        browser.get('https://www.taobao.com/')
        input_ = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR,'#q'))
        )
        submit = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR,'#J_TSearchForm > div.search-button > button'))
        )
        input_.send_keys('美食')
        submit.click()
        total = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '#mainsrp-pager > div > div > div > div.total'))
        )
        get_product()
        reg = re.compile(r'(\d+)')
        total = int(reg.search(total.text).group(1))
        return total
    except TimeoutException:
        return search()

def next_page(page_number):
    print(page_number)
    try:
        input_ = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '#mainsrp-pager > div > div > div > div.form > input'))
        )
        submit = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, '#mainsrp-pager > div > div > div > div.form > span.btn.J_Submit'))
        )
        input_.clear()
        input_.send_keys(page_number)
        submit.click()
        wait.until(
            EC.text_to_be_present_in_element((By.CSS_SELECTOR, '#mainsrp-pager > div > div > div > ul > li.item.active > span'),str(page_number))
        )
        get_product()
    except TimeoutException:
        next_page(page_number)

def get_product():

    input_ = wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, '#mainsrp-itemlist .items .item'))
    )
    html = browser.page_source.replace('xmlns','another_attr')
    doc = PyQuery(html)
    items = doc('#mainsrp-itemlist .items .item').items()

    for item in items:
        product = {
            'image':'http:'+ item.find('.pic img').attr('data-src'),
            'price':item.find('strong').text(),
            'location':item.find('.location').text(),
            'shop':item.find('.dsrs').next().text(),
            'title':item.find('div.title>a').text(),
            'purchase quantity':item.find('.deal-cnt').text()[:-3]
        }
        save_to_mongodb(product)

def main():
    try:
        total = search()
        for x in range(2,total+1):
            next_page(x)
    except Exception:
        print('出错了')
    finally:
        browser.close()



if __name__=='__main__':
    main()
