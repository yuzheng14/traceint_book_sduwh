import json

from com.yuzheng14.traceint.utils.request import get_SToken, post, verify_cookie
from com.yuzheng14.traceint.utils.utils import log, wait_time, log_info


def cancel(cookie):
    if not verify_cookie(cookie):
        log('cookie失效，请输入有效cookie后重试')
        return

    with open('../../../json/cancel/cancel_para.json', 'r') as f:
        cancel_para = json.load(f)
    with open('../../../json/cancel/cancel_header.json', 'r') as f:
        cancel_header = json.load(f)
    cancel_header['Cookie'] = cookie

    log('开始等待验证cookie时间')
    wait_time(22, 29)
    if not verify_cookie(cookie):
        log('cookie无效，请重新输入cookie')
        return
    else:
        log('cookie有效，请等待预定时间')

    log('等待固定时间')

    wait_time(22, 30)

    s_token = get_SToken(cookie)
    cancel_para['variables']['sToken'] = s_token
    cancel_resp = post(cancel_para, cancel_header)
    log_info(_json=cancel_resp.json())


if __name__ == '__main__':
    cancel('')
