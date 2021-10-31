import requests
import json
import time

# seat_status=1为可预订


def post(post_para, headers):

    url = 'https://wechat.v2.traceint.com/index.php/graphql/'
    resp = requests.request("post", url, json=post_para, headers=headers)
    return resp


def verify_cookie(cookie):
    with open('json/book/index_headers.json') as f:
        headers = json.load(f)
    with open('json/book/index_para.json') as f:
        para = json.load(f)
    headers['Cookie'] = cookie
    resp = post(para, headers).json()
    return 'errors' not in resp


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
    while(True):
        resp = post(post_para, headers).json()
        if 'errors' in resp:
            print(resp)
            time.sleep(1)
            continue
        print("post请求成功")

        # 预定12号（常用座位）
        book_para["variables"]["seatKey"] = '19,75'
        print("开始预定12号")
        book_resp = post(book_para, book_headers).json()
        try:
            if book_resp["data"]["userAuth"]["reserve"]["reserveSeat"]:
                print("预定成功，座位为12号")
                return
        except:
            print("预定12号失败")

        seats = resp["data"]["userAuth"]["reserve"]["libs"][0]["lib_layout"]["seats"]
        seats.sort(key=take_seat_name)
        for seat in seats:
            if(seat["seat_status"] == 1):
                book_para["variables"]["seatKey"] = seat["key"]
                print(f"开始预定{seat['name']}号")
                book_resp = post(book_para, book_headers).json()
                try:
                    if book_resp["data"]["userAuth"]["reserve"]["reserveSeat"]:
                        print(f"预定成功，座位为{seat['name']}号")
                        return
                except:
                    print(f"预定{seat['name']}号失败")
                    continue
            else:
                print(f"{seat['name']}号座位无法预定")


def take_seat_name(elem):
    name = elem['name']
    if name != "" and name is not None:
        return int(elem['name'])
    return 5000


if __name__ == '__main__':
    book('FROM_TYPE=weixin; v=5.5; Hm_lvt_7ecd21a13263a714793f376c18038a87=1635546155,1635549931,1635550504,1635568036; wechatSESS_ID=a035e5e1fee15ca19b254278aedff1d20f3c9fc907607210; Authorization=eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJ1c2VySWQiOjIxMDAxOTM2LCJzY2hJZCI6MTI2LCJleHBpcmVBdCI6MTYzNTY5MjcwN30.Ez20IR5pBg0EAdZnqj-ERDSy5pxFdwnf5zUhDz4vprHbiYZj-8gfz2x7ZBqYAP0Q1AhdQc4PVpOx_PRkeFevgSqoaP7-TdZa_GWhl6D4nFZf0I_9YcaMuWdxxaNa4eGTMCV4j_MfNzaILDlJiCGg2xMYFVn3Gkpw8ODQJAg188Z4csOOIWtR4roKzrL_oJ3C0ZW2VIweyBTO_RUfn3A1A84U_IjsLwiHHkpo_nMX71xI5gT9kDiIjGtKOXbxHGjwXsNuCNtFXmvqRjuqsh79rOSVpMQZ6rNbN8BG7-08VP_x5rG4Zv5R3nWvSHJYFp3inWRCVhT9ZQPZaqpVok2p6w; SERVERID=e3fa93b0fb9e2e6d4f53273540d4e924|1635689107|1635689099')
    # book_test()
