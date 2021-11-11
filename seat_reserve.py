from utils import post,verify_cookie,take_seat_name,wait_time,log
import json
import time

# status=false时可以预定
def seat_prereserve(cookie):
    if not verify_cookie(cookie):
        log('cookie无效，请重新输入cookie')
        return
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
    log('尝试发送验证码')
    log(json.dumps(verify_captcha_para,indent=4))
    resp_captcha=post(captcha_para,captcha_headers).json()
    log(json.dumps(resp_captcha,indent=4))
    resp_verify_captcha=post(verify_captcha_para,verify_captcha_headers).json()
    if  resp_verify_captcha['data']['userAuth']['prereserve']['verifyCaptcha']:
        log('直接发送验证码成功')
    else:
        log('直接发送验证码失败')
        log(json.dumps(resp_verify_captcha,indent=4))
        return
    
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
        time.sleep(1)
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
    seat_prereserve('FROM_TYPE=weixin; v=5.5; Hm_lvt_7ecd21a13263a714793f376c18038a87=1636172899,1636259364,1636432169,1636446493; wechatSESS_ID=345f9db77839a9840268254f82712e3fc3861943a041887f; Authorization=eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJ1c2VySWQiOjIxMDAxOTM2LCJzY2hJZCI6MTI2LCJleHBpcmVBdCI6MTYzNjUyMTM2Mn0.Ill8I5AovfC4wlvG8FQMdugw1cOoLimCxDyfBqJx7pR8TOSc1Q8As9vhs48j7ZmLLEaLUIIc6B7tvYZbQkC22n_DpkKUgU2igbVxQnEbp8-vgS5y01y2-YSyQEJajQPT1xoWCZEZW-WCLiGja5DQWNA3MDDad8OENJxWg4ib_5ZrZMKNzhYzXuRJScse9OtJeBxOtKCl1jhRZnCiKcOU9D8JOy8KOt5Coyu4YdE-eWhH0Z3eJJhipQYKwKqAUmr7r_gNl-MlcG-4SDR29fO7czV8jY0fdrrV0RLhQBsjOUIHxw1zZm_8MqRPC03z5NvMrAkMJwELBw0ALoYHfCvuMQ; SERVERID=b9fc7bd86d2eed91b23d7347e0ee995e|1636517761|1636517755')