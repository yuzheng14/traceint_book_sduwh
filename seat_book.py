import time

from utils.request import wait_for_reserve, have_seat, pass_reserve
from utils.utils import log


# seat_status=1为可预订
def book(cookie: str, often_floor: int = 3, strict_mode: bool = True, reserve: bool = False):
    """
    闲时捡漏
    Args:
        cookie: headers中的cookie
        often_floor: 常用楼层
        strict_mode: 是否为严格模式，默认为true，false则为遍历全部楼层
        reserve: 是否倒序
    """
    # 验证cookie并等待开始抢座
    if not wait_for_reserve(cookie):
        log('cookie无效，请改正后重试')
        return

    # 循环遍历抢座
    while True and not have_seat():
        pass_reserve(cookie, often_floor, strict_mode, reserve)
        time.sleep(2)


if __name__ == '__main__':
    cookie = ''
    book(cookie)
    # book_test()
