import requests
import json
import time

# seat_status=1为可预订


def post(post_para, headers):

    url = 'https://wechat.v2.traceint.com/index.php/graphql/'
    resp = requests.request("post", url, json=post_para, headers=headers)
    return resp

def book(cookie):
    with open('10_para.json', 'r') as f:
        post_para = json.load(f)
    with open('10_headers.json','r') as f:
        headers=json.load(f)
    headers['Cookie']=cookie
    with open('book_para.json','r') as f:
        book_para=json.load(f)
    with open('book_headers.json','r') as f:
        book_headers=json.load(f)
    book_headers['Cookie']=headers['Cookie']
    while(True):
        resp=post(post_para,headers).json()
        if 'errors' in resp:
            print(resp)
            time.sleep(1)
            continue
        print("post请求成功")
        seats=resp["data"]["userAuth"]["reserve"]["libs"][0]["lib_layout"]["seats"]
        seats.sort(key=take_seat_name)
        for seat in seats:
            if(seat["seat_status"]==1):
                book_para["variables"]["seatKey"]=seat["key"]
                print(f"开始预定{seat['name']}号")
                book_resp=post(book_para,book_headers)
                try:
                    if book_resp["data"]["userAuth"]["reserve"]["reserveSeat"] :
                        print(f"预定成功，座位为{seat['name']}号")
                        return
                except:
                    print("预定失败")
                    continue
            else:
                print(f"{seat['name']}号座位无法预定")
        

def book_test():
    with open('book_para.json','r') as f:
        book_para=json.load(f)
    with open('10_resp.json','r') as f:
        resp=json.load(f)

    if 'errors' not in resp:
        seats=resp["data"]["userAuth"]["reserve"]["libs"][0]["lib_layout"]["seats"]
        seats.sort(key=take_seat_name)
        while True:
            for seat in seats:
                if(seat["seat_status"]==1):
                    book_para["variables"]["seatKey"]=seat["key"]
                    print(book_para)
                    try:
                        print(f"预定成功，座位为{seat['name']}号")
                        return
                    except:
                        continue
def take_seat_name(elem):
    name=elem['name']
    if name != "" and name is not None:
        return int(elem['name'])
    return 5000

if __name__ == '__main__':
    book('FROM_TYPE=weixin; v=5.5; Authorization=eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJ1c2VySWQiOjIxMDAxOTM2LCJzY2hJZCI6MTI2LCJleHBpcmVBdCI6MTYzNTU1MzUzMH0.jgq_S3qlBx44o3hqqa08DVX2i6J3V2alOXJXGUq61R0RQ3SGCJkT9c15Pl4uJ_xps4_WXEbkuW3QahMfNDvsmG-lwK-w1f9KNcV001QojJIQ6H1qfZg6wYZzhmHogSZwTK9nYbNoV6zUz-yviBf_qj4FpgfAHWWwqwNDSPaj_MlKOmsDaYzIGS9aUJKkoqKpnqh7lkAuvlW-Mkhy0_mgG-MbzqB7u07A6cUz_RhuXlW4lq_JR675lgLLEG73k_UWl7QE_ABoRFcCnEDGGsUPB6GDqNVorAXGHhC0rbpbvqIodQQDeKgj4S_TBaTMuTJza48yjMUvKiqREvKAzjDyrw; Hm_lvt_7ecd21a13263a714793f376c18038a87=1635515712,1635519596,1635546155,1635549931; Hm_lpvt_7ecd21a13263a714793f376c18038a87=1635549931; SERVERID=82967fec9605fac9a28c437e2a3ef1a4|1635549942|1635546149')