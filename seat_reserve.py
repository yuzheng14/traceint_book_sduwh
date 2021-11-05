from seat_book import post,verify_cookie,take_seat_name,wait_time
import json
from log import log
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
        log(prereserve_resp)
    
    log("预定12号失败")
    log(prereserve_resp)

    with open('json/reserve/pre_10_headers.json','r') as f:
        pre_headers=json.load(f)
    with open('json/reserve/pre_10_para.json','r') as f:
        pre_para=json.load(f)
    pre_headers['Cookie']=cookie
    
    
    resp=post(pre_para,pre_headers).json()
    while 'error' in resp:
        log('请求座位失败')
        log(resp)
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
                    log(prereserve_resp)
            except:
                log(f"预定{seat['name']}号失败")
                log(prereserve_resp)
                continue
        else:
            log(f"{seat['name']}号座位无法预定")


if __name__=='__main__':
    seat_prereserve('FROM_TYPE=weixin; v=5.5; Hm_lvt_7ecd21a13263a714793f376c18038a87=1635826405,1635862471,1635913594,1636000027; wechatSESS_ID=bdf45042cc7568920a9a8810ebafc4e2f4d582ed5759e7fd; Authorization=eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJ1c2VySWQiOjIxMDAxOTM2LCJzY2hJZCI6MTI2LCJleHBpcmVBdCI6MTYzNjA4OTY0MX0.U2V8UAqEZVSSTMrLdpTaM_8b7Ad3yIBeVuSSGQRYgBbua4gi7k19MVyow0rbuj3zob7g407H1FNLAQRuBhZsCtQ6pscPIHs-s0xGq181WgxsapHm_JFioEfTQF_8-Qoxggg_s56xFRF8DmMAfHMd2Ub-vK7fud0pnWRJW7ba1CoPUOJsM_tbU1G1z9iaigWwr88ooAjOMk70q92cKQkeqy67adkm3v-jhAOmZV5U_J-ga1rB-htYbpmcTWkd95UmOIryGwQCH9RMTDNkK2F1aZlrZzsaUXWJ1KNz-MrMXSkDRqhzrtLQgcOXUCkhQ5TKrEAZPYmYIHs7Gk98mcJoxw; SERVERID=82967fec9605fac9a28c437e2a3ef1a4|1636086041|1636086035')