from traceint.utils.request import is_sign
from traceint.utils.wait_func import wait_to_cancel
from traceint.utils.pass_func import pass_reserveCancle, pass_sign
from traceint.utils.utils import log


def cancel(cookie) -> bool:
    """
    退座
    Args:
        cookie: header中的cookie
    Returns:
        true为退座成功
    """
    if not wait_to_cancel(cookie):
        log("cookie失效")

    while not pass_reserveCancle(cookie):
        pass

    # 如果未签到则签到
    if not is_sign(cookie):
        log('检测到当前未签到，将自动进行签到')
        pass_sign(cookie)

    return True
