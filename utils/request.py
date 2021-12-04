import json
from enum import Enum

import requests

from utils.utils import log


# TODO doc注释
class Activity(Enum):
    headers = {
        "Host": "wechat.v2.traceint.com",
        "Connection": "keep-alive",
        "Content-Length": "729",
        "Origin": "https://web.traceint.com",
        "User-Agent":
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36 NetType/WIFI MicroMessenger/7.0.20.1781(0x6700143B) WindowsWechat(0x63040026)",
        "Content-Type": "application/json",
        "Accept": "*/*",
        "Cookie": "",
        "Sec-Fetch-Site": "same-site",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Dest": "empty",
        "Referer": "https://web.traceint.com/web/index.html",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7"
    }
    captcha = {
        "operationName":
        "getStep0",
        "query":
        "query getStep0 {\n userAuth {\n prereserve {\n getNum\n captcha {\n code\n data\n }\n }\n }\n}"
    }
    getStep = {
        "operationName":
        "getStep",
        "query":
        "query getStep {\n userAuth {\n prereserve {\n getStep\n queeUrl\n successUrl\n endTime\n }\n }\n}"
    }
    prereserveLibLayout = {
        "operationName": "libLayout",
        "query":
        "query libLayout($libId: Int!) {\n userAuth {\n prereserve {\n libLayout(libId: $libId) {\n max_x\n max_y\n seats_booking\n seats_total\n seats_used\n seats {\n key\n name\n seat_status\n status\n type\n x\n y\n }\n }\n }\n }\n}",
        "variables": {
            "libId": None
        }
    }


def post(post_para: dict, headers: dict) -> requests.Response:
    """对图书馆接口发送post请求

    Args:
        post_para (list(json)): 要发送的json数据
        headers (dict): headers参数
    """

    url = 'https://wechat.v2.traceint.com/index.php/graphql/'
    resp = requests.request("post", url, json=post_para, headers=headers)
    return resp


def get_para_and_headers(activity: Activity, cookie: str) -> tuple:
    """获取该项活动的json参数和headers

    Args:
        activity (Activity): 活动enum
        cookie (str): 传入cookie

    Returns:
        tuple: 返回json参数和headers组成的元组
    """

    headers = Activity.headers.value
    headers['Cookie'] = cookie

    return (activity.value, headers)


def get_step_response(cookie: str) -> requests.Response:
    """获取getStep的响应

    Args:
        cookie (str): 传入headers的cookie

    Returns:
        requests.Response: 返回响应
    """
    return get_resp(Activity.getStep, cookie)


def get_step(cookie: str) -> int:
    """获取getStep

    Args:
        cookie (str): headers中的cookie

    Returns:
        int: getStep
    """
    resp = get_step_response(cookie)
    return resp.json()['data']['userAuth']['prereserve']['getStep']


def get_prereseve_libLayout(cookie: str, lib_id: int) -> dict:
    """通过libId获取该层图书馆的座位信息

    Args:
        cookie (str): headers中的cookie
        lib_id (int): 图书馆楼层id

    Returns:
        dict: 楼层信息json
    """
    para, headers = get_para_and_headers(Activity.prereserveLibLayout, cookie)
    para['variables']['libId'] = lib_id
    return post(para, headers).json()


def get_resp(activity: Activity, cookie: str) -> requests.Response:
    """通过传入的活动获取response

    Args:
        activity (Activity): 活动enum
        cookie (str): 传入cookie

    Returns:
        requests.Response: 返回的response
    """
    para, headers = get_para_and_headers(activity, cookie)
    return post(para, headers)


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


def get_SToken(cookie: str) -> str:
    """获取退座所需要的SToken
    参数
    ---------------------
    cookie:str
        传入cookie
    返回值
    ---------------------
    str
        退座所需要的SToken
    """
    with open('json/book/index_headers.json') as f:
        headers = json.load(f)
    with open('json/book/index_para.json') as f:
        para = json.load(f)
    headers['Cookie'] = cookie
    resp = post(para, headers).json()
    return resp['data']['userAuth']['reserve']['getSToken']


# TODO doc注释
# TODO 完善函数
# TODO 未拆封微信浏览器之前无法完善
def renew_cookie(cookie: dict) -> dict:
    if verify_cookie(cookie):
        log('当前验证码有效，无需更新')
        return cookie
    pass
    return cookie


# TODO doc注释
# TODO 完善函数
def have_seat() -> bool:
    pass
