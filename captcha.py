import json
import os
import time
import traceback

import ddddocr
import requests

from utils import log, post, verify_cookie, wait_time


def ocr():
    images = os.listdir('resource/captcha/captchas')
    images.sort()
    ocr = ddddocr.DdddOcr()
    for img in images:
        with open(f'resource/captcha/captchas/{img}', 'rb') as f:
            try:
                captcha = ocr.classification(f.read())
            except Exception:
                log(f.read())
        with open('resource/captcha/captchas/captchas.out', 'a') as f:
            f.write(f'{{"name":"{img}","captcha":"{captcha}"}}\n')


def get_captcha_image():
    images = os.listdir('resource/captcha/chinese_captchas')
    with open('resource/captcha/chinese_captcha_site.out', 'r') as f:
        count = 0
        for line in f:
            data = json.loads(line)
            code = data['code']
            url = data['data']
            name = url.split('/')[-1]
            file_name = "_".join((code, name))
            if file_name in images:
                count = count + 1
                log(f'{code}已存在,当前已有{count}个')
                continue
            try:
                resp = requests.get(url)
                if resp.status_code == 200:
                    with open(f'resource/captcha/chinese_captchas/{file_name}',
                              'wb') as image:
                        image.write(resp.content)
                    count = count + 1
                    log(f'{code}已写入,当前已有{count}个')
                else:
                    log(f'{code}网页访问失败，状态码{resp.status_code}')
            except Exception:
                count = count + 1
                log(f'{code}写入失败,当前已有{count}个')


def get_captcha(cookie):
    with open('json/reserve/get_end_time_headers.json', 'r') as f:
        get_end_time_headers = json.load(f)
    with open('json/reserve/get_end_time_para.json', 'r') as f:
        get_end_time_para = json.load(f)
    get_end_time_headers['Cookie'] = cookie

    with open('json/reserve/captcha_headers.json', 'r') as f:
        captcha_headers = json.load(f)
    with open('json/reserve/captcha_para.json', 'r') as f:
        captcha_para = json.load(f)
    captcha_headers['Cookie'] = cookie

    if not verify_cookie(cookie):
        log('cookie无效，请更新后重试')
        return

    log('开始等待预定时间')
    wait_time(12, 30)

    resp_end_time = post(get_end_time_para, get_end_time_headers)
    log(resp_end_time)
    end_time = resp_end_time.json(
    )['data']['userAuth']['prereserve']['endTime']

    resp = post(captcha_para, captcha_headers)
    try:
        resp = resp.json()
    except Exception:
        log('body无json')
        log(resp.content)
        return

    number = 0
    while (time.time() < end_time):
        # while (True):
        if 'errors' not in resp:
            with open('resource/captcha/captcha-site.out', 'a') as f:
                f.write(
                    json.dumps(resp['data']['userAuth']['prereserve']
                               ['captcha']) + '\n')
                number = number + 1
                log(f'加入网址成功，当前已有{number}条')
        else:
            log(resp)
        resp = post(captcha_para, captcha_headers)
        try:
            resp = resp.json()
        except Exception:
            log('body无json')
            log(resp.content)
    log('时间截止')


def recognize_imgs_ddddocr():
    images = os.listdir('resource/captcha/chinese_captchas')
    ocr = ddddocr.DdddOcr()
    images.sort()
    for img in images:
        with open(f'resource/captcha/chinese_captchas/{img}', 'rb') as f:
            image_data = f.read()
        try:
            captcha = ocr.classification(image_data)

            if len(captcha) == 4:
                filename = "_".join((captcha, img))
                with open(f'resource/captcha/recognize_muggle_ocr/{filename}',
                          'wb') as image_file:
                    image_file.write(image_data)
        except Exception:
            traceback.print_exc()


def recognize_imgs_muggle_ocr():
    images = os.listdir('resource/captcha/chinese_captchas')
    ocr = ddddocr.DdddOcr()
    images.sort()
    for img in images:
        with open(f'resource/captcha/chinese_captchas/{img}', 'rb') as f:
            image_data = f.read()
        try:
            captcha = ocr.classification(image_data)

            if len(captcha) == 4:
                filename = "_".join((captcha, img))
                with open(f'resource/captcha/recognize_muggle_ocr/{filename}',
                          'wb') as image_file:
                    image_file.write(image_data)
        except Exception:
            traceback.print_exc()


if __name__ == '__main__':
    recognize_imgs_muggle_ocr()
