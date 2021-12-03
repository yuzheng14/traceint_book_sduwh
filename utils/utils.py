import json
import time
import traceback
from enum import Enum


# TODO doc注释
def wait_time(hour, minute):
    time_to_wait = hour * 60 + minute
    while time.localtime().tm_hour * 60 + time.localtime(
    ).tm_min < time_to_wait:
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
    print((time.strftime("[%Y-%m-%d %H:%M:%S] ", time.localtime()) + '\t' +
           f'{message}'))


def log_json(message_json):
    log(f'\n{json.dumps(message_json,indent=4,ensure_ascii=False)}')


# TODO doc注释
# TODO 完善函数
# TODO 未拆封微信浏览器之前无法完善
def renew_cookie(cookie: dict) -> dict:
    from utils.request import verify_cookie
    if verify_cookie(cookie):
        log('当前验证码有效，无需更新')
        return cookie
    pass
    return cookie


# TODO doc注释
# TODO 完善函数
def have_seat() -> bool:
    pass


# TODO doc注释
class Activity(Enum):
    captcha = {
        "operationName":
        "getStep0",
        "query":
        "query getStep0 {\n userAuth {\n prereserve {\n getNum\n captcha {\n code\n data\n }\n }\n }\n}"
    }
    prereserve_10_seats = {}
    get_end_time = {}
    prereserve = {}
    verify_captcha = {}
    reserve_10_seats = {}
    reserve_all_floors = {}
    reserve = {}
    index = {}
    withdraw = {}


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
