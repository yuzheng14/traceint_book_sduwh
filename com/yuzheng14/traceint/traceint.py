from com.yuzheng14.traceint.main_func.cancel import cancel
from com.yuzheng14.traceint.main_func.seat_book import book
from com.yuzheng14.traceint.main_func.seat_reserve import seat_prereserve


def seat_pickup(cookie: str, often_floor: int = 3, strict_mode: bool = True, reserve: bool = False):
    book(cookie, often_floor, strict_mode, reserve)


def seat_reserve(cookie: str, floor: int = 10, often_seat: int = 1, reverse: bool = False):
    seat_prereserve(cookie, floor, often_seat, reverse)


def seat_cancel(cookie: str):
    cancel(cookie)
