import json
import time
import traceback

import ddddocr
import requests
import websocket

from utils.utils import (log, save_recognized_image, save_unrecognized_image, take_seat_name, wait_time, log_info)
from utils.request import post, verify_cookie, need_captcha, get_ws_url, get_captcha_code_website, get_captcha_image, verify_captcha, get_queue_url, get_prereserve_libLayout


# status=false时可以预定
def seat_prereserve(cookie):
    if not verify_cookie(cookie):
        log('cookie无效，请重新输入cookie')
        return

    ocr = ddddocr.DdddOcr()

    queue_url = get_queue_url(cookie)

    with open('json/reserve/reserve_para.json', 'r') as f:
        prereserve_para = json.load(f)
    with open('json/reserve/reserve_headers.json', 'r') as f:
        prereserve_headers = json.load(f)
    prereserve_headers['Cookie'] = cookie
    prereserve_para["variables"]["key"] = '31,74'

    with open('json/reserve/pre_10_headers.json', 'r') as f:
        pre_headers = json.load(f)
    with open('json/reserve/pre_10_para.json', 'r') as f:
        pre_para = json.load(f)
    pre_headers['Cookie'] = cookie

    # 在开始明日预约前的1分钟确认cookie是否有效
    log('开始等待验证cookie时间')
    wait_time(12, 29)
    if not verify_cookie(cookie):
        log('cookie无效，请重新输入cookie')
        return
    else:
        log('cookie有效，请等待预定时间')

    # 等待明日预约开始
    log('开始等待预定时间')
    wait_time(12, 30)

    # 开始抢座
    try:
        # TODO 一个函数获取need_captcha,need_queue,ws_url
        # 如果没有验证验证码，则开始验证验证码
        if need_captcha(cookie):

            log('当前未验证验证码，开始验证验证码')

            # 获取验证码的code和网址，并获取图片二进制信息
            captcha_code, captcha_website = get_captcha_code_website(cookie)
            image_byte = get_captcha_image(captcha_website)

            # ocr识别验证码
            captcha = ocr.classification(image_byte)
            log_info(f'识别验证码为{captcha}')

            # 获取验证验证码是否成功以及获得ws_url地址
            verify_result, ws_url = verify_captcha(cookie, captcha, captcha_code)
            while not verify_result:

                log(f'{captcha_code}尝试失败，保存验证码图片后开始下一次尝试')
                save_unrecognized_image(image_byte, captcha_code, captcha_website)

                # 获取验证码的code和网址，并获取验证码图片二进制信息
                captcha_code, captcha_website = get_captcha_code_website(cookie)
                image_byte = get_captcha_image(captcha_website)

                # 识别验证码
                captcha = ocr.classification(image_byte)
                log_info(f'识别验证码为{captcha}')
                verify_result, ws_url = verify_captcha(cookie, captcha, captcha_code)

            log(f'验证码尝试成功，验证码为{captcha}')
        else:
            log('已验证验证码')
    except Exception:
        log('错误')
        traceback.print_exc()

    try:
        try:
            if ws_url is None:
                ws_url = get_ws_url(cookie)
        except Exception:
            ws_url = get_ws_url(cookie)

        log(f'wss连接地址{ws_url}')
        wss = websocket.create_connection(ws_url, timeout=30)
        log('create_connection连接成功')
    except Exception:
        log('create_connection连接异常')
        traceback.print_exc()

    resp_queue = requests.get(queue_url)
    queue_num = int(resp_queue.content)
    log(f'前方排队{queue_num}人')
    while queue_num > 0:
        log(f'前方排队{queue_num}人')
        if queue_num > 100:
            time.sleep(2)
        resp_queue = requests.get(queue_url)
        queue_num = int(resp_queue.content)
    log(f'前方排队{queue_num}人')
    log('排队完成')

    resp = post(pre_para, pre_headers).json()
    while 'errors' in resp:
        log('请求座位失败')
        log(json.dumps(resp, indent=4, ensure_ascii=False))

    seats = resp["data"]["userAuth"]["prereserve"]["libLayout"]["seats"]
    seats.sort(key=take_seat_name)
    for seat in seats:
        if seat['name'] == "" or seat['name'] is None:
            log("该座位不存在")
            continue
        if not seat["status"]:
            prereserve_para["variables"]["key"] = seat["key"]
            log(f"开始预定{seat['name']}号")
            prereserve_resp = post(prereserve_para, prereserve_headers).json()
            try:
                if prereserve_resp["data"]["userAuth"]["prereserve"]["save"]:
                    log(f"预定成功，座位为{seat['name']}号")
                    break
                else:
                    log(f"预定{seat['name']}号失败")
                    log(json.dumps(prereserve_resp, indent=4, ensure_ascii=False))
            except Exception:
                log(f"预定{seat['name']}号失败")
                log(json.dumps(prereserve_resp, indent=4, ensure_ascii=False))
                continue
        else:
            log(f"{seat['name']}号座位已有人")

    # 查看排队数据，已增强系统精准性
    resp_queue = requests.get(queue_url)
    queue_num = int(resp_queue.content)
    log(f'抢座完成后排队人数{queue_num}')

    if 'wss' in dir():  # vars() locals().keys()均可
        wss.close()
        log('create_connection连接关闭')

    resp_queue = requests.get(queue_url)
    queue_num = int(resp_queue.content)
    log(f'关闭websocket后排队人数{queue_num}')

    if 'image_byte' in dir():
        log('开始写入验证码图片')
        save_recognized_image(image_byte, captcha, captcha_code, captcha_website)


if __name__ == '__main__':
    seat_prereserve('')
