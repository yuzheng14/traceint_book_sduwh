from traceint.utils.pass_func import pass_sign


def sign(cookie: str):
    """
    签到
    Args:
        cookie: headers中的cookie

    Returns:
        true 为签到成功
    """
    return pass_sign(cookie)
