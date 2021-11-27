from utils import get_SToken,verify_cookie,log,wait_time,post,log_json

def cancel(cookie):
    if( not verify_cookie(cookie)):
        log('cookie失效，请输入有效cookie后重试')
        return
    
    with open('json/cancel/cancel_para.json','r') as f:
        cancel_para=f.read()
    with open('json/cancel/cancel_header.json','r') as f:
        cancel_header=f.read()
    cancel_header['Cookie']=cookie

    wait_time(22,30)
    cancel_resp=post(cancel_para,cancel_header)
    log_json(cancel_resp.json())