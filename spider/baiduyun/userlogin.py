import requests
import time
import re
import execjs
import rsa
import base64
import urllib.parse
from setting import *

now_time = round(time.time()*1000)
phantom = execjs.get('PhantomJS')
headers = {
        'Referer': 'https://baidu.com/',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.62 Safari/537.36',
    }

with open('baiduyunpara.js', 'r', encoding='utf-8') as f:
    para = f.read()
    js_content = phantom.compile(para)

def encript_password(password, pubkey):
    pub = rsa.PublicKey.load_pkcs1_openssl_pem(pubkey.encode('utf-8'))
    encript_passwd = rsa.encrypt(password.encode('utf-8'), pub)
    encript_passwd = base64.b64encode(encript_passwd).decode('utf-8')
    return encript_passwd

def data_str_to_dict(data_text):
    data = {}
    for data_unit_text in data_text.split('\n'):
        data_unit = data_unit_text.split(':',1)
        if len(data_unit) >= 2:
            data[data_unit[0].lstrip()] = data_unit[1]
    return data

def userlogin(username, password):
    session = requests.Session()
    session.get('https://baidu.com/', headers = headers)

    url_token = 'https://passport.baidu.com/v2/api/?getapi&tpl=netdisk&subpro=netdisk_web&apiver=v3&tt={tt}&class=login&gid={gid}&logintype=basicLogin&traceid=&callback={callback}'
    gid = js_content.call('guirandom')
    response_token = session.get(url_token.format(tt = now_time,gid = gid,callback = js_content.call('callback','bd__pcbs__')))
    reg_token = re.compile(r'token\".*?\"(.*?)\",',re.S)
    token = re.findall(reg_token,response_token.text)[0]

    url_pubkey = 'https://passport.baidu.com/v2/getpublickey?token={token}&tpl=netdisk&subpro=netdisk_web&apiver=v3&tt={tt}&gid={gid}&traceid=&callback={callback}'
    response_pubkey = session.get(url_pubkey.format(tt = now_time,gid = gid,token = token,callback = js_content.call('callback','bd__pcbs__')))
    reg_key = re.compile(r'pubkey\":\'(.*?)\',.*?key\":\'(.*?)\',')
    rsakey = re.findall(reg_key,response_pubkey.text)[0][1]
    pubkey = re.findall(reg_key,response_pubkey.text)[0][0]
    pubkey = pubkey.replace('\\n', '\n').replace('\\', '')

    log_url = 'https://passport.baidu.com/v2/api/?login'
    data = '''
    staticpage:https://pan.baidu.com/res/static/thirdparty/pass_v3_jump.html
    charset:utf-8
    token:4592fbb1c3d47f528ca2d564d874e2f2
    tpl:netdisk
    subpro:netdisk_web
    apiver:v3
    tt:1511839453733
    codestring:
    safeflg:0
    u:https://pan.baidu.com/disk/home
    isPhone:
    detect:1
    gid:53C5ABA-9DC3-4CCD-BC52-E451608C54BF
    quick_user:0
    logintype:basicLogin
    logLoginType:pc_loginBasic
    idc:
    loginmerge:true
    foreignusername:
    username:13867790217
    password:XvXfiC4OMA4IfoSNv5ByMsBS319xynIkvrXZpR/uAfjxdV6BoQkz4hlfzVgko5J4NewtyRKZ+9326UZu5ScAyo5k+TWk2IOkQ+Lle+N4sYG+iFTCV7q83JAotTLht3zPV60l7geq3geBf6m853OyxsPjVik6LV6EXFhCuueZ++k=
    mem_pass:on
    rsakey:VwRHYi6BKP681jRlfdGHdLXrrDY4aUWy
    crypttype:12
    ppui_logintime:14672
    countrycode:
    fp_uid:e465da9b2a3a64b3bc62503287548e75
    fp_info:e465da9b2a3a64b3bc62503287548e75002~~~e~eeaDoymizd2eo_meeusoC284U2YTV2rTjooC28T~7YTV2rTjYecTqAecTqIeebNeePwo0SeOvjk1Ylj7nEj2e3j1nOl78ZcOvVe742e78b-1ebl28alQ4ye18ux78be2r4lQzOU1nE-18a-78zcOijkt6XGOi3_FmebBmebTmebMmeqto0Yc3vRU0vXLDvmaDi1~DFmd0atgO6~h0sVXD6XLDvmemiz4tJtWD6mGKF1zDI1zOitgOIqGuJzLuF1fDitoma~2uJm4KFSg06z4tFRnDilxtFlx9LhitJ5eKFRd7nad1syy9naj2n4WJo0grtvm6uJmG0YlnDi~B0FlWuiXxKFRdO-lz1eOU1rT~1ehh2r3i1n4e2i2-7v2y7vol1r3~uitL283j28uj16t6u8bVtrh42iEl7ra~1i2UtF2x1nZ4u63yQnbyt6th7vZzueq616a-1r4yt6EluFuV28Xn1FZz1nq61ra~7r2e2e4U2ntntnXz280h1n3i7F2jueZ6u8u-un0ctvm6uJmG0YlnDi~B0FlWuiXxKFRdO-lz7v3y1v2i2FEl2iZh1F5z2nTx2et61i3j1v2y7vEy1e5htrtn78zn78uiu80htnzn2e0z7r1n781z7rq41nuUKmeqPmequmeqCmeqUeeoHoyP6TBExy_yoC0FlfD6R-DT__emeqOeebSmebEmebLmebGmebQmebhoY98ad1roV1rEy7roe7rOx1eox1E__
    dv:tk0.024715220108681991517546869090@zzt0cC8lnd4mjJsJftJXo8LxZsJxhE8oZEH0olHwRgHasd4lqT4vXd41XyEkUxAkqdI2oCFxrhvIZEJo8sLlFELwhVHw8wGwrXAk4b41HjAknf8tb~8DbbAoFhvXRDsJxELxhvJoSyLxZb7L8lR~ZTMmbl41qw4QbTCvFS8lUd4mjJsJftJXo8LxZsJxhE8oZEH0olHwRgHasd4lnT4kqd41XyEkXwAkqdI2oCFxrhvIZEJo8sLlFELwhVHw8wGwrXAk4l4k2~Aknf8tb_rt0EC8kqbAk4~8Qbj8vJb4TjiK9VyG9bd41XyEks~4Qbl81Jd4v7-4l7dGL3YR0xdAknf8tb-41Hd41H~Aknl8vqyAoFhvXRDsJxELxhvJoSyLxZiM9xQMLrs7L8lIwrVHth3HQbTCvFSCkJyAkn~8mbTCk2-8Tbd41XyEkUT4TblCknd4lHj4k4dI2oCFxrhvIZEJo8sLlFELw8x7axORoRT7LhbMLnd41XyEq__CppMyp-xxWH6h-ti4DbTAk7T~tlR0dbA1qT8kHj8vnT4k2bCk7-4vXf4vJj8lJy81U~Cvqf4q__itn6tFyHt4eATZb79-c7aoOMtJc7~ZiATjxGaF3Ma3cM9s_Btc8Tbi4lUd4vqy8Tbw4vUd4vXT4mbj4kUbAk2-8kUdCvJ-Ak2b8lH_Ft0dp4mbj4QblCmbw4mbwCmbf8Dbj4kJd4v4-Ak2xCmbj81qd4v7yAk2~8Dbj81Xd4vHTAk2w8Qbj8lXd4vUTAknj8mbT8l4d41H-Aknf8q__
    traceid:5C166601
    callback:parent.bd__pcbs__xr5hkj
    '''
    data = data_str_to_dict(data)
    dict_change = {
        'traceid':js_content.call('traceid'),
        'gid':gid,
        'callback':'parent.' + js_content.call('callback','bd__pcbs__'),
        'username':username,
        'password':encript_password(password,pubkey),
        'tt':now_time,
        'rsakey':rsakey,
        'token':token,
        'dv':js_content.call('ddvv'),
    }
    data = dict(data, **dict_change)
    response_log = session.post(log_url, data = data)
    reg_errno = re.compile(r'\"err\_no\=(\d+)\&')
    errno = re.findall(reg_errno,response_log.text)[0]
    if errno == '0':
        print('log successful')
    else:
        print('log failed')
    return session

def save_file(pan_url_surl, code, session):
    url_init = 'https://pan.baidu.com/share/init?surl={surl}'
    response_init = session.get(url_init.format(surl = pan_url_surl[1:]), headers = headers)
    reg_bdstoken = re.compile(r'bdstoken\"\:\"(.*?)\"\,', re.S)
    exist = re.findall(reg_bdstoken, response_init.text)
    if exist:
        bdstoken = exist[0]
        baiduid = session.cookies['BAIDUID']
        url = 'https://pan.baidu.com/share/verify?surl={surl}&t={t}&bdstoken={bdstoken}&channel=chunlei&clienttype=0&web=1&app_id=250528&logid={logid}'
        data = {
            'pwd': code,
            'vcode':'',
            'vcode_str':''
        }
        response_verify = session.post(url.format(surl = pan_url_surl[1:],bdstoken = bdstoken,t=now_time, logid = js_content.call('w',baiduid)),data = data,headers = headers)
        reg_verify = re.compile(r'errno\"\:(\d+)\,')
        verify_errno = re.findall(reg_verify,response_verify.text)[0]
        if verify_errno == '0':
            print('verify successful')
        else:
            print('verify failed')

        url_from = 'https://pan.baidu.com/s/{surl}'
        response_from = session.get(url_from.format(surl = pan_url_surl),headers = headers)
        reg_shareid = re.compile(r'shareid\"\:(.*?)\,',re.S)
        shareid = re.findall(reg_shareid,response_from.text)[0]
        reg_uk = re.compile(r'SHARE_UK\s\=\s\"(.*?)\"\;', re.S)
        uk = re.findall(reg_uk, response_from.text)[0]
        reg_path = re.compile(r'yunData.PATH\s\=\s\"(.*?)\"', re.S)
        filelist = re.findall(reg_path, response_from.content.decode(('utf-8')))[0]
        filelist = [filelist.replace('\\', '').replace('\'','\"')]

        data_transfer = {
            'filelist':urllib.parse.unquote(urllib.parse.quote(str(filelist)).replace('/','%2F').replace('%27','%22')),
            'path':urllib.parse.unquote('%2Ftest')}
        url_transfer = 'https://pan.baidu.com/share/transfer?shareid={shareid}&from={uk}&ondup=newcopy&async=1&bdstoken={bdstoken}&channel=chunlei&clienttype=0&web=1&app_id=250528&logid={logid}'
        response_transfer = session.post(url_transfer.format(shareid = shareid, uk = uk , bdstoken = bdstoken, logid = js_content.call('w',baiduid)), headers = headers, data =data_transfer)
        transfer_errno = re.findall(verify_errno, response_transfer.text)[0]
        if transfer_errno == '0':
            print('transfer successful')
        else:
            print('transfer failed')

def main():
    sessions = userlogin(USERNAME, PASSWORD)
    # save_file('1gftNtwn', 'zybg', sessions)

if __name__ == '__main__':
    main()