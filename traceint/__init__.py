from .cancel import cancel
from .seat_book import book
from .seat_reserve import seat_prereserve
from .sign import sign


def seat_pickup(cookie: str, often_floor: int = 3, strict_mode: bool = True, reserve: bool = False) -> bool:
    """
    座位闲时捡漏，函数将等待至7点开始运行
    Args:
        cookie: headers中的cookie
        often_floor: 常用楼层
        strict_mode: 是否为严格模式，默认为true，false则为遍历全部楼层
        reserve: 是否倒序

    Returns:
        true为捡漏成功
    """
    return book(cookie, often_floor, strict_mode, reserve)


def seat_reserve(cookie: str, floor: int = 10, often_seat: int = 1, reverse: bool = False) -> bool:
    """
    明日预约抢座
    Args:
        cookie: headers中的cookies
        floor: 抢座楼层
        often_seat: 常用座位
        reverse: 是否倒序
    Returns:
        true为抢座成功
    """
    return seat_prereserve(cookie, floor, often_seat, reverse)


def seat_cancel(cookie: str) -> bool:
    """
    退座
    Args:
        cookie: headers中的cookie

    Returns:
        true为退座成功
    """
    return cancel(cookie)


def credit_sign(cookie: str) -> bool:
    """
    积分签到
    Args:
        cookie: headers中的cookie

    Returns:
        true为签到成功
    """
    return sign(cookie)
