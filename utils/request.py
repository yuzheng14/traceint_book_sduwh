import json

import requests

from utils.utils import log, log_info
from utils.request_utils.request import post, Activity, get_para_and_headers, get_resp, get_step_response, get_step


def need_captcha(cookie: str) -> bool:
    """判断当前是否需要验证验证码

    Args:
        cookie (str): headers中的cookie

    Returns:
        bool: true为需要
    """
    return get_step(cookie) == 0


# TODO test
def get_prereserve_libLayout(cookie: str, lib_id: int) -> dict:
    """通过libId获取该层图书馆的座位信息

    Args:
        cookie (str): headers中的cookie
        lib_id (int): 图书馆楼层id

    Raises:
        e: 响应无json

    Returns:
        dict: 楼层信息json
    """
    para, headers = get_para_and_headers(Activity.prereserveLibLayout, cookie)
    para['variables']['libId'] = lib_id

    resp = post(para, headers)
    try:
        result = resp.json()
    except Exception as e:
        log_info("预约座位信息楼层响应无json")
        log_info(resp.content)
        raise e
    return result


# TODO try-except
# TODO doc-string
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
    resp = get_resp(Activity.index, cookie)
    try:
        resp = resp.json()
    except Exception as e:
        log_info(resp.content)
        raise e
    return 'errors' not in resp


# TODO restructure
# TODO doc-string
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


# TODO doc-string
def get_ws_url(cookie: str) -> str:
    """获取websocket链接地址（通常在程序崩溃时重新运行时获取）

    Args:
        cookie (str): headers中的cookie参数

    Returns:
        str: websocket地址
    """
    resp = get_step_response(cookie)
    try:
        resp = resp.json()
        result = resp['data']['userAuth']['prereserve']['queeUrl']
    except TypeError as e:
        log_info("获取ws地址json中无所需数据")
        log_info(_json=resp)
        raise e
    except Exception as e:
        log_info("获取ws地址响应无json")
        log_info(resp.content)
        raise e
    return result


def get_queue_url(cookie: str) -> str:
    """获取排队的get连接

    Args:
        cookie (str): cookie

    Raises:
        e: json中无所需数据
        e: 无json

    Returns:
        str: 排队的get连接
    """
    resp = get_step_response(cookie)
    try:
        resp = resp.json()
        result = resp['data']['userAuth']['prereserve']['successUrl']
    except TypeError as e:
        log_info("获取排队地址json中无所需数据")
        log_info(_json=resp)
        raise e
    except Exception as e:
        log_info("获取排队地址响应无json")
        log_info(resp.content)
        raise e
    return result


# TODO doc-string
# TODO try-except
def get_captcha_code_website(cookie: str) -> tuple:
    """获取验证码的code和网址

    Args:
        cookie (str): headers的cookie

    Returns:
        tuple: 返回元组，第一个元素为code(后面发送验证请求会用到)，第二个元素为网址
    """
    resp = get_resp(Activity.captcha, cookie)

    try:
        resp = resp.json()
        result = ((resp['data']['userAuth']['prereserve']['captcha']['code'], resp['data']['userAuth']['prereserve']['captcha']['data']))
    except TypeError as e:
        log_info("json中无code及网址")
        log_info(_json=resp)
        raise e
    except Exception as e:
        log_info("当前响应无json")
        log_info(resp.content)
        raise e

    return result


# TODO doc-string
# TODO Exception
def get_captcha_image(website: str) -> bytes:
    """根据网址获取验证码图片二进制信息

    Args:
        website (str): 验证码网址

    Returns:
        bytes: 图片二进制信息
    """
    resp = requests.get(website)
    if resp.status_code != 404:
        return resp.content
    else:
        log_info('图片地址404')
        raise Exception("404 Not Found")


# TODO try-exception
# TODO docstring
def verify_captcha(cookie: str, captcha: str, code: str) -> tuple:
    """验证验证码是否正确，返回结果以及websocket的url

    Args:
        cookie (str): 如变量名
        captcha (str): 识别出来的验证码
        code (str): 验证码的code（前面post请求得到的）

    Raises:
        e: 若无法找到json或者json解析出错则抛出异常

    Returns:
        tuple: 第一个元素为bool型，验证是否成功；第二个元素为str，websocket的url
    """
    para, headers = get_para_and_headers(Activity.verify_captcha, cookie)
    para['variables']['captcha'] = captcha
    para['variables']['captchaCode'] = code
    resp = post(para, headers)
    ws_url = None
    verify_result = False

    try:
        resp = resp.json()
        verify_result = resp['data']['userAuth']['prereserve']['verifyCaptcha']
        if verify_result:
            ws_url = resp['data']['userAuth']['prereserve']['setStep1']
    except Exception as e:
        log_info("响应无json")
        log_info(resp.content)
        raise e

    return (verify_result, ws_url)


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
