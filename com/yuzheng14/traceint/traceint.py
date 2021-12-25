from com.yuzheng14.traceint.main_func.cancel import cancel
from com.yuzheng14.traceint.main_func.seat_book import book
from com.yuzheng14.traceint.main_func.seat_reserve import seat_prereserve


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
