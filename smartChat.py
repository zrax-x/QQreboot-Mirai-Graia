# coding:utf-8
# https://zhuanlan.zhihu.com/p/110785806

import requests
import urllib
import json

# 青云客
def qingyunke(msg):
    url = 'http://api.qingyunke.com/api.php?key=free&appid=0&msg={}'.format(urllib.parse.quote(msg))
    html = requests.get(url)
    return html.json()["content"]

# ICEreboot551
'''
POST /s_api/game/getresponse?workflow=AIBeingsGFChat HTTP/1.1
Host: ux-plus.msxiaobing.com
Connection: close
Content-Length: 88
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36
Content-Type: application/json;charset=UTF-8
Accept: */*
Origin: https://ux-plus.msxiaobing.com
Sec-Fetch-Site: same-origin
Sec-Fetch-Mode: cors
Sec-Fetch-Dest: empty
Referer: https://ux-plus.msxiaobing.com/virtualgirlfriend?authcode=AAB51AEFCF24BECAE33BC517118A92BE
Accept-Encoding: gzip, deflate
Accept-Language: zh-CN,zh;q=0.9
Cookie: cpid=GDUnNlg0x0xfNigxekkrM86wFLUbTV0zJTXHNFtK1DBMAA; salt=0CD7630B59FB3522D3E3088F27F4BF1B; uxplusaffinity=1605665716.486.1619.904802; logInfo=%7B%22pageName%22%3A%22virtualchat%22%2C%22tid%22%3A%22a03cd7d721c196a1bda235d2210b9eb7%22%7D; subpid=; pname=; .AspNetCore.Session=CfDJ8NHGm0EXOyBDtaGQ0jsNsDj0gNhivPk4xV8lampnOot%2BTGdVRmZqy6orA0SXoGtEohxJp9fLlbpYXnywLnwlHdnYAtKwh2pfxxkhoaKUP9h8DVwa34MYcuoIMlO2Hz6lOTQ0gK9Q36IKBgBWSvuzQBBeSUdjpzDCY8nBlAIqS7EN; apieid=543d24ebe74244ed9b5271a0d2ecea7f

{"TraceId":"a03cd7d721c196a1bda235d2210b9eb7","Content":{"Text":"你好","Metadata":{}}}
'''
def xiaoice(msg):
    url_ = 'https://ux-plus.msxiaobing.com/s_api/game/getresponse?workflow=AIBeingsGFChat'
    head_dic = {
        "Host": "ux-plus.msxiaobing.com",
        "Connection": "close",
        "Content-Length": str(len(msg)),
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36",
        "Content-Type": "application/json;charset=UTF-8",
        "Accept": "*/*",
        "Origin": "https://ux-plus.msxiaobing.com",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Dest": "empty",
        "Referer": "https://ux-plus.msxiaobing.com/virtualgirlfriend?authcode=69865B088928D57027A836161CE5C78E",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.9",
        'Cookie': 'cpid=GDUnNlg0x0xfNigxekkrM86wFLUbTV0zJTXHNFtK1DBMAA; salt=0CD7630B59FB3522D3E3088F27F4BF1B; uxplusaffinity=1605665716.486.1619.904802; logInfo={"pageName":"virtualchat","tid":"a03cd7d721c196a1bda235d2210b9eb7"}; subpid=; pname=; .AspNetCore.Session=CfDJ8NHGm0EXOyBDtaGQ0jsNsDj0gNhivPk4xV8lampnOot+TGdVRmZqy6orA0SXoGtEohxJp9fLlbpYXnywLnwlHdnYAtKwh2pfxxkhoaKUP9h8DVwa34MYcuoIMlO2Hz6lOTQ0gK9Q36IKBgBWSvuzQBBeSUdjpzDCY8nBlAIqS7EN; apieid=cd35ba5fd89a48658a31269c5318c652'
    }
    cookies_ = {
        "cpid": "GDUnNlg0x0xfNigxekkrM86wFLUbTV0zJTXHNFtK1DBMAA",
        "salt": "0CD7630B59FB3522D3E3088F27F4BF1B",
        "uxplusaffinity": "1605665716.486.1619.904802",
        "logInfo": '{"pageName":"virtualchat","tid":"a03cd7d721c196a1bda235d2210b9eb7"}',
        "subpid": "",
        "pname": "",
        ".AspNetCore.Session": "CfDJ8NHGm0EXOyBDtaGQ0jsNsDj0gNhivPk4xV8lampnOot+TGdVRmZqy6orA0SXoGtEohxJp9fLlbpYXnywLnwlHdnYAtKwh2pfxxkhoaKUP9h8DVwa34MYcuoIMlO2Hz6lOTQ0gK9Q36IKBgBWSvuzQBBeSUdjpzDCY8nBlAIqS7EN", 
        "apieid": "cd35ba5fd89a48658a31269c5318c652",
    }
    data_ = json.dumps({"TraceId":"a03cd7d721c196a1bda235d2210b9eb7","Content":{"Text":msg,"Metadata":{}}})
    r = requests.post(url=url_, cookies=cookies_, headers=head_dic, data=data_)
    try:
        res = r.json()[0]['Content']['Text']
    except:
        res = ""
    return res

if __name__ == "__main__":
    msg = "爱你，宝贝"
    # print(qingyunke(msg))
    print(xiaoice(msg))