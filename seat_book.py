import time

import json
from utils.request import post, verify_cookie, wait_for_reserve
from utils.utils import log, wait_time


# seat_status=1为可预订
def book(cookie: str, often_floor: int = 3, strict_mode=False, reserve=False):

    with open('json/book/10_para.json', 'r') as f:
        post_para = json.load(f)
    with open('json/book/10_headers.json', 'r') as f:
        headers = json.load(f)
    headers['Cookie'] = cookie

    with open('json/book/book_para.json', 'r') as f:
        book_para = json.load(f)
    with open('json/book/book_headers.json', 'r') as f:
        book_headers = json.load(f)
    book_headers['Cookie'] = headers['Cookie']

    # 验证cookie并等待开始抢座
    if not wait_for_reserve(cookie):
        log('cookie无效，请改正后重试')
        return

    wait_time(7, 00)
    # log('等待九点钟')
    # wait_time(9, 00)
    while True:
        resp = post(post_para, headers).json()
        if 'errors' in resp:
            log(resp)
            continue
        log("post请求成功")

        seats = resp["data"]["userAuth"]["reserve"]["libs"][0]["lib_layout"][
            "seats"]
        seats.sort(key=lambda s: int(s['name']))
        for seat in seats:
            if seat['name'] == "" or seat['name'] is None:
                continue
            if seat["seat_status"] == 1:
                book_para["variables"]["seatKey"] = seat["key"]
                log(f"开始预定{seat['name']}号")
                book_resp = post(book_para, book_headers).json()
                try:
                    if book_resp["data"]["userAuth"]["reserve"]["reserveSeat"]:
                        log(f"预定成功，座位为{seat['name']}号")
                        return
                except Exception:
                    log(f"预定{seat['name']}号失败")
                    continue
        time.sleep(2)


if __name__ == '__main__':
    cookie = ''
    book(cookie)
    # book_test()
