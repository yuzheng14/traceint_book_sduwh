import json
import requests
import time
from enum import Enum

def verify_cookie(cookie):
    '''验证cookie有效性
    参数
    -------------------------------
    cookie:str
        传入cookie

    返回值
    -----------------------
    bool
        true为有效
    '''
    with open('json/book/index_headers.json') as f:
        headers = json.load(f)
    with open('json/book/index_para.json') as f:
        para = json.load(f)
    headers['Cookie'] = cookie
    resp = post(para, headers).json()
    return 'errors' not in resp

# TODO doc注释
def post(post_para, headers):

    url = 'https://wechat.v2.traceint.com/index.php/graphql/'
    resp = requests.request("post", url, json=post_para, headers=headers)
    return resp

# TODO doc注释
def wait_time(hour,minute):
    time_to_wait=hour*60+minute
    while time.localtime().tm_hour*60+time.localtime().tm_min < time_to_wait:
        pass

# TODO doc注释
def take_seat_name(elem):
    name = elem['name']
    if name != "" and name is not None:
        return int(elem['name'])
    return 5000

# TODO doc注释
def log(message):
    # with open('log.out','a',encoding='utf-8') as f:
        # f.write(time.strftime("[%Y-%m-%d %H:%M:%S] ", time.localtime())+'\t'+f'{message}'+'\n')
    print((time.strftime("[%Y-%m-%d %H:%M:%S] ", time.localtime())+'\t'+f'{message}'))

# TODO doc注释
# TODO 完善函数
def renew_cookie(cookie:dict) -> dict:
    if verify_cookie(cookie):
        log('当前验证码有效，无需更新')
        return cookie
    pass
    return cookie

# TODO doc注释
# TODO 完善函数
def have_seat() ->bool:
    pass

# TODO doc注释
class Activity(Enum):
    captcha={"operationName": "getStep0","query": "query getStep0 {\n userAuth {\n prereserve {\n getNum\n captcha {\n code\n data\n }\n }\n }\n}"}
    prereserve_10_seats={}
    get_end_time={}
    prereserve={}
    verify_captcha={}
    reserve_10_seats={}
    reserve_all_floors={}
    reserve={}
    index={}
    withdraw={}

# TODO doc注释
# TODO 完善函数
def get_para_and_headers(activity:Activity) -> tuple:
    return ()

# TODO doc注释
def get_resp(activity:Activity) -> requests.Response:
    para,headers=get_para_and_headers(activity)
    return post(para,headers)