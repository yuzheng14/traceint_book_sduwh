import traceback

import requests
import websocket

import json
from utils.request import post, verify_cookie, get_prereserve_libLayout, queue_init
from utils.utils import log, take_seat_name, wait_time, log_info, \
    seat_exist, pass_captcha, pass_queue


# status=false时可以预定
def seat_prereserve(cookie: str, floor=10):
    if not verify_cookie(cookie):
        log('cookie无效，请重新输入cookie')
        return

    lib_id = 758

    need_captcha, need_queue, ws_url, queue_url = queue_init(cookie)

    with open('json/reserve/reserve_para.json', 'r') as f:
        prereserve_para = json.load(f)
    with open('json/reserve/reserve_headers.json', 'r') as f:
        prereserve_headers = json.load(f)
    prereserve_headers['Cookie'] = cookie
    prereserve_para["variables"]["key"] = '31,74'

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
    # 如果没有验证验证码，则开始验证验证码
    if need_captcha:
        log('当前未验证验证码，开始验证验证码')
        ws_url = pass_captcha(cookie)
    else:
        log('已验证验证码')

    try:
        if need_captcha or need_queue:
            log('当前需要排队，即将开始排队')
            log_info(f'连接地址{ws_url}')
            ws = websocket.create_connection(ws_url, timeout=30)
            log_info('create_connection连接成功')
    except Exception:
        log_info(f'\n{traceback.format_exc()}')
        log_info('create_connection连接异常')

    pass_queue(queue_url)

    log('排队完成')

    # 获取10楼的座位信息
    seats = [seat for seat in get_prereserve_libLayout(cookie, lib_id) if seat_exist(lib_id)]
    seats.sort(key=take_seat_name)

    for seat in seats:
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

    if 'ws' in dir():  # vars() locals().keys()均可
        ws.close()
        log('create_connection连接关闭')

    resp_queue = requests.get(queue_url)
    queue_num = int(resp_queue.content)
    log(f'关闭websocket后排队人数{queue_num}')

    if 'image_byte' in dir():
        log('开始写入验证码图片')


if __name__ == '__main__':
    seat_prereserve('')
