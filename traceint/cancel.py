from traceint.utils.wait_func import wait_to_cancel
from traceint.utils.pass_func import pass_reserveCancle
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
    return True
