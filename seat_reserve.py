from seat_book import post
import json

def seat_reserve(cookie):
    with open('pre_10_headers.json','r') as f:
        pre_headers=json.load(f)
    with open('pre_10_para.json','r') as f:
        pre_para=json.load(f)
    pre_headers['Cookie']=cookie
    resp=post(pre_para,pre_headers).json()

if __name__=='__main__':
    seat_reserve('再说')