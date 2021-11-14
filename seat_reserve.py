from utils import post,verify_cookie,take_seat_name,wait_time,log,on_close,on_error,on_message
import json
import time
import ddddocr
import requests
import websocket
import traceback

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
    prereserve_para["variables"]["key"] = '31,74'

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

    with open('json/reserve/get_end_time_headers.json','r') as f:
        get_end_time_headers=json.load(f)
    with open('json/reserve/get_end_time_para.json','r') as f:
        get_end_time_para=json.load(f)
    get_end_time_headers['Cookie']=cookie

    log('开始等待预定时间')
    wait_time(12,30)
    try:
        resp_get_end_time=post(get_end_time_para,get_end_time_headers).json()
        if resp_get_end_time['data']['userAuth']['prereserve']['getStep'] ==0:
            log('尝试识别验证码')
            resp_captcha=post(captcha_para,captcha_headers).json()
            captcha_code=resp_captcha['data']['userAuth']['prereserve']['captcha']['code']
            captcha_website=resp_captcha['data']['userAuth']['prereserve']['captcha']['data']
            captcha=ocr.classification(requests.get(captcha_website).content)
            log(f'识别验证码为{captcha}')
            verify_captcha_para['variables']['captcha']=captcha
            verify_captcha_para['variables']['captchaCode']=captcha_code
            resp_verify_captcha=post(verify_captcha_para,verify_captcha_headers).json()
            while not resp_verify_captcha['data']['userAuth']['prereserve']['verifyCaptcha']:
                log(json.dumps(resp_verify_captcha,indent=4,ensure_ascii=False))
                log(f'{captcha_code}尝试失败，开始下一次尝试')
                resp_captcha=post(captcha_para,captcha_headers).json()
                captcha_code=resp_captcha['data']['userAuth']['prereserve']['captcha']['code']
                captcha_website=resp_captcha['data']['userAuth']['prereserve']['captcha']['data']
                captcha=ocr.classification(requests.get(captcha_website).content)
                log(f'识别验证码为{captcha}')
                verify_captcha_para['variables']['captcha']=captcha
                verify_captcha_para['variables']['captchaCode']=captcha_code
                resp_verify_captcha=post(verify_captcha_para,verify_captcha_headers).json()
            log(f'验证码尝试成功，验证码为{captcha}')
            log(json.dumps(resp_verify_captcha,indent=4,ensure_ascii=False))
        else:
            log('已验证验证码')
    except Exception as e:
        log(f'错误')
        traceback.print_exc()
    
    resp_get_end_time=post(get_end_time_para,get_end_time_headers).json()
    if resp_get_end_time['data']['userAuth']['prereserve']['getStep'] ==1:
        log('确认验证captcha成功')
    else:
        log('确认验证captcha失败')

    

    # log('开始尝试连接websocket')
    # TODO:修改websocket代码
    try:
        wss=websocket.create_connection(resp_get_end_time['data']['userAuth']['prereserve']['queeUrl'],timeout=30)
        log('websocke连接成功')
        message=wss.recv()
        wss.close()
    except Exception as e:
        log(f'websocket连接失败')
        traceback.print_exc()

    try:
        wss=websocket.WebSocketApp('wss://wechat.v2.traceint.com/quee/quee?sid=21001936&schId=126&in=3kQ5&time=1636000215&t=b832ed9029ca3e1a1f3e2328770de52f',
            header={'User-Agent: Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36 NetType/WIFI MicroMessenger/7.0.20.1781(0x6700143B) WindowsWechat(0x63040026)',f'Cookie: {cookie}'},
            cookie=cookie,
            on_message=on_message,
            on_close=on_close,
            on_error=on_error)
        wss.run_forever()
    except:
        log('websocketApp连接失败')
        traceback.print_exc()
    
    # log(message)
    # while 'out' not in message:
    #     meessage=wss.recv()
    time.sleep(1)
    resp_queue=requests.get('https://wechat.v2.traceint.com/quee/success?sid=21001936&schId=126&t=13b1b5fbc10742ac0fd0a0ff510ea917')
    log(f'前方排队{int(resp_queue.content)}人')
    while int(resp_queue.content) >0:
        log(f'前方排队{int(resp_queue.content)}人')
        resp_queue=requests.get('https://wechat.v2.traceint.com/quee/success?sid=21001936&schId=126&t=13b1b5fbc10742ac0fd0a0ff510ea917')

    log('排队完成')
    
    log("开始预定23号")
    prereserve_resp = post(prereserve_para, prereserve_headers).json()
    try:
        if prereserve_resp["data"]["userAuth"]["prereserve"]["save"]:
            log("预定成功，座位为23号")
            return
    except:
        log("预定23号异常")
        log(json.dumps(prereserve_resp,indent=4,ensure_ascii=False))
        traceback.print_exc()
    
    log("预定23号失败")
    log(json.dumps(prereserve_resp,indent=4,ensure_ascii=False))

    resp=post(pre_para,pre_headers).json()
    while 'errors' in resp:
        log('请求座位失败')
        log(json.dumps(resp,indent=4,ensure_ascii=False))
        # time.sleep(1)
    seats = resp["data"]["userAuth"]["prereserve"]["libLayout"]["seats"]
    seats.sort(key=take_seat_name)
    for seat in seats:
        if seat['name']==""or seat['name']==None:
            log("该座位不存在")
            continue
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
                    log(json.dumps(prereserve_resp,indent=4,ensure_ascii=False))
            except:
                log(f"预定{seat['name']}号失败")
                log(json.dumps(prereserve_resp,indent=4,ensure_ascii=False))
                continue
        else:
            log(f"{seat['name']}号座位已有人")


if __name__=='__main__':
    seat_prereserve('FROM_TYPE=weixin; v=5.5; Hm_lvt_7ecd21a13263a714793f376c18038a87=1636000165,1636122571,1636331028,1636863912; wechatSESS_ID=83bedebe9da0ad065a3ecd05719526f3937735f39ceb6fc7; Authorization=eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJ1c2VySWQiOjIxMDAxOTM2LCJzY2hJZCI6MTI2LCJleHBpcmVBdCI6MTYzNjg3MTMxNn0.V0MDtEaPuyuk-1qwBMkAe42g3BW_lbVADGpxNZhf1UUUZvBAH8Xjr4AnYeh0vUDVL3zrWVLmA6Xh2ysqDJigFn3nYEk5musPYOpvOybjmG-GisccpLPfge_Aq16Z6VR7hPguHe73mDlt5nOyIq1ZIP9MNa6xsO6_PTUJsZ7PEgJgS14ngzVTKq78R30iIEhV-wGymQapkLP9ohmGjKr-Vx4eyMJN11amkIn4HkYqrC4fjFwpWyKzrzd1W835nt2yfQQ2_ihjXTVesW_ddriPyrLB4LzFbdh1C3ZwIdXZ728ZdoSvY1p66vT-ccItaco5tDiOFTTLJx4fbJmBMT_9wQ; Hm_lpvt_7ecd21a13263a714793f376c18038a87=1636867716; SERVERID=d3936289adfff6c3874a2579058ac651|1636867785|1636867714')