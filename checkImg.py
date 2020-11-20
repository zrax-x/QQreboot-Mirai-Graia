# coding: utf8

import asyncio
import requests
from config import configs as myconfigs
import os
import hashlib
import re
import random
import html

def read_file_num(path):
    if not os.path.exists(path):
        write_file_num(path, 0)
    with open(path, "r") as f:
        try:
            num = int(f.read())
        except:
            num = 0
    return num

def write_file_num(path, num):
    with open(path, "w") as f:
        f.write(str(num))

def download_img(img_url, headers=None):
    if headers:
        r = requests.get(img_url, headers=headers, stream=True)
    else:
        r = requests.get(img_url, stream=True)
    if r.status_code == 200:
        idx = read_file_num(myconfigs['img_count_file'])
        write_file_num(myconfigs['img_count_file'], idx+1)
        img_file = os.path.join(myconfigs['img_dir'], str(idx)+'.jpg')
        open(img_file, 'wb').write(r.content) # 将内容写入图片
        return img_file
    else:
        return None
    
def download_bytes(img_url):
    r = requests.get(img_url, stream=True)
    if r.status_code == 200:
        return r.content
    else:
        return b""
    
def read_lines(path):
    if os.path.exists(path):
        with open(path, "r") as f:
            res = [x.strip() for x in f.readlines()]
            return res
    else:
        with open(path, 'w') as f:
            pass

def falsePositive(path):
    filenames = os.listdir(myconfigs['img_exception_dir'])
    digests = read_lines(myconfigs['exception_digest'])
    if len(filenames) != len(digests):
        updateExceptionSha256()
        digests = read_lines(myconfigs['exception_digest'])
    target = calcImgSha256(path)
    if type(target) == bytes:
        target = target.decode('latin')
    if target in digests:
        return True
    else:
        return False


def updateExceptionSha256():
    all_sha256 = []
    for file in os.listdir(myconfigs['img_exception_dir']):
        digest = calcImgSha256(os.path.join(myconfigs['img_exception_dir'], file))
        all_sha256.append(digest)
    with open(myconfigs['exception_digest'], 'w') as f:
        for digest in all_sha256:
            # print(type(digest))
            f.write(digest+'\n')
    return all_sha256
    

def calcImgSha256(path):
    if os.path.exists(path):
        with open(path, "rb") as f:
            img = f.read()
            digest = hashlib.sha256(img).hexdigest()
        return digest

async def searchImgfromMicroSoft():
    rnd_page = random.randint(1, 30)
    url = 'https://cn.bing.com/images/search?q=%e6%80%a7%e6%84%9f&qs=n&form=QBIR&sp=-1&pq=%e6%80%a7%e6%84%9f&sc=8-2&cvid=D89DD6FAA9504A7A8531F29007FB2F9E&first={}&scenario=ImageBasicHover'.format(rnd_page)
    headers = {
        "Host": "cn.bing.com",
        "Cache-Control": "max-age=0",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-User": "?1",
        "Sec-Fetch-Dest": "document",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Cookie": "ipv6=hit=1605684814951&t=4; MMCA=ID=F8EDFF5B51EC45FBAD523759756E34A6; MUID=28C8405A9A4466B41CFF4ED59B3B67BF; SRCHD=AF=NOFORM; SRCHUID=V=2&GUID=47494E7C90194DBAAE2DAF40C97422F1&dmnchg=1; MUIDB=28C8405A9A4466B41CFF4ED59B3B67BF; _UR=OMD=13238150628; _ga=GA1.2.268651699.1594776376; _BEC=PLTL=399&PLTA=534&PLTN=10; _HPVN=CS=eyJQbiI6eyJDbiI6MiwiU3QiOjAsIlFzIjowLCJQcm9kIjoiUCJ9LCJTYyI6eyJDbiI6MiwiU3QiOjAsIlFzIjowLCJQcm9kIjoiSCJ9LCJReiI6eyJDbiI6MiwiU3QiOjAsIlFzIjowLCJQcm9kIjoiVCJ9LCJBcCI6dHJ1ZSwiTXV0ZSI6dHJ1ZSwiTGFkIjoiMjAyMC0xMC0wN1QwMDowMDowMFoiLCJJb3RkIjowLCJEZnQiOm51bGwsIk12cyI6MCwiRmx0IjowLCJJbXAiOjIwfQ==; _RwBf=mtu=0&g=0&o=2&p=&c=&t=0&s=0001-01-01T00:00:00.0000000+00:00&ts=2020-10-07T14:11:47.1372170+00:00&ssg=0&cid=; MUIDB=28C8405A9A4466B41CFF4ED59B3B67BF; MSCC=1; _tarLang=default=en; _TTSS_OUT=hist=WyJpdCIsInpoLUhhbnMiLCJlbiJd; _TTSS_IN=hist=WyJpdCIsImVuIiwiemgtSGFucyIsImF1dG8tZGV0ZWN0Il0=; imgv=lodlg=1; _EDGE_V=1; ULC=P=1B4CC|11:9&H=1B4CC|11:9&T=1B4CC|11:9:1; ENSEARCH=BENVER=0; _SS=SID=1BFADFB076596F093E8AD03677776E4C&bIm=489106; ABDEF=V=12&ABDV=12&MRNB=1605681210775&MRB=0; SRCHUSR=DOB=20200514&T=1605681208000; _EDGE_S=mkt=zh-cn&ui=zh-cn&SID=138878DE5A40660B222C77585B0367A0; SNRHOP=I=&TS=; ipv6=hit=1605687087560&t=4; SRCHHPGUSR=CW=2048&CH=1026&DPR=1.25&UTC=480&HV=1605684662&WTS=63741278010&DM=0&PLTL=652&PLTA=606&PLTN=3&BRW=W&BRH=T&BZA=0"
    }
    r = requests.get(url=url, headers=headers)
    res = r.text
    regex = re.compile(r'<div class="img_cont hoff"><img(.*?)/>')
    raw = regex.findall(res)
    all_link = []
    for elem in raw:
        link_reg = re.compile(r'src="(.*?)"')
        link = link_reg.findall(elem)
        if link:
            link = link[0].strip('src="').strip('"')
            all_link.append(html.unescape(link))
    rnd_idx = random.randint(0, len(all_link))
    return all_link[rnd_idx]

async def searchImgQbhnLocal():
    rnd_dir_idx = random.randint(1,4)
    rnd_dir = os.path.join(myconfigs['qbhn_dir'], str(rnd_dir_idx))
    filenames = os.listdir(rnd_dir)
    rnd_img_idx = random.randint(0, len(filenames)-1)
    return os.path.join(rnd_dir, filenames[rnd_img_idx])

async def searchVmgirls():
    with open(myconfigs['yjny_links'], "r") as f:
        all_url = [x.strip() for x in f.readlines()]
    rnd_url_idx = random.randint(0, len(all_url))
    url = all_url[rnd_url_idx]
    # url = "https://www.vmgirls.com/14012.html"
    headers = {
        "Host": "www.vmgirls.com",
        "Cache-Control": "max-age=0",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-User": "?1",
        "Sec-Fetch-Dest": "document",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Cookie": "__cfduid=da98f2bcd5d445070525798d7b68a6f8f1605772610; Hm_lvt_a5eba7a40c339f057e1c5b5ac4ab4cc9=1605772615; __gads=ID=993a6d43b09cb10d-229bd4dcd5c40039:T=1605772615:RT=1605772615:S=ALNI_MZig4qJ041VNAjQQ9yBcVZELNMXUA; _GPSLSC=; Hm_lpvt_a5eba7a40c339f057e1c5b5ac4ab4cc9=1605772722"
    }
    r = requests.get(url=url, headers=headers)
    res = r.text
    # print('<a href="//static.vmgirls.com/' in res)
    regex = re.compile(r'<a href="//static.vmgirls.com/(.*?)>')
    raw = regex.findall(res)
    # print(raw)
    all_link = []
    for elem in raw:
        link_reg = re.compile(r'(.*?).jpeg"')
        link = link_reg.findall(elem)
        if link:
            link = 'https://static.vmgirls.com/' + link[0] + '.jpeg'
            all_link.append(html.unescape(link))
    # print(all_link)
    if all_link:
        rnd_idx = random.randint(0, len(all_link)-1)
        return all_link[rnd_idx]
    else:
        return None

# 下载要的图片
# img_url = "http://gchat.qpic.cn/gchatpic_new/214920976/557116842-2809299664-FEE614556787A7365D7A60E321BDD399/0?term=2"
# download_img(img_url)

# print(falsePositive("./exceptation/_ER@M(`4]XO5~D_5IG1V]TC.jpg"))

# img_path = searchImgfromMicroSoft()
# print(img_path)
# img_file = download_img(img_path)
# print(img_file)

# print(searchImgQbhnLocal())

header_yjny = {
    "Host": "static.vmgirls.com",
    "Cache-Control": "max-age=0",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "Sec-Fetch-Site": "same-origin",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-User": "?1",
    "Sec-Fetch-Dest": "document",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "zh-CN,zh;q=0.9",
    "Cookie": "__cfduid=da98f2bcd5d445070525798d7b68a6f8f1605772610; __gads=ID=993a6d43b09cb10d-229bd4dcd5c40039:T=1605772615:RT=1605772615:S=ALNI_MZig4qJ041VNAjQQ9yBcVZELNMXUA",
    "If-None-Match": '"5efedb9e-1d8df7"',
    "If-Modified-Since": 'Fri, 03 Jul 2020 07:17:50 GMT'

}
# img_url = searchVmgirls()
# print(img_url)
# img_path = download_img(img_url, headers)
# print(img_path)

# regex = re.compile(r'<a href="(.*?)>')
# test = '<a href="//static.vmgirls.com/image/2020/07/2020070307171263-scaled.jpeg" alt="古着女孩儿" title="古着女孩儿"><'

# print(regex.findall(test))