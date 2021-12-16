import requests
from utils.utils import log
from utils.request import Activity

headers = Activity.headers.value
# resp = requests.get('https://wechat.v2.traceint.com/index.php/reserve/index.html?f=wechat', headers=headers, allow_redirects=False)
# log(resp.cookies)
# log(resp.headers)
# log(resp.request.headers)
# log(resp.url)
resp = requests.get('https://wechat.v2.traceint.com/index.php/reserve/index.html?f=wechat', headers=headers)
log(resp.cookies)
log(resp.headers)
log(resp.request.headers)
log(resp.url)
log(resp.content)
log(resp.status_code)
