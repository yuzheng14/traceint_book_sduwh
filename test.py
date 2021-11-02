from seat_book import book,post,take_seat_name,verify_cookie
import json
import time
from log import log

def cookie_test(cookie):
    with open('json/book/10_para.json', 'r') as f:
        post_para = json.load(f)
    with open('json/book/10_headers.json','r') as f:
        headers=json.load(f)
    headers['Cookie']=cookie
    resp=post(post_para,headers).json()
    print(resp)

def book_test():
    with open('json/book/book_para.json','r') as f:
        book_para=json.load(f)
    with open('json/book/10_resp.json','r') as f:
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

def verify_cookie_test(cookie):
    print(verify_cookie(cookie))

def wait_time(hour,minute):
    time_to_wait=hour*60+minute
    while time.localtime().tm_hour*60+time.localtime().tm_min < time_to_wait:
        pass
def prereserve_test():
    with open('json/reserve/reserve_para.json','r') as f:
        prereserve_para=json.load(f)
    with open('json/reserve/pre_10_resp.json','r') as f:
        pre_10_resp=json.load(f)
    with open('json/reserve/reserve_resp.json','r') as f:
        represerve_resp=json.load(f)
    log('开始等待预定时间')
    wait_time(10,50)
    while 'error' in represerve_resp:
        log('请求座位失败')
        time.sleep(1)
    seats = pre_10_resp["data"]["userAuth"]["prereserve"]["libLayout"]["seats"]
    seats.sort(key=take_seat_name)
    for seat in seats:
        if not seat["status"]:
            prereserve_para["variables"]["key"] = seat["key"]
            log(f"开始预定{seat['name']}号")
            log(prereserve_para)
            try:
                if represerve_resp["data"]["userAuth"]["prereserve"]["save"]:
                    log(f"预定成功，座位为{seat['name']}号")
                    return
            except:
                log(f"预定{seat['name']}号失败")
                continue
        else:
            log(f"{seat['name']}号座位无法预定")
def partial_cookie_test():
    status=verify_cookie("FROM_TYPE=weixin; v=5.5; wechatSESS_ID=9339df68de0e05c90c28bec5e452336dd1d902e4a38fc7d0; Authorization=eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJ1c2VySWQiOjIxMDAxOTM2LCJzY2hJZCI6MTI2LCJleHBpcmVBdCI6MTYzNTgzMDAwNH0.M0HCiKFvNEnKejfF8WemOhUHYDRS9MG6Bb7xsWwfy30D40LCVlDHXUVDOfFZLnnra60Vdg6ilfHbmZqsqUXugMEes1swqUpXoXa54M9uiEl6qidIK960FJCSo18qH894e3pUL0nOBeClfvKLblWJ_qyPiw0Ffr8_7qfbh2zRosHqNawoJHmFgLrSL6qvbjkGtQ16TlVruy5AZSvQlXmx919PJOESoShBKxBBPpr5dJC4k09bwnxdX_dVzWuSdKxXT8nKTBCjL1mqA6-fKIeGFaZUL6wxpgq2URku-1XLUtO2DtX9nNkWvjU2-iaHKVLxTly1cI3tEdYB-Uq3TQDHCg; SERVERID=82967fec9605fac9a28c437e2a3ef1a4|1635826406|1635826398; Hm_lvt_7ecd21a13263a714793f376c18038a87=1635689109,1635740940,1635776764,1635826405; Hm_lpvt_7ecd21a13263a714793f376c18038a87=1635826405")
    log(f"cookie test 1 (complete): {status}")
    status=verify_cookie('FROM_TYPE=weixin; v=5.5; wechatSESS_ID=9339df68de0e05c90c28bec5e452336dd1d902e4a38fc7d0; Authorization=eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJ1c2VySWQiOjIxMDAxOTM2LCJzY2hJZCI6MTI2LCJleHBpcmVBdCI6MTYzNTgzMDAwNH0.M0HCiKFvNEnKejfF8WemOhUHYDRS9MG6Bb7xsWwfy30D40LCVlDHXUVDOfFZLnnra60Vdg6ilfHbmZqsqUXugMEes1swqUpXoXa54M9uiEl6qidIK960FJCSo18qH894e3pUL0nOBeClfvKLblWJ_qyPiw0Ffr8_7qfbh2zRosHqNawoJHmFgLrSL6qvbjkGtQ16TlVruy5AZSvQlXmx919PJOESoShBKxBBPpr5dJC4k09bwnxdX_dVzWuSdKxXT8nKTBCjL1mqA6-fKIeGFaZUL6wxpgq2URku-1XLUtO2DtX9nNkWvjU2-iaHKVLxTly1cI3tEdYB-Uq3TQDHCg; SERVERID=82967fec9605fac9a28c437e2a3ef1a4|1635826406|1635826398; Hm_lvt_7ecd21a13263a714793f376c18038a87=1635689109,1635740940,1635776764,1635826405; Hm_lpvt_7ecd21a13263a714793f376c18038a87=1635826405')
    log(f'cookie test 2 (none hm_lvt): {status}')
    status=verify_cookie('FROM_TYPE=weixin; v=5.5; wechatSESS_ID=9339df68de0e05c90c28bec5e452336dd1d902e4a38fc7d0; Authorization=eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJ1c2VySWQiOjIxMDAxOTM2LCJzY2hJZCI6MTI2LCJleHBpcmVBdCI6MTYzNTgzMDAwNH0.M0HCiKFvNEnKejfF8WemOhUHYDRS9MG6Bb7xsWwfy30D40LCVlDHXUVDOfFZLnnra60Vdg6ilfHbmZqsqUXugMEes1swqUpXoXa54M9uiEl6qidIK960FJCSo18qH894e3pUL0nOBeClfvKLblWJ_qyPiw0Ffr8_7qfbh2zRosHqNawoJHmFgLrSL6qvbjkGtQ16TlVruy5AZSvQlXmx919PJOESoShBKxBBPpr5dJC4k09bwnxdX_dVzWuSdKxXT8nKTBCjL1mqA6-fKIeGFaZUL6wxpgq2URku-1XLUtO2DtX9nNkWvjU2-iaHKVLxTly1cI3tEdYB-Uq3TQDHCg; SERVERID=82967fec9605fac9a28c437e2a3ef1a4|1635826406|1635826398; Hm_lvt_7ecd21a13263a714793f376c18038a87=1635689109,1635740940,1635776764,1635826405')
    log(f'cookie test 3 (none hm_lpvt): {status}')
    status=verify_cookie('FROM_TYPE=weixin; v=5.5; wechatSESS_ID=9339df68de0e05c90c28bec5e452336dd1d902e4a38fc7d0; Authorization=eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJ1c2VySWQiOjIxMDAxOTM2LCJzY2hJZCI6MTI2LCJleHBpcmVBdCI6MTYzNTgzMDAwNH0.M0HCiKFvNEnKejfF8WemOhUHYDRS9MG6Bb7xsWwfy30D40LCVlDHXUVDOfFZLnnra60Vdg6ilfHbmZqsqUXugMEes1swqUpXoXa54M9uiEl6qidIK960FJCSo18qH894e3pUL0nOBeClfvKLblWJ_qyPiw0Ffr8_7qfbh2zRosHqNawoJHmFgLrSL6qvbjkGtQ16TlVruy5AZSvQlXmx919PJOESoShBKxBBPpr5dJC4k09bwnxdX_dVzWuSdKxXT8nKTBCjL1mqA6-fKIeGFaZUL6wxpgq2URku-1XLUtO2DtX9nNkWvjU2-iaHKVLxTly1cI3tEdYB-Uq3TQDHCg; SERVERID=82967fec9605fac9a28c437e2a3ef1a4|1635826406|1635826398')
    log(f'cookie test 4 (none hm_lvt and hm_lpvt): {status}')

    # True
    status=verify_cookie('FROM_TYPE=weixin; v=5.5; wechatSESS_ID=9339df68de0e05c90c28bec5e452336dd1d902e4a38fc7d0; Authorization=eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJ1c2VySWQiOjIxMDAxOTM2LCJzY2hJZCI6MTI2LCJleHBpcmVBdCI6MTYzNTgzMDAwNH0.M0HCiKFvNEnKejfF8WemOhUHYDRS9MG6Bb7xsWwfy30D40LCVlDHXUVDOfFZLnnra60Vdg6ilfHbmZqsqUXugMEes1swqUpXoXa54M9uiEl6qidIK960FJCSo18qH894e3pUL0nOBeClfvKLblWJ_qyPiw0Ffr8_7qfbh2zRosHqNawoJHmFgLrSL6qvbjkGtQ16TlVruy5AZSvQlXmx919PJOESoShBKxBBPpr5dJC4k09bwnxdX_dVzWuSdKxXT8nKTBCjL1mqA6-fKIeGFaZUL6wxpgq2URku-1XLUtO2DtX9nNkWvjU2-iaHKVLxTly1cI3tEdYB-Uq3TQDHCg')
    log(f'cookie test 5 (none hm_lvt and hm_lpvt and SERVERID): {status}')
    status=verify_cookie('FROM_TYPE=weixin; v=5.5; wechatSESS_ID=9339df68de0e05c90c28bec5e452336dd1d902e4a38fc7d0')
    log(f'cookie test 6 (only FROM_TPYE and v and wechatSESS_ID) :{status}')


# 测试失效cookie
# cookie_test('FROM_TYPE=weixin; v=5.5; Authorization=eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJ1c2VySWQiOjIxMDAxOTM2LCJzY2hJZCI6MTI2LCJleHBpcmVBdCI6MTYzNTU1MzUzMH0.jgq_S3qlBx44o3hqqa08DVX2i6J3V2alOXJXGUq61R0RQ3SGCJkT9c15Pl4uJ_xps4_WXEbkuW3QahMfNDvsmG-lwK-w1f9KNcV001QojJIQ6H1qfZg6wYZzhmHogSZwTK9nYbNoV6zUz-yviBf_qj4FpgfAHWWwqwNDSPaj_MlKOmsDaYzIGS9aUJKkoqKpnqh7lkAuvlW-Mkhy0_mgG-MbzqB7u07A6cUz_RhuXlW4lq_JR675lgLLEG73k_UWl7QE_ABoRFcCnEDGGsUPB6GDqNVorAXGHhC0rbpbvqIodQQDeKgj4S_TBaTMuTJza48yjMUvKiqREvKAzjDyrw; Hm_lvt_7ecd21a13263a714793f376c18038a87=1635515712,1635519596,1635546155,1635549931; Hm_lpvt_7ecd21a13263a714793f376c18038a87=1635549931; SERVERID=82967fec9605fac9a28c437e2a3ef1a4|1635549942|1635546149')
# verify_cookie_test('FROM_TYPE=weixin; v=5.5; Authorization=eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJ1c2VySWQiOjIxMDAxOTM2LCJzY2hJZCI6MTI2LCJleHBpcmVBdCI6MTYzNTU1MzUzMH0.jgq_S3qlBx44o3hqqa08DVX2i6J3V2alOXJXGUq61R0RQ3SGCJkT9c15Pl4uJ_xps4_WXEbkuW3QahMfNDvsmG-lwK-w1f9KNcV001QojJIQ6H1qfZg6wYZzhmHogSZwTK9nYbNoV6zUz-yviBf_qj4FpgfAHWWwqwNDSPaj_MlKOmsDaYzIGS9aUJKkoqKpnqh7lkAuvlW-Mkhy0_mgG-MbzqB7u07A6cUz_RhuXlW4lq_JR675lgLLEG73k_UWl7QE_ABoRFcCnEDGGsUPB6GDqNVorAXGHhC0rbpbvqIodQQDeKgj4S_TBaTMuTJza48yjMUvKiqREvKAzjDyrw; Hm_lvt_7ecd21a13263a714793f376c18038a87=1635515712,1635519596,1635546155,1635549931; Hm_lpvt_7ecd21a13263a714793f376c18038a87=1635549931; SERVERID=82967fec9605fac9a28c437e2a3ef1a4|1635549942|1635546149')
# wait_time(23,50)
# prereserve_test()
partial_cookie_test()