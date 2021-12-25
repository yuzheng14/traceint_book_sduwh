from com.yuzheng14.traceint.utils.request import pass_reserveCancle, wait_to_cancel
from com.yuzheng14.traceint.utils.utils import log


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
    return True
