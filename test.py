from seat_book import book
from utils import post,take_seat_name,verify_cookie,wait_time,log
import json
import time
import os
import os.path
import requests

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

def wait_time_test(hour,minute):
    wait_time(hour,minute)


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

    # True
    status=verify_cookie('FROM_TYPE=weixin; v=5.5; wechatSESS_ID=d255ef050323f5af22671010049c2c1ef607a449f53974e4; Authorization=eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJ1c2VySWQiOjIxMDAxOTM2LCJzY2hJZCI6MTI2LCJleHBpcmVBdCI6MTYzNTg2NjA3MX0.Y4cvBDUU7jHFVMnFbS2m1z9W0fZ51bDdhuWed7M4KizrMXEJPTxSUMzk1TaQYTWBF1Oopd6xI9sI-CJjvbOzsah_VPfMpBxFSXsJauXzbqtQryQ4PfhsH0fDEtmE8vGnbyXh0l6vSLOQkPrQl20fZ9plMSdJcCwtVMbYvkvXPQuLE0DZDnIHWjP6J_qDJF3oLm48wjlQgLO0TBJfybvamCQCQWJgZXkG7NvltLLtW7zfOQlhnJb9bJTFGxDilSjd3skZfoU_6ZDMl5x0_f-GNvFEPA5E8RCuYxhYYlbF0WbGjh3JoAP6X3WG5_6fpEpPW1ofgcDVTDtg-pfjXsVRuw; Hm_lvt_7ecd21a13263a714793f376c18038a87=1635740940,1635776764,1635826405,1635862471; Hm_lpvt_7ecd21a13263a714793f376c18038a87=1635862471; SERVERID=d3936289adfff6c3874a2579058ac651|1635862472|1635862464')
    log(f'cookie test 1 (completed): {status}')
    status=verify_cookie('FROM_TYPE=weixin; v=5.5; wechatSESS_ID=d255ef050323f5af22671010049c2c1ef607a449f53974e4; Authorization=eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJ1c2VySWQiOjIxMDAxOTM2LCJzY2hJZCI6MTI2LCJleHBpcmVBdCI6MTYzNTg2NjA3MX0.Y4cvBDUU7jHFVMnFbS2m1z9W0fZ51bDdhuWed7M4KizrMXEJPTxSUMzk1TaQYTWBF1Oopd6xI9sI-CJjvbOzsah_VPfMpBxFSXsJauXzbqtQryQ4PfhsH0fDEtmE8vGnbyXh0l6vSLOQkPrQl20fZ9plMSdJcCwtVMbYvkvXPQuLE0DZDnIHWjP6J_qDJF3oLm48wjlQgLO0TBJfybvamCQCQWJgZXkG7NvltLLtW7zfOQlhnJb9bJTFGxDilSjd3skZfoU_6ZDMl5x0_f-GNvFEPA5E8RCuYxhYYlbF0WbGjh3JoAP6X3WG5_6fpEpPW1ofgcDVTDtg-pfjXsVRuw')
    log(f'cookie test 5 (none hm_lvt and hm_lpvt and SERVERID): {status}')
    status=verify_cookie('FROM_TYPE=weixin; v=5.5; wechatSESS_ID=d255ef050323f5af22671010049c2c1ef607a449f53974e4')
    log(f'cookie test 6 (only FROM_TPYE and v and wechatSESS_ID) :{status}')
    status=verify_cookie('wechatSESS_ID=d255ef050323f5af22671010049c2c1ef607a449f53974e4; Authorization=eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJ1c2VySWQiOjIxMDAxOTM2LCJzY2hJZCI6MTI2LCJleHBpcmVBdCI6MTYzNTg2NjA3MX0.Y4cvBDUU7jHFVMnFbS2m1z9W0fZ51bDdhuWed7M4KizrMXEJPTxSUMzk1TaQYTWBF1Oopd6xI9sI-CJjvbOzsah_VPfMpBxFSXsJauXzbqtQryQ4PfhsH0fDEtmE8vGnbyXh0l6vSLOQkPrQl20fZ9plMSdJcCwtVMbYvkvXPQuLE0DZDnIHWjP6J_qDJF3oLm48wjlQgLO0TBJfybvamCQCQWJgZXkG7NvltLLtW7zfOQlhnJb9bJTFGxDilSjd3skZfoU_6ZDMl5x0_f-GNvFEPA5E8RCuYxhYYlbF0WbGjh3JoAP6X3WG5_6fpEpPW1ofgcDVTDtg-pfjXsVRuw')
    log(f'cookie test 7 (onely wechatSESS_ID and Authorization): {status}')
    status=verify_cookie('FROM_TYPE=weixin; v=5.5; wechatSESS_ID=d255ef050323f5af22671010049c2c1ef607a449f53974e4; Hm_lvt_7ecd21a13263a714793f376c18038a87=1635740940,1635776764,1635826405,1635862471; Hm_lpvt_7ecd21a13263a714793f376c18038a87=1635862471; SERVERID=d3936289adfff6c3874a2579058ac651|1635862472|1635862464')
    log(f'cookie test 8 (none Authorization): {status}')
    status=verify_cookie('Authorization=eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJ1c2VySWQiOjIxMDAxOTM2LCJzY2hJZCI6MTI2LCJleHBpcmVBdCI6MTYzNTg2NjA3MX0.Y4cvBDUU7jHFVMnFbS2m1z9W0fZ51bDdhuWed7M4KizrMXEJPTxSUMzk1TaQYTWBF1Oopd6xI9sI-CJjvbOzsah_VPfMpBxFSXsJauXzbqtQryQ4PfhsH0fDEtmE8vGnbyXh0l6vSLOQkPrQl20fZ9plMSdJcCwtVMbYvkvXPQuLE0DZDnIHWjP6J_qDJF3oLm48wjlQgLO0TBJfybvamCQCQWJgZXkG7NvltLLtW7zfOQlhnJb9bJTFGxDilSjd3skZfoU_6ZDMl5x0_f-GNvFEPA5E8RCuYxhYYlbF0WbGjh3JoAP6X3WG5_6fpEpPW1ofgcDVTDtg-pfjXsVRuw')
    log(f'cookie test 9 (only Authorization): {status}')

def content_length_test():
    with open('json/reserve/captcha_headers.json','r') as f:
        captcha_headers=json.load(f)
    with open('json/book/10_headers.json','r') as f:
        ten_headers=json.load(f)
    with open('json/book/all_headers.json','r') as f:
        all_headers=json.load(f)
    with open('json/book/book_headers.json','r') as f:
        book_headers=json.load(f)
    with open('json/reserve/pre_10_headers.json','r') as f:
        pre_10_headers=json.load(f)
    
    # del captcha_headers['Content-Length']
    # del ten_headers['Content-Length']
    # del all_headers['Content-Length']
    # del book_headers['Content-Length']
    # del pre_10_headers['Content-Length']
    headers_dict={}
    headers_dict['captcha_headers']=captcha_headers
    headers_dict['ten_headers']=ten_headers
    headers_dict['all_headers']=all_headers
    headers_dict['book_headers']=book_headers
    headers_dict['pre_10_headers']=pre_10_headers
    # heads_list.append(captcha_headers)
    # heads_list.append(ten_headers)
    # heads_list.append(all_headers)
    # heads_list.append(book_headers)
    # heads_list.append(pre_10_headers)
    for header in headers_dict.values():
        # log(header)
        del header['Content-Length']
        del header['Cookie']

    for key1,value1 in headers_dict.items():
        for key2,value2 in headers_dict.items():
            if json.dumps(value1,separators={',',':'}) == json.dumps(value2,separators={',',':'}):
                log(f"{key1}与{key2}相同")
            else:
                log(f"{key1}与{key2}不同")
def file_append_test():
    for i in range(5):
        with open('test.out','a') as f:
            f.write(time.strftime("[%Y-%m-%d %H:%M:%S] ", time.localtime())+'\n')
    log('完毕')

def get_captcha_test():
    with open('json/reserve/captcha_resp.json','r') as f:
        resp=json.load(f)
    log(resp)

    if 'errors' not in resp:
        with open('resource/captcha/captcha-site.out','a') as f:
            f.write(json.dumps(resp['data']['userAuth']['prereserve']['captcha'])+'\n')
            log('加入网址成功')
    else:
        log(resp)
    log('时间截止')

def string_test():
    string='https://static.wechat.v2.traceint.com/template/theme2/cache/yzm/063ee37065ad6229126baca416d1ca17.jpg'
    log(string.split('/')[-1])
    code='1'
    name='2.jpg'
    string='_'.join((code,name))
    log(string)
    log(f'{string}')
    log(f"{'_'.join(('1','2'))}")
def in_test():
    alist=['1','2']
    log('1' in alist)
def get_captcha_bytes_test():
    resp=requests.get('https://static.wechat.v2.traceint.com/template/theme2/cache/yzm/10d84ba656ed060957f90bc8731d902d.jpg')
    log(resp.content)
    with open('json/reserve/captcha_resp.json','r') as f:
        resp=json.load(f)['data']['userAuth']['prereserve']['captcha']['data']
    log(resp)
    resp=requests.get(resp)
    log(resp.content)
def log_para():
    with open('json/reserve/captcha_para.json') as f:
        para=json.load(f)
    log(para)

# 测试失效cookie
# cookie_test('FROM_TYPE=weixin; v=5.5; Authorization=eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJ1c2VySWQiOjIxMDAxOTM2LCJzY2hJZCI6MTI2LCJleHBpcmVBdCI6MTYzNTU1MzUzMH0.jgq_S3qlBx44o3hqqa08DVX2i6J3V2alOXJXGUq61R0RQ3SGCJkT9c15Pl4uJ_xps4_WXEbkuW3QahMfNDvsmG-lwK-w1f9KNcV001QojJIQ6H1qfZg6wYZzhmHogSZwTK9nYbNoV6zUz-yviBf_qj4FpgfAHWWwqwNDSPaj_MlKOmsDaYzIGS9aUJKkoqKpnqh7lkAuvlW-Mkhy0_mgG-MbzqB7u07A6cUz_RhuXlW4lq_JR675lgLLEG73k_UWl7QE_ABoRFcCnEDGGsUPB6GDqNVorAXGHhC0rbpbvqIodQQDeKgj4S_TBaTMuTJza48yjMUvKiqREvKAzjDyrw; Hm_lvt_7ecd21a13263a714793f376c18038a87=1635515712,1635519596,1635546155,1635549931; Hm_lpvt_7ecd21a13263a714793f376c18038a87=1635549931; SERVERID=82967fec9605fac9a28c437e2a3ef1a4|1635549942|1635546149')
# verify_cookie_test('FROM_TYPE=weixin; v=5.5; Authorization=eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJ1c2VySWQiOjIxMDAxOTM2LCJzY2hJZCI6MTI2LCJleHBpcmVBdCI6MTYzNTU1MzUzMH0.jgq_S3qlBx44o3hqqa08DVX2i6J3V2alOXJXGUq61R0RQ3SGCJkT9c15Pl4uJ_xps4_WXEbkuW3QahMfNDvsmG-lwK-w1f9KNcV001QojJIQ6H1qfZg6wYZzhmHogSZwTK9nYbNoV6zUz-yviBf_qj4FpgfAHWWwqwNDSPaj_MlKOmsDaYzIGS9aUJKkoqKpnqh7lkAuvlW-Mkhy0_mgG-MbzqB7u07A6cUz_RhuXlW4lq_JR675lgLLEG73k_UWl7QE_ABoRFcCnEDGGsUPB6GDqNVorAXGHhC0rbpbvqIodQQDeKgj4S_TBaTMuTJza48yjMUvKiqREvKAzjDyrw; Hm_lvt_7ecd21a13263a714793f376c18038a87=1635515712,1635519596,1635546155,1635549931; Hm_lpvt_7ecd21a13263a714793f376c18038a87=1635549931; SERVERID=82967fec9605fac9a28c437e2a3ef1a4|1635549942|1635546149')
# wait_time_test(24,-16)
# log('')
# prereserve_test()
# partial_cookie_test()
# content_length_test()
# file_append_test()
# get_captcha_test()
# string_test()
# log(len('ba315bdcb30fd7f55cd8fe1d443d4024'))
# log(len(os.listdir('resource/captcha/captchas')))
# in_test()
# get_captcha_bytes_test()
log_para()