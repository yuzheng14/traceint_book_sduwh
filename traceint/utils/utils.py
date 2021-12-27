import json
import time
import traceback

from traceint.utils.io_func import log_file, save_image, path_exist


def wait_time(hour: int, minute: int):
    """等待至参数指定的时间（时间可为负值）

    Args:
        hour (int): 等待的点
        minute (int): 等待的分
    """
    time_to_wait = hour * 60 + minute
    while time.localtime().tm_hour * 60 + time.localtime().tm_min < time_to_wait:
        pass


def log(msg=None, _json=None):
    """
    输出格式化信息到控制台（可能会改为到文件
    Args:
        msg: plain信息
        _json: json信息
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
        return f'{msg}+{_json}'

    if msg is None:
        return f'\n{json.dumps(_json, indent=4, ensure_ascii=False)}'
    else:
        return msg


def log_info(info=None, _json=None):
    """记录错误至info.out文件，两个参数有且仅可有一个参数有值

    Args:
        info (str, optional): 要输出的错误信息. Defaults to None.
        _json (dict, optional): 要输出错误发生时的json. Defaults to None.
    """
    msg = msg_or_json(info, _json)
    path_exist('log')
    log_file(msg, "log/info.out")


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


def get_lib_id(floor: int) -> int:
    """
    返回楼层对应的libID
    Args:
        floor: 楼层，1为电子阅览室，2为自带电脑学习区，,13为图东环3楼，14为图东环4楼其余楼层对应

    Returns:
        int: lib_id
    """
    lib = [118707, 114074, 716, 730, 737, 765, 744, 786, 751, 758, 772, 779, 793, 800]
    try:
        return lib[floor - 1]
    except IndexError as index_exc:
        log_info(f'\n{traceback.format_exc()}')
        log_info(f'get_lib_id时索引超出范围，索引值为{floor}')
        raise index_exc


def queue_delay(resp: dict) -> bool:
    """
    判断服务器排队是否延迟
    Args:
        resp: 响应转换成str

    Returns:

    """

    return '请先排队' in json.dumps(resp, ensure_ascii=False)
