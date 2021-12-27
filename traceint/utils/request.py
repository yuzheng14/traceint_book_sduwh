import traceback
from enum import Enum
from typing import List, Optional

import requests

from traceint.utils.utils import log_info, seat_exist, get_lib_id, log, queue_delay


def have_seat(cookie: str) -> bool:
    """
    判断当前是否有座位
    Args:
        cookie: headers中的cookie

    Returns:
        true为有座位
    """
    resp = get_resp(Activity.index, cookie)
    try:
        resp = resp.json()
        return resp['data']['userAuth']['reserve']['reserve'] is not None
    except ValueError as value_exc:
        log_info('\n' + traceback.format_exc())
        log_info("have_seat时无json")
        log_info(resp.content)
        raise value_exc
    except Exception as e:
        log_info('\n' + traceback.format_exc())
        log_info("have_seat时发生其他异常")
        raise e


def is_sign(cookie: str) -> bool:
    """
    是否签到
    Args:
        cookie: headers中的cookie

    Returns:
        true为已经签到
    """
    task = get_task(cookie)
    while task is None:
        task = get_task(cookie)
    return task['status'] == 2


class Activity(Enum):
    headers = {"Host": "wechat.v2.traceint.com", "Connection": "keep-alive", "Origin": "https://web.traceint.com",
               "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36 NetType/WIFI MicroMessenger/7.0.20.1781(0x6700143B) WindowsWechat(0x63040026)",
               "Content-Type": "application/json", "Accept": "*/*", "Sec-Fetch-Site": "same-site",
               "Sec-Fetch-Mode": "cors", "Sec-Fetch-Dest": "empty",
               "Referer": "https://web.traceint.com/web/index.html", "Accept-Encoding": "gzip, deflate, br",
               "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7"}
    captcha = {"operationName": "getStep0",
               "query": "query getStep0 {\n userAuth {\n prereserve {\n getNum\n captcha {\n code\n data\n }\n }\n }\n}"}
    getStep = {"operationName": "getStep",
               "query": "query getStep {\n userAuth {\n prereserve {\n getStep\n queeUrl\n successUrl\n endTime\n }\n }\n}"}
    prereserveLibLayout = {"operationName": "libLayout",
                           "query": "query libLayout($libId: Int!) {\n userAuth {\n prereserve {\n libLayout(libId: $libId) {\n max_x\n max_y\n seats_booking\n seats_total\n seats_used\n seats {\n key\n name\n seat_status\n status\n type\n x\n y\n }\n }\n }\n }\n}",
                           "variables": {"libId": None}}
    index = {"operationName": "index",
             "query": "query index($pos: String!, $param: [hash]) {\n userAuth {\n oftenseat {\n list {\n id\n info\n lib_id\n seat_key\n status\n }\n }\n message {\n new(from: \"system\") {\n has\n from_user\n title\n num\n }\n indexMsg {\n message_id\n title\n content\n isread\n isused\n from_user\n create_time\n }\n }\n reserve {\n reserve {\n token\n status\n user_id\n user_nick\n sch_name\n lib_id\n lib_name\n lib_floor\n seat_key\n seat_name\n date\n exp_date\n exp_date_str\n validate_date\n hold_date\n diff\n diff_str\n mark_source\n isRecordUser\n isChooseSeat\n isRecord\n mistakeNum\n openTime\n threshold\n daynum\n mistakeNum\n closeTime\n timerange\n forbidQrValid\n renewTimeNext\n forbidRenewTime\n forbidWechatCancle\n }\n getSToken\n }\n currentUser {\n user_id\n user_nick\n user_mobile\n user_sex\n user_sch_id\n user_sch\n user_last_login\n user_avatar(size: MIDDLE)\n user_adate\n user_student_no\n user_student_name\n area_name\n user_deny {\n deny_deadline\n }\n sch {\n sch_id\n sch_name\n activityUrl\n isShowCommon\n isBusy\n }\n }\n }\n ad(pos: $pos, param: $param) {\n name\n pic\n url\n }\n}",
             "variables": {"pos": "App-首页"}}
    verify_captcha = {"operationName": "setStep1",
                      "query": "mutation setStep1($captcha: String!, $captchaCode: String!) {\n userAuth {\n prereserve {\n verifyCaptcha(captcha: $captcha, code: $captchaCode)\n setStep1\n }\n }\n}",
                      "variables": {"captcha": "wvsb", "captchaCode": "ba315bdcb30fd7f55cd8fe1d443d4024"}}
    save = {"operationName": "save",
            "query": "mutation save($key: String!, $libid: Int!, $captchaCode: String, $captcha: String) {\n userAuth {\n prereserve {\n save(key: $key, libId: $libid, captcha: $captcha, captchaCode: $captchaCode)\n }\n }\n}",
            "variables": {
                "key": "19,75",
                "libid": 758,
                "captchaCode": "",
                "captcha": ""
            }}
    libLayout = {
        "operationName": "libLayout",
        "query": "query libLayout($libId: Int, $libType: Int) {\n userAuth {\n reserve {\n libs(libType: $libType, libId: $libId) {\n lib_id\n is_open\n lib_floor\n lib_name\n lib_type\n lib_layout {\n seats_total\n seats_booking\n seats_used\n max_x\n max_y\n seats {\n x\n y\n key\n type\n name\n seat_status\n status\n }\n }\n }\n }\n }\n}",
        "variables": {
            "libId": 765
        }
    }
    reserveSeat = {
        "operationName": "reserveSeat",
        "query": "mutation reserveSeat($libId: Int!, $seatKey: String!, $captchaCode: String, $captcha: String!) {\n userAuth {\n reserve {\n reserveSeat(\n libId: $libId\n seatKey: $seatKey\n captchaCode: $captchaCode\n captcha: $captcha\n )\n }\n }\n}",
        "variables": {
            "seatKey": "27,74",
            "libId": 765,
            "captchaCode": "",
            "captcha": ""
        }
    }
    reserveCancle = {
        "operationName": "pass_reserveCancle",
        "query": "mutation pass_reserveCancle($sToken: String!) {\n userAuth {\n reserve {\n pass_reserveCancle(sToken: $sToken) {\n timerange\n img\n hours\n mins\n per\n }\n }\n }\n}",
        "variables": {
            "sToken": "c4902bd615587a0f73d24573d083d24f09f10aa6"
        }
    }
    getList = {
        "operationName": "getList",
        "query": "query getList {\n userAuth {\n credit {\n tasks {\n id\n task_id\n task_name\n task_info\n task_url\n credit_num\n contents\n conditions\n task_type\n status\n }\n staticTasks {\n id\n name\n task_type_name\n credit_num\n contents\n button\n }\n }\n }\n}"
    }
    done = {
        "operationName": "done",
        "query": "mutation done($user_task_id: Int!) {\n userAuth {\n credit {\n done(user_task_id: $user_task_id)\n }\n }\n}",
        "variables": {
            "user_task_id": 39265747
        }
    }


def post(post_para: dict, headers: dict) -> requests.Response:
    """对图书馆接口发送post请求

    Args:
        post_para (list(json)): 要发送的json数据
        headers (dict): headers参数
    """

    url = 'https://wechat.v2.traceint.com/index.php/graphql/'
    resp = requests.request("post", url, json=post_para, headers=headers)
    return resp


def get_para_and_headers(activity: Activity, cookie: str) -> tuple:
    """获取该项活动的json参数和headers

    Args:
        activity (Activity): 活动enum
        cookie (str): 传入cookie

    Returns:
        tuple: 返回json参数和headers组成的元组
    """

    headers = Activity.headers.value
    headers['Cookie'] = cookie

    return activity.value, headers


def get_resp(activity: Activity, cookie: str) -> requests.Response:
    """通过传入的活动获取response

    Args:
        activity (Activity): 活动enum
        cookie (str): 传入cookie

    Returns:
        requests.Response: 返回的response
    """
    para, headers = get_para_and_headers(activity, cookie)
    return post(para, headers)


def get_step_response(cookie: str) -> requests.Response:
    """获取getStep的响应

    Args:
        cookie (str): headers中的cookie

    Returns:
        requests.Response: 返回响应
    """
    return get_resp(Activity.getStep, cookie)


def get_step(cookie: str) -> int:
    """获取getStep

    Args:
        cookie (str): headers中的cookie

    Raises:
        value_exc: 无json
        key_exc: json无数据
        type_exc: json中含有空对象
        e: 其他异常

    Returns:
        int: getStep
    """
    resp = get_step_response(cookie)
    try:
        resp = resp.json()
        result = resp['data']['userAuth']['prereserve']['getStep']
    except ValueError as value_exc:
        log_info('\n' + traceback.format_exc())
        log_info("get_step时无json")
        log_info(resp.content)
        raise value_exc
    except KeyError as key_exc:
        log_info('\n' + traceback.format_exc())
        log_info("get_step时json中无code及网址")
        log_info(_json=resp)
        raise key_exc
    except TypeError as type_exc:
        log_info('\n' + traceback.format_exc())
        log_info('get_step时json中有None对象，疑似cookie过期')
        log_info(_json=resp)
        raise type_exc
    except Exception as e:
        log_info('\n' + traceback.format_exc())
        log_info("get_step时发生其他异常")
        raise e
    return result


def get_prereserve_libLayout(cookie: str, lib_id: int) -> list:
    """通过libId获取该层图书馆的座位信息

    Args:
        cookie (str): headers中的cookie
        lib_id (int): 图书馆楼层id

    Raises:
        value_exc: 无json
        key_exc: json无数据
        e: 其他异常

    Returns:
        list: 座位信息list
    """
    para, headers = get_para_and_headers(Activity.prereserveLibLayout, cookie)
    para['variables']['libId'] = lib_id

    resp = post(para, headers)
    try:
        resp = resp.json()
        result = resp["data"]["userAuth"]["prereserve"]["libLayout"]["seats"]
    except ValueError as value_exc:
        log_info('\n' + traceback.format_exc())
        log_info("get_prereserve_libLayout时无json")
        log_info(resp.content)
        raise value_exc
    except KeyError as key_exc:
        log_info('\n' + traceback.format_exc())
        log_info("get_prereserve_libLayout时无json无数据")
        log_info(resp)
        raise key_exc
    except Exception as e:
        log_info('\n' + traceback.format_exc())
        log_info("get_prereserve_libLayout时发生其他异常")
        raise e
    return [seat for seat in result if seat_exist(seat)]


def verify_cookie(cookie: str) -> bool:
    """验证cookie有效性

    Args:
        cookie (str): headers中的cookie参数

    Raises:
        e: 响应无json

    Returns:
        bool: true则cookie有效
    """
    resp = get_resp(Activity.index, cookie)
    try:
        resp = resp.json()
    except ValueError as value_exc:
        log_info('\n' + traceback.format_exc())
        log_info("verify_cookie时无json")
        log_info(resp.content)
        raise value_exc
    except Exception as e:
        log_info('\n' + traceback.format_exc())
        log_info("verify_cookie时发生其他异常")
        raise e
    return 'errors' not in resp


def get_SToken(cookie: str) -> str:
    """获取退座所需要的SToken

    Args:
        cookie (str): headers中的cookie参数

    Raises:
        key_exc: json无对应键值
        value_exc: 响应无json
        e: 其他异常

    Returns:
        str: 退座所需要的SToken
    """
    resp = get_resp(Activity.index, cookie)
    try:
        resp = resp.json()
        result = resp['data']['userAuth']['reserve']['getSToken']
    except KeyError as key_exc:
        log_info('\n' + traceback.format_exc())
        log_info("get_SToken时无所需数据")
        log_info(_json=resp)
        raise key_exc
    except ValueError as value_exc:
        log_info('\n' + traceback.format_exc())
        log_info("get_SToken时无json")
        log_info(resp.content)
        raise value_exc
    except Exception as e:
        log_info('\n' + traceback.format_exc())
        log_info("get_SToken时发生其他异常")
        raise e
    return result


def get_ws_url(cookie: str) -> str:
    """获取websocket链接地址（通常在程序崩溃时重新运行时获取）

    Args:
        cookie (str): headers中的cookie参数

    Raises:
        value_exc: 无json
        key_exc: json无数据
        e: 其他异常

    Returns:
        str: websocket地址
    """
    resp = get_step_response(cookie)
    try:
        resp = resp.json()
        result = resp['data']['userAuth']['prereserve']['queeUrl']
    except ValueError as value_exc:
        log_info('\n' + traceback.format_exc())
        log_info("get_ws_url时无json")
        log_info(resp.content)
        raise value_exc
    except KeyError as key_exc:
        log_info('\n' + traceback.format_exc())
        log_info("get_ws_url时json中无所需数据")
        log_info(_json=resp)
        raise key_exc
    except Exception as e:
        log_info('\n' + traceback.format_exc())
        log_info("get_ws_url时发生其他错误")
        raise e
    return result


def get_queue_url(cookie: str) -> str:
    """获取排队的get连接

    Args:
        cookie (str): headers中的cookie参数

    Raises:
        value_exc: 无json
        key_exc: json无数据
        e: 其他异常

    Returns:
        str: 排队的get连接
    """
    resp = get_step_response(cookie)
    try:
        resp = resp.json()
        result = resp['data']['userAuth']['prereserve']['successUrl']
    except ValueError as value_exc:
        log_info('\n' + traceback.format_exc())
        log_info("get_queue_url时无json")
        log_info(resp.content)
        raise value_exc
    except KeyError as key_exc:
        log_info('\n' + traceback.format_exc())
        log_info("get_queue_url时json中无所需数据")
        log_info(_json=resp)
        raise key_exc
    except Exception as e:
        log_info('\n' + traceback.format_exc())
        log_info("get_queue_url时发生其他异常")
        raise e
    return result


def get_captcha_code_website(cookie: str) -> tuple:
    """获取验证码的code和网址

    Args:
        cookie (str): headers的cookie

    Raises:
        value_exc: 无json
        key_exc: json数据
        e: 其他异常

    Returns:
        tuple: 返回元组，第一个元素为code(后面发送验证请求会用到)，第二个元素为网址
    """
    resp = get_resp(Activity.captcha, cookie)

    try:
        resp = resp.json()
        result = (resp['data']['userAuth']['prereserve']['captcha']['code'],
                  resp['data']['userAuth']['prereserve']['captcha']['data'])
    except ValueError as value_exc:
        log_info('\n' + traceback.format_exc())
        log_info("get_captcha_code_website时无json")
        log_info(resp.content)
        raise value_exc
    except KeyError as key_exc:
        log_info('\n' + traceback.format_exc())
        log_info("get_captcha_code_website时json中无code及网址")
        log_info(_json=resp)
        raise key_exc
    except Exception as e:
        log_info('\n' + traceback.format_exc())
        log_info("get_captcha_code_website时发生其他异常")
        raise e

    return result


def get_captcha_image(website: str) -> bytes:
    """根据网址获取验证码图片二进制信息

    Args:
        website (str): 验证码网址

    Raises:
        Exception: 图片地址404

    Returns:
        bytes: 图片二进制信息
    """
    resp = requests.get(website)
    if resp.status_code != 404:
        return resp.content
    else:
        log_info('图片地址404')
        raise Exception("get_captcha_image时404 Not Found")


def verify_captcha(cookie: str, captcha: str, code: str) -> tuple:
    """验证验证码是否正确，返回结果以及websocket的url

    Args:
        cookie (str): headers的cookie
        captcha (str): 识别出来的验证码
        code (str): 验证码的code（前面post请求得到的）

    Raises:
        value_exc: 无json
        key_exc: json无数据
        e: 其他异常

    Returns:
        tuple: 第一个元素为bool型，验证是否成功；第二个元素为str，websocket的url
    """
    para, headers = get_para_and_headers(Activity.verify_captcha, cookie)
    para['variables']['captcha'] = captcha
    para['variables']['captchaCode'] = code
    resp = post(para, headers)
    ws_url = None

    try:
        resp = resp.json()
        verify_result = resp['data']['userAuth']['prereserve']['verifyCaptcha']
        if verify_result:
            ws_url = resp['data']['userAuth']['prereserve']['setStep1']
    except ValueError as value_exc:
        log_info('\n' + traceback.format_exc())
        log_info("verify_captcha时无json")
        log_info(resp.content)
        raise value_exc
    except KeyError as key_exc:
        log_info('\n' + traceback.format_exc())
        log_info("verify_captcha时json中无code及网址")
        log_info(_json=resp)
        raise key_exc
    except Exception as e:
        log_info('\n' + traceback.format_exc())
        log_info("verify_captcha时发生其他异常")
        raise e

    return verify_result, ws_url


def save(cookie: str, key: str, lib_id: int) -> bool:
    """
    预定座位
    Args:
        cookie: headers中的cookie
        key: 座位key，seat字典中获取
        lib_id: 楼层id

    Returns:
        true为预定成功
    """
    para, headers = get_para_and_headers(Activity.save, cookie)
    para["variables"]["key"] = key
    para['variables']['libid'] = lib_id
    resp = post(para, headers)
    try:
        resp = resp.json()
        # 如果服务器排队有延迟则再预定一次
        # TODO 测试延迟
        if queue_delay(resp):
            log_info('save时服务器有延迟,即将再试一次')
            log_info(_json=resp)
            resp = post(para, headers)
            resp = resp.json()
        if 'errors' in resp:
            log_info('save时json数据内含错误或预定失败')
            log_info(_json=resp)
            return False
        return resp["data"]["userAuth"]["prereserve"]["save"]
    except ValueError as value_exc:
        log_info('\n' + traceback.format_exc())
        log_info("save时无json")
        log_info(resp.content)
        raise value_exc
    except KeyError as key_exc:
        log_info('\n' + traceback.format_exc())
        log_info("save时json无对应数据")
        log_info(_json=resp)
        raise key_exc
    except Exception as e:
        log_info('\n' + traceback.format_exc())
        log_info("save时发生其他异常")
        log_info(resp)
        log_info(resp.content)
        raise e


def get_libLayout(cookie: str, lib_id: int) -> List[dict]:
    """
    获取捡漏座位信息
    Args:
        cookie: headers中的cookie
        lib_id: 图书馆楼层id

    Returns:
        List[dict]: 座位信息list
    """
    para, headers = get_para_and_headers(Activity.libLayout, cookie)
    para['variables']['libId'] = lib_id

    resp = post(para, headers)
    try:
        resp = resp.json()
        result = resp["data"]["userAuth"]["reserve"]["libs"][0]["lib_layout"]["seats"]
    except ValueError as value_exc:
        log_info('\n' + traceback.format_exc())
        log_info("get_libLayout时无json")
        log_info(resp.content)
        raise value_exc
    except KeyError as key_exc:
        log_info('\n' + traceback.format_exc())
        log_info("get_libLayout时无json无数据")
        log_info(resp)
        raise key_exc
    except Exception as e:
        log_info('\n' + traceback.format_exc())
        log_info("get_libLayout时发生其他异常")
        raise e
    return [seat for seat in result if seat_exist(seat)]


def reserveSeat(cookie: str, seat_key: str, lib_id: int) -> bool:
    """
    预定当日座位
    Args:
        cookie: headers中的cookie
        seat_key: 座位id，seat信息中
        lib_id: 楼层id

    Returns:
        true为预定成功
    """
    para, headers = get_para_and_headers(Activity.reserveSeat, cookie)
    para["variables"]["seatKey"] = seat_key
    para['variables']['libId'] = lib_id
    resp = post(para, headers)
    try:
        resp = resp.json()
        if 'errors' in resp:
            log_info('reserveSeat时json数据内含错误或预定失败')
            log_info(_json=resp)
            return False
        return resp["data"]["userAuth"]["reserve"]["reserveSeat"]
    except ValueError as value_exc:
        log_info('\n' + traceback.format_exc())
        log_info("reserveSeat时无json")
        log_info(resp.content)
        raise value_exc
    except KeyError as key_exc:
        log_info('\n' + traceback.format_exc())
        log_info("reserveSeat时json无对应数据")
        log_info(_json=resp)
        raise key_exc
    except Exception as e:
        log_info('\n' + traceback.format_exc())
        log_info("reserveSeat时发生其他异常")
        log_info(resp)
        log_info(resp.content)
        raise e


def reserve_floor(cookie: str, floor: int, reverse: bool) -> str:
    """
    遍历一整层楼的座位，预定空座位
    Args:
        cookie: headers中的cookie
        floor: 楼层
        reverse: 是否倒序

    Returns:
        成功则返回座位号，否则返回空字符串
    """
    lib_id = get_lib_id(floor)
    seats = get_libLayout(cookie, lib_id)
    seats.sort(key=lambda s: int(s['name']), reverse=reverse)
    log_info(f'开始遍历{floor}楼')
    for seat in seats:
        if seat["seat_status"] == 1:
            log_info(f"开始预定{seat['name']}号")
            try:
                if reserveSeat(cookie, seat['key'], lib_id):
                    log_info(f"预定成功，座位为{seat['name']}号")
                    return seat['name']
            except Exception:
                log_info(f'预定{seat["name"]}时发生错误')
                return ''
    return ''


# TODO doc注释
# TODO 完善函数
# TODO 未拆封微信浏览器之前无法完善
def renew_cookie(cookie: str) -> str:
    if verify_cookie(cookie):
        log('当前验证码有效，无需更新')
        return cookie
    pass
    return cookie


def queue_init(cookie: str) -> tuple:
    """初始化排队并获取need_captcha, need_queue, ws_url, queue_url

    Args:
        cookie (str): header参数cookie

    Raises:
        value_exc: 无json
        key_exc: json无数据
        e: 其他异常

    Returns:
        tuple: 按顺序分别为need_captcha, need_queue, ws_url, queue_url
    """
    resp = get_step_response(cookie)
    try:
        resp = resp.json()
        get_step = resp['data']['userAuth']['prereserve']['getStep']
        ws_url = resp['data']['userAuth']['prereserve']['queeUrl']
        queue_url = resp['data']['userAuth']['prereserve']['successUrl']
        if get_step == 0:
            need_captcha = True
        else:
            need_captcha = False
        if get_step == 1:
            need_queue = True
        else:
            need_queue = False
    except ValueError as value_exc:
        log_info('\n' + traceback.format_exc())
        log_info("queue_init时无json")
        log_info(resp.content)
        raise value_exc
    except KeyError as key_exc:
        log_info('\n' + traceback.format_exc())
        log_info("queue_init时无json无数据")
        log_info(resp)
        raise key_exc
    except Exception as e:
        log_info('\n' + traceback.format_exc())
        log_info("queue_init时发生其他异常")
        raise e
    return need_captcha, need_queue, ws_url, queue_url


def get_task_resp(cookie: str) -> requests.Response:
    """
    获取签到任务response
    Args:
        cookie: headers中的cookie

    Returns:
        requests.Response: 返回task响应
    """
    return get_resp(Activity.getList, cookie)


def get_task(cookie: str) -> Optional[dict]:
    """
    获取签到任务
    Args:
        cookie: headers中的cookie

    Returns:
        dict: 返回签到任务字典
    """
    resp = get_task_resp(cookie)
    try:
        resp = resp.json()
        tasks = resp['data']['userAuth']['credit']['tasks']
        if tasks is not None:
            return tasks[0]
        else:
            log_info('get_task时tasks体为空')
            log_info(f'tasks:{tasks}')
            return None
    except ValueError as value_exc:
        log_info(f'\n{traceback.format_exc()}')
        log_info('get_task时无json')
        log_info(resp.content)
        raise value_exc
    except KeyError as key_exec:
        log_info(f'\n{traceback.format_exc()}')
        log_info('get_task时json无数据')
        log_info(resp)
        raise key_exec
    except Exception as exc:
        log_info(f'\n{traceback.format_exc()}')
        log_info('get_task时发生其他错误')
        raise exc


def get_task_id(cookie: str) -> int:
    """
    获取签到任务id
    Args:
        cookie: headers中的cookie

    Returns:
        int: 签到任务id
    """
    task = get_task(cookie)
    while task is None:
        task = get_task(cookie)
    return task['id']
