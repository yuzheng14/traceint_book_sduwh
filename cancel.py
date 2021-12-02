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
    cancel('')