from utils.request import pass_captcha, pass_queue, pass_save, wait_for_start
from utils.utils import log, log_info


# status=false时可以预定
def seat_prereserve(cookie: str, floor: int = 10, often_seat: int = 1, reverse: bool = False):
    cookie_ok, need_captcha, need_queue, ws_url, queue_url = wait_for_start(cookie)
    # TODO 根据cookie_ok更改下面行为

    # 如果没有验证验证码，则开始验证验证码
    if need_captcha:
        log('当前未验证验证码，开始验证验证码')
        ws_url = pass_captcha(cookie)
    else:
        log('已验证验证码')
    ws = pass_queue(queue_url, ws_url, need_captcha, need_queue)
    log('排队完成')

    log('开始预定座位')
    log(f"预定成功，座位为{pass_save(cookie, floor, often_seat, reverse)}号")

    if ws is not None:  # vars() locals().keys()均可
        ws.close()
        log_info('create_connection连接关闭')


if __name__ == '__main__':
    seat_prereserve('')
