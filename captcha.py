import requests
import json
from seat_book import post

def ocr():
    # 打开一张验证码图片
    with open("./resource/captcha/jfem.jpg", "rb") as f:
        img_bytes = f.read()
    # 步骤 1

    import time
    start=time.time()
    import ddddocr

    ocr=ddddocr.DdddOcr()



    text=ocr.classification(img_bytes)
    print(text)
    print(time.time()-start)

def get_captcha():
    with open('json/reserve/captcha_headers.json','r') as f:
        captcha_headers=json.load(f)
    with open('json/reserve/captcha_para.json','r') as f:
        captcha_para=json.load(f)
    captcha_headers['Cookie']='FROM_TYPE=weixin; v=5.5; Hm_lvt_7ecd21a13263a714793f376c18038a87=1636086043,1636172899,1636259364,1636432169; wechatSESS_ID=425de0efbe7c24056d7a744b0713647c1c027572777cca40; Authorization=eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJ1c2VySWQiOjIxMDAxOTM2LCJzY2hJZCI6MTI2LCJleHBpcmVBdCI6MTYzNjQ1MDA5M30.y38Xzb1E7ms0Gw5dJs4jC9graD_soI8rUjpccjzjKxRXkqBwwB5zYnz6L35tFMJry_QUI-qFz9_Eher6X1ztS11IDANkheuycn27LYp8UPDWHDpTNMA9GKmM40tvZwMTQMMB5VWDef6sxF2LKNAvkrWAlsCfaX9T3hS_L-JTk3HufedIhCJynoHqaYRALsK99Tzu3s81XfBmMk0FB4aJM7OnnGHr39NjJb9GtA-Vtb2BgmyP5uTTiVTHhJ1Pirxd3FucKYBDEfbnYqzIgcpYZ_AK9vqPI2JhzmWtXFkV3Uc2KK8TuIIs9T231LGwZMdPQH6lLbqv7UCEHzg_sWjfqA; SERVERID=82967fec9605fac9a28c437e2a3ef1a4|1636446493|1636446487'
    resp=post(captcha_para,captcha_headers)
    print(resp.json())
if __name__=='__main__':
    get_captcha()