import requests
import json
from utils.utils import log
from utils.request import Activity


def dispose_json(_json):
    return json.loads(str(resp.request.headers).replace("'", '"'))


headers = Activity.headers.value
headers['Cookie'] = 'FROM_TYPE=weixin; v=5.5; Hm_lvt_7ecd21a13263a714793f376c18038a87=1638590314; wechatSESS_ID=acd56330154697ffc964552e73de519d6a5a94251ffe9378; Authorization=eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJ1c2VySWQiOjEwMDg2MjMsInNjaElkIjoxMjYsImV4cGlyZUF0IjoxNjM5MDk5MTM1fQ.cTQJe09lK_ecrH5pFm_MmADxX-bGu2Uw1dLBTvbT_GCKKwmk9henq9BGEjUSwzR2BQi82LSFnMIXnVT4lh0Zi4DOWdtY9lX9f0pdcYLhXv7iwERL_O1RAQhwFSilGgRryjF5f1R46h6IznyGUmZQ7cuJV67SZrxFDwe45wcePhHWVFdJ7rKgiug-QeZWVSNRdmKqkfbvrZZE_3eCbwrq2RmsR4KMQ8j7FXgda9ZHDaS8Zt7wC6UjzwFvpgkJ7yG6-SepH2l29qTJJvHvM9rWVW5O9Vj1-oVF5_dy5sO51XclmAQFILaceFHpHKt7Quxvy-J6kX4jscwIJcJug4Q1Rg; Hm_lpvt_7ecd21a13263a714793f376c18038a87=1639095818; SERVERID=d3936289adfff6c3874a2579058ac651|1639096044|1639095527'
# resp = requests.get('https://wechat.v2.traceint.com/index.php/reserve/index.html?f=wechat', headers=headers, allow_redirects=False)
# log(resp.cookies)
# log(resp.headers)
# log(resp.request.headers)
# log(resp.url)
resp = requests.get('https://wechat.v2.traceint.com/index.php/reserve/index.html?f=wechat', headers=headers)
log(resp.cookies)
log(_json=dispose_json(resp.headers))
log(_json=dispose_json(resp.request.headers))
log(resp.url)
log(resp.content)
log(resp.status_code)
log(dispose_json(resp.history[0].cookies))
