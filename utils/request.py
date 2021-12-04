import json

import requests

from utils.utils import Activity, log


def post(post_para: dict, headers: dict) -> requests.Response:
    """对图书馆接口发送post请求

    Args:
        post_para (list(json)): 要发送的json数据
        headers (dict): headers参数
    """

    url = 'https://wechat.v2.traceint.com/index.php/graphql/'
    resp = requests.request("post", url, json=post_para, headers=headers)
    return resp


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


def get_step_response(cookie: str) -> requests.Response:
    """获取getStep的响应

    Args:
        cookie (str): 传入headers的cookie

    Returns:
        requests.Response: 返回响应
    """
    return get_resp(Activity.get_step, cookie)


def get_step(cookie: str) -> int:
    """获取getStep

    Args:
        cookie (str): headers中的cookie

    Returns:
        int: getStep
    """
    resp = get_step_response(cookie)
    return resp.json()['data']['userAuth']['prereserve']['getStep']
