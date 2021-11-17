import json
import requests
import time
from enum import Enum
import traceback

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

def on_message(ws,meessage):
    log(f'WebSocketApp:\t')

def on_close(ws,a,b):
    log('WebSocketApp:\twss关闭')

def on_error(ws,error):
    log('WebSocketApp:\t出现异常')
    log(error)
    traceback.print_exc()

if __name__=='__main__':
    status=verify_cookie('FROM_TYPE=weixin; v=5.5; Hm_lvt_7ecd21a13263a714793f376c18038a87=1635913724,1636000165,1636122571,1636331028; Authorization=eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJ1c2VySWQiOjIxMDAxOTM2LCJzY2hJZCI6MTI2LCJleHBpcmVBdCI6MTYzNjcwMjUzMX0.xjUtxYhsKj1-41z0I9M0kHmb6XwSF3V0seiZrQtVH9fuSOoA4tAGmcWTziQbokYXn98nf7oDlkYzX9A-muTQ7Pi3Mj0xdw1L-EGETj3uFKm30e3gIAd6Fkq_zL5YfmDY0WeFPbAnfpPSoLHOQkw4pUyZPYNTaB-2Q0DQGdwqeSNn6dN7nIaGLBKETYfZioa86W34X8CgHA8lMX7Z1lLkmKAGK6F9WY6sd0P-80P8wDzABdg88tr2cdK9FGlDCcEgbd7cJPbzIfIsJq1vbvA0a559bq90L1iMg4wuCVyO6ZSvJBUdQCsbR_XYZtBMlFuhvHwcQEkjO-VHCF2cdz9uuA; wechatSESS_ID=583a79f0a5c3db1d9e13ebe6f2ebe4c1243bdfa21a467134; Hm_lpvt_7ecd21a13263a714793f376c18038a87=1636700727; SERVERID=d3936289adfff6c3874a2579058ac651|1636700840|1636698929')
    log(status)