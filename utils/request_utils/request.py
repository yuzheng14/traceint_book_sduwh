import requests
import traceback
from enum import Enum
from utils.utils import log_info


# TODO doc注释
class Activity(Enum):
    headers = {"Host": "wechat.v2.traceint.com", "Connection": "keep-alive", "Origin": "https://web.traceint.com", "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36 NetType/WIFI MicroMessenger/7.0.20.1781(0x6700143B) WindowsWechat(0x63040026)", "Content-Type": "application/json", "Accept": "*/*", "Sec-Fetch-Site": "same-site", "Sec-Fetch-Mode": "cors", "Sec-Fetch-Dest": "empty", "Referer": "https://web.traceint.com/web/index.html", "Accept-Encoding": "gzip, deflate, br", "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7"}
    captcha = {"operationName": "getStep0", "query": "query getStep0 {\n userAuth {\n prereserve {\n getNum\n captcha {\n code\n data\n }\n }\n }\n}"}
    getStep = {"operationName": "getStep", "query": "query getStep {\n userAuth {\n prereserve {\n getStep\n queeUrl\n successUrl\n endTime\n }\n }\n}"}
    prereserveLibLayout = {"operationName": "libLayout", "query": "query libLayout($libId: Int!) {\n userAuth {\n prereserve {\n libLayout(libId: $libId) {\n max_x\n max_y\n seats_booking\n seats_total\n seats_used\n seats {\n key\n name\n seat_status\n status\n type\n x\n y\n }\n }\n }\n }\n}", "variables": {"libId": None}}
    index = {"operationName": "index", "query": "query index($pos: String!, $param: [hash]) {\n userAuth {\n oftenseat {\n list {\n id\n info\n lib_id\n seat_key\n status\n }\n }\n message {\n new(from: \"system\") {\n has\n from_user\n title\n num\n }\n indexMsg {\n message_id\n title\n content\n isread\n isused\n from_user\n create_time\n }\n }\n reserve {\n reserve {\n token\n status\n user_id\n user_nick\n sch_name\n lib_id\n lib_name\n lib_floor\n seat_key\n seat_name\n date\n exp_date\n exp_date_str\n validate_date\n hold_date\n diff\n diff_str\n mark_source\n isRecordUser\n isChooseSeat\n isRecord\n mistakeNum\n openTime\n threshold\n daynum\n mistakeNum\n closeTime\n timerange\n forbidQrValid\n renewTimeNext\n forbidRenewTime\n forbidWechatCancle\n }\n getSToken\n }\n currentUser {\n user_id\n user_nick\n user_mobile\n user_sex\n user_sch_id\n user_sch\n user_last_login\n user_avatar(size: MIDDLE)\n user_adate\n user_student_no\n user_student_name\n area_name\n user_deny {\n deny_deadline\n }\n sch {\n sch_id\n sch_name\n activityUrl\n isShowCommon\n isBusy\n }\n }\n }\n ad(pos: $pos, param: $param) {\n name\n pic\n url\n }\n}", "variables": {"pos": "App-首页"}}
    verify_captcha = {"operationName": "setStep1", "query": "mutation setStep1($captcha: String!, $captchaCode: String!) {\n userAuth {\n prereserve {\n verifyCaptcha(captcha: $captcha, code: $captchaCode)\n setStep1\n }\n }\n}", "variables": {"captcha": "wvsb", "captchaCode": "ba315bdcb30fd7f55cd8fe1d443d4024"}}


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

    return (activity.value, headers)


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


# TODO test
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
