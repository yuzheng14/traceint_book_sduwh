from seat_book import post,verify_cookie,take_seat_name,wait_time
import json
from log import log
import time

# status=false时可以预定
def seat_prereserve(cookie):
    if not verify_cookie(cookie):
        log('cookie无效，请重新输入cookie')
    with open('json/reserve/reserve_para.json','r') as f:
        prereserve_para=json.load(f)
    with open('json/reserve/reserve_headers.json','r') as f:
        prereserve_headers=json.load(f)
    prereserve_headers['Cookie']=cookie
    prereserve_para["variables"]["key"] = '19,75'
    log('开始等待预定时间')
    wait_time(12,30)
    log("开始预定12号")
    prereserve_resp = post(prereserve_para, prereserve_headers).json()
    try:
        if prereserve_resp["data"]["userAuth"]["prereserve"]["save"]:
            log("预定成功，座位为12号")
            return
    except:
        log("预定12号失败")
    log("预定12号失败")

    with open('pre_10_headers.json','r') as f:
        pre_headers=json.load(f)
    with open('pre_10_para.json','r') as f:
        pre_para=json.load(f)
    pre_headers['Cookie']=cookie
    
    
    resp=post(pre_para,pre_headers).json()
    while 'error' in resp:
        log('请求座位失败')
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
            except:
                log(f"预定{seat['name']}号失败")
                continue
        else:
            log(f"{seat['name']}号座位无法预定")


if __name__=='__main__':
    seat_prereserve('再说')