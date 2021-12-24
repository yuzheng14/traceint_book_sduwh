import json

from com.yuzheng14.traceint.utils.request import get_SToken, post, verify_cookie, reserveCancle, pass_to_cancel
from com.yuzheng14.traceint.utils.utils import log, wait_time, log_info


# TODO restructure
def cancel(cookie):
    """
    退座
    Args:
        cookie: header中的cookie
    """
    if not pass_to_cancel(cookie):
        log("cookie失效")

    while not reserveCancle(cookie):
        pass
