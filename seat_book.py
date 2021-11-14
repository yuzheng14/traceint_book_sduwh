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
    book('FROM_TYPE=weixin; v=5.5; Hm_lvt_7ecd21a13263a714793f376c18038a87=1635913724,1636000165,1636122571,1636331028; Hm_lpvt_7ecd21a13263a714793f376c18038a87=1636715350; wechatSESS_ID=07ad61e863664a12e47245cb9a969234853c420a3994e54c; Authorization=eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJ1c2VySWQiOjIxMDAxOTM2LCJzY2hJZCI6MTI2LCJleHBpcmVBdCI6MTYzNjc2MDg3N30.Dzo3RIzjtOS0AJ6n5LdB3frpLmM4mJdW6EypwapzYysgVwV_SZNx6NbxcdzLvIO6QSORZeGj-enWQzOy4GqrrjRI_bhVY9LT8Y8owrGp7QSUU3ZXJNa65lEQFUpEUo0oaDLzpgzq-NpXhWoWjCv5otbsFEEjiPKIZKF0LnGmZFfkvBQD91siNsdxdUx42GRBfFs0qRkCqmFS4kxH_lORYgAEDsY8d6fxpj-Z8VCRzSp7rSr_mCvmHVbZ2VQr0N_CFmbVnanEtL7KYcXzNRcOiIOMBP4p928C14HBs8vv2G8cuATvyTXTQOXtALSxgMpXckpRJwATDexuHLuqiAmRZA; SERVERID=b9fc7bd86d2eed91b23d7347e0ee995e|1636757279|1636757276')
    # book_test()
