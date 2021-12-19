import json
import time
import traceback

import requests


def wait_time(hour: int, minute: int):
    """等待至参数指定的时间（时间可为负值）

    Args:
        hour (int): 等待的点
        minute (int): 等待的分
    """
    time_to_wait = hour * 60 + minute
    while time.localtime().tm_hour * 60 + time.localtime().tm_min < time_to_wait:
        pass


def take_seat_name(elem: dict):
    """从seat dict中获取座位号

    Args:
        elem (dict): seat dict

    Returns:
        int: 座位号
    """
    name = elem['name']
    if name != "" and name is not None:
        return int(elem['name'])
    return 5000


def log(msg=None, _json=None):
    """输出格式化信息到控制台（可能会改为到文件

    Args:
        message (str): 要输出的信息
    """
    # with open('log.out','a',encoding='utf-8') as f:
    # f.write(time.strftime("[%Y-%m-%d %H:%M:%S] ", time.localtime())+'\t'+f'{message}'+'\n')
    msg = msg_or_json(msg, _json)
    print(f'{time.strftime("[%Y-%m-%d %H:%M:%S] ", time.localtime())}\t{msg}')


def msg_or_json(msg=None, _json=None) -> str:
    """根据传入参数返回处理好的信息，两个参数有且仅有一个参数不为none

    Args:
        msg (str, optional): 普通信息. Defaults to None.
        _json (dict, optional): json信息. Defaults to None.
    """
    if (msg is None and _json is None) or (msg is not None and _json is not None):
        log("非法！错误信息及json信息同时为空或同时不为空")
        return

    if (msg is None):
        return f'\n{json.dumps(_json, indent=4, ensure_ascii=False)}'
    else:
        return msg


def log_info(info=None, _json=None):
    """记录错误至info.out文件，两个参数有且仅可有一个参数有值

    Args:
        error (str, optional): 要输出的错误信息. Defaults to None.
        json (dict, optional): 要输出错误发生时的json. Defaults to None.
    """
    msg = msg_or_json(info, _json)
    log_file(msg, "log/info.out")


def log_file(msg: str, file: str):
    """将msg输出到file指定的文件中

    Args:
        msg (str): 输出信息
        file (str): 文件名称及路径
    """
    with open(file, 'a') as f:
        f.write(f'{time.strftime("[%Y-%m-%d %H:%M:%S] ", time.localtime())}\t{msg}\n')


def save_image(image_byte: bytes, name: str, image_path: str):
    '''保存验证码图片
    参数
    -----------------------
    image_byte:bytes
        要保存的图片二进制数据
    name:str
        保存图片文件名称
    image_path:str
        保存地址/路径
    '''
    try:
        with open(f'{image_path}/{name}', 'wb') as f:
            f.write(image_byte)
    except Exception:
        traceback.print_exc()


def save_unrecognized_image(image_byte: bytes, code: str, website: str):
    """保存未验证的验证码图片到对应文件夹

    Args:
        image_byte (bytes): 图片二进制信息
        code (str): 该验证码code（通过前面post请求获取）
        website (str): 该验证码的网址
    """
    name = '_'.join((code, website.split('/')[-1]))
    save_image(image_byte, name, 'resource/captcha/unrecognized_captcha')


def save_recognized_image(image_byte: bytes, captcha: str, code: str, website: str):
    """保存已验证的验证码图片到对应文件夹

    Args:
        image_byte (bytes): 验证码图片二进制信息
        captcha (str): 识别出来的验证码
        code (str): 验证码code（通过前面post请求获取）
        website (str): 该验证码图片的网址
    """
    name = '_'.join((captcha, code, website.split('/')[-1]))
    save_image(image_byte, name, 'resource/captcha/recognized_captcha')


def seat_exist(seat: dict) -> bool:
    """判断当前座位是否存在

    Args:
        seat (dict): 座位dict

    Raises:
        key_exc: 座位无数据
        e: 其他异常

    Returns:
        bool: true为座位存在
    """
    try:
        if seat['name'] == "" or seat['name'] is None:
            return False
        else:
            return True
    except KeyError as key_exc:
        log_info(f'\n{traceback.format_exc()}')
        log_info("seat_exist时座位无数据")
        log_info(seat)
        raise key_exc
    except Exception as e:
        log_info(f'\n{traceback.format_exc()}')
        log_info("seat_exist时发生其他错误")
        log_info(seat)
        raise e


def pass_captcha(cookie: str) -> str:
    """进行验证码验证,并返回websocket连接地址

    Args:
        cookie (str): header中的cookie

    Returns:
        str: websocket连接地址
    """
    from utils.request import get_captcha_code_website, get_captcha_image, verify_captcha
    from ddddocr import DdddOcr

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


def pass_queue(queue_url: str):
    """通过排队

    Args:
        queue_url: 排队人数连接
    """
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
