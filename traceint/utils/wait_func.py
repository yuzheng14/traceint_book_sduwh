from typing import Tuple

from traceint.utils.request import verify_cookie, queue_init
from traceint.utils.utils import log_info, log, wait_time


def wait_for_start(cookie: str) -> Tuple[bool, bool, bool, str, str]:
    """
    等待明日预约开始时间并初始化数据
    Args:
        cookie: headers中的cookie

    Returns:
        tuple: 按顺序为cookie_ok, need_captcha, need_queue, ws_url, queue_url
    """
    if not verify_cookie(cookie):
        log_info('cookie无效，请重新输入cookie')
        return False, False, False, '', ''
    # 在开始明日预约前的1分钟确认cookie是否有效
    log('开始等待验证cookie时间')
    wait_time(12, 29)
    if not verify_cookie(cookie):
        log_info('cookie无效，请重新输入cookie')
        return False, False, False, '', ''
    else:
        log('cookie有效，请等待预定时间')

    # 等待明日预约开始
    log('开始等待预定时间')
    wait_time(12, 30)
    need_captcha, need_queue, ws_url, queue_url = queue_init(cookie)
    return True, need_captcha, need_queue, ws_url, queue_url


def wait_for_reserve(cookie: str) -> bool:
    """
    等待捡漏开始
    Args:
        cookie: headers中的cookie

    Returns:
        bool: true为cookie验证成功
    """
    if not verify_cookie(cookie):
        log_info('cookie无效，请重新输入cookie')
        return False
    # 在开始明日预约前的1分钟确认cookie是否有效
    log('开始等待验证cookie时间')
    wait_time(6, 59)
    if not verify_cookie(cookie):
        log_info('cookie无效，请重新输入cookie')
        return False
    else:
        log('cookie有效，请等待预定时间')

    # 等待明日预约开始
    log('开始等待预定时间')
    wait_time(7, 00)
    return True


def wait_to_cancel(cookie: str) -> bool:
    """
    等待退座
    Args:
        cookie: headers中的cookie

    Returns:
        true为cookie失效
    """
    if not verify_cookie(cookie):
        log_info('cookie失效，请输入有效cookie后重试')
        return False

    log('开始等待验证cookie时间')
    wait_time(22, 29)
    if not verify_cookie(cookie):
        log_info('cookie无效，请重新输入cookie')
        return False
    else:
        log_info('cookie有效，请等待预定时间')

    log('等待固定时间')

    wait_time(22, 30)
    return True
