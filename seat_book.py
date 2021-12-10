import json
import time

from utils.utils import log, wait_time, take_seat_name
from utils.request import post, verify_cookie


# seat_status=1为可预订
def book(cookie):
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
    if not verify_cookie(cookie):
        log('cookie无效，请重新输入')
    log('开始等待开始时间')
    wait_time(7, 00)
    log('等待九点钟')
    wait_time(9, 00)
    while (True):
        resp = post(post_para, headers).json()
        if 'errors' in resp:
            log(resp)
            continue
        log("post请求成功")

        seats = resp["data"]["userAuth"]["reserve"]["libs"][0]["lib_layout"][
            "seats"]
        seats.sort(key=take_seat_name)
        for seat in seats:
            if seat['name'] == "" or seat['name'] is None:
                continue
            if (seat["seat_status"] == 1):
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
    book(
        'FROM_TYPE=weixin; v=5.5; Hm_lvt_7ecd21a13263a714793f376c18038a87=1638590314; wechatSESS_ID=acd56330154697ffc964552e73de519d6a5a94251ffe9378; Authorization=eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJ1c2VySWQiOjEwMDg2MjMsInNjaElkIjoxMjYsImV4cGlyZUF0IjoxNjM5MDk5MTM1fQ.cTQJe09lK_ecrH5pFm_MmADxX-bGu2Uw1dLBTvbT_GCKKwmk9henq9BGEjUSwzR2BQi82LSFnMIXnVT4lh0Zi4DOWdtY9lX9f0pdcYLhXv7iwERL_O1RAQhwFSilGgRryjF5f1R46h6IznyGUmZQ7cuJV67SZrxFDwe45wcePhHWVFdJ7rKgiug-QeZWVSNRdmKqkfbvrZZE_3eCbwrq2RmsR4KMQ8j7FXgda9ZHDaS8Zt7wC6UjzwFvpgkJ7yG6-SepH2l29qTJJvHvM9rWVW5O9Vj1-oVF5_dy5sO51XclmAQFILaceFHpHKt7Quxvy-J6kX4jscwIJcJug4Q1Rg; Hm_lpvt_7ecd21a13263a714793f376c18038a87=1639095818; SERVERID=d3936289adfff6c3874a2579058ac651|1639096044|1639095527'
    )
    # book_test()
