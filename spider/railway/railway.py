import requests
import urllib.parse
import json
from verify import Yundama
from setting import *
import re
from citycode import city_contrast
import time

header = {
    # 'Host':'kyfw.12306.cn',
    # 'Referer':'https://kyfw.12306.cn/otn/leftTicket/init',
    'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.62 Safari/537.36',
}
ydm = Yundama(YDM_USERNAME, YDM_PASSWORD, YDM_ID, YDM_KEY)
dict_coordinate = {
   '1':'40,50',
   '2':'110,50',
   '3':'180,50',
   '4':'250,50',
   '5':'40,120',
   '6':'110,120',
   '7':'180,120',
   '8':'250,120'
}

class Railway():

    def __init__(self, username, password, date, from_location, to_location, l_time, u_time):
        self.username = username
        self.password = password
        self.date = date
        self.from_location = from_location
        self.to_location = to_location
        self.l_time = l_time
        self.u_time = u_time
        self.session = requests.session()

    def queryticket(self):
        reg_time = re.compile(r'(\d+)\:')
        queryurl = 'https://kyfw.12306.cn/otn/leftTicket/queryZ?leftTicketDTO.train_date={date}&leftTicketDTO.from_station={from_}&leftTicketDTO.to_station={to_}&purpose_codes=ADULT'
        from_location = city_contrast[self.from_location]
        to_location = city_contrast[self.to_location]
        response_query = requests.get(queryurl.format(date = self.date,from_ = from_location,to_ = to_location),headers = header,verify = False)
        print(response_query.text)
        query_text = json.loads(response_query.text)
        query_result = query_text['data']['result']
        #30 二等 31一等 32 商务 0secretstr 9出发时间
        for x in query_result:
            y = x.split('|')
            # for i in y:
            #     print(i)
            time = int(re.findall(reg_time,y[9])[0])
            if time >= int(self.l_time) and time < int(self.u_time):
                if not y[30] == '无' or y[30] =='':
                    if y[30]=='有' or int(y[30]) >0:
                        print('有票')
                        secretStr = urllib.parse.unquote(y[0])
                        leftticketstr = urllib.parse.unquote(y[12])
                        train_location = y[15]
                        print(secretStr)
                        print(leftticketstr)
                        print(train_location)
                        if secretStr :
                            return [secretStr,leftticketstr,train_location]
        print('没票')

    def downverification(self):
        url = 'https://kyfw.12306.cn/passport/captcha/captcha-image?login_site=E&module=login&rand=sjrand&0.13150775634454748'
        response = self.session.get(url,headers = header,verify = False)
        res = response.content
        with open('code.png','wb') as fn:
            fn.write(res)

    def login(self):
        url = 'https://kyfw.12306.cn/passport/web/login'
        data = {
            'username':self.username,
            'password':self.password,
            'appid':'otn',
            '_json_att':''
        }
        response = self.session.post(url, data = data, headers = header, verify = False)
        text = json.loads(response.text)
        if text['result_code'] == 0:
            print('登录成功')
        else:
            print(text['result_code'])


    def verification(self):
        self.downverification()
        print('请输入验证码')
        code = ydm.identify(file = FILE)
        print(code)
        if code:
            result = []
            for x in range(1,9):
                if str(x) in code:
                    result.append(dict_coordinate[str(x)])
            real_code = ','.join(result)
            print(real_code)

            url = 'https://kyfw.12306.cn/passport/captcha/captcha-check'
            data = {'answer':real_code,
                    'login_site':'E',
                    'rand':'sjrand'}
            response = self.session.post(url, data = data , headers = header, verify = False)
            res2 = json.loads(response.text)
            if res2['result_code'] == '4':
                print('验证码校验成功')
                self.login()
            else:
                self.verification()
        else:
            self.verification()

    def uamtk(self):
        url = 'https://kyfw.12306.cn/passport/web/auth/uamtk'
        data = {
            'appid': 'otn'
        }
        response = self.session.post(url,data = data ,headers = header,verify = False)
        text = json.loads(response.text)
        if text['result_code'] == 0:
            tk = text['newapptk']
            return tk
        else:
            print(text['result_code'])

    def uama(self,tk):
        url = 'https://kyfw.12306.cn/otn/uamauthclient'
        data = {
            'tk':tk,
            '_json_att':''
        }
        response = self.session.post(url, data=data, headers=header, verify=False)
        print(response.text)

    def query(self):
        reg_time = re.compile(r'(\d+)\:')
        queryurl = 'https://kyfw.12306.cn/otn/leftTicket/log?leftTicketDTO.train_date=={date}&leftTicketDTO.from_station={from_}&leftTicketDTO.to_station={to_}&purpose_codes=ADULT'
        from_location = city_contrast[self.from_location]
        to_location = city_contrast[self.to_location]
        response_query = self.session.get(queryurl.format(date = self.date,from_ = from_location,to_ = to_location),headers = header,verify = False)
        print(response_query.text)

    def submitOrderRequest(self,secretstr):
        url = 'https://kyfw.12306.cn/otn/leftTicket/submitOrderRequest'
        data = {
            'secretStr':secretstr,
            'train_date':self.date,
            'back_train_date':'2017 - 12 - 09',
            'tour_flag':'dc',
            'purpose_codes':'ADULT',
            'query_from_station_name':self.from_location,
            'query_to_station_name':self.to_location,
            'undefined':'',
        }
        response = self.session.post(url,data = data ,headers = header, verify = False)
        print(response.text)

    def indc(self):
        reg_repeatsubmittoken = re.compile(r'globalRepeatSubmitToken\s\=\s\'(.*?)\'\;')
        reg_key_check_isChange = re.compile(r'key_check_isChange\'\:\'(.*?)\'\,')
        url = 'https://kyfw.12306.cn/otn/confirmPassenger/initDc'
        data = {
            '_json_att':'',
        }
        response = self.session.post(url,data = data,headers = header ,verify = False)
        repeatsubmittoken = re.findall(reg_repeatsubmittoken,response.text)
        key_check_isChange = re.findall(reg_key_check_isChange,response.text)
        print(repeatsubmittoken,key_check_isChange)
        return [repeatsubmittoken,key_check_isChange]

    def getPassengerDTOs(self,repeatsubmittoken):
        url = 'https://kyfw.12306.cn/otn/confirmPassenger/getPassengerDTOs'
        data = {
            '_json_att': '',
            'REPEAT_SUBMIT_TOKEN':repeatsubmittoken,
        }
        response = self.session.post(url, data=data, headers=header, verify = False)
        print(response.text)

    def check(self,repeatsubmittoken):
        url = 'https://kyfw.12306.cn/otn/confirmPassenger/checkOrderInfo'
        data = {
            'cancel_flag':'2',
            'bed_level_order_num':'000000000000000000000000000000',
            'passengerTicketStr':'O,0,1,'+ str(REAL_NAME) + ',1,'+ str(IDENTITY_CARD) +',,N',
            'oldPassengerStr':str(REAL_NAME) + ',1,'+ str(IDENTITY_CARD) +',1_',
            'tour_flag':'dc',
            'randCode':'',
            '_json_att':'',
            'REPEAT_SUBMIT_TOKEN':repeatsubmittoken,
        }
        response = self.session.post(url, data=data, headers=header, verify=False)
        print(response.text)

    def confirm(self,repeatsubmittoken,leftticketstr,train_location,key_check_isChange):
        url = 'https://kyfw.12306.cn/otn/confirmPassenger/confirmSingleForQueue'
        data = {
            'passengerTicketStr':'O,0,1,'+ str(REAL_NAME) + ',1,'+ str(IDENTITY_CARD) +',,N',
            'oldPassengerStr':str(REAL_NAME) + ',1,'+ str(IDENTITY_CARD) +',1_',
            'randCode':'',
            'purpose_codes':'00',
            'key_check_isChange':key_check_isChange,
            'leftTicketStr':leftticketstr,
            'train_location':train_location,
            'choose_seats':'1F',
            'seatDetailType':'000',
            'roomType':'00',
            'dwAll':'N',
            '_json_att':'',
            'REPEAT_SUBMIT_TOKEN':repeatsubmittoken,
        }
        response = self.session.post(url, data=data, headers=header, verify=False)
        print(response.text)
        data = json.loads(response.text)
        if isinstance(data['data'],type({})) and data['data']['submitStatus'] ==True:
            print('购票成功')
        else:
            print('购票失败')



def main():
    try:
        railway = Railway(USERNAME, PASSWORD, DATE, FROM_LOCATION, TO_LOCATION, L_TIME, U_TIME)
        list_ticket = railway.queryticket()
        if list_ticket:
            secretstr = list_ticket[0]
            leftticketstr = list_ticket[1]
            train_location = list_ticket[2]
            railway.verification()
            tk = railway.uamtk()
            railway.uama(tk)
            railway.query()
            railway.submitOrderRequest(secretstr)
            list_indc = railway.indc()
            repeatsubmittoken = list_indc[0]
            key_check_isChange = list_indc[1]
            railway.getPassengerDTOs(repeatsubmittoken)
            railway.check(repeatsubmittoken)
            railway.confirm(repeatsubmittoken, leftticketstr, train_location, key_check_isChange)
    except Exception:
        print('error')

if __name__ == '__main__':
    while True:
        main()
        time.sleep(5)