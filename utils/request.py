import traceback

import requests

from utils.request_utils.request import Activity, get_para_and_headers, get_resp, get_step, get_step_response, post
from utils.utils import log, log_info


def need_captcha(cookie: str) -> bool:
    """判断当前是否需要验证验证码

    Args:
        cookie (str): headers中的cookie

    Returns:
        bool: true为需要
    """
    return get_step(cookie) == 0


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
    except ValueError as value_exc:
        log_info('\n' + traceback.format_exc())
        log_info("get_prereserve_libLayout时无json")
        log_info(resp.content)
        raise value_exc
    except Exception as e:
        log_info('\n' + traceback.format_exc())
        log_info("get_prereserve_libLayout时发生其他异常")
        raise e
    return result


def verify_cookie(cookie: str) -> bool:
    """验证cookie有效性

    Args:
        cookie (str): headers中的cookie参数

    Raises:
        e: 响应无json

    Returns:
        bool: true则cookie有效
    """
    resp = get_resp(Activity.index, cookie)
    try:
        resp = resp.json()
    except ValueError as value_exc:
        log_info('\n' + traceback.format_exc())
        log_info("verify_cookie时无json")
        log_info(resp.content)
        raise value_exc
    except Exception as e:
        log_info('\n' + traceback.format_exc())
        log_info("verify_cookie时发生其他异常")
        raise e
    return 'errors' not in resp


def get_SToken(cookie: str) -> str:
    """获取退座所需要的SToken

    Args:
        cookie (str): headers中的cookie参数

    Raises:
        key_exc: json无对应键值
        value_exc: 响应无json
        e: 其他异常

    Returns:
        str: 退座所需要的SToken
    """
    resp = get_resp(Activity.index, cookie)
    try:
        resp = resp.json()
        result = resp['data']['userAuth']['reserve']['getSToken']
    except KeyError as key_exc:
        log_info('\n' + traceback.format_exc())
        log_info("get_SToken时无所需数据")
        log_info(_json=resp)
        raise key_exc
    except ValueError as value_exc:
        log_info('\n' + traceback.format_exc())
        log_info("get_SToken时无json")
        log_info(resp.content)
        raise value_exc
    except Exception as e:
        log_info('\n' + traceback.format_exc())
        log_info("get_SToken时发生其他异常")
        raise e
    return result


def get_ws_url(cookie: str) -> str:
    """获取websocket链接地址（通常在程序崩溃时重新运行时获取）

    Args:
        cookie (str): headers中的cookie参数

    Raises:
        value_exc: 无json
        key_exc: json无数据
        e: 其他异常

    Returns:
        str: websocket地址
    """
    resp = get_step_response(cookie)
    try:
        resp = resp.json()
        result = resp['data']['userAuth']['prereserve']['queeUrl']
    except ValueError as value_exc:
        log_info('\n' + traceback.format_exc())
        log_info("get_ws_url时无json")
        log_info(resp.content)
        raise value_exc
    except KeyError as key_exc:
        log_info('\n' + traceback.format_exc())
        log_info("get_ws_url时json中无所需数据")
        log_info(_json=resp)
        raise key_exc
    except Exception as e:
        log_info('\n' + traceback.format_exc())
        log_info("get_ws_url时发生其他错误")
        raise e
    return result


def get_queue_url(cookie: str) -> str:
    """获取排队的get连接

    Args:
        cookie (str): headers中的cookie参数

    Raises:
        value_exc: 无json
        key_exc: json无数据
        e: 其他异常

    Returns:
        str: 排队的get连接
    """
    resp = get_step_response(cookie)
    try:
        resp = resp.json()
        result = resp['data']['userAuth']['prereserve']['successUrl']
    except ValueError as value_exc:
        log_info('\n' + traceback.format_exc())
        log_info("get_queue_url时无json")
        log_info(resp.content)
        raise value_exc
    except KeyError as key_exc:
        log_info('\n' + traceback.format_exc())
        log_info("get_queue_url时json中无所需数据")
        log_info(_json=resp)
        raise key_exc
    except Exception as e:
        log_info('\n' + traceback.format_exc())
        log_info("get_queue_url时发生其他异常")
        raise e
    return result


def get_captcha_code_website(cookie: str) -> tuple:
    """获取验证码的code和网址

    Args:
        cookie (str): headers的cookie

    Raises:
        value_exc: 无json
        key_exc: json数据
        e: 其他异常

    Returns:
        tuple: 返回元组，第一个元素为code(后面发送验证请求会用到)，第二个元素为网址
    """
    resp = get_resp(Activity.captcha, cookie)

    try:
        resp = resp.json()
        result = ((resp['data']['userAuth']['prereserve']['captcha']['code'], resp['data']['userAuth']['prereserve']['captcha']['data']))
    except ValueError as value_exc:
        log_info('\n' + traceback.format_exc())
        log_info("get_captcha_code_website时无json")
        log_info(resp.content)
        raise value_exc
    except KeyError as key_exc:
        log_info('\n' + traceback.format_exc())
        log_info("get_captcha_code_website时json中无code及网址")
        log_info(_json=resp)
        raise key_exc
    except Exception as e:
        log_info('\n' + traceback.format_exc())
        log_info("get_captcha_code_website时发生其他异常")
        raise e

    return result


def get_captcha_image(website: str) -> bytes:
    """根据网址获取验证码图片二进制信息

    Args:
        website (str): 验证码网址

    Raises:
        Exception: 图片地址404

    Returns:
        bytes: 图片二进制信息
    """
    resp = requests.get(website)
    if resp.status_code != 404:
        return resp.content
    else:
        log_info('图片地址404')
        raise Exception("get_captcha_image时404 Not Found")


def verify_captcha(cookie: str, captcha: str, code: str) -> tuple:
    """验证验证码是否正确，返回结果以及websocket的url

    Args:
        cookie (str): headers的cookie
        captcha (str): 识别出来的验证码
        code (str): 验证码的code（前面post请求得到的）

    Raises:
        value_exc: 无json
        key_exc: json无数据
        e: 其他异常

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
    except ValueError as value_exc:
        log_info('\n' + traceback.format_exc())
        log_info("verify_captcha时无json")
        log_info(resp.content)
        raise value_exc
    except KeyError as key_exc:
        log_info('\n' + traceback.format_exc())
        log_info("verify_captcha时json中无code及网址")
        log_info(_json=resp)
        raise key_exc
    except Exception as e:
        log_info('\n' + traceback.format_exc())
        log_info("verify_captcha时发生其他异常")
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
