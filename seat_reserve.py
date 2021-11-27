from utils import post,verify_cookie,take_seat_name,wait_time,log,on_close,on_error,on_message,save_unrecognized_image,save_recognized_image
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

    log('开始等待验证cookie时间')
    wait_time(12,29)
    if not verify_cookie(cookie):
        log('cookie无效，请重新输入cookie')
        return
    else:
        log('cookie有效，请等待预定时间')

    log('开始等待预定时间')
    wait_time(12,30)
    try:
        resp_get_end_time=post(get_end_time_para,get_end_time_headers).json()
        if resp_get_end_time['data']['userAuth']['prereserve']['getStep'] ==0:

            log('尝试识别验证码')
            resp_captcha=post(captcha_para,captcha_headers).json()
            captcha_code=resp_captcha['data']['userAuth']['prereserve']['captcha']['code']
            captcha_website=resp_captcha['data']['userAuth']['prereserve']['captcha']['data']
            image_byte=requests.get(captcha_website).content

            captcha=ocr.classification(image_byte)
            log(f'识别验证码为{captcha}')

            verify_captcha_para['variables']['captcha']=captcha
            verify_captcha_para['variables']['captchaCode']=captcha_code
            resp_verify_captcha=post(verify_captcha_para,verify_captcha_headers).json()

            while not resp_verify_captcha['data']['userAuth']['prereserve']['verifyCaptcha']:

                log(f'{captcha_code}尝试失败，保存验证码图片后开始下一次尝试')
                save_unrecognized_image(image_byte,'_'.join((captcha_code,captcha_website.split('/')[-1])))

                resp_captcha=post(captcha_para,captcha_headers).json()
                captcha_code=resp_captcha['data']['userAuth']['prereserve']['captcha']['code']
                captcha_website=resp_captcha['data']['userAuth']['prereserve']['captcha']['data']

                image_byte=requests.get(captcha_website).content
                captcha=ocr.classification(image_byte)

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

    # TODO:修改为若排队未完成且排队人数为-1且超出时间则一直连接wss连接
    try:
        try:
            wss_url=resp_verify_captcha['data']['userAuth']['prereserve']['setStep1']
        except:
            wss_url=resp_get_end_time['data']['userAuth']['prereserve']['queeUrl']
        log(f'wss连接地址{wss_url}')
        wss=websocket.create_connection(wss_url,timeout=30)
        log('create_connection连接成功')
    except Exception as e:
        log(f'create_connection连接异常')
        traceback.print_exc()

    # TODO 此处改为更通用的写法
    resp_queue=requests.get('https://wechat.v2.traceint.com/quee/success?sid=21001936&schId=126&t=13b1b5fbc10742ac0fd0a0ff510ea917')
    queue_num=int(resp_queue.content)
    log(f'前方排队{queue_num}人')
    
    while queue_num >0:
        log(f'前方排队{queue_num}人')
        if queue_num >100:
            time.sleep(2)
        # TODO 此处改为更通用的写法
        resp_queue=requests.get('https://wechat.v2.traceint.com/quee/success?sid=21001936&schId=126&t=13b1b5fbc10742ac0fd0a0ff510ea917')
        queue_num=int(resp_queue.content)
    log(f'前方排队{queue_num}人')
    log('排队完成')

    resp=post(pre_para,pre_headers).json()
    while 'errors' in resp:
        log('请求座位失败')
        log(json.dumps(resp,indent=4,ensure_ascii=False))
        
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
                    break
                else:
                    log(f"预定{seat['name']}号失败")
                    log(json.dumps(prereserve_resp,indent=4,ensure_ascii=False))
            except:
                log(f"预定{seat['name']}号失败")
                log(json.dumps(prereserve_resp,indent=4,ensure_ascii=False))
                continue
        else:
            log(f"{seat['name']}号座位已有人")

    # 查看排队数据，已增强系统精准性
    resp_queue=requests.get('https://wechat.v2.traceint.com/quee/success?sid=21001936&schId=126&t=13b1b5fbc10742ac0fd0a0ff510ea917')
    queue_num=int(resp_queue.content)
    
    if 'wss' in dir(): # vars() locals().keys()均可
        wss.close()
        log('create_connection连接关闭')
    if 'image_byte' in dir():
        log('开始写入验证码图片')
        save_recognized_image(image_byte,'_'.join((captcha,captcha_code,captcha_website.split('/')[-1])))

if __name__=='__main__':
    seat_prereserve('FROM_TYPE=weixin; v=5.5; Hm_lvt_7ecd21a13263a714793f376c18038a87=1636950371,1637209490,1637287316,1637418775; wechatSESS_ID=ad316af26f39204b06b9dbbace48d2cfdd1a025177ae5e38; Authorization=eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJ1c2VySWQiOjIxMDAxOTM2LCJzY2hJZCI6MTI2LCJleHBpcmVBdCI6MTYzNzQ3MTk4MH0.PXvW0JPBbzyuet895fJ8HQNBvRkmjQzzDrs44TEuK_ikmA33VWwzdNerplQZB4Fmy1Djs4Pcz8bm35yxELOH4w0bRch6XsibMzSZKJ9YQv-hyG0n9wF_b92T9e6dP7m-eCfjD_tPFHwYXhAHvOsbnUOeL2PLFdQXDYrpAmkUUdG7HjBgXNGKlg4TylWKdvh2U8Tg3UT4-6H06C1LnhQDu3Bz7YgfNWzRj8axgh4rG2LIMrWT71CRbgkNjrtIXnuwdVvuQEJFIMuovTSSMaA0dTRWjUonef5LeoYz39W480Uo8iahHM2Aw9Ay0vxXmkU4BM8TrBly-77XUsMguFTFMQ; SERVERID=b9fc7bd86d2eed91b23d7347e0ee995e|1637468380|1637468378; Hm_lpvt_7ecd21a13263a714793f376c18038a87=1637468381')