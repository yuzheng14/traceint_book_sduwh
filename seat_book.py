import requests
import json
import time
from utils import post,verify_cookie,take_seat_name,log,wait_time

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
    wait_time(7,00)
    while(True):
        resp = post(post_para, headers).json()
        if 'errors' in resp:
            log(resp)
            time.sleep(1)
            continue
        log("post请求成功")

        # 预定12号（常用座位）
        book_para["variables"]["seatKey"] = '19,75'
        log("开始预定12号")
        book_resp = post(book_para, book_headers).json()
        try:
            if book_resp["data"]["userAuth"]["reserve"]["reserveSeat"]:
                log("预定成功，座位为12号")
                return
        except:
            log("预定12号失败")
        log("预定12号失败")
        seats = resp["data"]["userAuth"]["reserve"]["libs"][0]["lib_layout"]["seats"]
        seats.sort(key=take_seat_name)
        for seat in seats:
            if(seat["seat_status"] == 1):
                book_para["variables"]["seatKey"] = seat["key"]
                log(f"开始预定{seat['name']}号")
                book_resp = post(book_para, book_headers).json()
                try:
                    if book_resp["data"]["userAuth"]["reserve"]["reserveSeat"]:
                        log(f"预定成功，座位为{seat['name']}号")
                        return
                except:
                    log(f"预定{seat['name']}号失败")
                    continue
            else:
                log(f"{seat['name']}号座位已有人")

if __name__ == '__main__':
    book('FROM_TYPE=weixin; v=5.5; Hm_lvt_7ecd21a13263a714793f376c18038a87=1636000165,1636122571,1636331028,1636863912; wechatSESS_ID=fdb301ed98b92dbb5f1c505d515ac459a33b86df091bbada; Authorization=eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJ1c2VySWQiOjIxMDAxOTM2LCJzY2hJZCI6MTI2LCJleHBpcmVBdCI6MTYzNjkzMzI1OX0.OHJKq6FAPCA1VchhqFh8pbYO21JDXQGnnvLiRjB9sZWIiL0OJXClQbuWV8bmwvPKPldXJcwZ1w-ri6fnRQkbW71VnW_23DA7vS_2BYzaBKukYkC350571tUHkQpSBhe4MzcHcpuZ2XUBYGNGzJ3e-_iyygtEPbgB5jFIToAcuqAjBFB2TjRoneGzSeVJ-otMP5yqUufH4Fk50mowzwa4rjdGkRKNQT-rz7VMa5VLLfvJK8JDmhZo5Fq331mASOfufmtrDdzkYmDktWP9mUWE0R2Wg6c3SW8i2xiJXtmKG_5WLoLl9md_Q-ZSPJQeqols4HOrOLYU4n45dQC3FW_BdA; Hm_lpvt_7ecd21a13263a714793f376c18038a87=1636929664; SERVERID=e3fa93b0fb9e2e6d4f53273540d4e924|1636929669|1636929657')
    # book_test()
