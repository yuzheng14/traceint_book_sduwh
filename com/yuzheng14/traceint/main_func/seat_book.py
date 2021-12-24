import time

from com.yuzheng14.traceint.utils.utils import log
from com.yuzheng14.traceint.utils.request import wait_for_reserve, have_seat, pass_reserve


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
    while True and not have_seat(cookie):
        pass_reserve(cookie, often_floor, strict_mode, reserve)
        time.sleep(2)


if __name__ == '__main__':
    cookie = '; '.join(['FROM_TYPE=weixin',
                        'v=5.5',
                        'wechatSESS_ID=b5c65bfe59c857f9ffaf0dba50b38aa5577205aaa4816a97',
                        'Authorization=eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJ1c2VySWQiOjIzNTcyMTQ0LCJzY2hJZCI6MTI2LCJleHBpcmVBdCI6MTY0MDMwNzU2NH0.EKEqLVI1AMfQ8yhoNaubgtdSHzx4nW0huJYVAjqYRfuJZYVt_pCObbjpP-SGicch5Td9o45C3uw-L_CqYNDP7oMslC5niny63thETUdw565OAcjiJkt5iu_mJHe97Bdwuf7AAtGCG3z6jqRM318AanBPiu4qYh5nckiN8KfxqGcw9vSz71T689_caV0jtgG3IB3hsZU57fGkjURL0Mf2M8Npizq9hhGzdFdlRu5PmbtD4ByV5W3rkfiAGUsLarsmjAb0XPYxjkfo4It_9-6rvxyHWC6DcWK7xN9n_VrNsxmoYEZWd1HnxMiDP__cCYhGiM37ZJLN_vNIy4mcdsAkGA',
                        'SERVERID=e3fa93b0fb9e2e6d4f53273540d4e924|1640303549|1640303517',
                        'Hm_lvt_7ecd21a13263a714793f376c18038a87=1640182666',
                        'Hm_lpvt_7ecd21a13263a714793f376c18038a87=1640303537'])
    book(cookie, 5)
    # book_test()
