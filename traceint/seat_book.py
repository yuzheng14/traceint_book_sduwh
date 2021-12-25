import time

from traceint.utils.request import have_seat, is_sign
from traceint.utils.wait_func import wait_for_reserve
from traceint.utils.pass_func import pass_reserve, pass_sign
from traceint.utils.utils import log


# seat_status=1为可预订
def book(cookie: str, often_floor: int = 3, strict_mode: bool = True, reserve: bool = False) -> bool:
    """
    闲时捡漏
    Args:
        cookie: headers中的cookie
        often_floor: 常用楼层
        strict_mode: 是否为严格模式，默认为true，false则为遍历全部楼层
        reserve: 是否倒序
    Returns:
        true为捡漏成功
    """
    # 验证cookie并等待开始抢座
    if not wait_for_reserve(cookie):
        log('cookie无效，请改正后重试')
        return False

    # 循环遍历抢座
    while True and not have_seat(cookie):
        seat = pass_reserve(cookie, often_floor, strict_mode, reserve)
        if seat != '':
            log(f'预定成功，座位为{seat}号')
            return True
        time.sleep(2)

    # 如果未签到则签到
    if not is_sign(cookie):
        log('检测到当前未签到，将自动进行签到')
        pass_sign(cookie)

    if have_seat(cookie):
        return True
    return False
