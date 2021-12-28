from traceint import seat_reserve
import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="明日预约抢座脚本")
    parser.add_argument("--floor", type=int, default=10, help="楼层")
    parser.add_argument("--seat", type=int, default=1, help="座位号")
    parser.add_argument("--cookie", type=str, help="我去图书馆登录cookie")
    input_args = parser.parse_args()
    seat_reserve(input_args.cookie, input_args.floor, input_args.seat)