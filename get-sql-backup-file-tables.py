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

def verify(url):
    host = url.split("/")[2].split(":")[0]
    filetype = url.split(".")[-1]
    savefile =  host + "." + filetype
    patt = "CREATE TABLE `([^`]+)`"
    tablelist = []
    for item in open("temp/"+savefile, encoding="utf-8"):
        if "CREATE TABLE" in item:
            tablelist.append(re.findall(patt, item, re.I)[0])
    if len(tablelist) != 0:
        return ",".join(tablelist)
    return ""

    
if __name__=="__main__":
    target = sys.argv[1]
    info = verify(target)
    if info != "":
        print("[+]漏洞存在，数据库备份中的表名列表为：", info)
    else:
        print("[-]漏洞不存在")
