import requests
import json
from utils import post,wait_time,log,verify_cookie
import time

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

def get_captcha(cookie):
    wait_time(12,30)
    if not verify_cookie(cookie):
        log('cookie无效，请更新后重试')
    with open('json/reserve/get_end_time_headers.json','r') as f:
        get_end_time_headers=json.load(f)
    with open('json/reserve/get_end_time_para.json','r') as f:
        get_end_time_para=json.load(f)
    get_end_time_headers['Cookie']=cookie
    resp_end_time=post(get_end_time_para,get_end_time_headers)
    log(resp_end_time)
    end_time=resp_end_time.json()['data']['userAuth']['prereserve']['endTime']

    with open('json/reserve/captcha_headers.json','r') as f:
        captcha_headers=json.load(f)
    with open('json/reserve/captcha_para.json','r') as f:
        captcha_para=json.load(f)
    captcha_headers['Cookie']=cookie
    resp=post(captcha_para,captcha_headers).json()
    log(resp)
    number=0
    while(time.time()<end_time ):
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
    get_captcha('')