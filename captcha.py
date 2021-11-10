import requests
import json
from utils import post,wait_time,log,verify_cookie
import time
import os

def ocr():
    # 打开一张验证码图片
    with open("./resource/captcha/jfem.jpg", "rb") as f:
        img_bytes = f.read()
    # 步骤 1

    import time
    start=time.time()
    import ddddocr

    ocr=ddddocr.DdddOcr()



    text=ocr.classification(img_bytes)
    print(text)
    print(time.time()-start)

def get_captcha_image():
    images=os.listdir('resource/captcha/captchas')
    with open('resource/captcha/captcha-site.out','r') as f:
        count=0
        for line in f:
            data=json.loads(line)
            code=data['code']
            url=data['data']
            name=url.split('/')[-1]
            file_name="_".join((code,name))
            if  file_name in images:
                count=count+1
                log(f'{code}已存在,当前已有{count}个')
                continue
            try:
                resp=requests.get(url)
                with open(f'resource/captcha/captchas/{file_name}','wb') as image:
                    image.write(resp.content)
                count=count+1
                log(f'{code}已写入,当前已有{count}个')
            except:
                count=count+1
                log(f'{code}写入失败,当前已有{count}个')

def get_captcha(cookie):
    with open('json/reserve/get_end_time_headers.json','r') as f:
        get_end_time_headers=json.load(f)
    with open('json/reserve/get_end_time_para.json','r') as f:
        get_end_time_para=json.load(f)
    get_end_time_headers['Cookie']=cookie

    with open('json/reserve/captcha_headers.json','r') as f:
        captcha_headers=json.load(f)
    with open('json/reserve/captcha_para.json','r') as f:
        captcha_para=json.load(f)
    captcha_headers['Cookie']=cookie

    if not verify_cookie(cookie):
        log('cookie无效，请更新后重试')
        return
    
    log('开始等待预定时间')
    wait_time(12,30)
    
    
    resp_end_time=post(get_end_time_para,get_end_time_headers)
    log(resp_end_time)
    end_time=resp_end_time.json()['data']['userAuth']['prereserve']['endTime']

    resp=post(captcha_para,captcha_headers)
    try:
        resp=resp.json()
    except:
        log('body无json')
        log(resp.content)
        return
    
    number=0
    # while(time.time()<end_time ):
    while(True):
        if 'errors' not in resp:
            with open('resource/captcha/captcha-site.out','a') as f:
                f.write(json.dumps(resp['data']['userAuth']['prereserve']['captcha'])+'\n')
                number=number+1
                log(f'加入网址成功，当前已有{number}条')
        else:
            log(resp)
        resp=post(captcha_para,captcha_headers).json()
    log('时间截止')

if __name__=='__main__':
    # get_captcha('FROM_TYPE=weixin; v=5.5; Hm_lvt_7ecd21a13263a714793f376c18038a87=1636172899,1636259364,1636432169,1636446493; wechatSESS_ID=345f9db77839a9840268254f82712e3fc3861943a041887f; Authorization=eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJ1c2VySWQiOjIxMDAxOTM2LCJzY2hJZCI6MTI2LCJleHBpcmVBdCI6MTYzNjUyMTM2Mn0.Ill8I5AovfC4wlvG8FQMdugw1cOoLimCxDyfBqJx7pR8TOSc1Q8As9vhs48j7ZmLLEaLUIIc6B7tvYZbQkC22n_DpkKUgU2igbVxQnEbp8-vgS5y01y2-YSyQEJajQPT1xoWCZEZW-WCLiGja5DQWNA3MDDad8OENJxWg4ib_5ZrZMKNzhYzXuRJScse9OtJeBxOtKCl1jhRZnCiKcOU9D8JOy8KOt5Coyu4YdE-eWhH0Z3eJJhipQYKwKqAUmr7r_gNl-MlcG-4SDR29fO7czV8jY0fdrrV0RLhQBsjOUIHxw1zZm_8MqRPC03z5NvMrAkMJwELBw0ALoYHfCvuMQ; SERVERID=b9fc7bd86d2eed91b23d7347e0ee995e|1636517761|1636517755')
    get_captcha_image()