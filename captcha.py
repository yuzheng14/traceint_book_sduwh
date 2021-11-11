import requests
import json
from utils import post,wait_time,log,verify_cookie
import time
import os
import ddddocr

def ocr():
    images=os.listdir('resource/captcha/captchas')
    images.sort()
    ocr=ddddocr.DdddOcr()
    for img in images:
        with open(f'resource/captcha/captchas/{img}','rb') as f:
            try:
                captcha=ocr.classification(f.read())
            except:
                log(f.read())
        with open('resource/captcha/captchas/captchas.out','a') as f:
            f.write(f'{{"name":"{img}","captcha":"{captcha}"}}\n')

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
        resp=post(captcha_para,captcha_headers)
        try:
            resp=resp.json()
        except:
            log('body无json')
            log(resp.content)
    log('时间截止')

if __name__=='__main__':
    # get_captcha('FROM_TYPE=weixin; v=5.5; Authorization=eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJ1c2VySWQiOjIxMDAxOTM2LCJzY2hJZCI6MTI2LCJleHBpcmVBdCI6MTYzNjYwODE1Nn0.UdiaHaYub4aNi91D9YKBnJ5LWLuSKkNyUa7nSUeuLxpFNPQl9ANWLKZAhmNj9CQSwg8a8AOtLc_5xP_AxE-xTle3gnghsxIM-H6XSs0y0VS4j2GrNuODrB_67IOfsEdmDW-NiVd_nDMxnbKJGhb5l3wDgbKFqOJWKvanDoz7D8IO6ICBx39lPRRWZGt1BTxIwuueVG6hrgQRjJilknNzUiSE-EPCjOCGmR3AYp7rE4nWvEvB6h0Z6kaoy8xiD09liEtKUn7vK3LsmRP3lqPUJ3jUylqaMYJ_hFztNLUJZ3OQr_xVaqTJQb7qfJgwRSLvUw023e_QAZw1NWY7JiMA8A; SERVERID=82967fec9605fac9a28c437e2a3ef1a4|1636604556|1636604497; Hm_lvt_7ecd21a13263a714793f376c18038a87=1636446493,1636517763,1636604485,1636604557; Hm_lpvt_7ecd21a13263a714793f376c18038a87=1636604557')
    # get_captcha_image()
    ocr()