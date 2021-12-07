import json
import time
import traceback


def wait_time(hour: int, minute: int):
    """等待至参数指定的时间（时间可为负值）

    Args:
        hour (int): 等待的点
        minute (int): 等待的分
    """
    time_to_wait = hour * 60 + minute
    while time.localtime().tm_hour * 60 + time.localtime(
    ).tm_min < time_to_wait:
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


def log(message: str):
    """输出格式化信息到控制台（可能会改为到文件

    Args:
        message (str): 要输出的信息
    """
    # with open('log.out','a',encoding='utf-8') as f:
    # f.write(time.strftime("[%Y-%m-%d %H:%M:%S] ", time.localtime())+'\t'+f'{message}'+'\n')
    print((time.strftime("[%Y-%m-%d %H:%M:%S] ", time.localtime()) + '\t' +
           f'{message}'))


def log_json(message_json):
    log(f'\n{json.dumps(message_json,indent=4,ensure_ascii=False)}')


def log_error(error=None, _json=None):
    """记录错误至error.out文件，两个参数有且仅可有一个参数有值

    Args:
        error (str, optional): 要输出的错误信息. Defaults to None.
        json (dict, optional): 要输出错误发生时的json. Defaults to None.
    """
    if (error is None and _json is None) or (error is not None
                                             and _json is not None):
        log("非法！错误信息及json信息同时为空或同时不为空")

    if (error is None):
        msg = f'\n{json.dumps(_json,indent=4,ensure_ascii=False)}'
    else:
        msg = error

    log_file(msg, "log/error.out")


def log_file(msg: str, file: str):
    """将msg输出到file指定的文件中

    Args:
        msg (str): 输出信息
        file (str): 文件名称及路径
    """
    with open(file, 'a') as f:
        f.write(
            f'{time.strftime("[%Y-%m-%d %H:%M:%S] ", time.localtime())}\t{msg}\n'
        )


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


def save_unrecognized_image(image_byte: bytes, name: str):
    '''保存未验证的验证码图片到对应文件夹
    参数
    -------------------------
    image_bytes:bytes
        要保存的图片二进制代码
    name:str
        保存图片文件名称
    '''
    save_image(image_byte, name, 'resource/captcha/unrecognized_captcha')


def save_recognized_image(image_byte: bytes, name: str):
    '''保存已验证的验证码图片到对应文件夹
    参数
    -------------------------
    image_bytes:bytes
        要保存的图片二进制代码
    name:str
        保存图片文件名称
    '''
    save_image(image_byte, name, 'resource/captcha/recognized_captcha')
