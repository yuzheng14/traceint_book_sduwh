from traceint.utils.request import is_sign
from traceint.utils.wait_func import wait_for_start
from traceint.utils.pass_func import pass_captcha, pass_queue, pass_save, pass_sign
from traceint.utils.utils import log, log_info


# status=false时可以预定
def seat_prereserve(cookie: str, floor: int = 10, often_seat: int = 1, reverse: bool = False)->bool:
    """
    预定座位
    Args:
        cookie: headers中的cookies
        floor: 抢座楼层
        often_seat: 常用座位
        reverse: 是否倒序
    Returns:
        true为抢座成功
    """
    # 初始化并根据cookie有效性更改
    cookie_ok, need_captcha, need_queue, ws_url, queue_url = wait_for_start(cookie)
    if not cookie_ok:
        log('cookie无效，请改正后重试')
        return False

    # 如果没有验证验证码，则开始验证验证码
    if need_captcha:
        log('当前未验证验证码，开始验证验证码')
        ws_url = pass_captcha(cookie)
    else:
        log('已验证验证码')
    # 排队
    log('开始排队')
    ws = pass_queue(queue_url, ws_url, need_captcha, need_queue)
    log('排队完成')

    log('开始预定座位')
    log(f"预定成功，座位为{pass_save(cookie, floor, often_seat, reverse)}号")

    if ws is not None:  # vars() locals().keys()均可
        ws.close()
        log_info('create_connection连接关闭')

    # 如果未签到则签到
    if not is_sign(cookie):
        log('检测到当前未签到，将自动进行签到')
        pass_sign(cookie)

    return True
