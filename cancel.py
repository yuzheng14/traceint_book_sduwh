from utils import get_SToken,verify_cookie,log,wait_time,post,log_json
import json

def cancel(cookie):
    if( not verify_cookie(cookie)):
        log('cookie失效，请输入有效cookie后重试')
        return
    
    with open('json/cancel/cancel_para.json','r') as f:
        cancel_para=json.load(f)
    with open('json/cancel/cancel_header.json','r') as f:
        cancel_header=json.load(f)
    cancel_header['Cookie']=cookie

    log('开始等待验证cookie时间')
    wait_time(22,29)
    if not verify_cookie(cookie):
        log('cookie无效，请重新输入cookie')
        return
    else:
        log('cookie有效，请等待预定时间')

    log('等待固定时间')
    
    wait_time(22,30)

    s_token=get_SToken(cookie)
    cancel_para['variables']['sToken']=s_token
    cancel_resp=post(cancel_para,cancel_header)
    log_json(cancel_resp.json())

if __name__=='__main__':
    cancel('FROM_TYPE=weixin; v=5.5; Hm_lvt_7ecd21a13263a714793f376c18038a87=1637287316,1637418775,1637850891,1637985992; wechatSESS_ID=c3d3ade2792a77ce559f5b82ba2e16fed8471fcad1aab490; SERVERID=b9fc7bd86d2eed91b23d7347e0ee995e|1638022237|1638022236; Authorization=eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJ1c2VySWQiOjIxMDAxOTM2LCJzY2hJZCI6MTI2LCJleHBpcmVBdCI6MTYzODAyNTgzN30.o7K3KCZ5pEIBZEZXiypJXvrhieM1u3JSrm6OfvcUvvlZP0nuvq-BRIfwA7gyAM-5_D-LlPAo1Tndir6VlA9q_-9YnYkNB236j-6-Psk9_FDMMZ3RjbYvkQOpzX_9v8WAqMhOs_-TwtyNBgzDIph9_RkwHYoG9UiNT2UaatC-0YWTe-YOUJsBKQAnnETe-VW-VXA3F8-NwWVRVpxAJTX2r9R_eF51I0RhOG7zSzNqBVLjXJNhgDEpIfI3ruXZAqyxig0uV5hdDGKMhK547_nftzhTFA15pbXLOWElvhQRR_HLYvjS10EztPb-HQ37CyA5qlRYxGXFzGtudx3qkUjpxQ; Hm_lpvt_7ecd21a13263a714793f376c18038a87=1638022237')