from utils import post,verify_cookie,take_seat_name,wait_time,log
import json
import time
import ddddocr
import requests
import websocket

# status=false时可以预定
def seat_prereserve(cookie):
    if not verify_cookie(cookie):
        log('cookie无效，请重新输入cookie')
        return
    
    ocr=ddddocr.DdddOcr()

    with open('json/reserve/reserve_para.json','r') as f:
        prereserve_para=json.load(f)
    with open('json/reserve/reserve_headers.json','r') as f:
        prereserve_headers=json.load(f)
    prereserve_headers['Cookie']=cookie
    prereserve_para["variables"]["key"] = '19,75'

    with open('json/reserve/pre_10_headers.json','r') as f:
        pre_headers=json.load(f)
    with open('json/reserve/pre_10_para.json','r') as f:
        pre_para=json.load(f)
    pre_headers['Cookie']=cookie

    with open('json/reserve/verify_captcha_headers.json','r') as f:
        verify_captcha_headers=json.load(f)
    with open('json/reserve/verify_captcha_para.json','r') as f:
        verify_captcha_para=json.load(f)
    verify_captcha_headers['Cookie']=cookie

    with open('json/reserve/captcha_headers.json','r') as f:
        captcha_headers=json.load(f)
    with open('json/reserve/captcha_para.json','r') as f:
        captcha_para=json.load(f)
    captcha_headers['Cookie']=cookie

    log('开始等待预定时间')
    wait_time(12,30)
    log('尝试识别验证码')
    
    resp_captcha=post(captcha_para,captcha_headers).json()
    captcha_code=resp_captcha['data']['userAuth']['prereserve']['captcha']['code']
    captcha_website=resp_captcha['data']['userAuth']['prereserve']['captcha']['data']
    captcha=ocr.classification(requests.get(captcha_website).content)
    verify_captcha_para['variables']['captcha']=captcha
    verify_captcha_para['variables']['captchaCode']=captcha_code
    resp_verify_captcha=post(verify_captcha_para,verify_captcha_headers).json()
    while not resp_verify_captcha['data']['userAuth']['prereserve']['verifyCaptcha']:
        log(json.dumps(resp_verify_captcha,indent=4))
        log(f'{captcha_code}尝试失败，开始下一次尝试')
        resp_captcha=post(captcha_para,captcha_headers).json()
        captcha_code=resp_captcha['data']['userAuth']['prereserve']['captcha']['code']
        captcha_website=resp_captcha['data']['userAuth']['prereserve']['captcha']['data']
        captcha=ocr.classification(requests.get(captcha_website).content)
        if len(captcha) !=4:
            continue
        verify_captcha_para['variables']['captcha']=captcha
        verify_captcha_para['variables']['captchaCode']=captcha_code
        resp_verify_captcha=post(verify_captcha_para,verify_captcha_headers).json()
    log('验证码尝试成功')

    log('开始尝试连接websocket')
    # TODO:修改websocket代码
    while True:
        try:
            wss=websocket.create_connection(resp_verify_captcha['data']['data']['prereserve']['setStep1'],timeout=30)
            log('websocke连接成功')
            break
        except Exception as e:
            log(f'websocket连接失败，即将开始下一次尝试')
            log(e)
            continue

    message=wss.recv()
    while 'out' not in message:
        meessage=wss.recv()
    
    log("开始预定12号")
    prereserve_resp = post(prereserve_para, prereserve_headers).json()
    try:
        if prereserve_resp["data"]["userAuth"]["prereserve"]["save"]:
            log("预定成功，座位为12号")
            return
    except:
        log("预定12号失败")
        log(json.dumps(prereserve_resp,indent=4))
    
    log("预定12号失败")
    log(json.dumps(prereserve_resp,indent=4))

    resp=post(pre_para,pre_headers).json()
    while 'errors' in resp:
        log('请求座位失败')
        log(json.dumps(resp,indent=4))
        # time.sleep(1)
    seats = resp["data"]["userAuth"]["prereserve"]["libLayout"]["seats"]
    seats.sort(key=take_seat_name)
    for seat in seats:
        if not seat["status"]:
            prereserve_para["variables"]["key"] = seat["key"]
            log(f"开始预定{seat['name']}号")
            prereserve_resp = post(prereserve_para, prereserve_headers).json()
            try:
                if prereserve_resp["data"]["userAuth"]["prereserve"]["save"]:
                    log(f"预定成功，座位为{seat['name']}号")
                    return
                else:
                    log(f"预定{seat['name']}号失败")
                    log(json.dumps(prereserve_resp,indent=4))
            except:
                log(f"预定{seat['name']}号失败")
                log(json.dumps(prereserve_resp,indent=4))
                continue
        else:
            log(f"{seat['name']}号座位无法预定")


if __name__=='__main__':
    seat_prereserve('FROM_TYPE=weixin; v=5.5; Authorization=eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJ1c2VySWQiOjIxMDAxOTM2LCJzY2hJZCI6MTI2LCJleHBpcmVBdCI6MTYzNjYwODE1Nn0.UdiaHaYub4aNi91D9YKBnJ5LWLuSKkNyUa7nSUeuLxpFNPQl9ANWLKZAhmNj9CQSwg8a8AOtLc_5xP_AxE-xTle3gnghsxIM-H6XSs0y0VS4j2GrNuODrB_67IOfsEdmDW-NiVd_nDMxnbKJGhb5l3wDgbKFqOJWKvanDoz7D8IO6ICBx39lPRRWZGt1BTxIwuueVG6hrgQRjJilknNzUiSE-EPCjOCGmR3AYp7rE4nWvEvB6h0Z6kaoy8xiD09liEtKUn7vK3LsmRP3lqPUJ3jUylqaMYJ_hFztNLUJZ3OQr_xVaqTJQb7qfJgwRSLvUw023e_QAZw1NWY7JiMA8A; SERVERID=82967fec9605fac9a28c437e2a3ef1a4|1636604556|1636604497; Hm_lvt_7ecd21a13263a714793f376c18038a87=1636446493,1636517763,1636604485,1636604557; Hm_lpvt_7ecd21a13263a714793f376c18038a87=1636604557')