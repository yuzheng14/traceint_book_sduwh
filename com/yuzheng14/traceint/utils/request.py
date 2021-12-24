import time
import traceback
from typing import Tuple, List

import requests
import websocket
from ddddocr import DdddOcr

from com.yuzheng14.traceint.utils.request_utils.request import Activity, get_para_and_headers, get_resp, \
    get_step_response, post
from com.yuzheng14.traceint.utils.utils import log, log_info, seat_exist, save_unrecognized_image, \
    save_recognized_image, get_lib_id, wait_time


def queue_init(cookie: str) -> tuple:
    """初始化排队并获取need_captcha, need_queue, ws_url, queue_url

    Args:
        cookie (str): header参数cookie

    Raises:
        value_exc: 无json
        key_exc: json无数据
        e: 其他异常

    Returns:
        tuple: 按顺序分别为need_captcha, need_queue, ws_url, queue_url
    """
    resp = get_step_response(cookie)
    try:
        resp = resp.json()
        get_step = resp['data']['userAuth']['prereserve']['getStep']
        ws_url = resp['data']['userAuth']['prereserve']['queeUrl']
        queue_url = resp['data']['userAuth']['prereserve']['successUrl']
        if get_step == 0:
            need_captcha = True
        else:
            need_captcha = False
        if get_step == 1:
            need_queue = True
        else:
            need_queue = False
    except ValueError as value_exc:
        log_info('\n' + traceback.format_exc())
        log_info("queue_init时无json")
        log_info(resp.content)
        raise value_exc
    except KeyError as key_exc:
        log_info('\n' + traceback.format_exc())
        log_info("queue_init时无json无数据")
        log_info(resp)
        raise key_exc
    except Exception as e:
        log_info('\n' + traceback.format_exc())
        log_info("queue_init时发生其他异常")
        raise e
    return need_captcha, need_queue, ws_url, queue_url


def get_prereserve_libLayout(cookie: str, lib_id: int) -> list:
    """通过libId获取该层图书馆的座位信息

    Args:
        cookie (str): headers中的cookie
        lib_id (int): 图书馆楼层id

    Raises:
        value_exc: 无json
        key_exc: json无数据
        e: 其他异常

    Returns:
        list: 座位信息list
    """
    para, headers = get_para_and_headers(Activity.prereserveLibLayout, cookie)
    para['variables']['libId'] = lib_id

    resp = post(para, headers)
    try:
        resp = resp.json()
        result = resp["data"]["userAuth"]["prereserve"]["libLayout"]["seats"]
    except ValueError as value_exc:
        log_info('\n' + traceback.format_exc())
        log_info("get_prereserve_libLayout时无json")
        log_info(resp.content)
        raise value_exc
    except KeyError as key_exc:
        log_info('\n' + traceback.format_exc())
        log_info("get_prereserve_libLayout时无json无数据")
        log_info(resp)
        raise key_exc
    except Exception as e:
        log_info('\n' + traceback.format_exc())
        log_info("get_prereserve_libLayout时发生其他异常")
        raise e
    return [seat for seat in result if seat_exist(seat)]


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
        result = (resp['data']['userAuth']['prereserve']['captcha']['code'],
                  resp['data']['userAuth']['prereserve']['captcha']['data'])
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

    return verify_result, ws_url


def pass_captcha(cookie: str) -> str:
    """进行验证码验证,并返回websocket连接地址

    Args:
        cookie (str): header中的cookie

    Returns:
        str: websocket连接地址
    """

    ocr = DdddOcr()

    # 获取验证码的code和网址，并获取图片二进制信息
    captcha_code, captcha_website = get_captcha_code_website(cookie)
    image_byte = get_captcha_image(captcha_website)

    # ocr识别验证码
    captcha = ocr.classification(image_byte)
    log_info(f'识别验证码为{captcha}')

    # 获取验证验证码是否成功以及获得ws_url地址
    verify_result, ws_url = verify_captcha(cookie, captcha, captcha_code)
    while not verify_result:
        log_info(f'{captcha_code}尝试失败，保存验证码图片后开始下一次尝试')
        save_unrecognized_image(image_byte, captcha_code, captcha_website)

        # 获取验证码的code和网址，并获取验证码图片二进制信息
        captcha_code, captcha_website = get_captcha_code_website(cookie)
        image_byte = get_captcha_image(captcha_website)

        # 识别验证码
        captcha = ocr.classification(image_byte)
        log_info(f'识别验证码为{captcha}')
        verify_result, ws_url = verify_captcha(cookie, captcha, captcha_code)

    log_info(f'验证码尝试成功，验证码为{captcha}')
    save_recognized_image(image_byte, captcha, captcha_code, captcha_website)
    return ws_url


def pass_queue(queue_url: str, ws_url: str, need_captcha: bool, need_queue: bool) -> websocket._core.WebSocket:
    """
    通过排队
    Args:
        queue_url: 排队链接
        ws_url: websocket连接
        need_captcha: 是否需要验证验证码
        need_queue: 是否需要排队
    """
    ws = None
    try:
        if need_captcha or need_queue:
            log('当前需要排队，即将开始排队')
            log_info(f'连接地址{ws_url}')
            ws = websocket.create_connection(ws_url, timeout=30)
            log_info('create_connection连接成功')
    except Exception:
        log_info(f'\n{traceback.format_exc()}')
        log_info('create_connection连接异常')

    resp_queue = requests.get(queue_url)
    queue_num = int(resp_queue.content)
    log(f'前方排队{queue_num}人')
    while queue_num > 0:
        log_info(f'前方排队{queue_num}人')
        if queue_num > 100:
            time.sleep(2)
        resp_queue = requests.get(queue_url)
        queue_num = int(resp_queue.content)
    log_info(f'前方排队{queue_num}人')
    return ws


def save(cookie: str, key: str, lib_id: int) -> bool:
    """
    预定座位
    Args:
        cookie: headers中的cookie
        key: 座位key，seat字典中获取
        lib_id: 楼层id

    Returns:
        true为预定成功
    """
    para, headers = get_para_and_headers(Activity.save, cookie)
    para["variables"]["key"] = key
    para['variables']['libid'] = lib_id
    resp = post(para, headers)
    try:
        resp = resp.json()
        if 'errors' in resp:
            log_info('save时json数据内含错误或预定失败')
            log_info(_json=resp)
            return False
        return resp["data"]["userAuth"]["prereserve"]["save"]
    except ValueError as value_exc:
        log_info('\n' + traceback.format_exc())
        log_info("save时无json")
        log_info(resp.content)
        raise value_exc
    except KeyError as key_exc:
        log_info('\n' + traceback.format_exc())
        log_info("save时json无对应数据")
        log_info(_json=resp)
        raise key_exc
    except Exception as e:
        log_info('\n' + traceback.format_exc())
        log_info("save时发生其他异常")
        log_info(resp)
        log_info(resp.content)
        raise e


def pass_save(cookie: str, floor: int, often_seat: int, reverse: bool) -> str:
    """
    预定座位过程，成功则返回预定座位号
    Args:
        cookie: headers中的cookie
        floor: 楼层
        often_seat: 常用座位号
        reverse: 是否倒序

    Returns:
        预定座位号
    """
    lib_id = get_lib_id(floor)
    # 获取10楼的座位信息
    seats = get_prereserve_libLayout(cookie, lib_id)
    seats.sort(key=lambda s: abs(int(s['name']) - often_seat), reverse=reverse)
    # 预定座位
    for seat in seats:
        if not seat["status"]:
            log_info(f"开始预定{seat['name']}号")
            if save(cookie, seat['key'], lib_id):
                log_info(f"预定成功，座位为{seat['name']}号")
                return seat['name']
        else:
            log_info(f"{seat['name']}号座位已有人")


def wait_for_start(cookie: str) -> Tuple[bool, bool, bool, str, str]:
    """
    等待明日预约开始时间并初始化数据
    Args:
        cookie: headers中的cookie

    Returns:
        tuple: 按顺序为cookie_ok, need_captcha, need_queue, ws_url, queue_url
    """
    if not verify_cookie(cookie):
        log_info('cookie无效，请重新输入cookie')
        return False, False, False, '', ''
    # 在开始明日预约前的1分钟确认cookie是否有效
    log('开始等待验证cookie时间')
    wait_time(12, 29)
    if not verify_cookie(cookie):
        log_info('cookie无效，请重新输入cookie')
        return False, False, False, '', ''
    else:
        log('cookie有效，请等待预定时间')

    # 等待明日预约开始
    log('开始等待预定时间')
    wait_time(12, 30)
    need_captcha, need_queue, ws_url, queue_url = queue_init(cookie)
    return True, need_captcha, need_queue, ws_url, queue_url


def wait_for_reserve(cookie: str) -> bool:
    """
    等待捡漏开始
    Args:
        cookie: headers中的cookie

    Returns:
        bool: true为cookie验证成功
    """
    if not verify_cookie(cookie):
        log_info('cookie无效，请重新输入cookie')
        return False
    # 在开始明日预约前的1分钟确认cookie是否有效
    log('开始等待验证cookie时间')
    wait_time(6, 59)
    if not verify_cookie(cookie):
        log_info('cookie无效，请重新输入cookie')
        return False
    else:
        log('cookie有效，请等待预定时间')

    # 等待明日预约开始
    log('开始等待预定时间')
    wait_time(7, 00)
    return True


def get_libLayout(cookie: str, lib_id: int) -> List[dict]:
    """
    获取捡漏座位信息
    Args:
        cookie: headers中的cookie
        lib_id: 图书馆楼层id

    Returns:
        List[dict]: 座位信息list
    """
    para, headers = get_para_and_headers(Activity.libLayout, cookie)
    para['variables']['libId'] = lib_id

    resp = post(para, headers)
    try:
        resp = resp.json()
        result = resp["data"]["userAuth"]["reserve"]["libs"][0]["lib_layout"]["seats"]
    except ValueError as value_exc:
        log_info('\n' + traceback.format_exc())
        log_info("get_libLayout时无json")
        log_info(resp.content)
        raise value_exc
    except KeyError as key_exc:
        log_info('\n' + traceback.format_exc())
        log_info("get_libLayout时无json无数据")
        log_info(resp)
        raise key_exc
    except Exception as e:
        log_info('\n' + traceback.format_exc())
        log_info("get_libLayout时发生其他异常")
        raise e
    return [seat for seat in result if seat_exist(seat)]


def reserveSeat(cookie: str, seat_key: str, lib_id: int) -> bool:
    """
    预定当日座位
    Args:
        cookie: headers中的cookie
        seat_key: 座位id，seat信息中
        lib_id: 楼层id

    Returns:
        true为预定成功
    """
    para, headers = get_para_and_headers(Activity.reserveSeat, cookie)
    para["variables"]["seatKey"] = seat_key
    para['variables']['libId'] = lib_id
    resp = post(para, headers)
    try:
        resp = resp.json()
        if 'errors' in resp:
            log_info('reserveSeat时json数据内含错误或预定失败')
            log_info(_json=resp)
            return False
        return resp["data"]["userAuth"]["reserve"]["reserveSeat"]
    except ValueError as value_exc:
        log_info('\n' + traceback.format_exc())
        log_info("reserveSeat时无json")
        log_info(resp.content)
        raise value_exc
    except KeyError as key_exc:
        log_info('\n' + traceback.format_exc())
        log_info("reserveSeat时json无对应数据")
        log_info(_json=resp)
        raise key_exc
    except Exception as e:
        log_info('\n' + traceback.format_exc())
        log_info("reserveSeat时发生其他异常")
        log_info(resp)
        log_info(resp.content)
        raise e


def reserve_floor(cookie: str, floor: int, reverse: bool) -> str:
    """
    遍历一整层楼的座位，预定空座位
    Args:
        cookie: headers中的cookie
        floor: 楼层
        reverse: 是否倒序

    Returns:
        成功则返回座位号，否则返回空字符串
    """
    lib_id = get_lib_id(floor)
    seats = get_libLayout(cookie, lib_id)
    seats.sort(key=lambda s: int(s['name']), reverse=reverse)
    log_info(f'开始遍历{floor}楼')
    for seat in seats:
        if seat["seat_status"] == 1:
            log_info(f"开始预定{seat['name']}号")
            try:
                if reserveSeat(cookie, seat['key'], lib_id):
                    log_info(f"预定成功，座位为{seat['name']}号")
                    return seat['name']
            except Exception:
                log_info(f'预定{seat["name"]}时发生错误')
                return ''
    return ''


def pass_reserve(cookie: str, often_floor: int, strict_mode: bool, reserve: bool) -> str:
    """
    通过捡漏
    Args:
        cookie: headers中的cookie
        often_floor: 常用楼层
        strict_mode: 是否为严格模式，默认为true，false则为遍历全部楼层
        reserve: 是否倒序

    Returns:
        成功则返回座位号，否则返回空字符串
    """
    seat = reserve_floor(cookie, often_floor, reserve)
    if seat != '':
        return seat
    # 如果不是严格模式，则遍历全部楼层
    if not strict_mode:
        floor = [_ for _ in range(1, 15) if _ != often_floor]
        floor.sort(key=lambda f: abs(f - often_floor))
        for i in floor:
            seat = reserve_floor(cookie, get_lib_id(i), reserve)
            if seat != '':
                return seat
    return ''


def reserveCancle(cookie: str) -> bool:
    """
    退座
    Args:
        cookie: headers中的cookie

    Returns:
        true为退座成功
    """
    para, headers = get_para_and_headers(Activity.reserveCancle, cookie)
    para['variables']['sToken'] = get_SToken(cookie)
    resp = post(para, headers)
    try:
        resp = resp.json()
        if 'error' not in resp:
            return True
        log_info("reserveCancle发生错误")
        log_info(_json=resp)
    except ValueError as value_exc:
        log_info('\n' + traceback.format_exc())
        log_info("reserveCancle时无json")
        log_info(resp.content)
        raise value_exc
    except KeyError as key_exc:
        log_info('\n' + traceback.format_exc())
        log_info("reserveCancle时无json无数据")
        log_info(resp)
        raise key_exc
    except Exception as e:
        log_info('\n' + traceback.format_exc())
        log_info("reserveCancle时发生其他异常")
        raise e


def pass_to_cancel(cookie: str) -> bool:
    """
    等待退座
    Args:
        cookie: headers中的cookie

    Returns:
        true为cookie失效
    """
    if not verify_cookie(cookie):
        log_info('cookie失效，请输入有效cookie后重试')
        return False

    log('开始等待验证cookie时间')
    wait_time(22, 29)
    if not verify_cookie(cookie):
        log_info('cookie无效，请重新输入cookie')
        return False
    else:
        log_info('cookie有效，请等待预定时间')

    log('等待固定时间')

    wait_time(22, 30)
    return True


# TODO doc注释
# TODO 完善函数
# TODO 未拆封微信浏览器之前无法完善
def renew_cookie(cookie: str) -> str:
    if verify_cookie(cookie):
        log('当前验证码有效，无需更新')
        return cookie
    pass
    return cookie


# TODO doc注释
# TODO 完善函数
def have_seat(cookie: str) -> bool:
    """
    判断当前是否有座位
    Args:
        cookie: headers中的cookie

    Returns:
        true为有座位
    """
    resp = get_resp(Activity.index, cookie)
    try:
        resp = resp.json()
        return resp['data']['userAuth']['reserve']['reserve'] is not None
    except ValueError as value_exc:
        log_info('\n' + traceback.format_exc())
        log_info("have_seat时无json")
        log_info(resp.content)
        raise value_exc
    except Exception as e:
        log_info('\n' + traceback.format_exc())
        log_info("have_seat时发生其他异常")
        raise e
